import sys
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
import re
import sqlite3  # Added missing import

# Add project root to path for imports
# sys.path.append("/home/ubuntu")  # Not needed for Windows
import database_manager as db_manager
# Commenting out this import as it causes dependency issues with data_api
# from real_data_collector import RealDataCollector # May need collector for enriching prospect data

class LeadGenerationAgent:
    """Main class for the Lead Generation functionality using real data."""
    
    def __init__(self, db_conn=None):
        """Initialize the Lead Generation Agent with a database connection."""
        self.db_conn = db_conn if db_conn else db_manager.get_db_connection()
        if not self.db_conn:
            raise ConnectionError("Failed to establish database connection.")
            
        # Initialize components with DB connection
        self.prospector = ProspectIdentifier(self.db_conn)
        self.qualifier = LeadQualifier(self.db_conn)
        self.reporter = LeadReportGenerator(self.db_conn)
        print("LeadGenerationAgent initialized with database connection.")

    def define_icp(self, profile_name, criteria):
        """Define or update an Ideal Customer Profile (ICP) in the database."""
        print(f"Defining/Updating ICP: {profile_name}")
        if not isinstance(criteria, dict):
            raise ValueError("ICP criteria must be a dictionary.")
            
        criteria_json = json.dumps(criteria)
        icp_id = db_manager.add_or_update_icp(self.db_conn, profile_name, criteria_json)
        
        if icp_id:
            print(f"ICP {profile_name} saved successfully (ID: {icp_id}).")
            return {"icp_id": icp_id, "profile_name": profile_name, "criteria": criteria}
        else:
            print(f"Failed to save ICP: {profile_name}")
            return None

    def get_icp(self, profile_name):
        """Retrieve an ICP from the database by name."""
        print(f"Retrieving ICP: {profile_name}")
        icp_row = db_manager.get_icp_by_name(self.db_conn, profile_name)
        if icp_row:
            try:
                criteria = json.loads(icp_row["criteria_json"])
                return {"icp_id": icp_row["icp_id"], "profile_name": icp_row["profile_name"], "criteria": criteria}
            except json.JSONDecodeError as e:
                print(f"Error decoding ICP criteria JSON for {profile_name}: {e}")
                return None
        else:
            print(f"ICP {profile_name} not found.")
            return None

    def generate_leads(self, icp_profile_name, num_leads=10):
        """Generate a list of qualified leads based on a stored ICP name."""
        print(f"Starting lead generation based on ICP: {icp_profile_name}")
        
        # Retrieve the ICP from the database
        icp_data = self.get_icp(icp_profile_name)
        if not icp_data:
            # Fixed return type inconsistency - now returns a dictionary instead of tuple
            return {
                "error": f"ICP profile {icp_profile_name} not found.",
                "leads": [],
                "generated_at": datetime.now().isoformat()
            }
        icp_id = icp_data["icp_id"]
        icp_criteria = icp_data["criteria"]
        
        # Identify potential prospects from the database
        potential_prospects = self.prospector.find_prospects_from_db(icp_criteria, num_leads * 3) # Find more to allow for filtering
        
        # Qualify and score the prospects
        qualified_lead_ids = self.qualifier.qualify_and_score_leads(potential_prospects, icp_id, icp_criteria)
        
        # Retrieve qualified lead details from DB
        lead_rows = db_manager.get_leads_by_ids(self.db_conn, qualified_lead_ids)
        
        # Convert Row objects to dictionaries
        final_leads = [dict(lead) for lead in lead_rows]
        
        # Sort leads by score (highest first)
        final_leads.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        # Limit to the requested number of leads
        final_leads = final_leads[:num_leads]
        
        # Generate a report
        report = self.reporter.generate_lead_report(final_leads, icp_profile_name, icp_criteria)
        
        return report


class ProspectIdentifier:
    """Component responsible for identifying potential prospects from the database."""
    
    def __init__(self, db_conn):
        """Initialize the ProspectIdentifier with DB connection."""
        self.db_conn = db_conn
    
    def find_prospects_from_db(self, icp_criteria, max_prospects=50):
        """
        Find potential prospects from the companies table based on ICP criteria.
        This is a simplified version; a real version would be more complex,
        potentially joining with other tables or triggering data collection.
        """
        print(f"Searching database for prospects matching ICP... (Target: {max_prospects})")
        if not self.db_conn:
            print("Error: Database connection not available for prospect search.")
            return []
            
        cursor = self.db_conn.cursor()
        prospects = []
        
        # Build SQL query based on ICP criteria
        sql = "SELECT company_id, name, industry, region, employee_count, website FROM companies WHERE 1=1"
        params = []
        
        # --- Apply ICP Filters --- 
        # Use preferred lists primarily, required lists act as hard filters later if needed
        if "preferred_industries" in icp_criteria and icp_criteria["preferred_industries"]:
            placeholders = ",".join(["?"] * len(icp_criteria["preferred_industries"]))
            sql += f" AND industry IN ({placeholders})"
            params.extend(icp_criteria["preferred_industries"])
            
        if "preferred_regions" in icp_criteria and icp_criteria["preferred_regions"]:
            placeholders = ",".join(["?"] * len(icp_criteria["preferred_regions"]))
            sql += f" AND region IN ({placeholders})"
            params.extend(icp_criteria["preferred_regions"])
            
        # Company size needs mapping or range queries (simplification: using employee_count)
        # TODO: Implement more robust company size filtering based on employee_count ranges
        min_employees, max_employees = self._get_employee_range(icp_criteria.get("preferred_company_sizes"))
        if min_employees is not None:
            sql += " AND employee_count >= ?"
            params.append(min_employees)
        if max_employees is not None:
            sql += " AND employee_count <= ?"
            params.append(max_employees)
            
        # Add limit
        sql += " LIMIT ?"
        params.append(max_prospects)
        
        try:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            prospects = [dict(row) for row in results]
            print(f"Found {len(prospects)} potential prospects in database.")
        except sqlite3.Error as e:
            print(f"Database error during prospect search: {e}")
            # Added better error handling
            return []
        finally:
            if cursor:
                cursor.close()
                
        # TODO: Add logic to search other tables like india_real_estate_projects 
        # or india_architectural_firms based on ICP industry/keywords.
        # TODO: Potentially trigger RealDataCollector if DB results are insufficient.
                
        return prospects # Return list of company dictionaries

    def _get_employee_range(self, size_strings):
        """Helper to convert size strings (e.g., "51-200") to min/max employee counts."""
        if not size_strings:
            return None, None
            
        min_emp = float("inf")
        max_emp = 0
        
        mapping = {
            "1-10": (1, 10),
            "11-50": (11, 50),
            "51-200": (51, 200),
            "201-500": (201, 500),
            "501-1000": (501, 1000),
            "1000+": (1001, float("inf"))
        }
        
        found_range = False
        for s in size_strings:
            if s in mapping:
                found_range = True
                min_emp = min(min_emp, mapping[s][0])
                max_emp = max(max_emp, mapping[s][1])
                
        if not found_range:
            return None, None
            
        final_min = min_emp if min_emp != float("inf") else None
        final_max = max_emp if max_emp != float("inf") else None
        
        return final_min, final_max

class LeadQualifier:
    """Component responsible for qualifying and scoring leads based on ICP using DB data."""
    
    def __init__(self, db_conn):
        """Initialize the LeadQualifier with DB connection."""
        self.db_conn = db_conn

    def qualify_and_score_leads(self, prospects, icp_id, icp_criteria):
        """Qualify prospects (company dicts) against the ICP and update/create lead records in DB."""
        print(f"Qualifying {len(prospects)} prospects against ICP ID: {icp_id}...")
        qualified_lead_ids = []
        
        for prospect_company in prospects:
            company_id = prospect_company["company_id"]
            
            # Check if a lead record already exists for this company and ICP
            existing_leads = db_manager.get_lead_by_company_icp(self.db_conn, company_id, icp_id)
            # Use first result if exists, otherwise None
            existing_lead = existing_leads[0] if existing_leads and len(existing_leads) > 0 else None
            
            # Calculate score based on company data vs ICP criteria
            score = self._calculate_score(prospect_company, icp_criteria)
            qualification_status, reason = self._check_qualification(prospect_company, icp_criteria, score)
            
            lead_data = {
                "icp_id": icp_id,
                "company_name": prospect_company["name"],
                # "contact_name": None, # Need a way to find contacts
                # "job_title": None,
                "industry": prospect_company["industry"],
                # "company_size": prospect_company["employee_count"], # Map back to string?
                "region": prospect_company["region"],
                "website": prospect_company["website"],
                "source": "Database Prospecting",
                "qualification_status": qualification_status,
                "qualification_reason": reason,
                "score": score,
                "collected_date": datetime.now(),
                "status": "New" if qualification_status == "Qualified" else "Archived"
            }
            
            lead_id = None
            if existing_lead:
                # Update existing lead record
                lead_id = existing_lead["lead_id"]
                db_manager.update_lead(self.db_conn, lead_id, lead_data)
                print(f"Updated existing lead ID: {lead_id} for company: {prospect_company['name']}")
            else:
                # Update with correct string quote usage
                lead_id = db_manager.add_lead(self.db_conn, lead_data)
                if lead_id:
                    print(f"Created new lead ID: {lead_id} for company: {prospect_company['name']}")
                else:
                    print(f"Failed to create lead for company: {prospect_company['name']}")
            
            if lead_id and qualification_status == "Qualified":
                qualified_lead_ids.append(lead_id)
                # TODO: Implement contact finding and enrichment step here if needed
                # contact_info = self._find_and_enrich_contact(company_id, icp_criteria)
                # if contact_info:
                #    db_manager.update_lead(self.db_conn, lead_id, contact_info)
                
        print(f"Processed {len(prospects)} prospects. Found/Updated {len(qualified_lead_ids)} qualified leads linked to ICP {icp_id}.")
        return qualified_lead_ids # Return list of qualified lead IDs

    def _check_qualification(self, prospect_company, icp_criteria, score):
        """Check if a prospect meets the minimum qualification criteria."""
        min_score_threshold = icp_criteria.get("min_score_threshold", 0.5)
        reason = "Score too low" 

        # Hard filters
        if "required_industry" in icp_criteria and prospect_company.get("industry") not in icp_criteria["required_industry"]:
            return "Disqualified", "Industry mismatch"
        if "required_region" in icp_criteria and prospect_company.get("region") not in icp_criteria["required_region"]:
            return "Disqualified", "Region mismatch"
        # TODO: Add required company size check based on employee_count
        # TODO: Add required job title check (needs contact finding first)

        if score >= min_score_threshold:
            return "Qualified", None
        else:
            return "Disqualified", reason

    def _calculate_score(self, prospect_company, icp_criteria):
        """Calculate a score based on how well the prospect company matches the ICP."""
        score = 0.0
        max_score = 0.0
        
        if "preferred_industries" in icp_criteria:
            max_score += 1
            if prospect_company.get("industry") in icp_criteria["preferred_industries"]:
                score += 1
        
        if "preferred_regions" in icp_criteria:
            max_score += 1
            if prospect_company.get("region") in icp_criteria["preferred_regions"]:
                score += 1
        
        # Score based on company size (employee count)
        if "preferred_company_sizes" in icp_criteria:
            max_score += 1
            # Create a new instance with the current db connection instead of None
            min_emp, max_emp = self._get_employee_range_for_scoring(icp_criteria["preferred_company_sizes"])
            emp_count = prospect_company.get("employee_count")
            if emp_count is not None:
                if (min_emp is None or emp_count >= min_emp) and (max_emp is None or emp_count <= max_emp):
                    score += 1
                
        # TODO: Add scoring based on technologies used (requires collecting this data)
        # TODO: Add scoring based on engagement level (requires collecting this data)
        # TODO: Add scoring based on job titles (requires finding contacts)

        normalized_score = (score / max_score) if max_score > 0 else 0
        return round(normalized_score, 2)
    
    # Added this method to avoid creating a temporary ProspectIdentifier with None
    def _get_employee_range_for_scoring(self, size_strings):
        """Helper to convert size strings (e.g., "51-200") to min/max employee counts."""
        if not size_strings:
            return None, None
            
        min_emp = float("inf")
        max_emp = 0
        
        mapping = {
            "1-10": (1, 10),
            "11-50": (11, 50),
            "51-200": (51, 200),
            "201-500": (201, 500),
            "501-1000": (501, 1000),
            "1000+": (1001, float("inf"))
        }
        
        found_range = False
        for s in size_strings:
            if s in mapping:
                found_range = True
                min_emp = min(min_emp, mapping[s][0])
                max_emp = max(max_emp, mapping[s][1])
                
        if not found_range:
            return None, None
            
        final_min = min_emp if min_emp != float("inf") else None
        final_max = max_emp if max_emp != float("inf") else None
        
        return final_min, final_max

    # def _find_and_enrich_contact(self, company_id, icp_criteria):
    #     """Placeholder: Find relevant contacts within the company and enrich lead data."""
    #     # In a real implementation: 
    #     # 1. Use DB or external tools (e.g., LinkedIn Sales Nav, ZoomInfo - with compliance) 
    #     #    to find contacts matching preferred_job_titles in icp_criteria at company_id.
    #     # 2. Gather publicly available email/phone (strictly adhering to privacy laws).
    #     # 3. Return a dictionary with contact_name, job_title, email, phone, linkedin_profile.
    #     print(f"Placeholder: Finding contacts for company ID {company_id}")
    #     return None # Return None for now


class LeadReportGenerator:
    """Component responsible for generating reports of qualified leads from DB."""
    
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def generate_lead_report(self, leads, icp_profile_name, icp_criteria):
        """Generate a structured report containing the list of qualified leads (from DB)."""
        print(f"Generating lead report for ICP: {icp_profile_name}")
        
        report = {
            "title": f"Qualified Leads Report for ICP: {icp_profile_name}",
            "generated_at": datetime.now().isoformat(),
            "criteria": icp_criteria,
            "summary": {
                "total_qualified_leads": len(leads),
                "average_score": round(np.mean([lead["score"] for lead in leads]), 2) if leads else 0
            },
            "leads": [dict(lead) for lead in leads] # Convert Row objects to dicts
        }
        
        # Optionally, save to a file (e.g., CSV)
        # self.save_leads_to_csv(leads, f"/home/ubuntu/{icp_profile_name}_leads.csv")
        
        return report

    def save_leads_to_csv(self, leads, filename):
        """Save the list of leads (Row objects or dicts) to a CSV file."""
        if not leads:
            print("No leads to save.")
            return
            
        try:
            # Convert Row objects to dictionaries if necessary
            leads_dict = [dict(lead) for lead in leads]
            df = pd.DataFrame(leads_dict)
            # Select and order columns for CSV
            columns_to_save = [
                "lead_id", "score", "company_name", "industry", "region", 
                "website", "qualification_status", "status", "collected_date"
                # Add contact details if/when available
                # "contact_name", "job_title", "email", "phone", "linkedin_profile"
            ]
            df = df[[col for col in columns_to_save if col in df.columns]]
            df.to_csv(filename, index=False)
            print(f"Successfully saved {len(leads)} leads to {filename}")
        except Exception as e:
            print(f"Error saving leads to CSV {filename}: {e}")

# --- Main Execution / Test --- (Updated)
if __name__ == "__main__":
    print("Testing Lead Generation Agent with Real Data Integration...")
    
    # Ensure database exists and is initialized
    if not os.path.exists(db_manager.DATABASE_NAME):
        print("Database file not found. Initializing...")
        db_manager.initialize_database()
    
    db_connection = db_manager.get_db_connection()
    
    if not db_connection:
        print("Failed to connect to database. Exiting test.")
        sys.exit(1)
        
    try:
        agent = LeadGenerationAgent(db_connection)
        
        # --- Test ICP Definition ---
        icp_name = "Test_Software_ICP_US_CA"
        icp_criteria = {
            "preferred_industries": ["Software", "Technology"],
            "preferred_regions": ["US", "CA"],
            "preferred_company_sizes": ["51-200", "201-500"],
            "min_score_threshold": 0.6
            # "required_industry": ["Software"], # Example hard filter
            # "preferred_job_titles": ["CTO", "VP Engineering"] # For future contact finding
        }
        print(f"\n--- Defining ICP: {icp_name} ---")
        icp_result = agent.define_icp(icp_name, icp_criteria)
        if not icp_result:
            print("Failed to define ICP, exiting test.")
            sys.exit(1)
            
        # --- Add some test company data (if needed) ---
        # Ensure some companies matching the ICP exist in the DB for testing
        # Example: Add a matching company manually via db_manager or ensure collector ran
        db_manager.add_or_update_company(db_connection, {
            "name": "Sample Tech Co US", "ticker_symbol": "STCU.US", "region": "US", 
            "industry": "Software", "employee_count": 150, "data_source": "Manual"
        })
        db_manager.add_or_update_company(db_connection, {
            "name": "Another Tech Co CA", "ticker_symbol": "ATCC.CA", "region": "CA", 
            "industry": "Technology", "employee_count": 300, "data_source": "Manual"
        })
        db_manager.add_or_update_company(db_connection, {
            "name": "NonMatching Co EU", "ticker_symbol": "NMCE.EU", "region": "EU", 
            "industry": "Finance", "employee_count": 100, "data_source": "Manual"
        })

        # --- Test Lead Generation ---
        print(f"\n--- Generating Leads for ICP: {icp_name} ---")
        lead_report = agent.generate_leads(icp_profile_name=icp_name, num_leads=5)
        
        if "error" in lead_report:
            print(f"Error during lead generation: {lead_report['error']}")
        else:
            print(f"\nGenerated Lead Report:")
            # Fixed f-string quote usage
            print(f"Title: {lead_report['title']}")
            print(f"Total Qualified Leads: {lead_report['summary']['total_qualified_leads']}")
            print(f"Average Score: {lead_report['summary']['average_score']}")
            
            print("\nSample Leads Found:")
            for i, lead in enumerate(lead_report["leads"][:2]): # Print first 2 leads
                print(f"--- Lead {i+1} ---")
                # Fixed f-string quote usage
                print(f"  Lead ID: {lead['lead_id']}")
                print(f"  Score: {lead['score']}")
                print(f"  Company: {lead['company_name']}")
                print(f"  Industry: {lead['industry']}")
                print(f"  Region: {lead['region']}")
                print(f"  Status: {lead['status']}")
                
            # Example of saving to CSV
            csv_path = os.path.join(os.path.dirname(__file__), f"{icp_name}_leads.csv")
            agent.reporter.save_leads_to_csv(lead_report["leads"], csv_path)

    except Exception as e:
        print(f"An error occurred during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if db_connection:
            db_connection.close()
            print("\nDatabase connection closed after testing.")

