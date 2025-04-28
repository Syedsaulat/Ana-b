# Market-Ready Business AI Agent: Database Architecture (SQLite)

## 1. Overview

This document outlines the database architecture for the enhanced Business AI Agent. Based on the `enhanced_agent_requirements.md`, this design uses SQLite for simplicity and ease of deployment. The schema is designed to store company information, market data, leads, user configurations, and industry-specific details, particularly for India's Architecture and Real Estate sectors.

## 2. Database Choice

**SQLite:** Chosen for its serverless nature, zero-configuration setup, and single-file database format, making it suitable for a self-contained application package. For larger-scale deployments, migrating to PostgreSQL or another client-server database would be recommended.

## 3. Schema Design

The following tables define the structure of the database (`business_agent.db`):

### 3.1 `companies`

Stores profile information about companies (including competitors and the user's company).

```sql
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    ticker_symbol TEXT UNIQUE, -- For public companies (e.g., from Yahoo Finance)
    region TEXT, -- e.g., IN, US
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
    innovativeness_score REAL, -- From Yahoo Finance insights
    hiring_score REAL, -- From Yahoo Finance insights
    sustainability_score REAL, -- From Yahoo Finance insights
    insider_sentiment_score REAL, -- From Yahoo Finance insights
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source TEXT -- e.g., YahooFinance, WebScrape, Manual
);
```

### 3.2 `company_officers`

Stores information about key executives/officers for companies.

```sql
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
    FOREIGN KEY (company_id) REFERENCES companies (company_id)
);
```

### 3.3 `market_trends`

Stores identified market trends.

```sql
CREATE TABLE IF NOT EXISTS market_trends (
    trend_id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry TEXT,
    region TEXT,
    trend_description TEXT NOT NULL,
    trend_type TEXT, -- e.g., Emerging, Declining, Technology, Regulatory
    source TEXT, -- e.g., NewsAPI, WebScrape:TechCrunch, GoogleTrends
    source_url TEXT,
    published_date DATE,
    collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment_score REAL, -- Optional sentiment of the trend description/source
    relevance_score REAL -- Optional score indicating relevance to user/ICP
);
```

### 3.4 `news_articles`

Stores references to relevant news articles.

```sql
CREATE TABLE IF NOT EXISTS news_articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER, -- Link to company if article is company-specific
    industry TEXT, -- Link to industry if article is industry-specific
    topic TEXT, -- General topic if not specific to company/industry
    title TEXT NOT NULL,
    source_name TEXT,
    source_url TEXT UNIQUE NOT NULL,
    published_date TIMESTAMP,
    summary TEXT,
    sentiment_score REAL,
    sentiment_label TEXT, -- positive, negative, neutral
    collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies (company_id)
);
```

### 3.5 `icps` (Ideal Customer Profiles)

Stores user-defined Ideal Customer Profiles.

```sql
CREATE TABLE IF NOT EXISTS icps (
    icp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_name TEXT NOT NULL UNIQUE, -- User-defined name for the ICP
    criteria_json TEXT NOT NULL, -- Store the complex criteria as a JSON string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP
);
```

### 3.6 `leads`

Stores information about potential leads.

```sql
CREATE TABLE IF NOT EXISTS leads (
    lead_id INTEGER PRIMARY KEY AUTOINCREMENT,
    icp_id INTEGER, -- Link to the ICP used to find this lead
    company_name TEXT,
    contact_name TEXT,
    job_title TEXT,
    industry TEXT,
    company_size TEXT,
    region TEXT,
    website TEXT,
    email TEXT, -- Store ONLY if publicly available AND compliant with privacy laws
    phone TEXT, -- Store ONLY if publicly available AND compliant with privacy laws
    linkedin_profile TEXT, -- Store ONLY if publicly available
    source TEXT, -- e.g., LinkedIn Scrape, DirectoryX, ConferenceList
    qualification_status TEXT, -- e.g., Qualified, Disqualified, Pending
    qualification_reason TEXT, -- e.g., Score too low, Industry mismatch
    score REAL, -- Score based on ICP match (0-1)
    engagement_level REAL, -- Optional score based on interactions
    technologies_used TEXT, -- Store as comma-separated string or JSON array
    notes TEXT,
    collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_contacted TIMESTAMP,
    status TEXT DEFAULT 'New', -- e.g., New, Contacted, Nurturing, Closed
    FOREIGN KEY (icp_id) REFERENCES icps (icp_id)
);
```

### 3.7 `india_real_estate_projects`

Stores specific data for real estate projects in India.

```sql
CREATE TABLE IF NOT EXISTS india_real_estate_projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    developer_id INTEGER, -- Link to companies table if developer is listed
    developer_name TEXT, -- Store name even if not in companies table
    city TEXT,
    region TEXT, -- State/Region within India
    project_type TEXT, -- e.g., Residential, Commercial, Mixed-Use
    status TEXT, -- e.g., Upcoming, Under Construction, Completed
    rera_registration_id TEXT UNIQUE,
    launch_date DATE,
    expected_completion_date DATE,
    total_area_sqft REAL,
    price_per_sqft_range TEXT,
    key_features TEXT,
    source_url TEXT,
    collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (developer_id) REFERENCES companies (company_id)
);
```

### 3.8 `india_architectural_firms`

Stores specific data for architectural firms in India.

```sql
CREATE TABLE IF NOT EXISTS india_architectural_firms (
    firm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER UNIQUE, -- Link to companies table
    firm_name TEXT NOT NULL,
    city TEXT,
    region TEXT,
    specialization TEXT, -- e.g., Residential, Commercial, Institutional, Urban Planning
    notable_projects TEXT,
    key_personnel TEXT, -- Store as comma-separated string or JSON
    awards TEXT,
    coa_registration_id TEXT, -- Council of Architecture ID, if available
    source_url TEXT,
    collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies (company_id)
);
```

### 3.9 `analysis_results` (Optional but Recommended)

Stores the results of complex analyses like SWOT or full competitor reports.

```sql
CREATE TABLE IF NOT EXISTS analysis_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_type TEXT NOT NULL, -- e.g., SWOT, CompetitorReport, TrendReport
    target_entity_id INTEGER, -- e.g., company_id for SWOT/Competitor
    target_entity_name TEXT, -- e.g., Industry name for TrendReport
    result_json TEXT NOT NULL, -- Store the full analysis result as JSON
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. Relationships

- `companies` is central, linked to `company_officers`, `news_articles`, potentially `leads` (if lead is associated with a known company), `india_real_estate_projects` (via developer), `india_architectural_firms`.
- `leads` links to `icps`.
- `news_articles` can link to `companies` or be general (industry/topic).
- `india_real_estate_projects` links to `companies` (developer).
- `india_architectural_firms` links to `companies`.
- `analysis_results` links to the entity analyzed (e.g., a company).

## 5. Indexing

Consider adding indexes to frequently queried columns for performance:
- `companies`: `name`, `ticker_symbol`, `industry`, `region`
- `leads`: `icp_id`, `qualification_status`, `industry`, `region`, `score`
- `news_articles`: `company_id`, `industry`, `topic`, `published_date`
- `market_trends`: `industry`, `region`, `published_date`
- `india_real_estate_projects`: `city`, `region`, `developer_name`, `rera_registration_id`
- `india_architectural_firms`: `city`, `region`, `firm_name`

## 6. Data Interaction Layer

A dedicated Python module (e.g., `database_manager.py`) should be created to handle all interactions with the SQLite database. This module will contain functions for:
- Establishing a connection.
- Creating tables if they don't exist.
- Inserting, updating, and deleting records.
- Querying data based on various criteria.
- Handling potential database errors gracefully.
