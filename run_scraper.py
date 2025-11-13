"""
Quick Start Script for Job Market Data Collection

Run this script to collect job data for your analysis.
"""

import sys
from src.job_scraper import create_sample_scraped_data, IndeedScraper, BaytScraper
from src.database_manager import JobDatabase, load_csv_to_database


def main_menu():
    """Display main menu and handle user choice"""
    
    print("\n" + "="*80)
    print(" JOB MARKET DATA COLLECTION TOOL")
    print("="*80)
    print("\nChoose a data collection method:\n")
    print("1. Generate Sample Data (Fast & Recommended for testing)")
    print("2. Scrape Indeed.com (Real data, may be slow/blocked)")
    print("3. Scrape Bayt.com (Best for Saudi Arabia)")
    print("4. View Database Statistics")
    print("5. Exit")
    print("\n" + "="*80)
    
    choice = input("\nEnter your choice (1-5): ").strip()
    return choice


def generate_sample_data():
    """Generate sample data for testing"""
    print("\n" + "="*80)
    print("GENERATING SAMPLE DATA")
    print("="*80)
    
    num_jobs = input("\nHow many sample jobs? (default: 500): ").strip()
    num_jobs = int(num_jobs) if num_jobs.isdigit() else 500
    
    # Generate the data
    from src.job_scraper import pd, random, datetime
    
    companies = ['Saudi Aramco', 'SDAIA', 'STC', 'Thmanyah', 'Nana', 'Jahez', 
                 'Tamatem', 'Rewaa', 'Hungerstation', 'Noon', 'Mrsool', 'Seez']
    
    cities = ['Riyadh', 'Jeddah', 'Dammam', 'Khobar', 'Dhahran', 'Mecca', 'Medina']
    
    job_titles = [
        'Data Scientist', 'Machine Learning Engineer', 'Data Analyst',
        'Software Engineer', 'Full Stack Developer', 'DevOps Engineer',
        'Cloud Architect', 'AI Engineer', 'Business Intelligence Analyst',
        'Backend Developer', 'Frontend Developer', 'Data Engineer'
    ]
    
    descriptions = [
        'Seeking experienced professional with Python, SQL, Machine Learning, TensorFlow, AWS, Data Analysis skills',
        'Looking for talented engineer. Required: Java, Spring Boot, Kubernetes, Docker, Microservices, CI/CD',
        'Join our AI team! Skills needed: Python, PyTorch, NLP, Computer Vision, Deep Learning, TensorFlow',
        'Data role requiring SQL, Tableau, Power BI, Excel, Python, Statistical Analysis, Data Visualization',
        'Full stack position. React, Node.js, MongoDB, JavaScript, TypeScript, REST APIs, GraphQL',
        'Cloud engineer needed. AWS, Azure, Terraform, Kubernetes, CI/CD, DevOps, Docker practices',
        'Senior role requiring Python, Spark, Hadoop, Kafka, ETL, Data Pipeline, Airflow design',
        'Exciting opportunity! Java, Python, SQL, Agile, Git, Problem Solving, Spring Boot required',
        'ML Engineer position: Python, scikit-learn, TensorFlow, Keras, PyTorch, MLOps, AWS needed',
        'Backend developer: Node.js, Python, Django, Flask, PostgreSQL, Redis, API design'
    ]
    
    experience_levels = ['Entry Level', 'Mid Level', 'Senior Level', 'Lead']
    
    jobs = []
    for i in range(num_jobs):
        job = {
            'job_title': random.choice(job_titles),
            'company': random.choice(companies),
            'location': f"{random.choice(cities)}, Saudi Arabia",
            'description': random.choice(descriptions),
            'salary': random.choice(['', '15000-25000 SAR', '20000-35000 SAR', '30000-50000 SAR', '40000-60000 SAR']),
            'experience_level': random.choice(experience_levels),
            'posted_date': f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            'source': 'Sample Data',
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        jobs.append(job)
    
    # Save to CSV
    df = pd.DataFrame(jobs)
    filepath = 'data/raw/sample_scraped_jobs.csv'
    df.to_csv(filepath, index=False)
    
    print(f"\n✅ Generated {len(jobs)} sample jobs")
    print(f"✅ Saved to: {filepath}")
    
    # Ask if user wants to load into database
    load_db = input("\nLoad into database? (y/n): ").strip().lower()
    if load_db == 'y':
        db = load_csv_to_database(filepath, 'data/jobs.db')
        print("✅ Data loaded into database!")
    
    return filepath


def scrape_indeed():
    """Scrape from Indeed"""
    print("\n" + "="*80)
    print("SCRAPING INDEED.COM")
    print("="*80)
    print("\n⚠️ Note: Indeed may block scraping. Use sample data for testing.")
    
    proceed = input("\nContinue? (y/n): ").strip().lower()
    if proceed != 'y':
        return
    
    query = input("Job search query (e.g., 'data scientist'): ").strip() or 'software engineer'
    location = input("Location (e.g., 'riyadh'): ").strip() or 'riyadh'
    pages = input("Number of pages to scrape (1-10): ").strip()
    pages = int(pages) if pages.isdigit() and 1 <= int(pages) <= 10 else 3
    
    print(f"\n🔍 Searching for '{query}' in '{location}'...")
    
    scraper = IndeedScraper(country='sa')
    jobs = scraper.scrape_jobs(query=query, location=location, max_pages=pages)
    
    if jobs:
        scraper.save_to_csv(f'indeed_{query.replace(" ", "_")}_jobs.csv')
        
        load_db = input("\nLoad into database? (y/n): ").strip().lower()
        if load_db == 'y':
            scraper.save_to_database('data/jobs.db')
            print("✅ Data loaded into database!")
    else:
        print("\n⚠️ No jobs found. Consider using sample data instead.")


def scrape_bayt():
    """Scrape from Bayt"""
    print("\n" + "="*80)
    print("SCRAPING BAYT.COM")
    print("="*80)
    
    query = input("Job search query (e.g., 'data analyst'): ").strip() or 'software engineer'
    location = input("Location ('saudi-arabia', 'riyadh', etc.): ").strip() or 'saudi-arabia'
    pages = input("Number of pages to scrape (1-10): ").strip()
    pages = int(pages) if pages.isdigit() and 1 <= int(pages) <= 10 else 3
    
    print(f"\n🔍 Searching for '{query}' in '{location}'...")
    
    scraper = BaytScraper()
    jobs = scraper.scrape_jobs(query=query, location=location, max_pages=pages)
    
    if jobs:
        scraper.save_to_csv(f'bayt_{query.replace(" ", "_")}_jobs.csv')
        
        load_db = input("\nLoad into database? (y/n): ").strip().lower()
        if load_db == 'y':
            scraper.save_to_database('data/jobs.db')
            print("✅ Data loaded into database!")
    else:
        print("\n⚠️ No jobs found. Try different search terms.")


def show_database_stats():
    """Display database statistics"""
    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80)
    
    try:
        db = JobDatabase('data/jobs.db')
        stats = db.get_statistics()
        
        print(f"\n📊 Total Jobs: {stats['total_jobs']}")
        
        if stats['total_jobs'] > 0:
            print(f"\n📈 Jobs by Source:")
            for item in stats.get('jobs_by_source', []):
                print(f"   • {item['source']}: {item['count']}")
            
            print(f"\n🌍 Top Locations:")
            for item in stats.get('top_locations', [])[:10]:
                print(f"   • {item['location']}: {item['count']}")
            
            if stats.get('date_range'):
                print(f"\n📅 Date Range:")
                print(f"   • Earliest: {stats['date_range']['earliest']}")
                print(f"   • Latest: {stats['date_range']['latest']}")
            
            # Offer to export
            export = input("\n💾 Export to CSV? (y/n): ").strip().lower()
            if export == 'y':
                output_path = db.export_to_csv('data/processed/database_export.csv')
                print(f"✅ Exported to: {output_path}")
        else:
            print("\n⚠️ Database is empty. Collect some data first!")
    
    except Exception as e:
        print(f"\n❌ Error accessing database: {str(e)}")


def main():
    """Main function"""
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            generate_sample_data()
        elif choice == '2':
            scrape_indeed()
        elif choice == '3':
            scrape_bayt()
        elif choice == '4':
            show_database_stats()
        elif choice == '5':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n⚠️ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

