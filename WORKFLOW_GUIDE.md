# 🔄 Complete Workflow Guide

## From Data Collection to Dashboard in 3 Steps

This guide shows you the complete workflow from collecting data to viewing it in an interactive dashboard.

---

## 📋 Quick Summary

1. **Collect Data** → Run `python run_scraper.py` OR use Kaggle dataset
2. **Analyze Data** → Run Jupyter notebook cells
3. **View Dashboard** → Run `streamlit run streamlit_app.py`

---

## 🎯 Method 1: Quick Start (Sample Data - Fastest!)

### Step 1: Generate Sample Data (5 seconds)

```bash
python run_scraper.py
```

- Select **Option 1** (Generate Sample Data)
- Creates 500 sample Saudi tech jobs
- Output: `data/raw/sample_scraped_jobs.csv`

### Step 2: Run Analysis (2-3 minutes)

```bash
jupyter notebook
```

- Open `notebooks/job_market_analysis.ipynb`
- Click: `Kernel` → `Restart & Run All`
- Wait for all cells to execute
- Output files:
  - `data/processed/job_market_clean.csv` ← Main dataset
  - `data/processed/top_skills.csv` ← Top skills
  - `data/processed/analysis_summary.csv` ← Summary stats
  - 10 visualization PNG files in `visualizations/`

### Step 3: Launch Dashboard (instant)

```bash
streamlit run streamlit_app.py
```

- Opens automatically in your browser
- Explore interactive visualizations
- Filter by location, job title, experience level
- Download filtered data

**✅ Done! Total time: ~3-5 minutes**

---

## 🎯 Method 2: Real Data (Web Scraping)

### Step 1: Scrape Real Jobs (5-15 minutes)

```bash
python run_scraper.py
```

- Select **Option 3** (Scrape Bayt.com)
- Enter search terms (e.g., "software engineer")
- Enter location (e.g., "saudi-arabia")
- Choose number of pages (start with 3-5)
- Output: `data/raw/bayt_*.csv` and stored in `data/jobs.db`

### Step 2: Load into Database (optional)

The scraper automatically offers to load data into the database. If you skipped it:

```python
from src.database_manager import load_csv_to_database

db = load_csv_to_database('data/raw/bayt_jobs.csv')
db.export_to_csv('data/raw/scraped_jobs_export.csv')
```

### Step 3: Run Analysis

```bash
jupyter notebook
```

- Open `notebooks/job_market_analysis.ipynb`
- In **Cell 5**, update the data path:
  ```python
  data_path = '../data/raw/bayt_jobs.csv'  # or your scraped file
  ```
- Run all cells
- Output: Processed data in `data/processed/`

### Step 4: Launch Dashboard

```bash
streamlit run streamlit_app.py
```

---

## 🎯 Method 3: Kaggle Dataset

### Step 1: Download from Kaggle

1. Go to https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
2. Click "Download" (requires free account)
3. Extract the CSV file
4. Place in `data/raw/` folder
5. Rename to `linkedin_job_postings.csv` (or note the filename)

### Step 2: Run Analysis

```bash
jupyter notebook
```

- Open `notebooks/job_market_analysis.ipynb`
- In **Cell 5**, update the data path:
  ```python
  data_path = '../data/raw/linkedin_job_postings.csv'
  ```
- Run all cells

### Step 3: Launch Dashboard

```bash
streamlit run streamlit_app.py
```

---

## 🔍 Verify Data is Ready

Before launching the dashboard, verify your data:

```bash
python prepare_dashboard_data.py
```

This will:
- ✅ Check if processed data exists
- ✅ Show data statistics
- ✅ Verify all required columns are present
- ✅ Create sample data if needed

---

## 📁 Expected File Structure After Running

```
Job Market Analysis Tool/
├── data/
│   ├── raw/
│   │   └── sample_scraped_jobs.csv    ← Your raw data
│   ├── processed/
│   │   ├── job_market_clean.csv       ← Ready for Streamlit ✅
│   │   ├── top_skills.csv             ← Top 50 skills
│   │   └── analysis_summary.csv       ← Quick stats
│   └── jobs.db                         ← SQLite database (if using scraper)
│
├── visualizations/
│   ├── top_job_titles.png             ← 10 visualization files
│   ├── top_skills.png
│   ├── skills_wordcloud.png
│   └── ...
│
└── notebooks/
    └── job_market_analysis.ipynb       ← Jupyter notebook (executed)
```

---

## 🚨 Troubleshooting

### Issue: "Dataset not found" in Streamlit

**Cause:** Jupyter notebook hasn't been run yet, or processed data wasn't saved.

**Solution:**
```bash
# Option 1: Verify data
python prepare_dashboard_data.py

# Option 2: Create sample processed data
python prepare_dashboard_data.py
# Select 'y' when prompted

# Option 3: Run the notebook
jupyter notebook
# Open job_market_analysis.ipynb and run all cells
```

### Issue: Streamlit shows "No data available"

**Cause:** The CSV file is empty or corrupted.

**Solution:**
```bash
# Check the file
python -c "import pandas as pd; df = pd.read_csv('data/processed/job_market_clean.csv'); print(f'Rows: {len(df)}, Columns: {len(df.columns)}')"

# If error, regenerate data
python run_scraper.py  # Select option 1
# Then re-run the notebook
```

### Issue: "Skills column not found" in Streamlit

**Cause:** The notebook didn't extract skills, or the column was removed.

**Solution:**
- Re-run the Jupyter notebook (all cells)
- The skill extraction is in **Cell 19**
- Make sure it completes without errors

### Issue: Notebook crashes or freezes

**Cause:** Large dataset, memory issues, or missing dependencies.

**Solution:**
```bash
# Use sample data (smaller)
python run_scraper.py  # Option 1

# Or sample the dataset
# In notebook Cell 5, add:
df = df.sample(n=10000, random_state=42)  # Use 10,000 rows only
```

### Issue: Visualizations not showing

**Cause:** Missing matplotlib backend or display issue.

**Solution:**
Add this to the first code cell of the notebook:
```python
%matplotlib inline
```

---

## 💡 Pro Tips

### Tip 1: Quick Data Check

Before running the full analysis, check your data:

```python
import pandas as pd
df = pd.read_csv('data/raw/sample_scraped_jobs.csv')
print(df.head())
print(df.info())
```

### Tip 2: Incremental Development

When developing, run cells individually instead of all at once:
1. Run data loading cells (1-8)
2. Check output looks good
3. Run analysis cells (9-20)
4. Run visualization cells (21-30)
5. Run final save cells (31-34)

### Tip 3: Save Intermediate Results

After each major section, save a checkpoint:

```python
# After cleaning
df_clean.to_csv('../data/checkpoint_clean.csv', index=False)

# After skill extraction
df_clean.to_csv('../data/checkpoint_with_skills.csv', index=False)
```

### Tip 4: Dashboard Development Mode

While developing, use Streamlit's auto-reload:

```bash
streamlit run streamlit_app.py --server.runOnSave=true
```

Changes to `streamlit_app.py` will auto-reload the dashboard.

---

## 🔄 Complete Workflow Commands (Copy-Paste)

### For Sample Data (Fastest):

```bash
# 1. Generate data
python -c "from src.job_scraper import create_sample_scraped_data; create_sample_scraped_data()"

# 2. Verify data is ready
python prepare_dashboard_data.py

# 3. Launch Jupyter
jupyter notebook
# Run all cells in job_market_analysis.ipynb

# 4. Launch dashboard
streamlit run streamlit_app.py
```

### For Real Scraping:

```bash
# 1. Run scraper
python run_scraper.py
# Select option 1 or 3

# 2. Verify data
python prepare_dashboard_data.py

# 3. Analyze
jupyter notebook
# Update data path in Cell 5 if needed
# Run all cells

# 4. Dashboard
streamlit run streamlit_app.py
```

---

## 📊 What Each File Does

| File | Purpose | When It's Used |
|------|---------|----------------|
| `run_scraper.py` | Collect job data | Step 1 - Data Collection |
| `job_market_analysis.ipynb` | Analyze data & create visuals | Step 2 - Analysis |
| `streamlit_app.py` | Interactive dashboard | Step 3 - Visualization |
| `prepare_dashboard_data.py` | Verify data is ready | Between steps 2 & 3 |
| `job_market_clean.csv` | Processed data | Output of Step 2, Input of Step 3 |

---

## 🎓 Learning Path

### Beginner:
1. Use sample data (`python run_scraper.py` → Option 1)
2. Run notebook without modifications
3. View dashboard

### Intermediate:
1. Scrape real data from Bayt
2. Modify skill dictionary in notebook
3. Customize visualizations
4. Filter data by region

### Advanced:
1. Scrape multiple sources
2. Combine datasets
3. Add new analysis sections
4. Customize Streamlit dashboard
5. Add predictive models

---

## 🚀 Next Steps After Dashboard

Once your dashboard is working:

1. **Take Screenshots** - Capture key visualizations
2. **Record a Demo** - Screen record navigating the dashboard
3. **Write Findings** - Document 3-5 key insights
4. **Update README** - Add your insights to the README
5. **Share on LinkedIn** - Post with visualizations

---

## 📝 Checklist for Complete Project

- [ ] Data collected (sample or real)
- [ ] Jupyter notebook executed successfully
- [ ] All 10 visualizations generated
- [ ] Processed data saved in `data/processed/`
- [ ] Streamlit dashboard launches without errors
- [ ] Dashboard displays all sections
- [ ] Filters work correctly
- [ ] Can download data from dashboard
- [ ] Screenshots taken
- [ ] README updated with your findings

---

**🎉 You're now ready to demonstrate a complete end-to-end data science project!**

