"""
Data Collector for Business AI Agent - Real Data Integration

This module implements data collection from real sources including Yahoo Finance API
and web scraping for the Business AI Agent.
"""

import sys
import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Import the database manager
sys.path.append('/home/ubuntu')
import database_manager as db_manager

# Import the data API client for Yahoo Finance
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

# Ensure NLTK resources are available
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    nltk.download('stopwords')

class RealDataCollector:
    """Main class for collecting real data from various sources."""
    
    def __init__(self, db_conn=None):
        """Initialize the data collector with optional database connection."""
        self.db_conn = db_conn
        self.api_client = ApiClient()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.sia = SentimentIntensityAnalyzer()
        
        # Initialize database if connection not provided
        if not self.db_conn:
            self.db_conn = db_manager.get_db_connection()
            if self.db_conn:
                db_manager.create_tables(self.db_conn)
    
    def __del__(self):
        """Destructor to close database connection if it was created internally."""
        if hasattr(self, 'db_conn') and self.db_conn:
            self.db_conn.close()
            print("Database connection closed.")
    
    def collect_company_data_yahoo_finance(self, ticker_symbol, region="IN"):
        """
        Collect company data from Yahoo Finance API.
        
        Args:
            ticker_symbol (str): The stock ticker symbol
            region (str): Region code (e.g., "IN" for India, "US" for United States)
            
        Returns:
            dict: Company data or None if failed
        """
        print(f"Collecting data for {ticker_symbol} in region {region}...")
        
        try:
            # Get company profile
            profile_data = self.api_client.call_api(
                'YahooFinance/get_stock_profile', 
                query={'symbol': ticker_symbol, 'region': region}
            )
            
            if not profile_data or 'quoteSummary' not in profile_data:
                print(f"Failed to get profile data for {ticker_symbol}")
                return None
                
            # Extract relevant data from the profile
            company_data = {}
            
            # Navigate through the nested structure
            try:
                result = profile_data['quoteSummary']['result'][0]
                if 'summaryProfile' in result:
                    profile = result['summaryProfile']
                    company_data = {
                        'name': profile.get('name', ticker_symbol),  # Fallback to ticker if name not available
                        'ticker_symbol': ticker_symbol,
                        'region': region,
                        'industry': profile.get('industry'),
                        'sector': profile.get('sector'),
                        'website': profile.get('website'),
                        'address': self._combine_address(profile),
                        'phone': profile.get('phone'),
                        'employee_count': profile.get('fullTimeEmployees'),
                        'business_summary': profile.get('longBusinessSummary'),
                        'data_source': 'YahooFinance'
                    }
                    
                    # Get company officers if available
                    officers = profile.get('companyOfficers', [])
                    if officers:
                        company_data['officers'] = officers
                        
                    # Get executive team if available
                    exec_team = profile.get('executiveTeam', [])
                    if exec_team:
                        if 'officers' not in company_data:
                            company_data['officers'] = []
                        company_data['officers'].extend(exec_team)
            except (KeyError, IndexError) as e:
                print(f"Error parsing profile data: {e}")
            
            # Get additional insights if available
            try:
                insights_data = self.api_client.call_api(
                    'YahooFinance/get_stock_insights',
                    query={'symbol': ticker_symbol}
                )
                
                if insights_data and 'finance' in insights_data:
                    result = insights_data['finance']['result']
                    if 'companySnapshot' in result:
                        snapshot = result['companySnapshot']
                        if 'company' in snapshot:
                            company = snapshot['company']
                            company_data.update({
                                'innovativeness_score': company.get('innovativeness'),
                                'hiring_score': company.get('hiring'),
                                'sustainability_score': company.get('sustainability'),
                                'insider_sentiment_score': company.get('insiderSentiments')
                            })
            except Exception as e:
                print(f"Error getting insights data: {e}")
            
            # Store in database if connection available
            if self.db_conn and company_data:
                company_id = db_manager.add_or_update_company(self.db_conn, company_data)
                
                # Add officers if available
                if company_id and 'officers' in company_data:
                    db_manager.add_company_officers(self.db_conn, company_id, company_data['officers'])
                    
                company_data['company_id'] = company_id
            
            return company_data
            
        except Exception as e:
            print(f"Error collecting Yahoo Finance data for {ticker_symbol}: {e}")
            return None
    
    def _combine_address(self, profile):
        """Helper to combine address components from profile data."""
        address_parts = []
        for field in ['address1', 'address2', 'city', 'zip', 'country']:
            if field in profile and profile[field]:
                address_parts.append(profile[field])
        return ', '.join(address_parts) if address_parts else None
    
    def collect_news_for_company(self, company_name, num_articles=5):
        """
        Collect news articles about a specific company using web scraping.
        This is a simplified implementation that would need to be expanded with actual news sources.
        
        Args:
            company_name (str): The name of the company
            num_articles (int): Maximum number of articles to collect
            
        Returns:
            list: List of news article dictionaries
        """
        print(f"Collecting news for company: {company_name}")
        
        # In a real implementation, this would use a News API or web scraping
        # For demonstration, we'll create a simulated scraping function
        
        articles = self._simulate_news_scraping(company_name, num_articles)
        
        # Store in database if connection available
        if self.db_conn and articles:
            # Get company ID if available
            company = db_manager.get_company_by_name(self.db_conn, company_name)
            company_id = company['company_id'] if company else None
            
            # Add each article to database
            for article in articles:
                if company_id:
                    article['company_id'] = company_id
                db_manager.add_news_article(self.db_conn, article)
        
        return articles
    
    def _simulate_news_scraping(self, company_name, num_articles):
        """
        Simulates news scraping for demonstration purposes.
        In a real implementation, this would be replaced with actual web scraping or API calls.
        """
        articles = []
        sources = ["Economic Times", "Business Standard", "Mint", "Financial Express", "Business Today"]
        topics = ["financial results", "new product launch", "expansion", "management changes", "market strategy"]
        
        for i in range(num_articles):
            # Create a simulated article
            title = f"{company_name} {random.choice(topics)}"
            source = random.choice(sources)
            published_date = datetime.now()  # In real implementation, would parse actual dates
            summary = f"This is a simulated news article about {company_name} regarding {topics[i % len(topics)]}."
            
            # Perform sentiment analysis on the summary
            sentiment = self.sia.polarity_scores(summary)
            sentiment_score = sentiment['compound']
            sentiment_label = "positive" if sentiment_score > 0.05 else ("negative" if sentiment_score < -0.05 else "neutral")
            
            article = {
                'title': title,
                'source_name': source,
                'source_url': f"http://example.com/{company_name.lower().replace(' ', '-')}/article{i}",
                'published_date': published_date,
                'summary': summary,
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'collected_date': datetime.now()
            }
            
            articles.append(article)
        
        return articles
    
    def collect_india_real_estate_data(self, city=None, limit=10):
        """
        Collect data about real estate projects in India.
        This is a simplified implementation that would need to be expanded with actual data sources.
        
        Args:
            city (str, optional): Filter by city
            limit (int): Maximum number of projects to collect
            
        Returns:
            list: List of real estate project dictionaries
        """
        print(f"Collecting India real estate data for city: {city or 'All'}")
        
        # In a real implementation, this would scrape real estate websites or use APIs
        # For demonstration, we'll create simulated data
        
        projects = self._simulate_real_estate_data(city, limit)
        
        # Store in database if connection available
        if self.db_conn and projects:
            for project in projects:
                # Check if developer exists in companies table
                developer_name = project.get('developer_name')
                developer_id = None
                
                if developer_name:
                    company = db_manager.get_company_by_name(self.db_conn, developer_name)
                    if company:
                        developer_id = company['company_id']
                        project['developer_id'] = developer_id
                    else:
                        # Add developer as a company if not exists
                        developer_data = {
                            'name': developer_name,
                            'region': 'IN',
                            'industry': 'Real Estate',
                            'sector': 'Real Estate',
                            'data_source': 'Simulated'
                        }
                        developer_id = db_manager.add_or_update_company(self.db_conn, developer_data)
                        project['developer_id'] = developer_id
                
                # Add project to database
                db_manager.add_india_real_estate_project(self.db_conn, project)
        
        return projects
    
    def _simulate_real_estate_data(self, city=None, limit=10):
        """Simulates real estate data collection for demonstration purposes."""
        projects = []
        cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata"]
        developers = ["Prestige Group", "DLF Limited", "Godrej Properties", "Sobha Limited", "Brigade Group"]
        project_types = ["Residential", "Commercial", "Mixed-Use", "Retail"]
        statuses = ["Upcoming", "Under Construction", "Completed"]
        
        if city:
            cities = [city]
            
        for i in range(limit):
            selected_city = random.choice(cities)
            selected_developer = random.choice(developers)
            
            project = {
                'project_name': f"{selected_developer} {['Heights', 'Towers', 'Park', 'Plaza', 'Residency'][i % 5]} {selected_city}",
                'developer_name': selected_developer,
                'city': selected_city,
                'region': self._get_state_for_city(selected_city),
                'project_type': random.choice(project_types),
                'status': random.choice(statuses),
                'rera_registration_id': f"RERA{selected_city[:2].upper()}{random.randint(1000, 9999)}",
                'launch_date': f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                'expected_completion_date': f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                'total_area_sqft': random.randint(50000, 500000),
                'price_per_sqft_range': f"₹{random.randint(4000, 20000)} - ₹{random.randint(20001, 30000)}",
                'key_features': "Swimming Pool, Gym, Club House, 24x7 Security, Power Backup",
                'source_url': f"http://example.com/realestate/{selected_city.lower()}/{i}",
                'collected_date': datetime.now()
            }
            
            projects.append(project)
        
        return projects
    
    def _get_state_for_city(self, city):
        """Helper to map city to state in India."""
        state_map = {
            "Mumbai": "Maharashtra",
            "Pune": "Maharashtra",
            "Delhi": "Delhi NCR",
            "Gurgaon": "Delhi NCR",
            "Noida": "Delhi NCR",
            "Bangalore": "Karnataka",
            "Hyderabad": "Telangana",
            "Chennai": "Tamil Nadu",
            "Kolkata": "West Bengal",
            "Ahmedabad": "Gujarat"
        }
        return state_map.get(city, "Unknown")
    
    def collect_india_architectural_firms(self, city=None, limit=10):
        """
        Collect data about architectural firms in India.
        This is a simplified implementation that would need to be expanded with actual data sources.
        
        Args:
            city (str, optional): Filter by city
            limit (int): Maximum number of firms to collect
            
        Returns:
            list: List of architectural firm dictionaries
        """
        print(f"Collecting India architectural firms for city: {city or 'All'}")
        
        # In a real implementation, this would scrape websites or use APIs
        # For demonstration, we'll create simulated data
        
        firms = self._simulate_architectural_firms(city, limit)
        
        # Store in database if connection available
        if self.db_conn and firms:
            for firm in firms:
                # Check if firm exists in companies table
                firm_name = firm.get('firm_name')
                company_id = None
                
                if firm_name:
                    company = db_manager.get_company_by_name(self.db_conn, firm_name)
                    if company:
                        company_id = company['company_id']
                        firm['company_id'] = company_id
                    else:
                        # Add firm as a company if not exists
                        firm_data_for_company = {
                            'name': firm_name,
                            'region': 'IN',
                            'industry': 'Architecture & Planning',
                            'sector': 'Industrials', # Or another appropriate sector
                            'website': firm.get('source_url'), # Use source_url as website placeholder
                            'data_source': 'Simulated'
                        }
                        company_id = db_manager.add_or_update_company(self.db_conn, firm_data_for_company)
                        firm['company_id'] = company_id
                
                # Add firm to database
                db_manager.add_india_architectural_firm(self.db_conn, firm)
        
        return firms
    
    def _simulate_architectural_firms(self, city=None, limit=10):
        """Simulates architectural firm data collection for demonstration purposes."""
        firms = []
        cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata"]
        specializations = ["Residential", "Commercial", "Institutional", "Urban Planning", "Interior Design"]
        
        if city:
            cities = [city]
            
        for i in range(limit):
            selected_city = random.choice(cities)
            
            firm = {
                'firm_name': f"{['Innovative', 'Modern', 'Creative', 'Urban', 'Classic'][i % 5]} Architects",
                'city': selected_city,
                'region': self._get_state_for_city(selected_city),
                'specialization': random.choice(specializations),
                'notable_projects': f"Project A, Project B, Project C",
                'key_personnel': f"Architect {chr(65+i)}, Designer {chr(75+i)}",
                'awards': f"Best Design Award {2020+i%3}, Excellence in Architecture {2018+i%5}",
                'coa_registration_id': f"COA{random.randint(10000, 99999)}",
                'source_url': f"http://example.com/architects/{i}",
                'collected_date': datetime.now()
            }
            
            firms.append(firm)
        
        return firms

# Example usage
if __name__ == "__main__":
    # Initialize database
    db_manager.initialize_database()
    
    # Create data collector
    collector = RealDataCollector()
    
    # Test collecting company data from Yahoo Finance
    company_data = collector.collect_company_data_yahoo_finance("INFY.NS", "IN")
    if company_data:
        print(f"\nCollected data for {company_data.get('name', 'Unknown')}:")
        print(f"Industry: {company_data.get('industry', 'N/A')}")
        print(f"Sector: {company_data.get('sector', 'N/A')}")
        print(f"Website: {company_data.get('website', 'N/A')}")
        print(f"Employees: {company_data.get('employee_count', 'N/A')}")
        
        # Test collecting news
        news = collector.collect_news_for_company(company_data.get('name', 'Infosys'), 3)
        print(f"\nCollected {len(news)} news articles")
        
    # Test collecting real estate data
    real_estate = collector.collect_india_real_estate_data("Mumbai", 2)
    print(f"\nCollected {len(real_estate)} real estate projects")
    
    # Test collecting architectural firms
    firms = collector.collect_india_architectural_firms("Delhi", 2)
    print(f"\nCollected {len(firms)} architectural firms")
