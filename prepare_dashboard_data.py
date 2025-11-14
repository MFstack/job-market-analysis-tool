"""
Prepare Data for Streamlit Dashboard

This script ensures the processed data is ready for the Streamlit dashboard.
Run this after completing the Jupyter notebook analysis.
"""

import pandas as pd
import os
from pathlib import Path


def verify_and_prepare_data():
    """Verify that required data files exist and are properly formatted"""
    
    print("="*80)
    print("DATA PREPARATION FOR STREAMLIT DASHBOARD")
    print("="*80)
    
    # Check if processed data exists
    processed_file = 'data/processed/job_market_clean.csv'
    
    if not os.path.exists(processed_file):
        print(f"\n❌ File not found: {processed_file}")
        print("\n📋 To fix this:")
        print("1. Open the Jupyter notebook: notebooks/job_market_analysis.ipynb")
        print("2. Run all cells (Kernel → Restart & Run All)")
        print("3. The notebook will automatically save the processed data")
        print("\nAlternatively, generate sample data:")
        print("   python run_scraper.py")
        return False
    
    # Load and verify the data
    print(f"\n✅ Found processed data file")
    
    try:
        df = pd.read_csv(processed_file)
        print(f"✅ Successfully loaded {len(df):,} rows")
        
        # Check required columns
        required_columns = ['job_title', 'company', 'location', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"\n⚠️ Missing columns: {', '.join(missing_columns)}")
        else:
            print(f"✅ All required columns present")
        
        # Show column info
        print(f"\n📊 Dataset Info:")
        print(f"   • Total rows: {len(df):,}")
        print(f"   • Total columns: {len(df.columns)}")
        print(f"   • Columns: {', '.join(df.columns)}")
        
        # Check for skills column
        if 'skills' in df.columns:
            print(f"\n✅ Skills column found")
            # Count non-empty skills
            non_empty_skills = df['skills'].notna().sum()
            print(f"   • Rows with skills: {non_empty_skills:,}")
        else:
            print(f"\n⚠️ Skills column not found (advanced features may not work)")
        
        # Check for nulls
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            print(f"\n📋 Missing values:")
            for col, count in null_counts[null_counts > 0].items():
                print(f"   • {col}: {count} ({count/len(df)*100:.1f}%)")
        
        # Verify top skills file
        top_skills_file = 'data/processed/top_skills.csv'
        if os.path.exists(top_skills_file):
            skills_df = pd.read_csv(top_skills_file)
            print(f"\n✅ Top skills file found ({len(skills_df)} skills)")
        else:
            print(f"\n⚠️ Top skills file not found: {top_skills_file}")
        
        print("\n" + "="*80)
        print("✅ DATA IS READY FOR STREAMLIT DASHBOARD!")
        print("="*80)
        print("\n🚀 To launch the dashboard, run:")
        print("   streamlit run streamlit_app.py")
        print("\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error loading data: {str(e)}")
        return False


def create_sample_processed_data():
    """Create sample processed data if none exists"""
    
    print("\n🔄 Creating sample processed data...")
    
    # First, check if raw data exists
    raw_file = 'data/raw/sample_scraped_jobs.csv'
    
    if not os.path.exists(raw_file):
        print("Creating sample raw data first...")
        from src.job_scraper import create_sample_scraped_data
        create_sample_scraped_data(raw_file)
    
    # Load raw data
    df = pd.read_csv(raw_file)
    
    # Basic cleaning
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()
    df_clean = df_clean.fillna('')
    
    # Add a job_title_clean column if it doesn't exist
    if 'job_title_clean' not in df_clean.columns:
        df_clean['job_title_clean'] = df_clean['job_title'].str.lower().str.strip()
    
    # Save to processed folder
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/job_market_clean.csv'
    df_clean.to_csv(output_path, index=False)
    
    print(f"✅ Created sample processed data: {output_path}")
    print(f"   • {len(df_clean):,} jobs")
    print(f"   • {len(df_clean.columns)} columns")
    
    return output_path


def main():
    """Main function"""
    
    # Create directories if they don't exist
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/raw', exist_ok=True)
    
    # Check if data exists
    success = verify_and_prepare_data()
    
    if not success:
        print("\n" + "="*80)
        choice = input("\nWould you like to create sample data? (y/n): ").strip().lower()
        
        if choice == 'y':
            create_sample_processed_data()
            print("\n")
            verify_and_prepare_data()
        else:
            print("\n👋 Run the Jupyter notebook first, then try again.\n")


if __name__ == '__main__':
    main()

