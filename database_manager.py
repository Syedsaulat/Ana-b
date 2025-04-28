"""
Database Manager for Business AI Agent

Handles all interactions with the SQLite database (`business_agent.db`).
Provides functions for creating tables, inserting, updating, and querying data.
"""

import sqlite3
import json
from datetime import datetime
import os

# Changed to a relative path for compatibility across Windows and Linux
DATABASE_NAME = os.path.join(os.path.dirname(__file__), "business_agent.db")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
        conn.execute("PRAGMA foreign_keys = ON;") # Enforce foreign key constraints
        print(f"Database connection established to {DATABASE_NAME}")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_tables(conn):
    """Creates all necessary tables if they don't exist."""
    if not conn:
        return
        
    cursor = conn.cursor()
    try:
        # Companies Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            ticker_symbol TEXT UNIQUE,
            region TEXT,
            industry TEXT,
            sector TEXT,
            website TEXT,
            address TEXT,
            phone TEXT,
            employee_count INTEGER,
            business_summary TEXT,
            market_cap REAL,
            revenue REAL,
            growth_rate REAL,
            profit_margin REAL,
            innovativeness_score REAL,
            hiring_score REAL,
            sustainability_score REAL,
            insider_sentiment_score REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_source TEXT
        );
        """)
        print("Checked/Created companies table.")

        # Company Officers Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_officers (
            officer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            name TEXT,
            title TEXT,
            age INTEGER,
            year_born INTEGER,
            fiscal_year INTEGER,
            total_pay REAL,
            exercised_value REAL,
            unexercised_value REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies (company_id) ON DELETE CASCADE
        );
        """)
        print("Checked/Created company_officers table.")

        # Market Trends Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_trends (
            trend_id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry TEXT,
            region TEXT,
            trend_description TEXT NOT NULL,
            trend_type TEXT,
            source TEXT,
            source_url TEXT,
            published_date DATE,
            collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sentiment_score REAL,
            relevance_score REAL
        );
        """)
        print("Checked/Created market_trends table.")

        # News Articles Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_articles (
            article_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            industry TEXT,
            topic TEXT,
            title TEXT NOT NULL,
            source_name TEXT,
            source_url TEXT UNIQUE NOT NULL,
            published_date TIMESTAMP,
            summary TEXT,
            sentiment_score REAL,
            sentiment_label TEXT,
            collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies (company_id) ON DELETE SET NULL
        );
        """)
        print("Checked/Created news_articles table.")

        # ICPs Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS icps (
            icp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_name TEXT NOT NULL UNIQUE,
            criteria_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP
        );
        """)
        print("Checked/Created icps table.")

        # Leads Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id INTEGER PRIMARY KEY AUTOINCREMENT,
            icp_id INTEGER,
            company_name TEXT,
            contact_name TEXT,
            job_title TEXT,
            industry TEXT,
            company_size TEXT,
            region TEXT,
            website TEXT,
            email TEXT,
            phone TEXT,
            linkedin_profile TEXT,
            source TEXT,
            qualification_status TEXT,
            qualification_reason TEXT,
            score REAL,
            engagement_level REAL,
            technologies_used TEXT,
            notes TEXT,
            collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_contacted TIMESTAMP,
            status TEXT DEFAULT 'New',
            FOREIGN KEY (icp_id) REFERENCES icps (icp_id) ON DELETE SET NULL
        );
        """)
        print("Checked/Created leads table.")

        # India Real Estate Projects Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS india_real_estate_projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            developer_id INTEGER,
            developer_name TEXT,
            city TEXT,
            region TEXT,
            project_type TEXT,
            status TEXT,
            rera_registration_id TEXT UNIQUE,
            launch_date DATE,
            expected_completion_date DATE,
            total_area_sqft REAL,
            price_per_sqft_range TEXT,
            key_features TEXT,
            source_url TEXT,
            collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (developer_id) REFERENCES companies (company_id) ON DELETE SET NULL
        );
        """)
        print("Checked/Created india_real_estate_projects table.")

        # India Architectural Firms Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS india_architectural_firms (
            firm_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER UNIQUE,
            firm_name TEXT NOT NULL,
            city TEXT,
            region TEXT,
            specialization TEXT,
            notable_projects TEXT,
            key_personnel TEXT,
            awards TEXT,
            coa_registration_id TEXT,
            source_url TEXT,
            collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies (company_id) ON DELETE CASCADE
        );
        """)
        print("Checked/Created india_architectural_firms table.")

        # Analysis Results Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_type TEXT NOT NULL,
            target_entity_id INTEGER,
            target_entity_name TEXT,
            result_json TEXT NOT NULL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("Checked/Created analysis_results table.")

        # Create Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_name ON companies (name);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_ticker ON companies (ticker_symbol);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_industry ON companies (industry);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_leads_icp_id ON leads (icp_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_leads_industry ON leads (industry);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_articles_company_id ON news_articles (company_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_articles_published_date ON news_articles (published_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_market_trends_industry ON market_trends (industry);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_india_real_estate_city ON india_real_estate_projects (city);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_india_arch_firms_city ON india_architectural_firms (city);")
        print("Checked/Created indexes.")

        conn.commit()
        print("Database schema created/verified successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

def add_or_update_company(conn, company_data):
    """Adds a new company or updates an existing one based on name or ticker_symbol."""
    if not conn:
        return None
        
    cursor = conn.cursor()
    now = datetime.now()
    company_id = None
    
    # Define columns based on the table schema
    columns = [
        'name', 'ticker_symbol', 'region', 'industry', 'sector', 'website', 
        'address', 'phone', 'employee_count', 'business_summary', 'market_cap', 
        'revenue', 'growth_rate', 'profit_margin', 'innovativeness_score', 
        'hiring_score', 'sustainability_score', 'insider_sentiment_score', 
        'data_source'
    ]
    
    # Prepare data dictionary with only valid columns
    data_to_insert = {col: company_data.get(col) for col in columns if col in company_data}
    data_to_insert['last_updated'] = now
    
    # Check if company exists by ticker symbol or name
    existing_id = None
    if data_to_insert.get('ticker_symbol'):
        cursor.execute("SELECT company_id FROM companies WHERE ticker_symbol = ?", (data_to_insert['ticker_symbol'],))
        result = cursor.fetchone()
        if result:
            existing_id = result['company_id']
    
    if not existing_id and data_to_insert.get('name'):
        cursor.execute("SELECT company_id FROM companies WHERE name = ?", (data_to_insert['name'],))
        result = cursor.fetchone()
        if result:
            existing_id = result['company_id']

    try:
        if existing_id:
            # Update existing company
            company_id = existing_id
            update_cols = [f"{col} = ?" for col in data_to_insert.keys()]
            sql = f"UPDATE companies SET {', '.join(update_cols)} WHERE company_id = ?"
            values = list(data_to_insert.values()) + [company_id]
            cursor.execute(sql, values)
            print(f"Updated company: {data_to_insert.get('name', 'N/A')} (ID: {company_id})")
        else:
            # Insert new company
            cols_str = ', '.join(data_to_insert.keys())
            placeholders = ', '.join(['?'] * len(data_to_insert))
            sql = f"INSERT INTO companies ({cols_str}) VALUES ({placeholders})"
            cursor.execute(sql, list(data_to_insert.values()))
            company_id = cursor.lastrowid
            print(f"Inserted new company: {data_to_insert.get('name', 'N/A')} (ID: {company_id})")
            
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding/updating company: {e}")
        conn.rollback()
        company_id = None # Ensure None is returned on error
    finally:
        if cursor:
            cursor.close()
            
    return company_id

def get_company_by_ticker(conn, ticker_symbol):
    """Retrieves a company by its ticker symbol."""
    if not conn or not ticker_symbol:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM companies WHERE ticker_symbol = ?", (ticker_symbol,))
        return cursor.fetchone() # Returns a Row object or None
    except sqlite3.Error as e:
        print(f"Error getting company by ticker {ticker_symbol}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def get_company_by_name(conn, name):
    """Retrieves a company by its name."""
    if not conn or not name:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM companies WHERE name = ?", (name,))
        return cursor.fetchone() # Returns a Row object or None
    except sqlite3.Error as e:
        print(f"Error getting company by name {name}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

# --- Placeholder functions for other tables (to be implemented similarly) ---

def add_company_officers(conn, company_id, officers_data):
    """Adds officer data for a specific company, clearing old data first."""
    if not conn or not company_id or not officers_data:
        return False
    cursor = conn.cursor()
    try:
        # Clear existing officers for this company
        cursor.execute("DELETE FROM company_officers WHERE company_id = ?", (company_id,))
        
        # Insert new officers
        officer_cols = ['name', 'title', 'age', 'year_born', 'fiscal_year', 'total_pay', 'exercised_value', 'unexercised_value']
        rows_to_insert = []
        for officer in officers_data:
            row = {'company_id': company_id, 'last_updated': datetime.now()}
            row.update({col: officer.get(col) for col in officer_cols if col in officer})
            rows_to_insert.append(row)

        if rows_to_insert:
            cols_str = ', '.join(rows_to_insert[0].keys())
            placeholders = ', '.join(['?'] * len(rows_to_insert[0]))
            sql = f"INSERT INTO company_officers ({cols_str}) VALUES ({placeholders})"
            values_list = [list(row.values()) for row in rows_to_insert]
            cursor.executemany(sql, values_list)
            
        conn.commit()
        print(f"Added/Updated {len(rows_to_insert)} officers for company ID: {company_id}")
        return True
    except sqlite3.Error as e:
        print(f"Error adding company officers: {e}")
        conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

def add_news_article(conn, article_data):
    """Adds a news article, avoiding duplicates based on source_url."""
    if not conn or not article_data or not article_data.get('source_url'):
        return None
    cursor = conn.cursor()
    article_id = None
    try:
        # Check if article exists by URL
        cursor.execute("SELECT article_id FROM news_articles WHERE source_url = ?", (article_data['source_url'],))
        result = cursor.fetchone()
        if result:
            print(f"Article already exists: {article_data['source_url']}")
            return result['article_id']

        # Insert new article
        columns = ['company_id', 'industry', 'topic', 'title', 'source_name', 'source_url', 
                   'published_date', 'summary', 'sentiment_score', 'sentiment_label', 'collected_date']
        data_to_insert = {col: article_data.get(col) for col in columns if col in article_data}
        data_to_insert['collected_date'] = data_to_insert.get('collected_date', datetime.now())
        
        cols_str = ', '.join(data_to_insert.keys())
        placeholders = ', '.join(['?'] * len(data_to_insert))
        sql = f"INSERT INTO news_articles ({cols_str}) VALUES ({placeholders})"
        cursor.execute(sql, list(data_to_insert.values()))
        article_id = cursor.lastrowid
        conn.commit()
        print(f"Added news article: {article_data.get('title', 'N/A')} (ID: {article_id})")
    except sqlite3.Error as e:
        print(f"Error adding news article: {e}")
        conn.rollback()
        article_id = None
    finally:
        if cursor:
            cursor.close()
    return article_id

def add_or_update_icp(conn, profile_name, criteria_json):
    """Adds or updates an ICP profile.
    
    Args:
        conn: Database connection
        profile_name: Name of the ICP profile
        criteria_json: JSON string containing ICP criteria
        
    Returns:
        The ICP ID (int) if successful, None otherwise
    """
    if not conn or not profile_name or not criteria_json:
        return None
        
    cursor = conn.cursor()
    icp_id = None
    try:
        # Check if the ICP profile already exists
        cursor.execute("SELECT icp_id FROM icps WHERE profile_name = ?", (profile_name,))
        result = cursor.fetchone()
        
        now = datetime.now()
        
        if result:
            # Update existing ICP
            icp_id = result['icp_id']
            cursor.execute(
                "UPDATE icps SET criteria_json = ?, last_used = ? WHERE icp_id = ?",
                (criteria_json, now, icp_id)
            )
            print(f"Updated ICP profile: {profile_name} (ID: {icp_id})")
        else:
            # Insert new ICP
            cursor.execute(
                "INSERT INTO icps (profile_name, criteria_json, created_at, last_used) VALUES (?, ?, ?, ?)",
                (profile_name, criteria_json, now, now)
            )
            icp_id = cursor.lastrowid
            print(f"Created new ICP profile: {profile_name} (ID: {icp_id})")
            
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding/updating ICP profile: {e}")
        conn.rollback()
        icp_id = None
    finally:
        if cursor:
            cursor.close()
            
    return icp_id

def get_icp_by_name(conn, profile_name):
    """Retrieves an ICP by its name.
    
    Args:
        conn: Database connection
        profile_name: Name of the ICP profile to retrieve
        
    Returns:
        Dictionary-like Row object containing ICP data if found, None otherwise
    """
    if not conn or not profile_name:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM icps WHERE profile_name = ?", (profile_name,))
        result = cursor.fetchone()
        
        if result:
            # Update last_used timestamp
            now = datetime.now()
            cursor.execute("UPDATE icps SET last_used = ? WHERE icp_id = ?", 
                           (now, result['icp_id']))
            conn.commit()
            print(f"Retrieved ICP profile: {profile_name} (ID: {result['icp_id']})")
        else:
            print(f"ICP profile not found: {profile_name}")
            
        return result
    except sqlite3.Error as e:
        print(f"Error retrieving ICP profile: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def add_lead(conn, lead_data):
    """Adds a new lead.
    
    Args:
        conn: Database connection
        lead_data: Dictionary containing lead data
        
    Returns:
        The lead ID (int) if successful, None otherwise
    """
    if not conn or not lead_data:
        return None
        
    cursor = conn.cursor()
    lead_id = None
    try:
        # Define valid columns based on the table schema
        columns = [
            'icp_id', 'company_name', 'contact_name', 'job_title', 'industry',
            'company_size', 'region', 'website', 'email', 'phone', 'linkedin_profile',
            'source', 'qualification_status', 'qualification_reason', 'score',
            'engagement_level', 'technologies_used', 'notes', 'status'
        ]
        
        # Prepare data with only valid columns
        data_to_insert = {col: lead_data.get(col) for col in columns if col in lead_data}
        data_to_insert['collected_date'] = lead_data.get('collected_date', datetime.now())
        
        # Insert the lead
        cols_str = ', '.join(data_to_insert.keys())
        placeholders = ', '.join(['?'] * len(data_to_insert))
        sql = f"INSERT INTO leads ({cols_str}) VALUES ({placeholders})"
        cursor.execute(sql, list(data_to_insert.values()))
        lead_id = cursor.lastrowid
        
        conn.commit()
        print(f"Added new lead: {data_to_insert.get('company_name', 'N/A')} - {data_to_insert.get('contact_name', 'N/A')} (ID: {lead_id})")
    except sqlite3.Error as e:
        print(f"Error adding lead: {e}")
        conn.rollback()
        lead_id = None
    finally:
        if cursor:
            cursor.close()
            
    return lead_id

def update_lead(conn, lead_id, lead_data):
    """Updates an existing lead.
    
    Args:
        conn: Database connection
        lead_id: ID of the lead to update
        lead_data: Dictionary containing updated lead data
        
    Returns:
        Boolean indicating success or failure
    """
    if not conn or not lead_id or not lead_data:
        return False
        
    cursor = conn.cursor()
    try:
        # Define valid columns based on the table schema
        columns = [
            'icp_id', 'company_name', 'contact_name', 'job_title', 'industry',
            'company_size', 'region', 'website', 'email', 'phone', 'linkedin_profile',
            'source', 'qualification_status', 'qualification_reason', 'score',
            'engagement_level', 'technologies_used', 'notes', 'status', 'last_contacted'
        ]
        
        # Prepare data with only valid columns
        data_to_update = {col: lead_data.get(col) for col in columns if col in lead_data}
        
        if not data_to_update:
            print("No valid fields to update")
            return False
            
        # Update the lead
        update_cols = [f"{col} = ?" for col in data_to_update.keys()]
        sql = f"UPDATE leads SET {', '.join(update_cols)} WHERE lead_id = ?"
        values = list(data_to_update.values()) + [lead_id]
        cursor.execute(sql, values)
        
        if cursor.rowcount == 0:
            print(f"Lead ID {lead_id} not found or no changes made")
            return False
            
        conn.commit()
        print(f"Updated lead ID: {lead_id}")
        return True
    except sqlite3.Error as e:
        print(f"Error updating lead: {e}")
        conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

def add_market_trend(conn, trend_data):
    """Adds a market trend."""
    # ... implementation ...
    pass

def add_india_real_estate_project(conn, project_data):
    """Adds an India real estate project, avoiding duplicates based on RERA ID or name+developer."""
    if not conn or not project_data:
        return None
    cursor = conn.cursor()
    project_id = None
    try:
        # Check for duplicates based on RERA ID if available
        rera_id = project_data.get("rera_registration_id")
        if rera_id:
            cursor.execute("SELECT project_id FROM india_real_estate_projects WHERE rera_registration_id = ?", (rera_id,))
            result = cursor.fetchone()
            if result:
                print(f"Real estate project with RERA ID {rera_id} already exists.")
                return result["project_id"]
        
        # Check for duplicates based on name and developer name if RERA ID is not present or not found
        project_name = project_data.get("project_name")
        developer_name = project_data.get("developer_name")
        if project_name and developer_name:
             cursor.execute("SELECT project_id FROM india_real_estate_projects WHERE project_name = ? AND developer_name = ?", (project_name, developer_name))
             result = cursor.fetchone()
             if result:
                print(f"Real estate project {project_name} by {developer_name} already exists.")
                return result["project_id"]

        # Insert new project
        columns = [
            "project_name", "developer_id", "developer_name", "city", "region", 
            "project_type", "status", "rera_registration_id", "launch_date", 
            "expected_completion_date", "total_area_sqft", "price_per_sqft_range", 
            "key_features", "source_url", "collected_date"
        ]
        data_to_insert = {col: project_data.get(col) for col in columns if col in project_data}
        data_to_insert["collected_date"] = data_to_insert.get("collected_date", datetime.now())
        
        cols_str = ", ".join(data_to_insert.keys())
        placeholders = ", ".join(["?"] * len(data_to_insert))
        sql = f"INSERT INTO india_real_estate_projects ({cols_str}) VALUES ({placeholders})"
        cursor.execute(sql, list(data_to_insert.values()))
        project_id = cursor.lastrowid
        conn.commit()
        print(f"Added India real estate project: {project_data.get('project_name', 'N/A')} (ID: {project_id})")
    except sqlite3.Error as e:
        print(f"Error adding India real estate project: {e}")
        conn.rollback()
        project_id = None
    finally:
        if cursor:
            cursor.close()
    return project_id

def add_india_architectural_firm(conn, firm_data):
    """Adds an India architectural firm, avoiding duplicates based on firm name or COA registration ID."""
    if not conn or not firm_data:
        return None
    cursor = conn.cursor()
    firm_id = None
    try:
        # Check for duplicates based on COA registration ID if available
        coa_id = firm_data.get("coa_registration_id")
        if coa_id:
            cursor.execute("SELECT firm_id FROM india_architectural_firms WHERE coa_registration_id = ?", (coa_id,))
            result = cursor.fetchone()
            if result:
                print(f"Architectural firm with COA ID {coa_id} already exists.")
                return result["firm_id"]
        
        # Check for duplicates based on firm name
        firm_name = firm_data.get("firm_name")
        if firm_name:
            cursor.execute("SELECT firm_id FROM india_architectural_firms WHERE firm_name = ?", (firm_name,))
            result = cursor.fetchone()
            if result:
                print(f"Architectural firm {firm_name} already exists.")
                return result["firm_id"]

        # Insert new firm
        columns = [
            "company_id", "firm_name", "city", "region", "specialization", 
            "notable_projects", "key_personnel", "awards", "coa_registration_id", 
            "source_url", "collected_date"
        ]
        data_to_insert = {col: firm_data.get(col) for col in columns if col in firm_data}
        data_to_insert["collected_date"] = data_to_insert.get("collected_date", datetime.now())
        
        cols_str = ", ".join(data_to_insert.keys())
        placeholders = ", ".join(["?"] * len(data_to_insert))
        sql = f"INSERT INTO india_architectural_firms ({cols_str}) VALUES ({placeholders})"
        cursor.execute(sql, list(data_to_insert.values()))
        firm_id = cursor.lastrowid
        conn.commit()
        print(f"Added India architectural firm: {firm_data.get('firm_name', 'N/A')} (ID: {firm_id})")
    except sqlite3.Error as e:
        print(f"Error adding India architectural firm: {e}")
        conn.rollback()
        firm_id = None
    finally:
        if cursor:
            cursor.close()
    return firm_id

def add_analysis_result(conn, analysis_data):
    """Adds an analysis result."""
    # ... implementation ...
    pass

def get_leads_by_ids(conn, lead_ids):
    """Retrieves leads by their IDs.
    
    Args:
        conn: Database connection
        lead_ids: List of lead IDs to retrieve
        
    Returns:
        List of dictionary-like Row objects containing lead data
    """
    if not conn or not lead_ids:
        return []
        
    cursor = conn.cursor()
    results = []
    try:
        # Convert lead_ids to tuple for SQL IN clause
        if isinstance(lead_ids, (list, tuple)):
            # Format for SQL IN clause
            id_str = ','.join('?' for _ in lead_ids)
            query = f"SELECT * FROM leads WHERE lead_id IN ({id_str})"
            cursor.execute(query, lead_ids)
        else:
            # Single ID case
            cursor.execute("SELECT * FROM leads WHERE lead_id = ?", (lead_ids,))
            
        results = cursor.fetchall()
        print(f"Retrieved {len(results)} leads")
        return results
    except sqlite3.Error as e:
        print(f"Error retrieving leads by IDs: {e}")
        return []
    finally:
        if cursor:
            cursor.close()

def get_lead_by_company_icp(conn, company_name=None, icp_id=None):
    """Retrieves leads for a specific company matching an ICP.
    
    Args:
        conn: Database connection
        company_name: Name or ID of the company to filter leads by (optional)
        icp_id: ID of the ICP profile to filter leads by (optional)
        
    Returns:
        List of dictionary-like Row objects containing lead data
    """
    if not conn:
        return []
        
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM leads WHERE 1=1"
        params = []
        
        # Handle company_name parameter that could be a name string or company ID
        if company_name:
            # If company_name is an integer or can be converted to one, treat as company ID
            if isinstance(company_name, int) or (isinstance(company_name, str) and company_name.isdigit()):
                # First check if we can find the company name from companies table
                company_id = int(company_name)
                cursor.execute("SELECT name FROM companies WHERE company_id = ?", (company_id,))
                company_result = cursor.fetchone()
                if company_result:
                    company_name_str = company_result['name']
                    query += " AND company_name = ?"
                    params.append(company_name_str)
                else:
                    # Fallback: use ID directly (though not likely to match any entries)
                    query += " AND company_name = ?"
                    params.append(str(company_name))
            else:
                # Regular company name search (with LIKE for partial matches)
                query += " AND company_name LIKE ?"
                params.append(f"%{company_name}%")
            
        if icp_id:
            query += " AND icp_id = ?"
            params.append(icp_id)
        
        query += " ORDER BY score DESC, collected_date DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        if company_name and icp_id:
            print(f"Retrieved {len(results)} leads for company '{company_name}' with ICP ID {icp_id}")
        elif company_name:
            print(f"Retrieved {len(results)} leads for company '{company_name}'")
        elif icp_id:
            print(f"Retrieved {len(results)} leads for ICP ID {icp_id}")
        else:
            print(f"Retrieved {len(results)} leads (no filters applied)")
            
        return results
    except sqlite3.Error as e:
        print(f"Error retrieving leads by company and ICP: {e}")
        return []
    finally:
        if cursor:
            cursor.close()

# --- Initialization --- 
def initialize_database():
    """Initializes the database by creating tables if they don't exist."""
    print("Initializing database...")
    conn = get_db_connection()
    if conn:
        create_tables(conn)
        conn.close()
        print("Database initialization complete.")
    else:
        print("Database initialization failed: Could not connect.")

# Example usage / Basic Test
if __name__ == "__main__":
    # Ensure the directory exists (optional, SQLite creates the file)
    db_dir = os.path.dirname(DATABASE_NAME)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    initialize_database()
    
    # Test adding a company
    conn = get_db_connection()
    if conn:
        test_company = {
            'name': 'Test Company Inc.',
            'ticker_symbol': 'TEST.IN',
            'region': 'IN',
            'industry': 'Technology',
            'sector': 'Software',
            'website': 'http://testcompany.com',
            'employee_count': 100,
            'business_summary': 'A test company for demonstration.',
            'data_source': 'Manual'
        }
        company_id = add_or_update_company(conn, test_company)
        
        if company_id:
            # Test retrieving the company
            retrieved_company = get_company_by_ticker(conn, 'TEST.IN')
            if retrieved_company:
                print(f"\nRetrieved Company by Ticker ({retrieved_company['ticker_symbol']}):")
                print(dict(retrieved_company))
            else:
                print("\nFailed to retrieve company by ticker.")
                
            # Test adding officers
            test_officers = [
                {'name': 'John Doe', 'title': 'CEO', 'age': 45},
                {'name': 'Jane Smith', 'title': 'CTO', 'total_pay': 500000}
            ]
            add_company_officers(conn, company_id, test_officers)
            
            # Test adding a news article
            test_article = {
                'company_id': company_id,
                'title': 'Test Company Announces Breakthrough',
                'source_name': 'Test News',
                'source_url': 'http://testnews.com/article123',
                'published_date': datetime.now(),
                'summary': 'A major breakthrough was announced.',
                'sentiment_score': 0.8,
                'sentiment_label': 'positive'
            }
            add_news_article(conn, test_article)
            # Try adding the same article again (should be skipped)
            add_news_article(conn, test_article)
            
        else:
            print("\nFailed to add test company.")
            
        conn.close()
    else:
        print("\nFailed to connect to database for testing.")

