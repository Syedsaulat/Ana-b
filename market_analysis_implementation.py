"""
Business AI Agent - Market Analysis Module Implementation (Enhanced with Real Data)

This module implements the market analysis functionality for the Business AI Agent,
integrating with the database and real data collector.
"""

import sys
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3 # Added import

# Add project root to path for imports
sys.path.append("/home/ubuntu")
import database_manager as db_manager
from real_data_collector import RealDataCollector

# Ensure NLTK resources are available (should be downloaded by real_data_collector)
try:
    nltk.data.find("vader_lexicon")
except LookupError:
    print("NLTK vader_lexicon not found. Please run real_data_collector.py first to download.")
    # Attempt download again just in case
    try:
        nltk.download("vader_lexicon", quiet=True)
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
    except Exception as e:
        print(f"Failed to download NLTK data: {e}")

class MarketAnalysisAgent:
    """Main class for the Market Analysis functionality using real data."""

    def __init__(self, db_conn=None):
        """Initialize the Market Analysis Agent with a database connection."""
        self.db_conn = db_conn if db_conn else db_manager.get_db_connection()
        if not self.db_conn:
            raise ConnectionError("Failed to establish database connection.")

        self.data_collector = RealDataCollector(self.db_conn) # Pass connection
        self.analyzer = MarketAnalyzer(self.db_conn) # Pass connection
        self.reporter = ReportGenerator(self.db_conn) # Pass connection
        print("MarketAnalysisAgent initialized with database connection.")

    def __del__(self):
        """Close the database connection if it was created internally."""
        # Only close if the connection was created by this instance
        # Assuming external code manages externally provided connections
        pass # Let RealDataCollector handle its own connection management for now

    def analyze_competitor(self, competitor_ticker=None, competitor_name=None, industry=None, region="IN"):
        """Perform a comprehensive analysis of a specific competitor using real data."""
        print(f"Starting competitor analysis for: {competitor_ticker or competitor_name}")

        company_data = None
        company_id = None

        # 1. Collect/Retrieve Competitor Data
        if competitor_ticker:
            # Try fetching from DB first
            company_row = db_manager.get_company_by_ticker(self.db_conn, competitor_ticker)
            if company_row:
                print(f"Found competitor {competitor_ticker} in database.")
                company_data = dict(company_row)
                company_id = company_data["company_id"]
            else:
                print(f"Competitor {competitor_ticker} not in database. Collecting from Yahoo Finance...")
                # Collect from Yahoo Finance API via RealDataCollector
                company_data = self.data_collector.collect_company_data_yahoo_finance(competitor_ticker, region)
                if company_data:
                    company_id = company_data.get("company_id") # ID is added by collector
        elif competitor_name:
            # Try fetching by name from DB
            company_row = db_manager.get_company_by_name(self.db_conn, competitor_name)
            if company_row:
                print(f"Found competitor {competitor_name} in database.")
                company_data = dict(company_row)
                company_id = company_data["company_id"]
            else:
                # TODO: Implement web scraping or other methods for non-ticker companies
                print(f"Competitor {competitor_name} not found by name in DB. Data collection for non-ticker companies needs implementation.")
                # FIXED return statement
                return f"Error: Data collection for non-ticker company '{competitor_name}' not yet implemented."
        else:
            return "Error: Must provide either competitor_ticker or competitor_name."

        if not company_data or not company_id:
            return f"Error: Could not retrieve or collect data for competitor {competitor_ticker or competitor_name}."

        # 2. Collect Related News (if not recently collected)
        # TODO: Add logic to check last_updated for news and collect if needed
        self.data_collector.collect_news_for_company(company_data["name"])

        # 3. Analyze the data (using data from DB)
        analysis_results = self.analyzer.analyze_competitor(company_id, industry)

        # 4. Generate a report
        report = self.reporter.generate_competitor_report(analysis_results, company_data["name"])

        return report

    def identify_market_trends(self, industry, region="IN", timeframe="last_month"):
        """Identify trends in a specific industry over the given timeframe using real data."""
        print(f"Identifying market trends for industry: {industry} in {region} over {timeframe}")

        # 1. Collect Trend Data (e.g., from news, potentially specific trend sources)
        # TODO: Implement actual trend data collection in RealDataCollector
        # For now, relies on news collected for companies in that industry
        print("Trend data collection relies on existing news data. Implement dedicated trend sources for better results.")

        # 2. Analyze trends based on data in DB
        trend_analysis = self.analyzer.analyze_trends(industry, region, timeframe)

        # 3. Generate a trend report
        report = self.reporter.generate_trend_report(trend_analysis, industry, timeframe)

        return report

    def perform_swot_analysis(self, company_ticker=None, company_name=None, competitor_tickers=None, region="IN"):
        """Perform a SWOT analysis for the specified company using real data."""
        print(f"Performing SWOT analysis for: {company_ticker or company_name}")

        company_data = None
        company_id = None
        competitor_ids = []

        # 1. Collect/Retrieve Company Data
        if company_ticker:
            company_row = db_manager.get_company_by_ticker(self.db_conn, company_ticker)
            if company_row:
                company_data = dict(company_row)
                company_id = company_data["company_id"]
            else:
                company_data = self.data_collector.collect_company_data_yahoo_finance(company_ticker, region)
                if company_data:
                    company_id = company_data.get("company_id")
        elif company_name:
             company_row = db_manager.get_company_by_name(self.db_conn, company_name)
             if company_row:
                 company_data = dict(company_row)
                 company_id = company_data["company_id"]
             else:
                 print(f"Company {company_name} not found by name in DB. Data collection for non-ticker companies needs implementation.")
                 # FIXED return statement
                 return f"Error: Data collection for non-ticker company '{company_name}' not yet implemented."
        else:
            return "Error: Must provide either company_ticker or company_name."

        if not company_data or not company_id:
            return f"Error: Could not retrieve or collect data for company {company_ticker or company_name}."

        # 2. Collect/Retrieve Competitor Data
        if competitor_tickers:
            for ticker in competitor_tickers:
                comp_row = db_manager.get_company_by_ticker(self.db_conn, ticker)
                comp_id = None
                if comp_row:
                    comp_id = comp_row["company_id"]
                else:
                    comp_data = self.data_collector.collect_company_data_yahoo_finance(ticker, region)
                    if comp_data:
                        comp_id = comp_data.get("company_id")
                if comp_id:
                    competitor_ids.append(comp_id)
                else:
                    print(f"Warning: Could not get data for competitor ticker {ticker}")

        # 3. Perform SWOT analysis using data from DB
        swot_results = self.analyzer.perform_swot_analysis(company_id, competitor_ids)

        # 4. Generate SWOT report
        report = self.reporter.generate_swot_report(swot_results, company_data["name"])

        return report

    def analyze_market_segment(self, segment_name, industry, region="IN"):
        """Analyze a specific market segment within an industry using real data."""
        print(f"Analyzing market segment: {segment_name} in {industry} ({region})")

        # 1. Collect Segment Data (Relies on existing company/news/trend data tagged with industry/region)
        # TODO: Implement specific segment data collection in RealDataCollector if needed
        print("Segment analysis relies on existing data. Implement dedicated segment data sources for better results.")

        # 2. Analyze segment based on data in DB
        segment_analysis = self.analyzer.analyze_segment(segment_name, industry, region)

        # 3. Generate segment report
        report = self.reporter.generate_segment_report(segment_analysis, segment_name, industry)

        return report

# --- Analysis Logic --- (Refactored to use DB data)
class MarketAnalyzer:
    """Component responsible for analyzing processed market data from the database."""

    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.sia = SentimentIntensityAnalyzer()

    def analyze_competitor(self, company_id, industry=None):
        """Analyze a competitor based on data retrieved from the database."""
        print(f"Analyzing competitor with ID: {company_id}")
        if not self.db_conn:
            return {"error": "Database connection not available."}

        cursor = self.db_conn.cursor()
        analysis = {"company_id": company_id, "analysis_timestamp": datetime.now().isoformat()}

        try:
            # Get company profile
            cursor.execute("SELECT * FROM companies WHERE company_id = ?", (company_id,))
            company_profile = cursor.fetchone()
            if not company_profile:
                return {"error": f"Company with ID {company_id} not found."}
            analysis["profile"] = dict(company_profile)
            analysis["name"] = company_profile["name"]

            # Get recent news sentiment
            cursor.execute("""
                SELECT AVG(sentiment_score) as avg_sentiment, COUNT(*) as news_count
                FROM news_articles
                WHERE company_id = ? AND published_date >= date('now', '-30 days')
            """, (company_id,))
            news_sentiment = cursor.fetchone()
            analysis["recent_news_sentiment"] = dict(news_sentiment) if news_sentiment else {}

            # Get financial highlights (if available)
            analysis["financials"] = {
                "market_cap": company_profile["market_cap"],
                "revenue": company_profile["revenue"],
                "growth_rate": company_profile["growth_rate"],
                "profit_margin": company_profile["profit_margin"]
            }

            # Get insight scores (if available)
            analysis["insight_scores"] = {
                "innovativeness": company_profile["innovativeness_score"],
                "hiring": company_profile["hiring_score"],
                "sustainability": company_profile["sustainability_score"],
                "insider_sentiment": company_profile["insider_sentiment_score"]
            }

            # TODO: Add more sophisticated analysis - market position, comparisons
            # FIXED summary string generation and sentiment formatting
            avg_sentiment_val = analysis['recent_news_sentiment'].get('avg_sentiment')
            avg_sentiment_str = f"{avg_sentiment_val:.2f}" if avg_sentiment_val is not None else 'N/A'
            news_count_val = analysis['recent_news_sentiment'].get('news_count', 0)
            analysis["summary"] = f"Basic analysis for {analysis['name']}. Recent news sentiment score: {avg_sentiment_str} based on {news_count_val} articles."

        except sqlite3.Error as e:
            print(f"Database error during competitor analysis: {e}")
            analysis["error"] = str(e)
        finally:
            if cursor:
                cursor.close()

        return analysis

    def analyze_trends(self, industry, region, timeframe):
        """Analyze market trends based on data retrieved from the database."""
        print(f"Analyzing trends for {industry} in {region}...")
        if not self.db_conn:
            return {"error": "Database connection not available."}

        cursor = self.db_conn.cursor()
        analysis = {"industry": industry, "region": region, "timeframe": timeframe, "analysis_timestamp": datetime.now().isoformat()}

        try:
            # Get recent news sentiment for the industry
            # Note: This requires news articles to be tagged with industry
            cursor.execute("""
                SELECT AVG(sentiment_score) as avg_sentiment, COUNT(*) as news_count
                FROM news_articles
                WHERE industry = ? AND published_date >= date('now', '-30 days') -- Adjust timeframe logic
            """, (industry,))
            industry_sentiment = cursor.fetchone()
            analysis["overall_industry_sentiment"] = dict(industry_sentiment) if industry_sentiment else {}

            # Get identified market trends from the trends table
            cursor.execute("""
                SELECT * FROM market_trends
                WHERE industry = ? AND region = ? AND collected_date >= date('now', '-30 days') -- Adjust timeframe logic
                ORDER BY published_date DESC
                LIMIT 10
            """, (industry, region))
            trends = cursor.fetchall()
            analysis["identified_trends"] = [dict(row) for row in trends]

            # TODO: Add more sophisticated trend analysis (e.g., topic modeling on news)
            # FIXED summary string generation and sentiment formatting
            avg_sentiment_val = analysis['overall_industry_sentiment'].get('avg_sentiment')
            avg_sentiment_str = f"{avg_sentiment_val:.2f}" if avg_sentiment_val is not None else 'N/A'
            analysis["summary"] = f"Identified {len(analysis['identified_trends'])} recent trends for {industry} in {region}. Overall sentiment score: {avg_sentiment_str}."

        except sqlite3.Error as e:
            print(f"Database error during trend analysis: {e}")
            analysis["error"] = str(e)
        finally:
            if cursor:
                cursor.close()

        return analysis

    def perform_swot_analysis(self, company_id, competitor_ids):
        """Perform SWOT analysis based on data retrieved from the database."""
        print(f"Performing SWOT for company ID: {company_id} against competitors: {competitor_ids}")
        if not self.db_conn:
            return {"error": "Database connection not available."}

        cursor = self.db_conn.cursor()
        swot = {
            "company_id": company_id,
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "threats": [],
            "analysis_timestamp": datetime.now().isoformat()
        }

        try:
            # Get company profile
            cursor.execute("SELECT * FROM companies WHERE company_id = ?", (company_id,))
            company_profile = cursor.fetchone()
            if not company_profile:
                return {"error": f"Company with ID {company_id} not found."}
            swot["company_name"] = company_profile["name"]

            # --- Strengths (Internal, Positive) ---
            if company_profile["profit_margin"] and company_profile["profit_margin"] > 0.15: # Example threshold
                swot["strengths"].append(f"Strong profit margin ({company_profile['profit_margin']*100:.1f}%)")
            if company_profile["innovativeness_score"] and company_profile["innovativeness_score"] > 0.7:
                swot["strengths"].append(f"High innovativeness score ({company_profile['innovativeness_score']:.2f})")
            # TODO: Add more strength indicators (market share, brand reputation from sentiment, etc.)

            # --- Weaknesses (Internal, Negative) ---
            if company_profile["growth_rate"] is not None and company_profile["growth_rate"] < 0.05:
                swot["weaknesses"].append(f"Low revenue growth rate ({company_profile['growth_rate']*100:.1f}%)")
            if company_profile["hiring_score"] and company_profile["hiring_score"] < 0.5:
                 swot["weaknesses"].append(f"Potentially slow hiring momentum ({company_profile['hiring_score']:.2f})")
            # TODO: Add more weakness indicators (negative news sentiment, debt levels, etc.)

            # --- Opportunities (External, Positive) ---
            # Look for positive industry trends
            cursor.execute("""
                SELECT trend_description FROM market_trends
                WHERE industry = ? AND region = ? AND sentiment_score > 0.1 -- Positive trends
                ORDER BY published_date DESC LIMIT 3
            """, (company_profile["industry"], company_profile["region"]))
            positive_trends = cursor.fetchall()
            for trend in positive_trends:
                swot["opportunities"].append(f"Emerging industry trend: {trend['trend_description']}")
            # TODO: Add more opportunities (new markets, competitor weaknesses)

            # --- Threats (External, Negative) ---
            # Look for strong competitors
            if competitor_ids:
                placeholders = ",".join(["?"] * len(competitor_ids))
                cursor.execute(f"""
                    SELECT name, market_cap FROM companies
                    WHERE company_id IN ({placeholders}) AND market_cap > ?
                    ORDER BY market_cap DESC LIMIT 3
                """, competitor_ids + [company_profile["market_cap"] or 0])
                strong_competitors = cursor.fetchall()
                for comp in strong_competitors:
                    swot["threats"].append(f"Strong competitor: {comp['name']} (Market Cap: {comp['market_cap']})")

            # Look for negative industry trends
            cursor.execute("""
                SELECT trend_description FROM market_trends
                WHERE industry = ? AND region = ? AND sentiment_score < -0.1 -- Negative trends
                ORDER BY published_date DESC LIMIT 2
            """, (company_profile["industry"], company_profile["region"]))
            negative_trends = cursor.fetchall()
            for trend in negative_trends:
                swot["threats"].append(f"Concerning industry trend: {trend['trend_description']}")
            # TODO: Add more threats (regulatory changes, economic downturn)

            # Add default messages if lists are empty
            if not swot["strengths"]: swot["strengths"].append("No specific strengths identified from available data.")
            if not swot["weaknesses"]: swot["weaknesses"].append("No specific weaknesses identified from available data.")
            if not swot["opportunities"]: swot["opportunities"].append("No specific opportunities identified from available data.")
            if not swot["threats"]: swot["threats"].append("No specific threats identified from available data.")

        except sqlite3.Error as e:
            print(f"Database error during SWOT analysis: {e}")
            swot["error"] = str(e)
        finally:
            if cursor:
                cursor.close()

        return swot

    def analyze_segment(self, segment_name, industry, region):
        """Analyze a market segment based on data retrieved from the database."""
        print(f"Analyzing segment {segment_name} in {industry} ({region})...")
        if not self.db_conn:
            return {"error": "Database connection not available."}

        cursor = self.db_conn.cursor()
        analysis = {"segment": segment_name, "industry": industry, "region": region, "analysis_timestamp": datetime.now().isoformat()}

        try:
            # Find companies in this industry/segment/region
            # Note: This relies on companies being tagged with industry/sector
            cursor.execute("""
                SELECT company_id, name, market_cap, growth_rate
                FROM companies
                WHERE industry = ? AND region = ? -- Add segment filtering if possible
                ORDER BY market_cap DESC NULLS LAST
                LIMIT 10
            """, (industry, region))
            key_players = cursor.fetchall()
            analysis["key_players"] = [dict(row) for row in key_players]

            # Get overall sentiment for news related to the industry/segment
            cursor.execute("""
                SELECT AVG(sentiment_score) as avg_sentiment, COUNT(*) as news_count
                FROM news_articles
                WHERE industry = ? AND published_date >= date('now', '-90 days') -- Wider timeframe for segment
            """, (industry,))
            segment_sentiment = cursor.fetchone()
            analysis["segment_sentiment"] = dict(segment_sentiment) if segment_sentiment else {}

            # Get relevant trends
            cursor.execute("""
                SELECT * FROM market_trends
                WHERE industry = ? AND region = ? AND collected_date >= date('now', '-90 days')
                ORDER BY published_date DESC
                LIMIT 5
            """, (industry, region))
            trends = cursor.fetchall()
            analysis["relevant_trends"] = [dict(row) for row in trends]

            # Specific data for Real Estate / Architecture if applicable
            if industry == "Real Estate":
                 cursor.execute("""
                    SELECT * FROM india_real_estate_projects
                    WHERE region = ? -- Or filter by city if more specific
                    ORDER BY launch_date DESC LIMIT 10
                 """, (region,))
                 projects = cursor.fetchall()
                 analysis["recent_real_estate_projects"] = [dict(row) for row in projects]
            elif industry == "Architecture & Planning":
                 cursor.execute("""
                    SELECT * FROM india_architectural_firms
                    WHERE region = ? -- Or filter by city
                    ORDER BY firm_id DESC LIMIT 10
                 """, (region,))
                 firms = cursor.fetchall()
                 analysis["recent_architectural_firms"] = [dict(row) for row in firms]

            # TODO: Add more segment analysis (size estimation, growth potential)
            # FIXED summary string concatenation and sentiment formatting
            avg_sentiment_val = analysis['segment_sentiment'].get('avg_sentiment')
            avg_sentiment_str = f"{avg_sentiment_val:.2f}" if avg_sentiment_val is not None else 'N/A'
            analysis["summary"] = f"Analysis for segment '{segment_name}' in '{industry}' ({region}). Identified {len(analysis['key_players'])} key players. Overall sentiment: {avg_sentiment_str}."

        except sqlite3.Error as e:
            print(f"Database error during segment analysis: {e}")
            analysis["error"] = str(e)
        finally:
            if cursor:
                cursor.close()

        return analysis

# --- Reporting Logic --- (Refactored)
class ReportGenerator:
    """Component responsible for generating reports based on analysis results."""

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def generate_competitor_report(self, analysis_results, competitor_name):
        """Generate a formatted report for competitor analysis."""
        print(f"Generating competitor report for: {competitor_name}")
        if "error" in analysis_results:
            return f"Error generating report for {competitor_name}: {analysis_results['error']}"

        report = f"# Competitor Analysis Report: {competitor_name}\n\n"
        report += f"*Analysis Timestamp: {analysis_results.get('analysis_timestamp')}*\n\n"

        profile = analysis_results.get("profile", {})
        report += "## Company Profile\n"
        report += f"- **Industry:** {profile.get('industry', 'N/A')}\n"
        report += f"- **Sector:** {profile.get('sector', 'N/A')}\n"
        report += f"- **Website:** {profile.get('website', 'N/A')}\n"
        report += f"- **Employees:** {profile.get('employee_count', 'N/A')}\n"
        report += f"- **Summary:** {profile.get('business_summary', 'N/A')}\n\n"

        financials = analysis_results.get("financials", {})
        report += "## Financial Highlights\n"
        report += f"- **Market Cap:** {financials.get('market_cap', 'N/A')}\n"
        report += f"- **Revenue:** {financials.get('revenue', 'N/A')}\n"
        report += f"- **Growth Rate:** {financials.get('growth_rate', 'N/A')}\n"
        report += f"- **Profit Margin:** {financials.get('profit_margin', 'N/A')}\n\n"

        insights = analysis_results.get("insight_scores", {})
        report += "## Insight Scores (from Yahoo Finance)\n"
        report += f"- **Innovativeness:** {insights.get('innovativeness', 'N/A')}\n"
        report += f"- **Hiring:** {insights.get('hiring', 'N/A')}\n"
        report += f"- **Sustainability:** {insights.get('sustainability', 'N/A')}\n"
        # FIXED key typo
        report += f"- **Insider Sentiment:** {insights.get('insider_sentiment', 'N/A')}\n\n"

        sentiment = analysis_results.get("recent_news_sentiment", {})
        report += "## Recent News Sentiment (Last 30 Days)\n"
        # FIXED sentiment formatting
        avg_sentiment_val = sentiment.get("avg_sentiment")
        avg_sentiment_str = f"{avg_sentiment_val:.3f}" if avg_sentiment_val is not None else "N/A"
        report += f"- **Average Score:** {avg_sentiment_str}\n"
        report += f"- **Article Count:** {sentiment.get('news_count', 'N/A')}\n\n"

        report += f"## Summary\n{analysis_results.get('summary', 'N/A')}\n"

        # TODO: Add visualizations (e.g., sentiment over time)

        return report

    def generate_trend_report(self, trend_analysis, industry, timeframe):
        """Generate a formatted report for market trends."""
        print(f"Generating trend report for: {industry}")
        if "error" in trend_analysis:
            return f"Error generating trend report for {industry}: {trend_analysis['error']}"

        report = f"# Market Trend Report: {industry} ({timeframe})\n\n"
        report += f"*Analysis Timestamp: {trend_analysis.get('analysis_timestamp')}*\n\n"

        sentiment = trend_analysis.get("overall_industry_sentiment", {})
        report += "## Overall Industry Sentiment (News Based)\n"
        # FIXED sentiment formatting
        avg_sentiment_val = sentiment.get("avg_sentiment")
        avg_sentiment_str = f"{avg_sentiment_val:.3f}" if avg_sentiment_val is not None else "N/A"
        report += f"- **Average Score:** {avg_sentiment_str}\n"
        report += f"- **Article Count:** {sentiment.get('news_count', 'N/A')}\n\n"

        trends = trend_analysis.get("identified_trends", [])
        report += "## Identified Trends\n"
        if trends:
            for i, trend in enumerate(trends):
                report += f"### Trend {i+1}: {trend.get('trend_description', 'N/A')}\n"
                report += f"- **Type:** {trend.get('trend_type', 'N/A')}\n"
                report += f"- **Source:** {trend.get('source', 'N/A')}\n"
                report += f"- **Published:** {trend.get('published_date', 'N/A')}\n"
                report += f"- **Sentiment Score:** {trend.get('sentiment_score', 'N/A')}\n\n"
        else:
            report += "- No specific trends identified in the database for this period.\n\n"

        report += f"## Summary\n{trend_analysis.get('summary', 'N/A')}\n"

        # TODO: Add visualizations (e.g., trend timeline)

        return report

    def generate_swot_report(self, swot_results, company_name):
        """Generate a formatted report for SWOT analysis."""
        print(f"Generating SWOT report for: {company_name}")
        if "error" in swot_results:
            return f"Error generating SWOT report for {company_name}: {swot_results['error']}"

        report = f"# SWOT Analysis Report: {company_name}\n\n"
        report += f"*Analysis Timestamp: {swot_results.get('analysis_timestamp')}*\n\n"

        report += "## Strengths (Internal, Positive)\n"
        for item in swot_results.get("strengths", []):
            report += f"- {item}\n"
        report += "\n"

        report += "## Weaknesses (Internal, Negative)\n"
        for item in swot_results.get("weaknesses", []):
            report += f"- {item}\n"
        report += "\n"

        report += "## Opportunities (External, Positive)\n"
        for item in swot_results.get("opportunities", []):
            report += f"- {item}\n"
        report += "\n"

        report += "## Threats (External, Negative)\n"
        for item in swot_results.get("threats", []):
            report += f"- {item}\n"
        report += "\n"

        return report

    def generate_segment_report(self, segment_analysis, segment_name, industry):
        """Generate a formatted report for market segment analysis."""
        print(f"Generating segment report for: {segment_name} in {industry}")
        if "error" in segment_analysis:
            return f"Error generating segment report: {segment_analysis['error']}"

        report = f"# Market Segment Analysis Report: {segment_name} ({industry})\n\n"
        report += f"*Analysis Timestamp: {segment_analysis.get('analysis_timestamp')}*\n\n"
        report += f"*Region: {segment_analysis.get('region', 'N/A')}*\n\n"

        sentiment = segment_analysis.get("segment_sentiment", {})
        report += "## Segment Sentiment (Industry News Based)\n"
        # FIXED sentiment formatting
        avg_sentiment_val = sentiment.get("avg_sentiment")
        avg_sentiment_str = f"{avg_sentiment_val:.3f}" if avg_sentiment_val is not None else "N/A"
        report += f"- **Average Score:** {avg_sentiment_str}\n"
        report += f"- **Article Count:** {sentiment.get('news_count', 'N/A')}\n\n"

        players = segment_analysis.get("key_players", [])
        report += "## Key Players (Top 10 by Market Cap)\n"
        if players:
            df_players = pd.DataFrame(players)
            report += df_players.to_markdown(index=False)
            report += "\n\n"
        else:
            report += "- No key players identified in the database for this segment/region.\n\n"

        trends = segment_analysis.get("relevant_trends", [])
        report += "## Relevant Trends\n"
        if trends:
            for trend in trends:
                report += f"- {trend.get('trend_description', 'N/A')} (Source: {trend.get('source', 'N/A')}, Sentiment: {trend.get('sentiment_score', 'N/A')})\n"
            report += "\n"
        else:
            report += "- No specific trends identified in the database for this segment/region.\n\n"

        # Add industry-specific sections
        if "recent_real_estate_projects" in segment_analysis:
            projects = segment_analysis["recent_real_estate_projects"]
            report += "## Recent Real Estate Projects (India)\n"
            if projects:
                df_projects = pd.DataFrame(projects)[["project_name", "developer_name", "city", "status", "rera_registration_id"]]
                report += df_projects.to_markdown(index=False)
                report += "\n\n"
            else:
                report += "- No recent real estate projects found in the database for this region.\n\n"

        if "recent_architectural_firms" in segment_analysis:
            firms = segment_analysis["recent_architectural_firms"]
            report += "## Recent Architectural Firms (India)\n"
            if firms:
                df_firms = pd.DataFrame(firms)[["firm_name", "city", "specialization"]]
                report += df_firms.to_markdown(index=False)
                report += "\n\n"
            else:
                report += "- No recent architectural firms found in the database for this region.\n\n"

        # Summary is already fixed in analyze_segment method
        report += f"## Summary\n{segment_analysis.get('summary', 'N/A')}\n"

        return report

# --- Main Execution / Test --- (Updated)
if __name__ == "__main__":
    print("Testing Market Analysis Agent with Real Data Integration...")

    # Ensure database exists and is initialized
    if not os.path.exists(db_manager.DATABASE_NAME):
        print("Database file not found. Initializing...")
        db_manager.initialize_database()

    db_connection = db_manager.get_db_connection()

    if not db_connection:
        print("Failed to connect to database. Exiting test.")
        sys.exit(1)

    try:
        agent = MarketAnalysisAgent(db_connection)

        # --- Test Competitor Analysis ---
        print("\n--- Testing Competitor Analysis (INFY.NS) ---")
        # Ensure data exists (run collector test if needed, or rely on previous run)
        competitor_report = agent.analyze_competitor(competitor_ticker="INFY.NS", region="IN", industry="Information Technology Services")
        print(competitor_report)

        # --- Test Trend Analysis ---
        print("\n--- Testing Trend Analysis (Information Technology Services, IN) ---")
        trend_report = agent.identify_market_trends(industry="Information Technology Services", region="IN")
        print(trend_report)

        # --- Test SWOT Analysis ---
        print("\n--- Testing SWOT Analysis (INFY.NS vs TCS.NS) ---")
        # Ensure TCS data exists or is collected
        agent.data_collector.collect_company_data_yahoo_finance("TCS.NS", "IN")
        swot_report = agent.perform_swot_analysis(company_ticker="INFY.NS", competitor_tickers=["TCS.NS"], region="IN")
        print(swot_report)

        # --- Test Segment Analysis (Real Estate, IN) ---
        print("\n--- Testing Segment Analysis (Real Estate, IN) ---")
        # Ensure some real estate data exists (run collector test if needed)
        agent.data_collector.collect_india_real_estate_data(city="Mumbai", limit=5) # Add some data
        segment_report = agent.analyze_market_segment(segment_name="Residential", industry="Real Estate", region="Maharashtra")
        print(segment_report)

    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        if db_connection:
            db_connection.close()
            print("\nDatabase connection closed after testing.")

