# 🕷️ Web Scraping Guide

## Complete Guide to Collecting Job Market Data

This guide explains how to use the web scraping tools to collect your own job market data.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Data Collection Methods](#data-collection-methods)
3. [Storage Options](#storage-options)
4. [Using Scraped Data](#using-scraped-data)
5. [Ethical Scraping Guidelines](#ethical-scraping)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Method 1: Generate Sample Data (Fastest - No scraping needed)

```python
from src.job_scraper import create_sample_scraped_data

# Creates 500 sample Saudi Arabian tech jobs
create_sample_scraped_data('data/raw/scraped_jobs.csv')
```

**✅ Use this when:**
- You want to test the analysis pipeline quickly
- You're learning and don't need real data yet
- Real scraping is blocked or too slow

### Method 2: Real Web Scraping

```python
from src.job_scraper import IndeedScraper, BaytScraper

# Scrape from Indeed
scraper = IndeedScraper(country='sa')  # Saudi Arabia
jobs = scraper.scrape_jobs(
    query='data scientist',
    location='riyadh',
    max_pages=5
)

# Save results
scraper.save_to_csv('indeed_jobs.csv')
scraper.save_to_database()
```

---

## 📊 Data Collection Methods

### Option 1: Indeed.com Scraper

```python
from src.job_scraper import IndeedScraper

scraper = IndeedScraper(country='sa')  # Options: 'sa', 'ae', 'uk', 'us'

# Scrape jobs
jobs = scraper.scrape_jobs(
    query='machine learning engineer',
    location='jeddah',
    max_pages=3
)

# Save to CSV
scraper.save_to_csv('indeed_ml_jobs.csv')
```

**Pros:**
- Global coverage
- Large database
- English interface

**Cons:**
- Anti-scraping measures
- May block frequent requests
- Consider using ScraperAPI for production

### Option 2: Bayt.com Scraper (Best for Saudi Arabia)

```python
from src.job_scraper import BaytScraper

scraper = BaytScraper()

# Scrape Saudi jobs
jobs = scraper.scrape_jobs(
    query='software engineer',
    location='saudi-arabia',
    max_pages=5
)

scraper.save_to_csv('bayt_jobs.csv')
```

**Pros:**
- Popular in Middle East
- Focus on Gulf region
- Arabic & English support

**Cons:**
- Regional focus (not global)
- May change HTML structure

### Option 3: Multiple Sources Combined

```python
from src.job_scraper import scrape_multiple_sources

# Automatically scrapes Indeed + Bayt + LinkedIn
all_jobs = scrape_multiple_sources()

# Results saved automatically to: data/raw/combined_jobs_[timestamp].csv
```

---

## 💾 Storage Options

### Option 1: CSV Files (Simplest)

```python
scraper.save_to_csv('my_jobs.csv')
```

**When to use:**
- Small datasets (< 10,000 jobs)
- One-time analysis
- Easy to share and open in Excel

### Option 2: JSON Files (Structured)

```python
scraper.save_to_json('my_jobs.json')
```

**When to use:**
- Complex nested data
- Need to preserve data types
- Integration with web APIs

### Option 3: SQLite Database (Recommended for large datasets)

```python
# Save to database
scraper.save_to_database('data/jobs.db')

# Later: Load and query
from src.database_manager import JobDatabase

db = JobDatabase('data/jobs.db')
df = db.get_all_jobs()  # Get all jobs as DataFrame
```

**When to use:**
- Large datasets (10,000+ jobs)
- Continuous scraping over time
- Need to query and filter efficiently
- Want to avoid duplicates

---

## 🔄 Using Scraped Data in Your Analysis

### Step 1: Collect the Data

```python
from src.job_scraper import create_sample_scraped_data

# Generate sample data (or use real scraper)
create_sample_scraped_data('data/raw/scraped_jobs.csv')
```

### Step 2: Load into Database

```python
from src.database_manager import load_csv_to_database

# Load CSV into database
db = load_csv_to_database('data/raw/scraped_jobs.csv', 'data/jobs.db')

# Check statistics
stats = db.get_statistics()
print(f"Total jobs in database: {stats['total_jobs']}")
```

### Step 3: Export for Analysis

```python
# Export clean data for Jupyter notebook
db.export_to_csv('data/raw/jobs_for_analysis.csv')
```

### Step 4: Use in Jupyter Notebook

In your notebook (`notebooks/job_market_analysis.ipynb`):

```python
# Instead of loading the default dataset, load your scraped data
df = pd.read_csv('../data/raw/jobs_for_analysis.csv')

# Or load directly from database
from src.database_manager import JobDatabase
db = JobDatabase('../data/jobs.db')
df = db.get_all_jobs()

# Continue with analysis as normal...
```

---

## 🗄️ Database Management

### Initialize Database

```python
from src.database_manager import JobDatabase

db = JobDatabase('data/jobs.db')
```

### Query Data

```python
# Get all jobs
all_jobs = db.get_all_jobs()

# Get jobs by title
data_science_jobs = db.get_jobs_by_title('data scientist')

# Get jobs by location
riyadh_jobs = db.get_jobs_by_location('riyadh')

# Get recent jobs
recent = db.get_recent_jobs(limit=50)

# Get jobs in date range
jobs = db.get_jobs_by_date_range('2024-01-01', '2024-12-31')
```

### Maintenance

```python
# Remove duplicates
db.remove_duplicates()

# Get statistics
stats = db.get_statistics()
print(stats)

# Export to CSV
db.export_to_csv('data/processed/all_jobs.csv')
```

### Merge Multiple CSV Files

```python
from src.database_manager import merge_multiple_sources

# Combine multiple scraping sessions
csv_files = [
    'data/raw/indeed_jobs.csv',
    'data/raw/bayt_jobs.csv',
    'data/raw/sample_scraped_jobs.csv'
]

merged_df = merge_multiple_sources(csv_files, 'data/raw/all_jobs_combined.csv')
```

---

## ⚖️ Ethical Scraping Guidelines

### ✅ DO:

1. **Check robots.txt**
   ```
   https://www.indeed.com/robots.txt
   https://www.bayt.com/robots.txt
   ```

2. **Add delays between requests**
   ```python
   scraper.add_delay(min_seconds=3, max_seconds=7)
   ```

3. **Use official APIs when available**
   - LinkedIn Official API
   - Indeed Publisher API
   - Consider paid services for production

4. **Respect rate limits**
   - Don't scrape aggressively
   - Spread scraping over hours/days

5. **Identify yourself**
   ```python
   headers = {
       'User-Agent': 'JobMarketResearchBot/1.0 (yourname@example.com)'
   }
   ```

6. **Store data responsibly**
   - Don't share personally identifiable information
   - Follow GDPR/data protection laws

### ❌ DON'T:

1. ❌ Overwhelm servers with rapid requests
2. ❌ Ignore robots.txt
3. ❌ Scrape sensitive personal data
4. ❌ Violate terms of service
5. ❌ Sell or redistribute scraped data
6. ❌ Use scraped data for spam or harassment

### 🔐 For Production Use

Consider these professional services:

- **ScraperAPI** - https://www.scraperapi.com
- **Bright Data** - https://brightdata.com
- **Apify** - https://apify.com
- **Oxylabs** - https://oxylabs.io

These handle:
- IP rotation
- CAPTCHA solving
- Browser automation
- Legal compliance

---

## 🐛 Troubleshooting

### Issue: "No jobs found"

**Possible causes:**
1. Website structure changed
2. Anti-scraping measures kicked in
3. Wrong URL parameters

**Solutions:**
```python
# Use sample data instead
create_sample_scraped_data()

# Or increase delays
scraper.add_delay(min_seconds=5, max_seconds=10)

# Or use different search terms
scraper.scrape_jobs(query='python developer', location='saudi arabia')
```

### Issue: "Connection timeout"

**Solutions:**
```python
import requests

# Increase timeout
response = requests.get(url, timeout=30)

# Add retry logic
from time import sleep
for attempt in range(3):
    try:
        response = requests.get(url)
        break
    except:
        sleep(10)
```

### Issue: "429 Too Many Requests"

**Solutions:**
```python
# Increase delays
scraper.add_delay(min_seconds=10, max_seconds=20)

# Reduce pages
scraper.scrape_jobs(max_pages=1)

# Come back later (rate limit resets after time)
```

### Issue: "CAPTCHA appearing"

**Solutions:**
- Use ScraperAPI or similar service
- Switch to Selenium with human-like behavior
- Use official APIs
- Generate sample data for testing

### Issue: "Database locked"

**Solutions:**
```python
# Close connection properly
import sqlite3
conn = sqlite3.connect('data/jobs.db')
# ... do work ...
conn.close()

# Or use context manager
with sqlite3.connect('data/jobs.db') as conn:
    # do work
    pass  # auto-closes
```

---

## 📝 Complete Workflow Example

Here's a complete end-to-end workflow:

```python
# 1. Import libraries
from src.job_scraper import IndeedScraper, BaytScraper, create_sample_scraped_data
from src.database_manager import JobDatabase, load_csv_to_database

# 2. Collect data (choose one method)

# Method A: Sample data (fastest)
create_sample_scraped_data('data/raw/sample_jobs.csv')

# Method B: Real scraping
scraper = IndeedScraper(country='sa')
scraper.scrape_jobs('data analyst', 'riyadh', max_pages=3)
scraper.save_to_csv('data/raw/indeed_jobs.csv')

# 3. Load into database
db = load_csv_to_database('data/raw/sample_jobs.csv')

# 4. Clean and query
db.remove_duplicates()
stats = db.get_statistics()
print(f"Total unique jobs: {stats['total_jobs']}")

# 5. Export for analysis
db.export_to_csv('data/raw/jobs_for_analysis.csv')

# 6. Use in Jupyter notebook
# Open notebooks/job_market_analysis.ipynb
# Update data path to 'data/raw/jobs_for_analysis.csv'
# Run analysis!
```

---

## 🎯 Recommended Approach for Your Project

### For Portfolio/Learning (Recommended):

```python
# Use sample data - it's fast, reliable, and perfect for demonstrations
from src.job_scraper import create_sample_scraped_data

create_sample_scraped_data('data/raw/scraped_jobs.csv')

# Then run your analysis notebook
# Shows you can work with "scraped" data structure
```

### For Real Insights:

```python
# Scrape Bayt.com (best for Saudi market, fewer anti-bot measures)
from src.job_scraper import BaytScraper

scraper = BaytScraper()
jobs = scraper.scrape_jobs('software engineer', 'saudi-arabia', max_pages=10)
scraper.save_to_database()
```

### For Production Application:

```python
# Use official APIs or paid services
# LinkedIn API: https://developer.linkedin.com
# ScraperAPI: https://www.scraperapi.com
# Indeed API: https://www.indeed.com/publisher
```

---

## 📚 Additional Resources

- **Beautiful Soup Documentation**: https://www.crummy.com/software/BeautifulSoup/
- **Requests Library**: https://requests.readthedocs.io
- **Scrapy Framework**: https://scrapy.org
- **Selenium WebDriver**: https://selenium-python.readthedocs.io
- **Web Scraping Best Practices**: https://www.scrapingbee.com/blog/web-scraping-best-practices/

---

## 🎉 Quick Commands Reference

```python
# Generate sample data
from src.job_scraper import create_sample_scraped_data
create_sample_scraped_data()

# Scrape Indeed
from src.job_scraper import IndeedScraper
scraper = IndeedScraper(country='sa')
scraper.scrape_jobs('data scientist', 'riyadh', max_pages=3)
scraper.save_to_csv('indeed_jobs.csv')

# Scrape Bayt
from src.job_scraper import BaytScraper
scraper = BaytScraper()
scraper.scrape_jobs('software engineer', 'saudi-arabia', max_pages=5)
scraper.save_to_database()

# Database management
from src.database_manager import JobDatabase
db = JobDatabase('data/jobs.db')
df = db.get_all_jobs()
stats = db.get_statistics()
db.export_to_csv('output.csv')
```

---

**Good luck with your data collection! 🚀**

