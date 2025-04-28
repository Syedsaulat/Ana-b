"""
Add Bengaluru Real Estate and Construction Data

This script populates the database with real estate developers, construction companies,
architectural firms, and real estate projects based in Bengaluru, India.
"""

import os
import sqlite3
from datetime import datetime, timedelta
import random
import sys

# Import database manager
sys.path.append(os.path.dirname(__file__))
import database_manager as db_manager

# Realistic Bengaluru real estate developers
BENGALURU_DEVELOPERS = [
    {
        "name": "Prestige Group",
        "ticker_symbol": "PRESTIGE.NS",
        "region": "IN",
        "industry": "Real Estate Development",
        "sector": "Real Estate",
        "website": "https://www.prestigeconstructions.com",
        "address": "The Falcon House, No. 1, Main Guard Cross Road, Bengaluru",
        "phone": "+91-80-25591080",
        "employee_count": 1200,
        "business_summary": "One of South India's leading real estate developers with projects across residential, commercial, retail, leisure and hospitality segments.",
        "market_cap": 60000000000.0,  # 6000 Crores INR
        "revenue": 12000000000.0,  # 1200 Crores INR annually
        "growth_rate": 15.3,
        "profit_margin": 22.4,
        "innovativeness_score": 0.78,
        "sustainability_score": 0.82,
        "data_source": "Manual Entry"
    },
    {
        "name": "Brigade Group",
        "ticker_symbol": "BRIGADE.NS",
        "region": "IN",
        "industry": "Real Estate Development",
        "sector": "Real Estate",
        "website": "https://www.brigadegroup.com",
        "address": "Brigade Gateway, 26/1, Dr. Rajkumar Road, Bengaluru",
        "phone": "+91-80-41379200",
        "employee_count": 850,
        "business_summary": "Leading property developer focusing on residential, commercial, retail and hospitality sectors with projects in Bengaluru, Chennai, Hyderabad, and Mysore.",
        "market_cap": 42000000000.0,  # 4200 Crores INR
        "revenue": 8500000000.0,  # 850 Crores INR annually
        "growth_rate": 12.8,
        "profit_margin": 18.6,
        "innovativeness_score": 0.73,
        "sustainability_score": 0.76,
        "data_source": "Manual Entry"
    },
    {
        "name": "Sobha Limited",
        "ticker_symbol": "SOBHA.NS",
        "region": "IN",
        "industry": "Real Estate Development",
        "sector": "Real Estate",
        "website": "https://www.sobha.com",
        "address": "SOBHA House, Sarjapur-Marathahalli Outer Ring Road, Bengaluru",
        "phone": "+91-80-49320000",
        "employee_count": 3000,
        "business_summary": "Leading backward integrated real estate developer with presence in 27 cities and 13 states in India, focusing on luxury residential projects.",
        "market_cap": 38000000000.0,  # 3800 Crores INR
        "revenue": 10000000000.0,  # 1000 Crores INR annually
        "growth_rate": 11.5,
        "profit_margin": 17.3,
        "innovativeness_score": 0.81,
        "sustainability_score": 0.79,
        "data_source": "Manual Entry"
    },
    {
        "name": "Puravankara Limited",
        "ticker_symbol": "PURVA.NS",
        "region": "IN",
        "industry": "Real Estate Development",
        "sector": "Real Estate",
        "website": "https://www.puravankara.com",
        "address": "130/1, Ulsoor Road, Bengaluru",
        "phone": "+91-80-25599000",
        "employee_count": 750,
        "business_summary": "Leading real estate company with a strong presence in Bengaluru, Chennai, Hyderabad, Pune and Kochi, with a focus on affordable and luxury housing.",
        "market_cap": 28000000000.0,  # 2800 Crores INR
        "revenue": 6500000000.0,  # 650 Crores INR annually
        "growth_rate": 9.2,
        "profit_margin": 14.8,
        "innovativeness_score": 0.68,
        "sustainability_score": 0.72,
        "data_source": "Manual Entry"
    },
    {
        "name": "Embassy Group",
        "ticker_symbol": "EMBASSY.NSE",  # Embassy Office Parks REIT
        "region": "IN",
        "industry": "Real Estate Development",
        "sector": "Real Estate",
        "website": "https://www.embassyindia.com",
        "address": "Embassy Point, 150, Infantry Road, Bengaluru",
        "phone": "+91-80-22280881",
        "employee_count": 950,
        "business_summary": "Leading developer of commercial and residential real estate with significant portfolio of office parks, hotels, and residential properties across India.",
        "market_cap": 120000000000.0,  # 12000 Crores INR (for the REIT)
        "revenue": 23000000000.0,  # 2300 Crores INR annually
        "growth_rate": 18.7,
        "profit_margin": 26.3,
        "innovativeness_score": 0.86,
        "sustainability_score": 0.84,
        "data_source": "Manual Entry"
    }
]

# Realistic Bengaluru construction companies
BENGALURU_CONSTRUCTION = [
    {
        "name": "Ahluwalia Contracts (India) Limited",
        "ticker_symbol": "AHLUCONT.NS",
        "region": "IN",
        "industry": "Construction",
        "sector": "Infrastructure",
        "website": "https://www.acilnet.com",
        "address": "4th Floor, Ahluwalia House, Plot No. 28, Bengaluru",
        "phone": "+91-80-41132965",
        "employee_count": 2200,
        "business_summary": "Leading construction company specializing in commercial, residential, institutional and industrial projects across India.",
        "market_cap": 30000000000.0,  # 3000 Crores INR
        "revenue": 15000000000.0,  # 1500 Crores INR annually
        "growth_rate": 8.7,
        "profit_margin": 10.2,
        "innovativeness_score": 0.65,
        "sustainability_score": 0.67,
        "data_source": "Manual Entry"
    },
    {
        "name": "Nagarjuna Construction Company",
        "ticker_symbol": "NCC.NS",
        "region": "IN",
        "industry": "Construction",
        "sector": "Infrastructure",
        "website": "https://www.ncclimited.com",
        "address": "NCC House, Madhapur, Bengaluru Office",
        "phone": "+91-80-26566498",
        "employee_count": 3500,
        "business_summary": "Infrastructure construction company with operations in buildings, water, environment, transportation, irrigation, power, metals, mining and railways.",
        "market_cap": 25000000000.0,  # 2500 Crores INR
        "revenue": 18000000000.0,  # 1800 Crores INR annually
        "growth_rate": 7.9,
        "profit_margin": 8.5,
        "innovativeness_score": 0.61,
        "sustainability_score": 0.65,
        "data_source": "Manual Entry"
    },
    {
        "name": "JMC Projects (India) Limited",
        "ticker_symbol": "JMCPROJECT.NS",
        "region": "IN",
        "industry": "Construction",
        "sector": "Infrastructure",
        "website": "https://www.jmcprojects.com",
        "address": "Bengaluru Regional Office, Koramangala",
        "phone": "+91-80-40115611",
        "employee_count": 1800,
        "business_summary": "Leading construction company executing projects in buildings, factories, housing, road, bridges, water supply and irrigation sectors.",
        "market_cap": 15000000000.0,  # 1500 Crores INR
        "revenue": 9000000000.0,  # 900 Crores INR annually
        "growth_rate": 6.8,
        "profit_margin": 7.2,
        "innovativeness_score": 0.59,
        "sustainability_score": 0.64,
        "data_source": "Manual Entry"
    }
]

# Realistic Bengaluru architectural firms
BENGALURU_ARCHITECTURE_FIRMS = [
    {
        "firm_name": "Mindspace Architects",
        "city": "Bengaluru",
        "region": "Karnataka",
        "specialization": "Residential, Commercial, Institutional",
        "notable_projects": "Brigade Orchards Clubhouse, UVCE Centenary Building",
        "key_personnel": "Ar. Sanjay Mohe, Ar. Vasuki Prakash, Ar. Suryanarayanan",
        "awards": "IIA Award for Excellence in Architecture 2018, A+D Awards for Public Buildings 2021",
        "coa_registration_id": "CA/2000/23456",
        "source_url": "https://www.mindspacearchitects.com"
    },
    {
        "firm_name": "Cadence Architects",
        "city": "Bengaluru",
        "region": "Karnataka",
        "specialization": "Residential, Commercial, Hospitality",
        "notable_projects": "Elastica House, The Shoreline Villas, The Library House",
        "key_personnel": "Ar. Narendra Pirgal, Ar. Vikram Rajashekar, Ar. Smaran Mallesh",
        "awards": "NDTV Design & Architecture Awards 2023, IIID Design Excellence Award 2019",
        "coa_registration_id": "CA/2005/34215",
        "source_url": "https://www.cadencearchitects.com"
    },
    {
        "firm_name": "BetweenSpaces",
        "city": "Bengaluru",
        "region": "Karnataka",
        "specialization": "Residential, Interior Design, Urban Design",
        "notable_projects": "The Cuckoo's Nest, Badari Residence, Volume House",
        "key_personnel": "Ar. Divya Ethirajan, Ar. Pramod Jaiswal",
        "awards": "The Merit List 2022, JK AYA Awards for Young Architects 2017",
        "coa_registration_id": "CA/2010/45268",
        "source_url": "https://www.betweenspaces.in"
    },
    {
        "firm_name": "Architecture Paradigm",
        "city": "Bengaluru",
        "region": "Karnataka",
        "specialization": "Institutional, Residential, Urban Planning",
        "notable_projects": "School of Sciences for Christ University, SDM Institute, Agastya International Foundation",
        "key_personnel": "Ar. Sandeep J, Ar. Manoj Ladhad, Ar. Vimal Jain",
        "awards": "World Architecture Community Award 2021, HUDCO Design Awards 2019",
        "coa_registration_id": "CA/2003/27189",
        "source_url": "https://www.architectureparadigm.com"
    }
]

# Realistic Bengaluru real estate projects
BENGALURU_REAL_ESTATE_PROJECTS = [
    {
        "project_name": "Prestige Lakeside Habitat",
        "developer_name": "Prestige Group",
        "city": "Bengaluru",
        "region": "Karnataka",
        "project_type": "Residential",
        "status": "Completed",
        "rera_registration_id": "PRM/KA/RERA/1251/446/PR/171014/000433",
        "launch_date": (datetime.now() - timedelta(days=1200)).strftime('%Y-%m-%d'),
        "expected_completion_date": (datetime.now() - timedelta(days=300)).strftime('%Y-%m-%d'),
        "total_area_sqft": 5200000,
        "price_per_sqft_range": "7,500 - 8,500 INR",
        "key_features": "Lakefront apartments, 80 acres township, 3 & 4 BHK configurations, Clubhouse, Swimming pool, Gym",
        "source_url": "https://www.prestigeconstructions.com/projects/prestige-lakeside-habitat"
    },
    {
        "project_name": "Brigade Meadows",
        "developer_name": "Brigade Group",
        "city": "Bengaluru",
        "region": "Karnataka",
        "project_type": "Residential",
        "status": "Ongoing",
        "rera_registration_id": "PRM/KA/RERA/1251/310/PR/190729/002644",
        "launch_date": (datetime.now() - timedelta(days=800)).strftime('%Y-%m-%d'),
        "expected_completion_date": (datetime.now() + timedelta(days=400)).strftime('%Y-%m-%d'),
        "total_area_sqft": 3600000,
        "price_per_sqft_range": "6,200 - 7,100 INR",
        "key_features": "60 acres township, 1, 2 & 3 BHK apartments, School, Retail spaces, Healthcare facilities",
        "source_url": "https://www.brigadegroup.com/residential/bangalore/south-bangalore/brigade-meadows"
    },
    {
        "project_name": "Sobha Dream Gardens",
        "developer_name": "Sobha Limited",
        "city": "Bengaluru",
        "region": "Karnataka",
        "project_type": "Residential",
        "status": "Ongoing",
        "rera_registration_id": "PRM/KA/RERA/1251/309/PR/180519/001895",
        "launch_date": (datetime.now() - timedelta(days=900)).strftime('%Y-%m-%d'),
        "expected_completion_date": (datetime.now() + timedelta(days=500)).strftime('%Y-%m-%d'),
        "total_area_sqft": 2800000,
        "price_per_sqft_range": "7,000 - 7,600 INR",
        "key_features": "1, 2 & 3 BHK apartments, 28 acres development, Clubhouse, Swimming pool, Sports facilities",
        "source_url": "https://www.sobha.com/projects/sobha-dream-gardens"
    },
    {
        "project_name": "Embassy Springs",
        "developer_name": "Embassy Group",
        "city": "Bengaluru",
        "region": "Karnataka",
        "project_type": "Residential",
        "status": "Ongoing",
        "rera_registration_id": "PRM/KA/RERA/1251/446/PR/171128/000495",
        "launch_date": (datetime.now() - timedelta(days=1500)).strftime('%Y-%m-%d'),
        "expected_completion_date": (datetime.now() + timedelta(days=900)).strftime('%Y-%m-%d'),
        "total_area_sqft": 8800000,
        "price_per_sqft_range": "6,800 - 8,000 INR",
        "key_features": "288 acres township, Villa plots, Apartments, Golf course, International school, Hospital",
        "source_url": "https://www.embassysprings.com"
    },
    {
        "project_name": "Purva Atmosphere",
        "developer_name": "Puravankara Limited",
        "city": "Bengaluru",
        "region": "Karnataka",
        "project_type": "Residential",
        "status": "Under Construction",
        "rera_registration_id": "PRM/KA/RERA/1251/309/PR/190511/002460",
        "launch_date": (datetime.now() - timedelta(days=600)).strftime('%Y-%m-%d'),
        "expected_completion_date": (datetime.now() + timedelta(days=700)).strftime('%Y-%m-%d'),
        "total_area_sqft": 2100000,
        "price_per_sqft_range": "6,500 - 7,200 INR",
        "key_features": "2 & 3 BHK apartments, 14 acres development, BluNex Life (smart home features), Clubhouse, Sports arena",
        "source_url": "https://www.puravankara.com/projects/bengaluru/north-bangalore/purva-atmosphere"
    },
    {
        "project_name": "Adarsh Palm Retreat",
        "developer_name": "Adarsh Developers",
        "city": "Bengaluru",
        "region": "Karnataka",
        "project_type": "Residential",
        "status": "Completed",
        "rera_registration_id": "PRM/KA/RERA/1251/310/PR/131118/002193",
        "launch_date": (datetime.now() - timedelta(days=1800)).strftime('%Y-%m-%d'),
        "expected_completion_date": (datetime.now() - timedelta(days=500)).strftime('%Y-%m-%d'),
        "total_area_sqft": 4500000,
        "price_per_sqft_range": "7,800 - 9,000 INR",
        "key_features": "Luxury villas and apartments, 72 acres township, Clubhouse, Swimming pool, Tennis courts",
        "source_url": "https://www.adarshdevelopers.com/projects/adarsh-palm-retreat"
    },
    {
        "project_name": "Prestige Tech Cloud",
        "developer_name": "Prestige Group",
        "city": "Bengaluru",
        "region": "Karnataka",
        "project_type": "Commercial",
        "status": "Ongoing",
        "rera_registration_id": "PRM/KA/RERA/1251/446/PR/200205/003112",
        "launch_date": (datetime.now() - timedelta(days=500)).strftime('%Y-%m-%d'),
        "expected_completion_date": (datetime.now() + timedelta(days=600)).strftime('%Y-%m-%d'),
        "total_area_sqft": 1800000,
        "price_per_sqft_range": "12,000 - 14,000 INR",
        "key_features": "Grade A office spaces, LEED Gold certification, High-speed elevators, 24x7 security, Power backup",
        "source_url": "https://www.prestigeconstructions.com/projects/prestige-tech-cloud"
    },
    {
        "project_name": "Brigade Orchards",
        "developer_name": "Brigade Group",
        "city": "Bengaluru",
        "region": "Karnataka",
        "project_type": "Mixed Use",
        "status": "Partially Completed",
        "rera_registration_id": "PRM/KA/RERA/1251/309/PR/170829/000214",
        "launch_date": (datetime.now() - timedelta(days=2200)).strftime('%Y-%m-%d'),
        "expected_completion_date": (datetime.now() + timedelta(days=1100)).strftime('%Y-%m-%d'),
        "total_area_sqft": 12500000,
        "price_per_sqft_range": "6,500 - 8,500 INR",
        "key_features": "130+ acres integrated township, Apartments, Villas, Office spaces, Sports arena, School, Hospital",
        "source_url": "https://www.brigadegroup.com/residential/bangalore/north-bangalore/brigade-orchards"
    }
]

# News articles for these companies/projects
BENGALURU_NEWS_ARTICLES = [
    {
        "company_name": "Prestige Group",
        "title": "Prestige Group Reports 28% YoY Growth in Q4 FY25",
        "source_name": "Economic Times Real Estate",
        "source_url": "https://realty.economictimes.indiatimes.com/news/prestige-group-q4-fy25-results",
        "published_date": (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
        "summary": "Prestige Group announced a 28% year-on-year growth in revenue for Q4 FY25, with pre-sales value reaching ₹4,267 crore. The company launched 4 new projects in Bengaluru during the quarter.",
        "sentiment_score": 0.72,
        "sentiment_label": "positive"
    },
    {
        "company_name": "Brigade Group",
        "title": "Brigade Group to Invest ₹3,000 Crore in Bengaluru Commercial Projects",
        "source_name": "Business Standard",
        "source_url": "https://www.business-standard.com/article/companies/brigade-group-invest-3000cr-bengaluru",
        "published_date": (datetime.now() - timedelta(days=22)).strftime('%Y-%m-%d'),
        "summary": "Brigade Group has announced plans to invest approximately ₹3,000 crore over the next 3 years to develop 5 million sq ft of commercial space in Bengaluru, capitalizing on the growing demand for Grade A office spaces.",
        "sentiment_score": 0.65,
        "sentiment_label": "positive"
    },
    {
        "company_name": "Sobha Limited",
        "title": "Sobha Limited Focuses on Sustainable Development in New Projects",
        "source_name": "Indian Real Estate News",
        "source_url": "https://www.indianrealestate.com/news/sobha-sustainable-development-focus",
        "published_date": (datetime.now() - timedelta(days=35)).strftime('%Y-%m-%d'),
        "summary": "Sobha Limited has announced its renewed focus on sustainable development practices for all upcoming projects, with plans to achieve GRIHA 5-star rating for its new residential developments in Bengaluru.",
        "sentiment_score": 0.68,
        "sentiment_label": "positive"
    },
    {
        "company_name": "Embassy Group",
        "title": "Embassy Office Parks REIT Announces 4% Increase in Distributions",
        "source_name": "Financial Express",
        "source_url": "https://www.financialexpress.com/real-estate/embassy-reit-q4-distribution",
        "published_date": (datetime.now() - timedelta(days=12)).strftime('%Y-%m-%d'),
        "summary": "Embassy Office Parks REIT has announced a 4% YoY increase in distributions to unitholders for Q4 FY25, reflecting strong lease renewals and new occupier signings in their Bengaluru properties despite challenging market conditions.",
        "sentiment_score": 0.58,
        "sentiment_label": "positive"
    },
    {
        "company_name": "Puravankara Limited",
        "title": "Puravankara Limited Faces Approval Delays for New Bengaluru Project",
        "source_name": "Property News India",
        "source_url": "https://www.propertynewsindia.com/puravankara-approval-delays-bengaluru",
        "published_date": (datetime.now() - timedelta(days=18)).strftime('%Y-%m-%d'),
        "summary": "Puravankara Limited is experiencing delays in receiving environmental clearances for its upcoming residential project in North Bengaluru, potentially pushing the launch date by 3-4 months according to company officials.",
        "sentiment_score": -0.32,
        "sentiment_label": "negative"
    },
    {
        "company_name": "Real Estate Bengaluru",
        "title": "Bengaluru Real Estate Market Shows Resilience Amid Rising Interest Rates",
        "source_name": "Housing News",
        "source_url": "https://housing.com/news/bengaluru-real-estate-market-q1-2025",
        "published_date": (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
        "summary": "Despite rising home loan interest rates, the Bengaluru residential market has shown remarkable resilience with a 12% YoY growth in sales volume in Q1 2025, driven primarily by strong demand in the mid-premium segment.",
        "sentiment_score": 0.61,
        "sentiment_label": "positive"
    },
    {
        "company_name": "Construction Bengaluru",
        "title": "Construction Costs in Bengaluru Increase by 15% YoY",
        "source_name": "Construction World",
        "source_url": "https://www.constructionworld.in/bengaluru-construction-costs-2025",
        "published_date": (datetime.now() - timedelta(days=40)).strftime('%Y-%m-%d'),
        "summary": "Construction costs in Bengaluru have risen by approximately 15% year-on-year, primarily due to increasing raw material prices and labor costs, putting pressure on developers' margins and potentially leading to price increases for end consumers.",
        "sentiment_score": -0.28,
        "sentiment_label": "negative"
    },
    {
        "company_name": "Architecture Bengaluru",
        "title": "Bengaluru Architects Embrace Climate-Responsive Design",
        "source_name": "Architecture & Design",
        "source_url": "https://www.architectureanddesign.com/bengaluru-climate-responsive-design",
        "published_date": (datetime.now() - timedelta(days=55)).strftime('%Y-%m-%d'),
        "summary": "Leading architectural firms in Bengaluru are increasingly adopting climate-responsive design principles, incorporating passive cooling techniques, rainwater harvesting, and sustainable materials to address the city's changing climate conditions.",
        "sentiment_score": 0.75,
        "sentiment_label": "positive"
    }
]

def add_bengaluru_real_estate_data():
    """Add Bengaluru real estate and construction data to the database."""
    print("Adding Bengaluru real estate and construction data to the database...")
    
    # Connect to the database
    conn = db_manager.get_db_connection()
    if not conn:
        print("Failed to connect to database. Exiting.")
        return False
    
    try:
        # Add companies (developers and construction firms)
        company_ids = {}
        all_companies = BENGALURU_DEVELOPERS + BENGALURU_CONSTRUCTION
        
        for company_data in all_companies:
            company_id = db_manager.add_or_update_company(conn, company_data)
            if company_id:
                company_ids[company_data["name"]] = company_id
                print(f"Added/Updated company: {company_data['name']} (ID: {company_id})")
        
        # Add architectural firms
        for firm_data in BENGALURU_ARCHITECTURE_FIRMS:
            # If the firm has a corresponding company in our database, link it
            company_id = company_ids.get(firm_data["firm_name"])
            if company_id:
                firm_data["company_id"] = company_id
                
            firm_id = db_manager.add_india_architectural_firm(conn, firm_data)
            if firm_id:
                print(f"Added architectural firm: {firm_data['firm_name']} (ID: {firm_id})")
        
        # Add real estate projects
        for project_data in BENGALURU_REAL_ESTATE_PROJECTS:
            # If the project's developer has a corresponding company in our database, link it
            developer_id = company_ids.get(project_data["developer_name"])
            if developer_id:
                project_data["developer_id"] = developer_id
                
            project_id = db_manager.add_india_real_estate_project(conn, project_data)
            if project_id:
                print(f"Added real estate project: {project_data['project_name']} (ID: {project_id})")
        
        # Add news articles
        for article_data in BENGALURU_NEWS_ARTICLES:
            company_name = article_data.pop("company_name", None)
            company_id = None
            
            # Try to link article to company if exists
            if company_name:
                company_id = company_ids.get(company_name)
                
                # If not a company name, search by industry keyword
                if not company_id:
                    if "Real Estate" in company_name:
                        article_data["industry"] = "Real Estate Development"
                    elif "Construction" in company_name:
                        article_data["industry"] = "Construction"
                    elif "Architecture" in company_name:
                        article_data["industry"] = "Architecture"
            
            if company_id:
                article_data["company_id"] = company_id
                
            article_id = db_manager.add_news_article(conn, article_data)
            if article_id:
                print(f"Added news article: {article_data['title']} (ID: {article_id})")
        
        print("Successfully added Bengaluru real estate and construction data to the database!")
        return True
        
    except Exception as e:
        print(f"Error adding data: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# Add market trends for real estate in Bengaluru
def add_bengaluru_market_trends(conn):
    """Add market trends for real estate in Bengaluru."""
    # This would implement adding market trends to the database
    # For now, we'll skip this part to keep the script simpler
    pass

# Main execution
if __name__ == "__main__":
    add_bengaluru_real_estate_data()