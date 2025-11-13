"""
Database Manager for Job Market Analysis
Handles storage and retrieval of scraped job data
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os


class JobDatabase:
    """Manage job postings in SQLite database"""
    
    def __init__(self, db_path='data/jobs.db'):
        self.db_path = db_path
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create job_postings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_postings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                description TEXT,
                salary TEXT,
                experience_level TEXT,
                posted_date TEXT,
                source TEXT,
                scraped_at TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_job_title 
            ON job_postings(job_title)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_location 
            ON job_postings(location)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_posted_date 
            ON job_postings(posted_date)
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database initialized: {self.db_path}")
    
    def insert_jobs(self, jobs_df):
        """
        Insert job postings from DataFrame
        
        Args:
            jobs_df: pandas DataFrame with job data
        """
        conn = sqlite3.connect(self.db_path)
        jobs_df.to_sql('job_postings', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()
        
        print(f"✅ Inserted {len(jobs_df)} jobs into database")
    
    def get_all_jobs(self):
        """Retrieve all jobs from database"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM job_postings', conn)
        conn.close()
        return df
    
    def get_jobs_by_title(self, job_title):
        """Get jobs matching a specific title"""
        conn = sqlite3.connect(self.db_path)
        query = 'SELECT * FROM job_postings WHERE job_title LIKE ?'
        df = pd.read_sql_query(query, conn, params=(f'%{job_title}%',))
        conn.close()
        return df
    
    def get_jobs_by_location(self, location):
        """Get jobs in a specific location"""
        conn = sqlite3.connect(self.db_path)
        query = 'SELECT * FROM job_postings WHERE location LIKE ?'
        df = pd.read_sql_query(query, conn, params=(f'%{location}%',))
        conn.close()
        return df
    
    def get_jobs_by_date_range(self, start_date, end_date):
        """Get jobs posted within a date range"""
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT * FROM job_postings 
            WHERE posted_date BETWEEN ? AND ?
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df
    
    def get_recent_jobs(self, limit=100):
        """Get most recently scraped jobs"""
        conn = sqlite3.connect(self.db_path)
        query = f'''
            SELECT * FROM job_postings 
            ORDER BY scraped_at DESC 
            LIMIT {limit}
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def remove_duplicates(self):
        """Remove duplicate job postings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Keep only the first occurrence of each unique job
        cursor.execute('''
            DELETE FROM job_postings 
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM job_postings 
                GROUP BY job_title, company, location
            )
        ''')
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"✅ Removed {deleted} duplicate jobs")
        return deleted
    
    def get_statistics(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        
        stats = {}
        
        # Total jobs
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM job_postings')
        stats['total_jobs'] = cursor.fetchone()[0]
        
        # Jobs by source
        df = pd.read_sql_query('''
            SELECT source, COUNT(*) as count 
            FROM job_postings 
            GROUP BY source
        ''', conn)
        stats['jobs_by_source'] = df.to_dict('records')
        
        # Jobs by location
        df = pd.read_sql_query('''
            SELECT location, COUNT(*) as count 
            FROM job_postings 
            GROUP BY location 
            ORDER BY count DESC 
            LIMIT 10
        ''', conn)
        stats['top_locations'] = df.to_dict('records')
        
        # Date range
        cursor.execute('''
            SELECT MIN(posted_date), MAX(posted_date) 
            FROM job_postings
        ''')
        min_date, max_date = cursor.fetchone()
        stats['date_range'] = {'earliest': min_date, 'latest': max_date}
        
        conn.close()
        return stats
    
    def export_to_csv(self, output_path='data/processed/database_export.csv'):
        """Export entire database to CSV"""
        df = self.get_all_jobs()
        df.to_csv(output_path, index=False)
        print(f"✅ Exported {len(df)} jobs to {output_path}")
        return output_path
    
    def clear_database(self):
        """Clear all data from database (use with caution!)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM job_postings')
        conn.commit()
        conn.close()
        
        print("⚠️ Database cleared!")


def load_csv_to_database(csv_path, db_path='data/jobs.db'):
    """
    Load jobs from CSV file into database
    
    Args:
        csv_path: Path to CSV file with job data
        db_path: Path to SQLite database
    """
    print(f"📥 Loading data from {csv_path}...")
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Initialize database
    db = JobDatabase(db_path)
    
    # Insert jobs
    db.insert_jobs(df)
    
    print(f"✅ Successfully loaded {len(df)} jobs into database")
    return db


def merge_multiple_sources(csv_files, output_path='data/raw/merged_jobs.csv'):
    """
    Merge multiple CSV files into one
    
    Args:
        csv_files: List of CSV file paths
        output_path: Where to save merged data
    """
    all_dfs = []
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            all_dfs.append(df)
            print(f"✅ Loaded {len(df)} jobs from {csv_file}")
        else:
            print(f"⚠️ File not found: {csv_file}")
    
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        
        # Remove duplicates
        initial_count = len(merged_df)
        merged_df = merged_df.drop_duplicates(subset=['job_title', 'company', 'location'])
        removed = initial_count - len(merged_df)
        
        # Save
        merged_df.to_csv(output_path, index=False)
        
        print(f"\n✅ Merged {len(all_dfs)} files")
        print(f"✅ Total jobs: {len(merged_df)}")
        print(f"✅ Duplicates removed: {removed}")
        print(f"✅ Saved to: {output_path}")
        
        return merged_df
    else:
        print("❌ No data to merge")
        return None


if __name__ == '__main__':
    print("="*80)
    print("DATABASE MANAGER - Testing")
    print("="*80)
    
    # Initialize database
    db = JobDatabase('data/jobs.db')
    
    # Show statistics
    print("\n📊 Database Statistics:")
    stats = db.get_statistics()
    print(f"Total Jobs: {stats['total_jobs']}")
    
    if stats['total_jobs'] > 0:
        print(f"\nJobs by Source:")
        for item in stats['jobs_by_source']:
            print(f"  • {item['source']}: {item['count']}")
        
        print(f"\nTop Locations:")
        for item in stats['top_locations'][:5]:
            print(f"  • {item['location']}: {item['count']}")
        
        print(f"\nDate Range:")
        print(f"  • Earliest: {stats['date_range']['earliest']}")
        print(f"  • Latest: {stats['date_range']['latest']}")
    else:
        print("\n⚠️ Database is empty. Run the scraper first!")

