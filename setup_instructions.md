# Business AI Agent - Setup Instructions

This document provides detailed instructions for setting up and running the enhanced Business AI Agent with real data integration, focusing on market analysis, lead generation, and business support for the architecture and real estate industries in India.

## System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.10 or higher
- **Storage**: At least 500MB of free disk space
- **Memory**: Minimum 4GB RAM recommended
- **Internet Connection**: Required for data collection and API access

## Installation Steps

### 1. Clone or Download the Repository

```bash
git clone https://github.com/your-organization/business-ai-agent.git
cd business-ai-agent
```

Or unzip the provided package:

```bash
unzip business_ai_agent_package.zip -d business-ai-agent
cd business-ai-agent
```

### 2. Set Up a Python Virtual Environment (Recommended)

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
python3 database_manager.py
```

This will create the SQLite database file (`business_agent.db`) with all necessary tables.

### 5. Collect Initial Data (Optional but Recommended)

```bash
python3 real_data_collector.py
```

This will populate the database with initial data from Yahoo Finance and other sources. You can customize the data collection by editing the script or passing arguments.

## Running the Application

### Start the Streamlit Web Interface

```bash
streamlit run business_ai_agent_ui.py
```

This will start the web interface on `http://localhost:8501` by default.

## Module Usage

The Business AI Agent consists of three main modules that can be used independently or together:

### 1. Market Analysis Module

```python
from market_analysis_implementation import MarketAnalysisAgent

# Initialize with database connection
agent = MarketAnalysisAgent()

# Analyze a competitor
report = agent.analyze_competitor(competitor_ticker="INFY.NS", region="IN")

# Identify market trends
trends = agent.identify_market_trends(industry="Real Estate", region="IN")

# Perform SWOT analysis
swot = agent.perform_swot_analysis(company_ticker="HDFC.NS", competitor_tickers=["ICICIB.NS"])

# Analyze market segment
segment = agent.analyze_market_segment(segment_name="Residential", industry="Real Estate", region="Maharashtra")
```

### 2. Lead Generation Module

```python
from lead_generation_implementation import LeadGenerationAgent

# Initialize with database connection
agent = LeadGenerationAgent()

# Define an Ideal Customer Profile (ICP)
icp_criteria = {
    "preferred_industries": ["Real Estate", "Architecture & Planning"],
    "preferred_regions": ["Maharashtra", "Karnataka", "Delhi"],
    "preferred_company_sizes": ["51-200", "201-500"],
    "min_score_threshold": 0.6
}
agent.define_icp("India Real Estate Developers", icp_criteria)

# Generate leads based on the ICP
leads = agent.generate_leads(icp_profile_name="India Real Estate Developers", num_leads=10)
```

### 3. Business Support Module

```python
from business_support_implementation import BusinessSupportAgent

# Initialize with database connection
agent = BusinessSupportAgent()

# Analyze public sentiment
sentiment = agent.analyze_public_sentiment(topic="Affordable Housing")

# Get industry news
news = agent.get_industry_news(industry="Architecture & Planning", region="IN")

# Set a reminder
agent.set_reminder(task="Follow up with lead", due_date="2025-05-15", notes="High priority")

# Generate automated report
report = agent.generate_automated_report(company_ticker="HDFC.NS", competitor_tickers=["ICICIB.NS"])
```

## Data Collection and Management

### Adding New Data Sources

To add new data sources:

1. Edit `real_data_collector.py` to implement new collection methods
2. Update the database schema in `database_manager.py` if necessary
3. Run the collector with appropriate parameters

### Database Management

The database is managed through the `database_manager.py` module, which provides functions for:

- Creating and initializing the database
- Adding or updating companies, news, trends, and other data
- Retrieving and querying data for analysis

## Customization

### Adding New Industries

To add support for industries beyond real estate and architecture:

1. Update the data collection methods in `real_data_collector.py`
2. Add industry-specific analysis logic to the relevant modules
3. Update the UI to include the new industries

### Regional Customization

The system is designed with a focus on India but can be adapted for other regions:

1. Update region codes and parameters in data collection methods
2. Modify analysis logic to account for regional differences
3. Update UI labels and filters for the new regions

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Ensure the database file exists and has proper permissions
   - Check that no other process is locking the database file

2. **API Access Issues**:
   - Verify internet connectivity
   - Check that the data_api module is properly installed

3. **Missing Dependencies**:
   - Run `pip install -r requirements.txt` again
   - Check for error messages during installation

### Logging

The application logs information to:
- Console output
- `reminders.log` (for the scheduler component)

## Security Considerations

- The application uses SQLite, which stores data in a local file
- No authentication is built into the application by default
- Sensitive data should be properly secured if deployed in a production environment

## License and Attribution

This Business AI Agent is provided for demonstration and educational purposes.
When using in production, ensure compliance with:

- Terms of service for all data sources
- Privacy laws regarding lead data collection and storage
- Licensing requirements for all dependencies

## Support

For questions or issues, please contact:
- Email: support@example.com
- GitHub Issues: https://github.com/your-organization/business-ai-agent/issues
