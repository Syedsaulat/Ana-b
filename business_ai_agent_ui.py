"""
Business AI Agent - Main Interface Implementation

This module implements a web-based user interface for the Business AI Agent
using Streamlit, providing access to all agent functionalities.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Import the agent modules (assuming they are in the same directory)
# In a real implementation, these would be proper imports
# For this simulation, we'll mock/initialize them as needed

# Check if required packages are installed, install if needed
try:
    import streamlit
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "plotly"])
    import streamlit

class BusinessAIAgentUI:
    """Main class for the Business AI Agent User Interface."""
    
    def __init__(self):
        """Initialize the UI components and agent modules."""
        # Set page configuration
        st.set_page_config(
            page_title="Business AI Agent",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize agent modules (in a real implementation, these would be imported)
        self.init_agent_modules()
        
    def init_agent_modules(self):
        """Initialize the agent modules (market analysis, lead generation, business support)."""
        # In a real implementation, these would be imported from their respective modules
        # For this simulation, we'll create simplified versions or mock them
        
        # Mock the MarketAnalysisAgent
        class MockMarketAnalysisAgent:
            def analyze_competitor(self, competitor_name, industry=None):
                st.info(f"Simulating competitor analysis for: {competitor_name} in {industry or 'general'} industry")
                # Return simulated data
                return {
                    "title": f"Competitor Analysis: {competitor_name}",
                    "generated_at": datetime.now().isoformat(),
                    "content": {
                        "strengths": ["Strong brand presence", "Innovative product line", "Effective marketing"],
                        "weaknesses": ["Limited international presence", "High pricing", "Customer service issues"],
                        "market_position": {"market_share": 0.15, "position_statement": "Strong mid-market position"},
                        "sentiment_analysis": {"overall": 0.65, "news": 0.7, "social": 0.6},
                        "key_products": [f"Product A by {competitor_name}", f"Product B by {competitor_name}"]
                    }
                }
                
            def identify_market_trends(self, industry, timeframe="last_month"):
                st.info(f"Simulating market trend analysis for: {industry} over {timeframe}")
                # Return simulated data
                return {
                    "title": f"Market Trends Analysis: {industry}",
                    "generated_at": datetime.now().isoformat(),
                    "content": {
                        "emerging_trends": [
                            f"Digital transformation in {industry}", 
                            f"Sustainability initiatives in {industry}",
                            f"AI adoption in {industry}"
                        ],
                        "declining_trends": [
                            f"Traditional marketing in {industry}",
                            f"Legacy systems in {industry}"
                        ],
                        "sentiment_trends": {"current": 0.65, "previous": 0.58, "change": 0.07, "trend": "Improving"},
                        "key_influencers": [f"Leading company in {industry}", f"Industry association for {industry}"]
                    }
                }
                
            def perform_swot_analysis(self, company_name, competitors=None):
                st.info(f"Simulating SWOT analysis for: {company_name}")
                # Return simulated data
                return {
                    "title": f"SWOT Analysis: {company_name}",
                    "generated_at": datetime.now().isoformat(),
                    "content": {
                        "strengths": ["Market leadership", "Strong R&D", "Talented workforce"],
                        "weaknesses": ["High costs", "Product gaps", "Technical debt"],
                        "opportunities": ["Emerging markets", "New technologies", "Strategic partnerships"],
                        "threats": ["Increasing competition", "Regulatory changes", "Economic uncertainty"]
                    }
                }
        
        # Mock the LeadGenerationAgent
        class MockLeadGenerationAgent:
            def define_icp(self, criteria):
                st.info(f"Defining Ideal Customer Profile with {len(criteria)} criteria")
                return criteria
                
            def generate_leads(self, icp, target_industry=None, target_region=None, num_leads=10):
                st.info(f"Simulating lead generation for {target_industry or 'all industries'} in {target_region or 'all regions'}")
                # Generate simulated leads
                leads = []
                for i in range(num_leads):
                    score = round(np.random.uniform(0.6, 0.95), 2)
                    industry = target_industry or np.random.choice(["Technology", "Finance", "Healthcare", "Retail"])
                    region = target_region or np.random.choice(["North America", "Europe", "Asia", "LATAM"])
                    company_size = np.random.choice(["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"])
                    
                    lead = {
                        "score": score,
                        "contact_name": f"Contact Person {i+1}",
                        "job_title": np.random.choice(["CEO", "CTO", "Marketing Manager", "Sales Director"]),
                        "company_name": f"Prospect Company {i+1}",
                        "industry": industry,
                        "company_size": company_size,
                        "region": region,
                        "contact_info": {
                            "email": f"contact{i+1}@prospect{i+1}.com",
                            "phone": f"+1-{np.random.randint(100, 999)}-{np.random.randint(100, 999)}-{np.random.randint(1000, 9999)}",
                            "linkedin_profile": f"http://linkedin.com/in/contact{i+1}"
                        }
                    }
                    leads.append(lead)
                
                # Return simulated report
                return {
                    "title": "Qualified Leads Report",
                    "generated_at": datetime.now().isoformat(),
                    "summary": {
                        "total_qualified_leads": len(leads),
                        "average_score": round(np.mean([lead["score"] for lead in leads]), 2)
                    },
                    "leads": leads
                }
        
        # Mock the BusinessSupportAgent
        class MockBusinessSupportAgent:
            def analyze_public_sentiment(self, topic, sources=["news", "social_media"]):
                st.info(f"Simulating sentiment analysis for: {topic} from {', '.join(sources)}")
                # Return simulated data
                return {
                    "aggregate_summary": {
                        "total_analyzed": 30,
                        "positive_count": 18,
                        "negative_count": 7,
                        "neutral_count": 5,
                        "average_compound_score": 0.42
                    }
                }
                
            def get_industry_news(self, industry, num_articles=5):
                st.info(f"Simulating news aggregation for: {industry}")
                # Return simulated data
                articles = []
                for i in range(num_articles):
                    articles.append({
                        "title": f"{industry} News Headline {i+1}",
                        "source": f"News Source {np.random.choice(['A', 'B', 'C'])}",
                        "date": (datetime.now() - timedelta(days=np.random.randint(1, 30))).isoformat(),
                        "summary": f"This is a summary for the news article {i+1} about {industry}.",
                        "url": f"http://news.example.com/{industry.lower()}/article{i+1}"
                    })
                return {
                    "query": industry,
                    "aggregated_at": datetime.now().isoformat(),
                    "articles": articles
                }
                
            def set_reminder(self, task, due_date, notes=""):
                st.info(f"Simulating reminder creation for: {task} due on {due_date}")
                # Return simulated data
                return {
                    "status": "success", 
                    "message": f"Reminder for '{task}' logged.",
                    "log_entry": f"{datetime.now().isoformat()} | DUE: {due_date} | TASK: {task} | NOTES: {notes}"
                }
                
            def generate_automated_report(self, report_type="weekly_summary", company_name="Our Company", competitors=None):
                st.info(f"Simulating automated report generation: {report_type} for {company_name}")
                # Return simulated data
                return {
                    "title": f"{report_type.replace('_', ' ').title()} Report for {company_name}",
                    "generated_at": datetime.now().isoformat(),
                    "report_period": "Last Week",
                    "sections": [
                        {
                            "title": "Market Summary",
                            "content": {
                                "key_trends": ["Trend A", "Trend B"],
                                "overall_sentiment": "Positive (0.65)",
                                "market_size_estimate": "$10B"
                            }
                        },
                        {
                            "title": "Competitor Activity",
                            "content": {
                                "summary": [f"{comp}: Recent activity summary." for comp in (competitors or [])]
                            }
                        },
                        {
                            "title": "Lead Generation Summary",
                            "content": {
                                "new_qualified_leads": np.random.randint(5, 25),
                                "top_lead_source": "LinkedIn",
                                "average_lead_score": round(np.random.uniform(0.6, 0.85), 2)
                            }
                        }
                    ]
                }
        
        # Initialize the mock agents
        self.market_analysis_agent = MockMarketAnalysisAgent()
        self.lead_generation_agent = MockLeadGenerationAgent()
        self.business_support_agent = MockBusinessSupportAgent()
    
    def run(self):
        """Run the Streamlit application."""
        # Set up the sidebar navigation
        self.setup_sidebar()
        
        # Display the selected page
        page = st.session_state.get("page", "Home")
        
        if page == "Home":
            self.show_home_page()
        elif page == "Market Analysis":
            self.show_market_analysis_page()
        elif page == "Lead Generation":
            self.show_lead_generation_page()
        elif page == "Business Support":
            self.show_business_support_page()
        elif page == "Documentation":
            self.show_documentation_page()
    
    def setup_sidebar(self):
        """Set up the sidebar navigation."""
        with st.sidebar:
            st.title("Business AI Agent")
            st.image("https://via.placeholder.com/150?text=AI+Agent", width=150)
            
            # Navigation
            st.subheader("Navigation")
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()
            if st.button("📊 Market Analysis", use_container_width=True):
                st.session_state.page = "Market Analysis"
                st.rerun()
            if st.button("🎯 Lead Generation", use_container_width=True):
                st.session_state.page = "Lead Generation"
                st.rerun()
            if st.button("🔧 Business Support", use_container_width=True):
                st.session_state.page = "Business Support"
                st.rerun()
            if st.button("📚 Documentation", use_container_width=True):
                st.session_state.page = "Documentation"
                st.rerun()
            
            # Footer
            st.sidebar.markdown("---")
            st.sidebar.caption("© 2025 Business AI Agent")
    
    def show_home_page(self):
        """Display the home page."""
        st.title("Welcome to the Business AI Agent")
        
        st.markdown("""
        This AI agent helps businesses with market analysis, lead generation, and other business intelligence tasks.
        
        ### Key Features:
        
        - **Market Analysis**: Analyze competitors, identify market trends, and perform SWOT analysis.
        - **Lead Generation**: Define ideal customer profiles, identify and qualify leads.
        - **Business Support**: Analyze public sentiment, aggregate industry news, set reminders, and generate automated reports.
        
        Use the sidebar navigation to access different functionalities.
        """)
        
        # Quick access cards
        st.subheader("Quick Access")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Market Analysis")
            st.markdown("Analyze competitors and market trends")
            if st.button("Go to Market Analysis", key="home_market"):
                st.session_state.page = "Market Analysis"
                st.rerun()
        
        with col2:
            st.markdown("### 🎯 Lead Generation")
            st.markdown("Generate and qualify leads for your business")
            if st.button("Go to Lead Generation", key="home_lead"):
                st.session_state.page = "Lead Generation"
                st.rerun()
        
        with col3:
            st.markdown("### 🔧 Business Support")
            st.markdown("Access additional business support features")
            if st.button("Go to Business Support", key="home_support"):
                st.session_state.page = "Business Support"
                st.rerun()
        
        # Recent activity (simulated)
        st.subheader("Recent Activity")
        activity_data = [
            {"date": "2025-04-28", "activity": "Competitor analysis for TechCorp completed"},
            {"date": "2025-04-27", "activity": "15 new leads generated for SaaS industry"},
            {"date": "2025-04-26", "activity": "Sentiment analysis for Product X completed"},
            {"date": "2025-04-25", "activity": "Weekly summary report generated"}
        ]
        
        activity_df = pd.DataFrame(activity_data)
        st.dataframe(activity_df, hide_index=True, use_container_width=True)
    
    def show_market_analysis_page(self):
        """Display the market analysis page."""
        st.title("Market Analysis")
        
        # Create tabs for different market analysis functions
        tabs = st.tabs(["Competitor Analysis", "Market Trends", "SWOT Analysis"])
        
        # Competitor Analysis Tab
        with tabs[0]:
            st.header("Competitor Analysis")
            st.markdown("Analyze a specific competitor to understand their strengths, weaknesses, and market position.")
            
            # Input form
            with st.form("competitor_analysis_form"):
                competitor_name = st.text_input("Competitor Name", "Example Corp")
                industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing", "Other"])
                submitted = st.form_submit_button("Analyze Competitor")
            
            # Handle form submission
            if submitted:
                with st.spinner(f"Analyzing competitor: {competitor_name}..."):
                    # Call the market analysis agent
                    result = self.market_analysis_agent.analyze_competitor(competitor_name, industry)
                    
                    # Display results
                    st.subheader(result["title"])
                    st.caption(f"Generated at: {result['generated_at']}")
                    
                    # Display content in columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Strengths")
                        for strength in result["content"]["strengths"]:
                            st.markdown(f"- {strength}")
                        
                        st.subheader("Market Position")
                        st.markdown(f"**Market Share:** {result['content']['market_position']['market_share'] * 100:.1f}%")
                        st.markdown(f"**Position Statement:** {result['content']['market_position']['position_statement']}")
                    
                    with col2:
                        st.subheader("Weaknesses")
                        for weakness in result["content"]["weaknesses"]:
                            st.markdown(f"- {weakness}")
                        
                        st.subheader("Key Products")
                        for product in result["content"]["key_products"]:
                            st.markdown(f"- {product}")
                    
                    # Sentiment Analysis Visualization
                    st.subheader("Sentiment Analysis")
                    sentiment = result["content"]["sentiment_analysis"]
                    
                    # Create a bar chart for sentiment
                    sentiment_data = pd.DataFrame({
                        'Source': ['Overall', 'News', 'Social Media'],
                        'Sentiment Score': [sentiment['overall'], sentiment['news'], sentiment['social']]
                    })
                    
                    fig = px.bar(sentiment_data, x='Source', y='Sentiment Score', 
                                color='Sentiment Score', color_continuous_scale='RdYlGn',
                                range_color=[-1, 1], height=300)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Market Trends Tab
        with tabs[1]:
            st.header("Market Trends")
            st.markdown("Identify emerging and declining trends in a specific industry.")
            
            # Input form
            with st.form("market_trends_form"):
                industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing", "Other"], key="trends_industry")
                timeframe = st.selectbox("Timeframe", ["last_week", "last_month", "last_quarter", "last_year"])
                submitted = st.form_submit_button("Identify Trends")
            
            # Handle form submission
            if submitted:
                with st.spinner(f"Identifying trends for {industry}..."):
                    # Call the market analysis agent
                    result = self.market_analysis_agent.identify_market_trends(industry, timeframe)
                    
                    # Display results
                    st.subheader(result["title"])
                    st.caption(f"Generated at: {result['generated_at']}")
                    
                    # Display content in columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Emerging Trends")
                        for trend in result["content"]["emerging_trends"]:
                            st.markdown(f"- {trend}")
                    
                    with col2:
                        st.subheader("Declining Trends")
                        for trend in result["content"]["declining_trends"]:
                            st.markdown(f"- {trend}")
                    
                    # Sentiment Trend Visualization
                    st.subheader("Sentiment Trend")
                    sentiment_trend = result["content"]["sentiment_trends"]
                    
                    # Create a simple trend visualization
                    trend_data = pd.DataFrame({
                        'Period': ['Previous', 'Current'],
                        'Sentiment Score': [sentiment_trend['previous'], sentiment_trend['current']]
                    })
                    
                    fig = px.line(trend_data, x='Period', y='Sentiment Score', markers=True,
                                 range_y=[-1, 1], height=300)
                    fig.add_hline(y=0, line_dash="dash", line_color="gray")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown(f"**Trend Direction:** {sentiment_trend['trend']} (Change: {sentiment_trend['change']:+.2f})")
                    
                    # Key Influencers
                    st.subheader("Key Influencers")
                    for influencer in result["content"]["key_influencers"]:
                        st.markdown(f"- {influencer}")
        
        # SWOT Analysis Tab
        with tabs[2]:
            st.header("SWOT Analysis")
            st.markdown("Perform a SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis for your company.")
            
            # Input form
            with st.form("swot_analysis_form"):
                company_name = st.text_input("Company Name", "Our Company")
                
                st.subheader("Competitors (Optional)")
                competitors = []
                for i in range(3):
                    competitor = st.text_input(f"Competitor {i+1}", "", key=f"swot_competitor_{i}")
                    if competitor:
                        competitors.append(competitor)
                
                submitted = st.form_submit_button("Perform SWOT Analysis")
            
            # Handle form submission
            if submitted:
                with st.spinner(f"Performing SWOT analysis for {company_name}..."):
                    # Call the market analysis agent
                    result = self.market_analysis_agent.perform_swot_analysis(company_name, competitors if competitors else None)
                    
                    # Display results
                    st.subheader(result["title"])
                    st.caption(f"Generated at: {result['generated_at']}")
                    
                    # Create a SWOT matrix visualization
                    swot_data = {
                        'Strengths': '<br>'.join([f"• {s}" for s in result["content"]["strengths"]]),
                        'Weaknesses': '<br>'.join([f"• {w}" for w in result["content"]["weaknesses"]]),
                        'Opportunities': '<br>'.join([f"• {o}" for o in result["content"]["opportunities"]]),
                        'Threats': '<br>'.join([f"• {t}" for t in result["content"]["threats"]])
                    }
                    
                    fig = go.Figure(data=[go.Table(
                        header=dict(
                            values=["<b>Strengths</b>", "<b>Weaknesses</b>"],
                            fill_color=['rgba(0, 128, 0, 0.2)', 'rgba(255, 0, 0, 0.2)'],
                            align='center',
                            font=dict(size=14)
                        ),
                        cells=dict(
                            values=[swot_data['Strengths'], swot_data['Weaknesses']],
                            fill_color=['rgba(0, 128, 0, 0.1)', 'rgba(255, 0, 0, 0.1)'],
                            align='left',
                            height=30,
                            font=dict(size=12)
                        )
                    )])
                    
                    fig.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    fig2 = go.Figure(data=[go.Table(
                        header=dict(
                            values=["<b>Opportunities</b>", "<b>Threats</b>"],
                            fill_color=['rgba(0, 0, 255, 0.2)', 'rgba(255, 165, 0, 0.2)'],
                            align='center',
                            font=dict(size=14)
                        ),
                        cells=dict(
                            values=[swot_data['Opportunities'], swot_data['Threats']],
                            fill_color=['rgba(0, 0, 255, 0.1)', 'rgba(255, 165, 0, 0.1)'],
                            align='left',
                            height=30,
                            font=dict(size=12)
                        )
                    )])
                    
                    fig2.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig2, use_container_width=True)
    
    def show_lead_generation_page(self):
        """Display the lead generation page."""
        st.title("Lead Generation")
        
        # Create tabs for different lead generation functions
        tabs = st.tabs(["Define ICP", "Generate Leads"])
        
        # Define ICP Tab
        with tabs[0]:
            st.header("Define Ideal Customer Profile (ICP)")
            st.markdown("Define the characteristics of your ideal customers to improve lead quality.")
            
            # Input form for ICP definition
            with st.form("define_icp_form"):
                st.subheader("Industry Preferences")
                preferred_industries = st.multiselect(
                    "Preferred Industries",
                    ["Technology", "SaaS", "Finance", "Healthcare", "Retail", "Manufacturing", "Education", "Government", "Non-profit"],
                    ["Technology", "SaaS"]
                )
                
                required_industry = st.checkbox("Make industry a hard requirement")
                
                st.subheader("Region Preferences")
                preferred_regions = st.multiselect(
                    "Preferred Regions",
                    ["North America", "Europe", "Asia", "LATAM", "Middle East", "Africa", "Australia/Oceania"],
                    ["North America"]
                )
                
                required_region = st.checkbox("Make region a hard requirement")
                
                st.subheader("Company Size Preferences")
                preferred_company_sizes = st.multiselect(
                    "Preferred Company Sizes",
                    ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"],
                    ["51-200", "201-500"]
                )
                
                st.subheader("Job Title Preferences")
                preferred_job_titles = st.multiselect(
                    "Preferred Job Titles",
                    ["CEO", "CTO", "CFO", "CMO", "VP of Engineering", "VP of Sales", "VP of Marketing", 
                     "Director of IT", "Director of Operations", "Product Manager", "Marketing Manager"],
                    ["CTO", "VP of Engineering"]
                )
                
                required_job_title = st.checkbox("Make job title a hard requirement")
                
                st.subheader("Technology Preferences")
                preferred_technologies = st.multiselect(
                    "Preferred Technologies",
                    ["AWS", "Azure", "Google Cloud", "Salesforce", "HubSpot", "Oracle", "SAP", 
                     "Microsoft Dynamics", "Shopify", "WordPress", "React", "Angular", "Vue.js"],
                    ["AWS", "Azure"]
                )
                
                st.subheader("Qualification Threshold")
                min_score_threshold = st.slider("Minimum Score Threshold", 0.0, 1.0, 0.6, 0.05)
                
                submitted = st.form_submit_button("Define ICP")
            
            # Handle form submission
            if submitted:
                # Build the ICP criteria
                icp_criteria = {
                    "preferred_industries": preferred_industries,
                    "preferred_regions": preferred_regions,
                    "preferred_company_sizes": preferred_company_sizes,
                    "preferred_job_titles": preferred_job_titles,
                    "preferred_technologies": preferred_technologies,
                    "min_score_threshold": min_score_threshold
                }
                
                # Add hard requirements if specified
                if required_industry:
                    icp_criteria["required_industry"] = preferred_industries
                if required_region:
                    icp_criteria["required_region"] = preferred_regions
                if required_job_title:
                    icp_criteria["required_job_titles"] = preferred_job_titles
                
                # Call the lead generation agent
                with st.spinner("Defining Ideal Customer Profile..."):
                    result = self.lead_generation_agent.define_icp(icp_criteria)
                    
                    # Store the ICP in session state for use in the Generate Leads tab
                    st.session_state.icp = result
                    
                    # Display success message
                    st.success("Ideal Customer Profile defined successfully!")
                    
                    # Display the defined ICP
                    st.json(result)
        
        # Generate Leads Tab
        with tabs[1]:
            st.header("Generate Leads")
            st.markdown("Generate qualified leads based on your Ideal Customer Profile (ICP).")
            
            # Check if ICP is defined
            if not hasattr(st.session_state, 'icp'):
                st.warning("Please define your Ideal Customer Profile (ICP) first in the 'Define ICP' tab.")
                if st.button("Use Default ICP"):
                    # Create a default ICP
                    st.session_state.icp = {
                        "preferred_industries": ["Technology", "SaaS"],
                        "preferred_regions": ["North America"],
                        "preferred_company_sizes": ["51-200", "201-500"],
                        "preferred_job_titles": ["CTO", "VP of Engineering"],
                        "preferred_technologies": ["AWS", "Azure"],
                        "min_score_threshold": 0.6
                    }
                    st.success("Default ICP applied. You can now generate leads.")
                    st.rerun()
            else:
                # Display the current ICP
                st.subheader("Current ICP")
                st.json(st.session_state.icp)
                
                # Input form for lead generation
                with st.form("generate_leads_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        target_industry = st.selectbox(
                            "Target Industry (Optional)",
                            [""] + st.session_state.icp.get("preferred_industries", []),
                            index=0
                        )
                    
                    with col2:
                        target_region = st.selectbox(
                            "Target Region (Optional)",
                            [""] + st.session_state.icp.get("preferred_regions", []),
                            index=0
                        )
                    
                    num_leads = st.slider("Number of Leads to Generate", 5, 50, 10, 5)
                    
                    submitted = st.form_submit_button("Generate Leads")
                
                # Handle form submission
                if submitted:
                    with st.spinner(f"Generating {num_leads} leads..."):
                        # Call the lead generation agent
                        result = self.lead_generation_agent.generate_leads(
                            icp=st.session_state.icp,
                            target_industry=target_industry if target_industry else None,
                            target_region=target_region if target_region else None,
                            num_leads=num_leads
                        )
                        
                        # Display results
                        st.subheader(result["title"])
                        st.caption(f"Generated at: {result['generated_at']}")
                        
                        # Display summary
                        st.markdown(f"**Total Qualified Leads:** {result['summary']['total_qualified_leads']}")
                        st.markdown(f"**Average Lead Score:** {result['summary']['average_score']}")
                        
                        # Create a dataframe for the leads
                        leads_data = []
                        for lead in result["leads"]:
                            leads_data.append({
                                "Score": lead["score"],
                                "Contact": lead["contact_name"],
                                "Title": lead["job_title"],
                                "Company": lead["company_name"],
                                "Industry": lead["industry"],
                                "Size": lead["company_size"],
                                "Region": lead["region"],
                                "Email": lead["contact_info"]["email"],
                                "Phone": lead["contact_info"]["phone"]
                            })
                        
                        leads_df = pd.DataFrame(leads_data)
                        
                        # Display the leads table
                        st.subheader("Qualified Leads")
                        st.dataframe(leads_df, hide_index=True, use_container_width=True)
                        
                        # Create a download button for CSV export
                        csv = leads_df.to_csv(index=False)
                        st.download_button(
                            label="Download Leads as CSV",
                            data=csv,
                            file_name="qualified_leads.csv",
                            mime="text/csv"
                        )
                        
                        # Display a score distribution chart
                        st.subheader("Lead Score Distribution")
                        fig = px.histogram(leads_df, x="Score", nbins=10, 
                                          color_discrete_sequence=["#3366cc"],
                                          labels={"Score": "Lead Score", "count": "Number of Leads"},
                                          height=300)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display industry distribution
                        st.subheader("Industry Distribution")
                        industry_counts = leads_df["Industry"].value_counts().reset_index()
                        industry_counts.columns = ["Industry", "Count"]
                        
                        fig = px.pie(industry_counts, values="Count", names="Industry", hole=0.4,
                                    height=300)
                        st.plotly_chart(fig, use_container_width=True)
    
    def show_business_support_page(self):
        """Display the business support page."""
        st.title("Business Support")
        
        # Create tabs for different business support functions
        tabs = st.tabs(["Sentiment Analysis", "News Aggregation", "Reminders", "Automated Reports"])
        
        # Sentiment Analysis Tab
        with tabs[0]:
            st.header("Sentiment Analysis")
            st.markdown("Analyze public sentiment about a topic from news and social media sources.")
            
            # Input form
            with st.form("sentiment_analysis_form"):
                topic = st.text_input("Topic", "Sustainable Energy")
                
                sources = st.multiselect(
                    "Data Sources",
                    ["news", "social_media"],
                    ["news", "social_media"]
                )
                
                submitted = st.form_submit_button("Analyze Sentiment")
            
            # Handle form submission
            if submitted:
                with st.spinner(f"Analyzing sentiment for: {topic}..."):
                    # Call the business support agent
                    result = self.business_support_agent.analyze_public_sentiment(topic, sources)
                    
                    # Display results
                    st.subheader(f"Sentiment Analysis Results for: {topic}")
                    
                    # Display summary
                    summary = result["aggregate_summary"]
                    
                    # Create columns for summary stats
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Analyzed", summary["total_analyzed"])
                    
                    with col2:
                        st.metric("Positive", summary["positive_count"], 
                                 f"{summary['positive_count']/summary['total_analyzed']*100:.1f}%")
                    
                    with col3:
                        st.metric("Negative", summary["negative_count"],
                                 f"{summary['negative_count']/summary['total_analyzed']*100:.1f}%")
                    
                    with col4:
                        st.metric("Neutral", summary["neutral_count"],
                                 f"{summary['neutral_count']/summary['total_analyzed']*100:.1f}%")
                    
                    # Display average sentiment score with gauge
                    st.subheader("Average Sentiment Score")
                    
                    # Create a gauge chart for the sentiment score
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = summary["average_compound_score"],
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Sentiment"},
                        gauge = {
                            'axis': {'range': [-1, 1]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [-1, -0.5], 'color': "red"},
                                {'range': [-0.5, -0.05], 'color': "lightcoral"},
                                {'range': [-0.05, 0.05], 'color': "lightgray"},
                                {'range': [0.05, 0.5], 'color': "lightgreen"},
                                {'range': [0.5, 1], 'color': "green"}
                            ],
                            'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.75,
                                'value': summary["average_compound_score"]
                            }
                        }
                    ))
                    
                    fig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display sentiment distribution
                    st.subheader("Sentiment Distribution")
                    
                    sentiment_data = pd.DataFrame({
                        'Sentiment': ['Positive', 'Neutral', 'Negative'],
                        'Count': [summary["positive_count"], summary["neutral_count"], summary["negative_count"]]
                    })
                    
                    fig = px.bar(sentiment_data, x='Sentiment', y='Count', 
                                color='Sentiment',
                                color_discrete_map={
                                    'Positive': 'green',
                                    'Neutral': 'gray',
                                    'Negative': 'red'
                                },
                                height=300)
                    st.plotly_chart(fig, use_container_width=True)
        
        # News Aggregation Tab
        with tabs[1]:
            st.header("News Aggregation")
            st.markdown("Aggregate recent news articles for a specific industry or topic.")
            
            # Input form
            with st.form("news_aggregation_form"):
                query = st.text_input("Industry or Topic", "Artificial Intelligence")
                num_articles = st.slider("Number of Articles", 3, 20, 5)
                
                submitted = st.form_submit_button("Aggregate News")
            
            # Handle form submission
            if submitted:
                with st.spinner(f"Aggregating news for: {query}..."):
                    # Call the business support agent
                    result = self.business_support_agent.get_industry_news(query, num_articles)
                    
                    # Display results
                    st.subheader(f"News Articles for: {result['query']}")
                    st.caption(f"Aggregated at: {result['aggregated_at']}")
                    
                    # Display articles
                    for i, article in enumerate(result["articles"]):
                        with st.expander(f"{i+1}. {article['title']} ({article['source']})"):
                            st.markdown(f"**Date:** {article['date']}")
                            st.markdown(f"**Summary:** {article['summary']}")
                            st.markdown(f"**URL:** [{article['url']}]({article['url']})")
                    
                    # Create a download button for the news report
                    news_json = json.dumps(result, indent=2)
                    st.download_button(
                        label="Download News Report (JSON)",
                        data=news_json,
                        file_name=f"news_report_{query.replace(' ', '_')}.json",
                        mime="application/json"
                    )
        
        # Reminders Tab
        with tabs[2]:
            st.header("Reminders")
            st.markdown("Set and view reminders for tasks and follow-ups.")
            
            # Create columns for setting and viewing reminders
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Set a Reminder")
                
                # Input form
                with st.form("set_reminder_form"):
                    task = st.text_input("Task", "Follow up with lead")
                    due_date = st.date_input("Due Date")
                    due_time = st.time_input("Due Time")
                    notes = st.text_area("Notes", "")
                    
                    submitted = st.form_submit_button("Set Reminder")
                
                # Handle form submission
                if submitted:
                    # Combine date and time
                    due_datetime = datetime.combine(due_date, due_time)
                    
                    with st.spinner("Setting reminder..."):
                        # Call the business support agent
                        result = self.business_support_agent.set_reminder(
                            task=task,
                            due_date=due_datetime.isoformat(),
                            notes=notes
                        )
                        
                        # Display result
                        if result["status"] == "success":
                            st.success(result["message"])
                            
                            # Store the reminder in session state for display
                            if "reminders" not in st.session_state:
                                st.session_state.reminders = []
                            
                            st.session_state.reminders.append(result["log_entry"])
                        else:
                            st.error(result["message"])
            
            with col2:
                st.subheader("Recent Reminders")
                
                # Display reminders from session state
                if "reminders" in st.session_state and st.session_state.reminders:
                    for i, reminder in enumerate(st.session_state.reminders):
                        st.markdown(f"{i+1}. {reminder}")
                else:
                    # Simulated reminders for demonstration
                    st.markdown("1. 2025-04-28T10:00:00 | DUE: 2025-05-01T14:00:00 | TASK: Follow up with lead | NOTES: Discussed pricing")
                    st.markdown("2. 2025-04-27T15:30:00 | DUE: 2025-04-30T09:00:00 | TASK: Prepare quarterly report | NOTES: Include market analysis")
                    st.markdown("3. 2025-04-26T09:15:00 | DUE: 2025-04-29T11:00:00 | TASK: Schedule team meeting | NOTES: Discuss new leads")
        
        # Automated Reports Tab
        with tabs[3]:
            st.header("Automated Reports")
            st.markdown("Generate automated summary reports for your business.")
            
            # Input form
            with st.form("automated_report_form"):
                report_type = st.selectbox(
                    "Report Type",
                    ["weekly_summary", "monthly_summary", "competitor_activity", "lead_generation_summary"]
                )
                
                company_name = st.text_input("Company Name", "Our Company")
                
                st.subheader("Competitors (Optional)")
                competitors = []
                for i in range(3):
                    competitor = st.text_input(f"Competitor {i+1}", "", key=f"report_competitor_{i}")
                    if competitor:
                        competitors.append(competitor)
                
                submitted = st.form_submit_button("Generate Report")
            
            # Handle form submission
            if submitted:
                with st.spinner(f"Generating {report_type} report..."):
                    # Call the business support agent
                    result = self.business_support_agent.generate_automated_report(
                        report_type=report_type,
                        company_name=company_name,
                        competitors=competitors if competitors else None
                    )
                    
                    # Display results
                    st.subheader(result["title"])
                    st.caption(f"Generated at: {result['generated_at']}")
                    st.markdown(f"**Report Period:** {result['report_period']}")
                    
                    # Display sections
                    for section in result["sections"]:
                        with st.expander(section["title"], expanded=True):
                            content = section["content"]
                            
                            # Display content based on section type
                            if section["title"] == "Market Summary":
                                st.markdown("**Key Trends:**")
                                for trend in content["key_trends"]:
                                    st.markdown(f"- {trend}")
                                
                                st.markdown(f"**Overall Sentiment:** {content['overall_sentiment']}")
                                st.markdown(f"**Market Size Estimate:** {content['market_size_estimate']}")
                            
                            elif section["title"] == "Competitor Activity":
                                st.markdown("**Competitor Summary:**")
                                for summary in content["summary"]:
                                    st.markdown(f"- {summary}")
                            
                            elif section["title"] == "Lead Generation Summary":
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("New Qualified Leads", content["new_qualified_leads"])
                                
                                with col2:
                                    st.metric("Top Lead Source", content["top_lead_source"])
                                
                                with col3:
                                    st.metric("Average Lead Score", content["average_lead_score"])
                            
                            elif section["title"] == "Suggested Action Items":
                                st.markdown("**Action Items:**")
                                for item in content["items"]:
                                    st.markdown(f"- {item}")
                    
                    # Create a download button for the report
                    report_json = json.dumps(result, indent=2)
                    st.download_button(
                        label="Download Report (JSON)",
                        data=report_json,
                        file_name=f"{report_type}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
    
    def show_documentation_page(self):
        """Display the documentation page."""
        st.title("Documentation")
        
        # Create tabs for different documentation sections
        tabs = st.tabs(["Getting Started", "Market Analysis", "Lead Generation", "Business Support", "API Reference"])
        
        # Getting Started Tab
        with tabs[0]:
            st.header("Getting Started")
            
            st.markdown("""
            ## Welcome to the Business AI Agent
            
            The Business AI Agent is designed to help businesses with market analysis, lead generation, and other business intelligence tasks. This documentation will guide you through the various features and functionalities of the agent.
            
            ### System Requirements
            
            - Python 3.8 or higher
            - Required packages: streamlit, pandas, numpy, matplotlib, seaborn, plotly
            
            ### Installation
            
            1. Clone the repository:
               ```
               git clone https://github.com/example/business-ai-agent.git
               cd business-ai-agent
               ```
            
            2. Install dependencies:
               ```
               pip install -r requirements.txt
               ```
            
            3. Run the application:
               ```
               streamlit run app.py
               ```
            
            ### Quick Start Guide
            
            1. **Market Analysis**: Use the Market Analysis page to analyze competitors, identify market trends, and perform SWOT analysis.
            2. **Lead Generation**: Use the Lead Generation page to define your Ideal Customer Profile (ICP) and generate qualified leads.
            3. **Business Support**: Use the Business Support page to analyze public sentiment, aggregate industry news, set reminders, and generate automated reports.
            
            For more detailed information, refer to the specific documentation sections.
            """)
        
        # Market Analysis Tab
        with tabs[1]:
            st.header("Market Analysis Documentation")
            
            st.markdown("""
            ## Market Analysis Module
            
            The Market Analysis module provides tools for analyzing competitors, identifying market trends, and performing SWOT analysis.
            
            ### Competitor Analysis
            
            The Competitor Analysis feature allows you to analyze a specific competitor to understand their strengths, weaknesses, and market position.
            
            #### How to use:
            
            1. Navigate to the Market Analysis page and select the "Competitor Analysis" tab.
            2. Enter the competitor name and select the industry.
            3. Click "Analyze Competitor" to generate the analysis.
            
            #### Output:
            
            - Strengths and weaknesses of the competitor
            - Market position and market share
            - Key products or services
            - Sentiment analysis based on news and social media
            
            ### Market Trends
            
            The Market Trends feature helps you identify emerging and declining trends in a specific industry.
            
            #### How to use:
            
            1. Navigate to the Market Analysis page and select the "Market Trends" tab.
            2. Select the industry and timeframe.
            3. Click "Identify Trends" to generate the analysis.
            
            #### Output:
            
            - Emerging trends in the industry
            - Declining trends in the industry
            - Sentiment trend over time
            - Key influencers driving the trends
            
            ### SWOT Analysis
            
            The SWOT Analysis feature helps you perform a comprehensive analysis of your company's strengths, weaknesses, opportunities, and threats.
            
            #### How to use:
            
            1. Navigate to the Market Analysis page and select the "SWOT Analysis" tab.
            2. Enter your company name and optionally list competitors.
            3. Click "Perform SWOT Analysis" to generate the analysis.
            
            #### Output:
            
            - Strengths: Internal factors that give your company an advantage
            - Weaknesses: Internal factors that place your company at a disadvantage
            - Opportunities: External factors that your company could capitalize on
            - Threats: External factors that could cause trouble for your company
            """)
        
        # Lead Generation Tab
        with tabs[2]:
            st.header("Lead Generation Documentation")
            
            st.markdown("""
            ## Lead Generation Module
            
            The Lead Generation module provides tools for defining your Ideal Customer Profile (ICP) and generating qualified leads based on that profile.
            
            ### Define Ideal Customer Profile (ICP)
            
            The ICP definition feature allows you to specify the characteristics of your ideal customers to improve lead quality.
            
            #### How to use:
            
            1. Navigate to the Lead Generation page and select the "Define ICP" tab.
            2. Specify your preferences for industries, regions, company sizes, job titles, and technologies.
            3. Set the minimum score threshold for lead qualification.
            4. Optionally, make certain criteria hard requirements.
            5. Click "Define ICP" to save your profile.
            
            #### ICP Components:
            
            - **Preferred Industries**: Industries that your ideal customers operate in.
            - **Preferred Regions**: Geographic regions where your ideal customers are located.
            - **Preferred Company Sizes**: Size ranges of companies that make ideal customers.
            - **Preferred Job Titles**: Job titles of decision-makers or influencers you want to target.
            - **Preferred Technologies**: Technologies used by your ideal customers.
            - **Minimum Score Threshold**: The minimum score (0-1) required for a prospect to be considered a qualified lead.
            - **Hard Requirements**: Criteria that must be met for a prospect to be considered (optional).
            
            ### Generate Leads
            
            The lead generation feature uses your defined ICP to identify and qualify potential leads.
            
            #### How to use:
            
            1. Navigate to the Lead Generation page and select the "Generate Leads" tab.
            2. Ensure you have defined an ICP (or use the default).
            3. Optionally, specify a target industry or region to focus on.
            4. Set the number of leads you want to generate.
            5. Click "Generate Leads" to start the process.
            
            #### Output:
            
            - List of qualified leads with contact information
            - Lead score for each prospect
            - Summary statistics (total leads, average score)
            - Visualizations of lead score distribution and industry distribution
            - Option to download leads as a CSV file
            """)
        
        # Business Support Tab
        with tabs[3]:
            st.header("Business Support Documentation")
            
            st.markdown("""
            ## Business Support Module
            
            The Business Support module provides additional tools to support your business operations, including sentiment analysis, news aggregation, reminders, and automated reports.
            
            ### Sentiment Analysis
            
            The Sentiment Analysis feature helps you understand public sentiment about a specific topic from news and social media sources.
            
            #### How to use:
            
            1. Navigate to the Business Support page and select the "Sentiment Analysis" tab.
            2. Enter the topic you want to analyze.
            3. Select the data sources (news, social media, or both).
            4. Click "Analyze Sentiment" to generate the analysis.
            
            #### Output:
            
            - Overall sentiment score (-1 to 1, where -1 is very negative and 1 is very positive)
            - Breakdown of positive, negative, and neutral mentions
            - Sentiment distribution visualization
            
            ### News Aggregation
            
            The News Aggregation feature collects recent news articles about a specific industry or topic.
            
            #### How to use:
            
            1. Navigate to the Business Support page and select the "News Aggregation" tab.
            2. Enter the industry or topic you want to track.
            3. Set the number of articles to retrieve.
            4. Click "Aggregate News" to collect the articles.
            
            #### Output:
            
            - List of recent news articles with titles, sources, dates, and summaries
            - Links to the original articles
            - Option to download the news report as a JSON file
            
            ### Reminders
            
            The Reminders feature allows you to set and track reminders for tasks and follow-ups.
            
            #### How to use:
            
            1. Navigate to the Business Support page and select the "Reminders" tab.
            2. Enter the task, due date, due time, and optional notes.
            3. Click "Set Reminder" to create the reminder.
            
            #### Output:
            
            - Confirmation of the reminder creation
            - List of recent reminders
            
            ### Automated Reports
            
            The Automated Reports feature generates comprehensive summary reports for your business.
            
            #### How to use:
            
            1. Navigate to the Business Support page and select the "Automated Reports" tab.
            2. Select the report type (weekly summary, monthly summary, etc.).
            3. Enter your company name and optionally list competitors.
            4. Click "Generate Report" to create the report.
            
            #### Output:
            
            - Comprehensive report with multiple sections (market summary, competitor activity, lead generation summary, etc.)
            - Visualizations and metrics relevant to the report type
            - Option to download the report as a JSON file
            """)
        
        # API Reference Tab
        with tabs[4]:
            st.header("API Reference")
            
            st.markdown("""
            ## API Reference
            
            The Business AI Agent provides a Python API that allows you to integrate its functionalities into your own applications.
            
            ### Market Analysis API
            
            ```python
            from business_ai_agent import MarketAnalysisAgent
            
            # Initialize the agent
            market_agent = MarketAnalysisAgent()
            
            # Analyze a competitor
            competitor_report = market_agent.analyze_competitor("Example Corp", "Technology")
            
            # Identify market trends
            trend_report = market_agent.identify_market_trends("Technology", "last_month")
            
            # Perform SWOT analysis
            swot_report = market_agent.perform_swot_analysis("Our Company", ["Competitor A", "Competitor B"])
            ```
            
            ### Lead Generation API
            
            ```python
            from business_ai_agent import LeadGenerationAgent
            
            # Initialize the agent
            lead_agent = LeadGenerationAgent()
            
            # Define an Ideal Customer Profile (ICP)
            icp = lead_agent.define_icp({
                "preferred_industries": ["Technology", "SaaS"],
                "preferred_regions": ["North America"],
                "preferred_company_sizes": ["51-200", "201-500"],
                "preferred_job_titles": ["CTO", "VP of Engineering"],
                "preferred_technologies": ["AWS", "Azure"],
                "min_score_threshold": 0.6
            })
            
            # Generate leads based on the ICP
            lead_report = lead_agent.generate_leads(
                icp=icp,
                target_industry="Technology",
                target_region="North America",
                num_leads=10
            )
            ```
            
            ### Business Support API
            
            ```python
            from business_ai_agent import BusinessSupportAgent
            
            # Initialize the agent
            support_agent = BusinessSupportAgent()
            
            # Analyze sentiment
            sentiment_report = support_agent.analyze_public_sentiment("Sustainable Energy", ["news", "social_media"])
            
            # Aggregate news
            news_report = support_agent.get_industry_news("Artificial Intelligence", num_articles=5)
            
            # Set a reminder
            reminder_result = support_agent.set_reminder(
                task="Follow up with lead",
                due_date="2025-05-01T14:00:00",
                notes="Discussed pricing on last call"
            )
            
            # Generate an automated report
            auto_report = support_agent.generate_automated_report(
                report_type="weekly_summary",
                company_name="Our Company",
                competitors=["Competitor A", "Competitor B"]
            )
            ```
            
            For more detailed information on the API methods and parameters, refer to the source code documentation.
            """)

# Main entry point
if __name__ == "__main__":
    ui = BusinessAIAgentUI()
    ui.run()
