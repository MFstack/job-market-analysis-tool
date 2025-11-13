"""
Job Market Analysis - Data Collection Module
"""

from .job_scraper import (
    JobScraper,
    IndeedScraper,
    BaytScraper,
    LinkedInScraper,
    create_sample_scraped_data,
    scrape_indeed_jobs,
    scrape_bayt_jobs,
    scrape_multiple_sources
)

from .database_manager import (
    JobDatabase,
    load_csv_to_database,
    merge_multiple_sources
)

__all__ = [
    'JobScraper',
    'IndeedScraper',
    'BaytScraper',
    'LinkedInScraper',
    'create_sample_scraped_data',
    'scrape_indeed_jobs',
    'scrape_bayt_jobs',
    'scrape_multiple_sources',
    'JobDatabase',
    'load_csv_to_database',
    'merge_multiple_sources'
]

