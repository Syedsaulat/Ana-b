"""
Business AI Agent - Business Support Module Implementation (Enhanced with Real Data)

This module implements additional business support features for the Business AI Agent,
integrating with the database for sentiment analysis, news aggregation, and reporting.
"""

import sys
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import sqlite3 # Import sqlite3 for error handling

# Add project root to path for imports
sys.path.append("/home/ubuntu")
import database_manager as db_manager
# from real_data_collector import RealDataCollector # May not be needed directly if data is in DB

# Ensure NLTK resources are available
try:
    nltk.data.find("vader_lexicon")
except LookupError:
    print("NLTK vader_lexicon not found. Attempting download...")
    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception as e:
        print(f"Failed to download NLTK data: {e}")

class BusinessSupportAgent:
    """Main class for additional business support functionalities using real data."""
    
    def __init__(self, db_conn=None):
        """Initialize the Business Support Agent with a database connection."""
        self.db_conn = db_conn if db_conn else db_manager.get_db_connection()
        if not self.db_conn:
            raise ConnectionError("Failed to establish database connection.")
            
        self.sentiment_analyzer = EnhancedSentimentAnalyzer(self.db_conn)
        self.news_aggregator = NewsAggregator(self.db_conn)
        self.scheduler = BasicScheduler() # Keep file-based for now
        self.auto_reporter = AutomatedReporter(self.db_conn)
        print("BusinessSupportAgent initialized with database connection.")
        
    def analyze_public_sentiment(self, topic, sources=["news"]):
        """Analyze public sentiment about a topic using data from the database."""
        print(f"Analyzing public sentiment for topic: {topic} from sources: {sources}")
        # Currently only supports "news" source from DB
        if "news" not in sources:
            return {"error": "Currently only supports sentiment analysis from news articles in the database."}
        return self.sentiment_analyzer.analyze_topic_sentiment_from_db(topic)
        
    def get_industry_news(self, industry, region=None, num_articles=10):
        """Aggregate recent news articles for a specific industry from the database."""
        print(f"Aggregating news for industry: {industry} (Region: {region or 'Any'})")
        return self.news_aggregator.aggregate_news_from_db(industry=industry, region=region, limit=num_articles)

    def get_company_news(self, company_id=None, company_ticker=None, num_articles=10):
        """Aggregate recent news articles for a specific company from the database."""
        if not company_id and not company_ticker:
            return {"error": "Must provide company_id or company_ticker"}
            
        _company_id = company_id
        if not _company_id and company_ticker:
            company = db_manager.get_company_by_ticker(self.db_conn, company_ticker)
            if company:
                _company_id = company["company_id"]
            else:
                return {"error": f"Company with ticker {company_ticker} not found."}
        
        print(f"Aggregating news for company ID: {_company_id}")
        return self.news_aggregator.aggregate_news_from_db(company_id=_company_id, limit=num_articles)
        
    def set_reminder(self, task, due_date, notes=""):
        """Set a reminder for a specific task (logs it to file)."""
        print(f"Setting reminder for task: {task}")
        return self.scheduler.add_reminder(task, due_date, notes)
        
    def view_reminders(self, limit=10):
         """View recent reminders from the log file."""
         return self.scheduler.view_reminders(limit=limit)
         
    def generate_automated_report(self, report_type="weekly_summary", company_id=None, company_ticker=None, competitor_tickers=None, region="IN"):
        """Generate an automated summary report using data from the database."""
        print(f"Generating automated report: {report_type}")
        
        _company_id = company_id
        if not _company_id and company_ticker:
            company = db_manager.get_company_by_ticker(self.db_conn, company_ticker)
            if company:
                _company_id = company["company_id"]
            else:
                return {"error": f"Company with ticker {company_ticker} not found for report generation."}
        elif not _company_id:
             return {"error": "Must provide company_id or company_ticker for the main company."}
             
        competitor_ids = []
        if competitor_tickers:
            for ticker in competitor_tickers:
                comp = db_manager.get_company_by_ticker(self.db_conn, ticker)
                if comp:
                    competitor_ids.append(comp["company_id"])
                else:
                    print(f"Warning: Competitor ticker {ticker} not found in DB for report.")
                    
        return self.auto_reporter.generate_summary_report(
            report_type=report_type, 
            company_id=_company_id, 
            competitor_ids=competitor_ids, 
            region=region
        )

class EnhancedSentimentAnalyzer:
    """Component for performing sentiment analysis on text data from the database."""
    
    def __init__(self, db_conn):
        """Initialize the sentiment analyzer with DB connection."""
        self.db_conn = db_conn
        try:
            self.sia = SentimentIntensityAnalyzer()
        except Exception as e:
            print(f"Error initializing SentimentIntensityAnalyzer: {e}")
            self.sia = None
            
    def analyze_text_sentiment(self, text):
        """Analyze the sentiment of a single piece of text."""
        # ... (Keep the same implementation as before) ...
        if not self.sia:
            return {"error": "Sentiment analyzer not initialized."}
        if not text or not isinstance(text, str):
            # Return neutral for empty text instead of error
            return {"compound": 0.0, "neg": 0.0, "neu": 1.0, "pos": 0.0, "label": "neutral"}
            
        try:
            scores = self.sia.polarity_scores(text)
            if scores["compound"] >= 0.05:
                scores["label"] = "positive"
            elif scores["compound"] <= -0.05:
                scores["label"] = "negative"
            else:
                scores["label"] = "neutral"
            return scores
        except Exception as e:
            print(f"Error during sentiment analysis: {e}")
            return {"error": f"Sentiment analysis failed: {e}"}

    def analyze_multiple_texts(self, texts_with_meta):
        """Analyze sentiment for a list of texts (dicts with summary/text) and return aggregated results."""
        # ... (Keep the same implementation as before, ensure input format matches) ...
        if not self.sia:
            return {"error": "Sentiment analyzer not initialized."}
        if not texts_with_meta or not isinstance(texts_with_meta, list):
             return {"error": "Input must be a list of text dictionaries."}
             
        results = []
        for item in texts_with_meta:
            text_to_analyze = item.get("summary", item.get("text", "")) # Adapt to news/social structure
            sentiment = self.analyze_text_sentiment(text_to_analyze)
            results.append({"data": item, "sentiment": sentiment})
            
        overall_sentiment = {"positive": 0, "negative": 0, "neutral": 0, "compound_sum": 0.0}
        valid_analyses = 0
        for res in results:
            if "label" in res["sentiment"]:
                overall_sentiment[res["sentiment"]["label"]] += 1
                overall_sentiment["compound_sum"] += res["sentiment"]["compound"]
                valid_analyses += 1
                
        average_compound = (overall_sentiment["compound_sum"] / valid_analyses) if valid_analyses > 0 else 0
        
        return {
            "individual_results": results,
            "aggregate_summary": {
                "total_analyzed": len(texts_with_meta),
                "positive_count": overall_sentiment["positive"],
                "negative_count": overall_sentiment["negative"],
                "neutral_count": overall_sentiment["neutral"],
                "average_compound_score": round(average_compound, 3)
            }
        }

    def analyze_topic_sentiment_from_db(self, topic, limit=50):
        """Fetch news data from DB related to the topic and analyze sentiment."""
        print(f"Fetching news from DB for sentiment analysis on topic: {topic}")
        if not self.db_conn:
            return {"error": "Database connection not available."}
            
        cursor = self.db_conn.cursor()
        articles = []
        try:
            # Search for topic in title, summary, or as company name/ticker
            # This is a basic search, could be improved with full-text search if using PostgreSQL etc.
            cursor.execute("""
                SELECT article_id, title, summary, published_date, source_name, source_url 
                FROM news_articles 
                WHERE company_id = (SELECT company_id FROM companies WHERE name LIKE ? OR ticker_symbol LIKE ?) 
                   OR title LIKE ? 
                   OR summary LIKE ? 
                   OR topic LIKE ?
                ORDER BY published_date DESC
                LIMIT ?
            """, (f"%{topic}%", f"%{topic}%", f"%{topic}%", f"%{topic}%", f"%{topic}%", limit))
            results = cursor.fetchall()
            articles = [dict(row) for row in results]
            print(f"Found {len(articles)} articles related to {topic} in DB.")
        except sqlite3.Error as e:
            print(f"Database error fetching news for sentiment analysis: {e}")
            return {"error": f"Database error: {e}"}
        finally:
            if cursor:
                cursor.close()
                
        if not articles:
            return {"error": f"No news articles found in the database for topic: {topic}"}
            
        # Analyze sentiment of the collected articles
        return self.analyze_multiple_texts(articles)

class NewsAggregator:
    """Component for aggregating news articles from the database."""
    
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def aggregate_news_from_db(self, industry=None, company_id=None, region=None, limit=10):
        """Fetch and aggregate news articles from the database based on criteria."""
        print(f"Aggregating news from DB (Industry: {industry}, CompanyID: {company_id}, Region: {region}, Limit: {limit})")
        if not self.db_conn:
            return {"error": "Database connection not available."}
            
        cursor = self.db_conn.cursor()
        articles = []
        query_parts = []
        params = []
        
        sql = "SELECT article_id, title, summary, published_date, source_name, source_url, sentiment_score, sentiment_label FROM news_articles WHERE 1=1"
        
        if company_id:
            sql += " AND company_id = ?"
            params.append(company_id)
        elif industry: # Only use industry if company_id is not specified
            sql += " AND industry = ?"
            params.append(industry)
            # Optionally filter by region if industry is specified
            # if region:
            #    sql += " AND company_id IN (SELECT company_id FROM companies WHERE region = ?)" # Less efficient
            #    params.append(region)

        sql += " ORDER BY published_date DESC LIMIT ?"
        params.append(limit)
        
        try:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            articles = [dict(row) for row in results]
            print(f"Found {len(articles)} articles matching criteria.")
        except sqlite3.Error as e:
            print(f"Database error aggregating news: {e}")
            return {"error": f"Database error: {e}"}
        finally:
            if cursor:
                cursor.close()
                
        return {
            "query": {"industry": industry, "company_id": company_id, "region": region},
            "aggregated_at": datetime.now().isoformat(),
            "articles": articles
        }

class BasicScheduler:
    """Component for logging reminders (simulated scheduling - kept file-based)."""
    # ... (Keep the same implementation as before) ...
    def __init__(self, reminder_file=None):
        # Use a platform-independent path for the reminder file
        if reminder_file is None:
            self.reminder_file = os.path.join(os.path.dirname(__file__), "reminders.log")
        else:
            self.reminder_file = reminder_file
            
    def add_reminder(self, task, due_date_str, notes=""):
        try:
            due_date = datetime.fromisoformat(due_date_str)
            log_entry = f"{datetime.now().isoformat()} | DUE: {due_date.isoformat()} | TASK: {task} | NOTES: {notes}\n"
            with open(self.reminder_file, "a") as f:
                f.write(log_entry)
            print(f"Reminder logged to {self.reminder_file}")
            return {"status": "success", "message": f"Reminder for {task} logged.", "log_entry": log_entry.strip()}
        except ValueError:
            print(f"Error: Invalid due date format. Please use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).")
            # Try parsing date only
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                log_entry = f"{datetime.now().isoformat()} | DUE: {due_date.isoformat()} | TASK: {task} | NOTES: {notes}\n"
                with open(self.reminder_file, "a") as f:
                    f.write(log_entry)
                print(f"Reminder logged to {self.reminder_file}")
                return {"status": "success", "message": f"Reminder for {task} logged.", "log_entry": log_entry.strip()}
            except ValueError:
                 return {"status": "error", "message": "Invalid due date format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS."}
        except Exception as e:
            print(f"Error logging reminder: {e}")
            return {"status": "error", "message": f"Failed to log reminder: {e}"}

    def view_reminders(self, limit=10):
        try:
            if not os.path.exists(self.reminder_file):
                return {"status": "success", "reminders": [], "message": "No reminders logged yet."}
            with open(self.reminder_file, "r") as f:
                lines = f.readlines()
            recent_reminders = [line.strip() for line in lines[-limit:]]
            recent_reminders.reverse()
            return {"status": "success", "reminders": recent_reminders}
        except Exception as e:
            print(f"Error reading reminders: {e}")
            return {"status": "error", "message": f"Failed to read reminders: {e}"}

class AutomatedReporter:
    """Component for generating automated summary reports using database data."""
    
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def generate_summary_report(self, report_type, company_id, competitor_ids=None, region="IN"):
        """Generate a summary report using data queried from the database."""
        print(f"Generating {report_type} for company ID: {company_id}")
        if not self.db_conn:
            return {"error": "Database connection not available."}
            
        cursor = self.db_conn.cursor()
        report = {
            "title": f"{report_type.replace('_', ' ').title()} Report",
            "generated_at": datetime.now().isoformat(),
            "report_period": f"Data up to {datetime.now().date().isoformat()}",
            "sections": []
        }
        company_name = "Unknown Company"
        company_industry = None
        
        try:
            # Get main company info
            cursor.execute("SELECT name, industry FROM companies WHERE company_id = ?", (company_id,))
            company_info = cursor.fetchone()
            if company_info:
                company_name = company_info["name"]
                company_industry = company_info["industry"]
                report["title"] += f" for {company_name}"
            else:
                print(f"Warning: Company ID {company_id} not found for report generation.")
                return {"error": f"Company ID {company_id} not found."}

            # --- Market Summary Section ---
            market_summary = {"key_trends": [], "overall_sentiment": "N/A", "sentiment_article_count": 0}
            if company_industry:
                # Get recent trends for the industry
                cursor.execute("""
                    SELECT trend_description, sentiment_score FROM market_trends 
                    WHERE industry = ? AND region = ? AND published_date >= date("now", "-7 days")
                    ORDER BY published_date DESC LIMIT 3
                """, (company_industry, region))
                trends = cursor.fetchall()
                market_summary["key_trends"] = [f"{row['trend_description']} (Sentiment: {row['sentiment_score']:.2f})" for row in trends]
                
                # Get recent industry sentiment from news
                cursor.execute("""
                    SELECT AVG(sentiment_score) as avg_sent, COUNT(*) as count 
                    FROM news_articles 
                    WHERE industry = ? AND published_date >= date("now", "-7 days")
                """, (company_industry,))
                industry_sentiment = cursor.fetchone()
                if industry_sentiment and industry_sentiment["count"] > 0:
                    market_summary["overall_sentiment"] = f"{industry_sentiment['avg_sent']:.2f}"
                    market_summary["sentiment_article_count"] = industry_sentiment["count"]
            report["sections"].append({"title": "Market Summary (Last 7 Days)", "content": market_summary})

            # --- Competitor Activity Section ---
            if competitor_ids:
                comp_activity = []
                placeholders = ",".join(["?"] * len(competitor_ids))
                # Get recent news headlines for competitors
                cursor.execute(f"""
                    SELECT c.name, na.title, na.sentiment_label 
                    FROM news_articles na JOIN companies c ON na.company_id = c.company_id
                    WHERE na.company_id IN ({placeholders}) AND na.published_date >= date("now", "-7 days")
                    ORDER BY c.name, na.published_date DESC
                """, competitor_ids)
                comp_news = cursor.fetchall()
                # Simple summary
                current_comp = ""
                news_count = 0
                for row in comp_news:
                    if row["name"] != current_comp:
                        if current_comp: comp_activity.append(f"{current_comp}: {news_count} recent news articles found.")
                        current_comp = row["name"]
                        news_count = 0
                    news_count += 1
                if current_comp: comp_activity.append(f"{current_comp}: {news_count} recent news articles found.")
                
                if not comp_activity:
                    comp_activity.append("No significant competitor news found in the last 7 days.")
                    
                report["sections"].append({"title": "Competitor Activity (Last 7 Days)", "content": {"summary": comp_activity}})

            # --- Lead Generation Summary Section ---
            lead_summary = {"new_qualified_leads": 0, "top_lead_source": "N/A", "average_lead_score": 0.0}
            # Get leads qualified in the last 7 days for any ICP
            cursor.execute("""
                SELECT COUNT(*) as count, AVG(score) as avg_score, source 
                FROM leads 
                WHERE qualification_status = 'Qualified' AND collected_date >= date('now', '-7 days')
                GROUP BY source ORDER BY count DESC LIMIT 1
            """,)
            recent_leads = cursor.fetchone()
            if recent_leads:
                 # Need total count separately
                 cursor.execute("SELECT COUNT(*) FROM leads WHERE qualification_status = 'Qualified' AND collected_date >= date('now', '-7 days')")
                 total_count = cursor.fetchone()[0]
                 lead_summary["new_qualified_leads"] = total_count
                 lead_summary["top_lead_source"] = recent_leads["source"]
                 # Avg score needs to be calculated across all recent qualified leads
                 cursor.execute("SELECT AVG(score) FROM leads WHERE qualification_status = 'Qualified' AND collected_date >= date('now', '-7 days')")
                 avg_score_res = cursor.fetchone()
                 if avg_score_res and avg_score_res[0] is not None:
                     lead_summary["average_lead_score"] = round(avg_score_res[0], 2)
                     
            report["sections"].append({"title": "Lead Generation Summary (Last 7 Days)", "content": lead_summary})

            # --- Action Items Section (Placeholder) ---
            action_items = {"items": [
                "Review market trends and sentiment.",
                "Check competitor news for strategic insights.",
                "Follow up on newly qualified leads."
            ]}
            report["sections"].append({"title": "Suggested Action Items", "content": action_items})

        except sqlite3.Error as e:
            print(f"Database error during report generation: {e}")
            report["error"] = str(e)
        finally:
            if cursor:
                cursor.close()
                
        return report

# Example usage (Updated)
if __name__ == "__main__":
    print("Testing Business Support Agent with Real Data Integration...")
    
    # Ensure database exists and is initialized
    if not os.path.exists(db_manager.DATABASE_NAME):
        print("Database file not found. Initializing...")
        db_manager.initialize_database()
    
    db_connection = db_manager.get_db_connection()
    
    if not db_connection:
        print("Failed to connect to database. Exiting test.")
        sys.exit(1)
        
    try:
        agent = BusinessSupportAgent(db_connection)
        
        # --- Add Test Data (News) ---
        # Ensure some news exists for testing sentiment and aggregation
        # Find a company ID for testing (e.g., INFY.NS)
        infy_comp = db_manager.get_company_by_ticker(db_connection, "INFY.NS")
        infy_id = infy_comp["company_id"] if infy_comp else None
        if infy_id:
            db_manager.add_news_article(db_connection, {
                "company_id": infy_id,
                "industry": "Information Technology Services",
                "title": "Infosys Reports Strong Growth",
                "source_name": "Test News Source",
                "source_url": "http://test.com/infy-growth",
                "published_date": datetime.now() - timedelta(days=1),
                "summary": "Infosys announced strong quarterly growth, exceeding expectations.",
                "sentiment_score": 0.7, "sentiment_label": "positive"
            })
            db_manager.add_news_article(db_connection, {
                "company_id": infy_id,
                "industry": "Information Technology Services",
                "title": "Infosys Faces New Challenges",
                "source_name": "Test News Source 2",
                "source_url": "http://test.com/infy-challenge",
                "published_date": datetime.now() - timedelta(days=2),
                "summary": "Despite growth, Infosys faces challenges in the European market.",
                "sentiment_score": -0.3, "sentiment_label": "negative"
            })
        else:
            print("Warning: INFY.NS not found, cannot add test news.")
            
        # --- Test Sentiment Analysis ---
        print("\n--- Testing Sentiment Analysis (Infosys) ---")
        sentiment_report = agent.analyze_public_sentiment(topic="Infosys")
        if "aggregate_summary" in sentiment_report:
            print(json.dumps(sentiment_report["aggregate_summary"], indent=2))
        else:
            print(sentiment_report)
            
        # --- Test News Aggregation (Industry) ---
        print("\n--- Testing News Aggregation (Information Technology Services) ---")
        news_report = agent.get_industry_news(industry="Information Technology Services", num_articles=5)
        if "articles" in news_report:
            print(f"Found {len(news_report['articles'])} articles:")
            for article in news_report["articles"]:
                print(f"- {article['title']} ({article['source_name']}) - Sent: {article.get('sentiment_label', 'N/A')}")
        else:
            print(news_report)
            
        # --- Test News Aggregation (Company) ---
        if infy_id:
            print("\n--- Testing News Aggregation (INFY.NS) ---")
            comp_news_report = agent.get_company_news(company_id=infy_id, num_articles=5)
            if "articles" in comp_news_report:
                print(f"Found {len(comp_news_report['articles'])} articles:")
                for article in comp_news_report["articles"]:
                    print(f"- {article['title']} ({article['source_name']}) - Sent: {article.get('sentiment_label', 'N/A')}")
            else:
                print(comp_news_report)

        # --- Test Reminder ---
        print("\n--- Testing Reminders ---")
        reminder_result = agent.set_reminder(
            task="Prepare Weekly Report", 
            due_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), # Use YYYY-MM-DD format
            notes="Include market sentiment data"
        )
        print(json.dumps(reminder_result, indent=2))
        reminders_view = agent.view_reminders(limit=5)
        print("Recent Reminders:")
        print(json.dumps(reminders_view, indent=2))
        
        # --- Test Automated Report ---
        if infy_id:
            print("\n--- Testing Automated Report (INFY.NS) ---")
            # Find competitor ID (e.g., TCS.NS)
            tcs_comp = db_manager.get_company_by_ticker(db_connection, "TCS.NS")
            tcs_id = tcs_comp["company_id"] if tcs_comp else None
            competitor_ids_for_report = [tcs_id] if tcs_id else []
            
            auto_report = agent.generate_automated_report(
                report_type="weekly_summary", 
                company_id=infy_id, 
                competitor_ids=competitor_ids_for_report, 
                region="IN"
            )
            if "error" in auto_report:
                print(f"Error generating report: {auto_report['error']}")
            else:
                print(f"Title: {auto_report['title']}")
                print(f"Generated: {auto_report['generated_at']}")
                for section in auto_report["sections"]:
                    print(f"\n## {section['title']}")
                    print(json.dumps(section["content"], indent=2))
                # Optionally save
                # report_filename = f"/home/ubuntu/{auto_report['title'].replace(' ', '_')}.json"
                # with open(report_filename, "w") as f:
                #     json.dump(auto_report, f, indent=2)
                # print(f"\nFull report saved to {report_filename}")
        else:
            print("\nSkipping automated report test as INFY.NS ID not found.")

    except Exception as e:
        print(f"An error occurred during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if db_connection:
            db_connection.close()
            print("\nDatabase connection closed after testing.")

