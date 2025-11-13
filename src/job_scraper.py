"""
Job Market Data Scraper
Collects job postings from multiple sources

⚠️ IMPORTANT - ETHICAL SCRAPING:
- Always check robots.txt before scraping
- Add delays between requests (respect rate limits)
- Don't overwhelm servers
- Consider using official APIs when available
- For production use, consider services like ScraperAPI or Bright Data
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
from datetime import datetime
import sqlite3
import re
from typing import List, Dict
import os


class JobScraper:
    """Base class for job scraping functionality"""
    
    def __init__(self, output_dir='data/raw'):
        self.output_dir = output_dir
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def add_delay(self, min_seconds=2, max_seconds=5):
        """Add random delay between requests to be respectful"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def save_to_csv(self, filename=None):
        """Save scraped jobs to CSV"""
        if not self.jobs:
            print("⚠️ No jobs to save!")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'scraped_jobs_{timestamp}.csv'
        
        filepath = os.path.join(self.output_dir, filename)
        df = pd.DataFrame(self.jobs)
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"✅ Saved {len(self.jobs)} jobs to {filepath}")
        return filepath
    
    def save_to_json(self, filename=None):
        """Save scraped jobs to JSON"""
        if not self.jobs:
            print("⚠️ No jobs to save!")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'scraped_jobs_{timestamp}.json'
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(self.jobs)} jobs to {filepath}")
        return filepath
    
    def save_to_database(self, db_path='data/jobs.db'):
        """Save scraped jobs to SQLite database"""
        if not self.jobs:
            print("⚠️ No jobs to save!")
            return
        
        conn = sqlite3.connect(db_path)
        df = pd.DataFrame(self.jobs)
        
        # Create table if it doesn't exist
        df.to_sql('job_postings', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()
        
        print(f"✅ Saved {len(self.jobs)} jobs to database: {db_path}")
        return db_path


class IndeedScraper(JobScraper):
    """
    Scraper for Indeed.com
    
    Note: Indeed has anti-scraping measures. For production:
    - Use Indeed's official API (requires partnership)
    - Use ScraperAPI or similar services
    - This is for educational purposes only
    """
    
    def __init__(self, country='sa', output_dir='data/raw'):
        super().__init__(output_dir)
        self.base_url = f'https://{country}.indeed.com'
    
    def scrape_jobs(self, query='data scientist', location='riyadh', max_pages=3):
        """
        Scrape jobs from Indeed
        
        Args:
            query: Job title or keywords
            location: City or region
            max_pages: Number of pages to scrape
        """
        print(f"🔍 Scraping Indeed for '{query}' in '{location}'...")
        print("⚠️ Note: This is a simplified example. Indeed has anti-bot protection.")
        
        for page in range(max_pages):
            start = page * 10
            url = f"{self.base_url}/jobs?q={query}&l={location}&start={start}"
            
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find job cards (Note: HTML structure may change)
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    if not job_cards:
                        print(f"⚠️ No jobs found on page {page + 1}")
                        break
                    
                    for card in job_cards:
                        job_data = self._parse_job_card(card)
                        if job_data:
                            self.jobs.append(job_data)
                    
                    print(f"✅ Scraped page {page + 1}: Found {len(job_cards)} jobs")
                    self.add_delay()
                else:
                    print(f"❌ Failed to fetch page {page + 1}: Status {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"❌ Error on page {page + 1}: {str(e)}")
                break
        
        print(f"\n✅ Total jobs scraped: {len(self.jobs)}")
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            # Extract job details (structure may vary)
            title_elem = card.find('h2', class_='jobTitle')
            company_elem = card.find('span', class_='companyName')
            location_elem = card.find('div', class_='companyLocation')
            description_elem = card.find('div', class_='job-snippet')
            
            job_data = {
                'job_title': self.clean_text(title_elem.text) if title_elem else '',
                'company': self.clean_text(company_elem.text) if company_elem else '',
                'location': self.clean_text(location_elem.text) if location_elem else '',
                'description': self.clean_text(description_elem.text) if description_elem else '',
                'salary': '',  # Indeed often doesn't show salary
                'experience_level': '',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Indeed',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return job_data
            
        except Exception as e:
            print(f"⚠️ Error parsing job card: {str(e)}")
            return None


class LinkedInScraper(JobScraper):
    """
    LinkedIn scraper (Educational purposes only)
    
    IMPORTANT: LinkedIn actively blocks scrapers and requires login.
    For production use:
    - Use LinkedIn's official API (requires approval)
    - Use services like Bright Data or ScraperAPI
    - Consider Selenium with authenticated sessions
    
    This is a placeholder showing the structure.
    """
    
    def scrape_jobs(self, query='data scientist', location='Saudi Arabia', max_jobs=50):
        print("⚠️ LinkedIn Scraper - Educational Example Only")
        print("LinkedIn requires authentication and actively blocks scrapers.")
        print("\nFor real LinkedIn scraping, consider:")
        print("1. LinkedIn Official API (requires partnership)")
        print("2. Bright Data or ScraperAPI services")
        print("3. Selenium with authenticated sessions")
        
        return []


class BaytScraper(JobScraper):
    """
    Scraper for Bayt.com (popular in Middle East)
    Better for Saudi Arabia job market
    """
    
    def __init__(self, output_dir='data/raw'):
        super().__init__(output_dir)
        self.base_url = 'https://www.bayt.com'
    
    def scrape_jobs(self, query='data scientist', location='saudi-arabia', max_pages=5):
        """
        Scrape jobs from Bayt.com
        
        Args:
            query: Job title or keywords
            location: Location slug (e.g., 'saudi-arabia', 'riyadh')
            max_pages: Number of pages to scrape
        """
        print(f"🔍 Scraping Bayt.com for '{query}' in '{location}'...")
        
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/en/saudi-arabia/jobs/{query.replace(' ', '-')}-jobs/?page={page}"
            
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find job listings (structure may vary)
                    job_cards = soup.find_all('li', class_='has-pointer-d')
                    
                    if not job_cards:
                        print(f"⚠️ No jobs found on page {page}")
                        break
                    
                    for card in job_cards:
                        job_data = self._parse_job_card(card)
                        if job_data:
                            self.jobs.append(job_data)
                    
                    print(f"✅ Scraped page {page}: Found {len(job_cards)} jobs")
                    self.add_delay()
                else:
                    print(f"❌ Failed to fetch page {page}: Status {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"❌ Error on page {page}: {str(e)}")
                break
        
        print(f"\n✅ Total jobs scraped: {len(self.jobs)}")
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card from Bayt"""
        try:
            job_data = {
                'job_title': '',
                'company': '',
                'location': '',
                'description': '',
                'salary': '',
                'experience_level': '',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Bayt',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Extract details (HTML structure may change)
            title_elem = card.find('h2')
            if title_elem:
                job_data['job_title'] = self.clean_text(title_elem.text)
            
            company_elem = card.find('b', class_='t-default')
            if company_elem:
                job_data['company'] = self.clean_text(company_elem.text)
            
            location_elem = card.find('span', class_='t-mute')
            if location_elem:
                job_data['location'] = self.clean_text(location_elem.text)
            
            return job_data
            
        except Exception as e:
            print(f"⚠️ Error parsing job card: {str(e)}")
            return None


def create_sample_scraped_data(output_path='data/raw/sample_scraped_jobs.csv'):
    """
    Create sample scraped data for testing
    Useful when you can't scrape real data immediately
    """
    print("🔄 Creating sample scraped job data...")
    
    jobs = []
    
    # Sample Saudi Arabian companies and job types
    companies = ['Saudi Aramco', 'SDAIA', 'STC', 'Thmanyah', 'Nana', 'Jahez', 
                 'Tamatem', 'Rewaa', 'Hungerstation', 'Noon']
    
    cities = ['Riyadh', 'Jeddah', 'Dammam', 'Khobar', 'Dhahran']
    
    job_titles = [
        'Data Scientist', 'Machine Learning Engineer', 'Data Analyst',
        'Software Engineer', 'Full Stack Developer', 'DevOps Engineer',
        'Cloud Architect', 'AI Engineer', 'Business Intelligence Analyst'
    ]
    
    descriptions = [
        'Seeking experienced professional with Python, SQL, Machine Learning, TensorFlow, AWS skills',
        'Looking for talented engineer. Required: Java, Spring Boot, Kubernetes, Docker, Microservices',
        'Join our AI team! Skills needed: Python, PyTorch, NLP, Computer Vision, Deep Learning',
        'Data role requiring SQL, Tableau, Power BI, Excel, Python, Statistical Analysis',
        'Full stack position. React, Node.js, MongoDB, JavaScript, TypeScript, REST APIs',
        'Cloud engineer needed. AWS, Azure, Terraform, Kubernetes, CI/CD, DevOps practices',
        'Senior role requiring Python, Spark, Hadoop, Kafka, ETL, Data Pipeline design',
        'Exciting opportunity! Java, Python, SQL, Agile, Git, Problem Solving required'
    ]
    
    experience_levels = ['Entry Level', 'Mid Level', 'Senior Level', 'Lead']
    
    for i in range(500):  # Generate 500 sample jobs
        job = {
            'job_title': random.choice(job_titles),
            'company': random.choice(companies),
            'location': f"{random.choice(cities)}, Saudi Arabia",
            'description': random.choice(descriptions),
            'salary': random.choice(['', '15000-25000 SAR', '20000-35000 SAR', '30000-50000 SAR']),
            'experience_level': random.choice(experience_levels),
            'posted_date': f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            'source': random.choice(['Indeed', 'Bayt', 'LinkedIn']),
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        jobs.append(job)
    
    df = pd.DataFrame(jobs)
    df.to_csv(output_path, index=False)
    print(f"✅ Created {len(jobs)} sample jobs at: {output_path}")
    return output_path


# Example usage functions
def scrape_indeed_jobs():
    """Example: Scrape from Indeed"""
    scraper = IndeedScraper(country='sa')  # Saudi Arabia
    scraper.scrape_jobs(query='data scientist', location='riyadh', max_pages=3)
    scraper.save_to_csv('indeed_jobs.csv')
    scraper.save_to_database()
    return scraper.jobs


def scrape_bayt_jobs():
    """Example: Scrape from Bayt"""
    scraper = BaytScraper()
    scraper.scrape_jobs(query='data analyst', location='saudi-arabia', max_pages=3)
    scraper.save_to_csv('bayt_jobs.csv')
    scraper.save_to_database()
    return scraper.jobs


def scrape_multiple_sources():
    """Example: Scrape from multiple sources and combine"""
    all_jobs = []
    
    # Scrape Indeed
    print("\n" + "="*80)
    print("SCRAPING INDEED")
    print("="*80)
    indeed_scraper = IndeedScraper(country='sa')
    indeed_jobs = indeed_scraper.scrape_jobs('software engineer', 'riyadh', max_pages=2)
    all_jobs.extend(indeed_jobs)
    
    # Scrape Bayt
    print("\n" + "="*80)
    print("SCRAPING BAYT")
    print("="*80)
    bayt_scraper = BaytScraper()
    bayt_jobs = bayt_scraper.scrape_jobs('data scientist', 'saudi-arabia', max_pages=2)
    all_jobs.extend(bayt_jobs)
    
    # Save combined results
    if all_jobs:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        df = pd.DataFrame(all_jobs)
        filepath = f'data/raw/combined_jobs_{timestamp}.csv'
        df.to_csv(filepath, index=False)
        print(f"\n✅ Total jobs collected: {len(all_jobs)}")
        print(f"✅ Saved to: {filepath}")
    
    return all_jobs


if __name__ == '__main__':
    print("="*80)
    print("JOB MARKET DATA SCRAPER")
    print("="*80)
    print("\n⚠️ IMPORTANT: Web scraping should be done ethically and responsibly")
    print("- Always respect robots.txt")
    print("- Add delays between requests")
    print("- Consider using official APIs when available")
    print("- This code is for educational purposes\n")
    
    # For quick testing, create sample data
    print("Creating sample data for testing...")
    create_sample_scraped_data()
    
    print("\n💡 To scrape real data, uncomment the functions below")
    print("   and ensure you comply with website terms of service:\n")
    print("   # scrape_indeed_jobs()")
    print("   # scrape_bayt_jobs()")
    print("   # scrape_multiple_sources()")

