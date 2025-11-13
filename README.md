# Job Market Analysis Tool

A comprehensive data-driven analysis of the tech job market, focusing on in-demand skills, salary trends, and role requirements.

## 🎯 Project Objective

This project analyzes job market data to extract actionable insights about:
- Most in-demand programming languages and technical skills
- Salary ranges by role and experience level
- Geographic distribution of job opportunities
- Trending skills and technologies
- Job role clustering and similarities

## 📊 Dataset

This project uses the **LinkedIn Job Postings Dataset** from Kaggle:
- [LinkedIn Job Postings - 2023 Dataset](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)

**Alternative datasets:**
- [Data Science Job Postings](https://www.kaggle.com/datasets/rashikrahmanpritom/data-science-job-posting-on-glassdoor)
- [Job Posts Data](https://www.kaggle.com/datasets/madhab/jobposts)

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **Data Processing:** pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly, WordCloud
- **NLP:** NLTK, spaCy
- **ML:** scikit-learn
- **Dashboard:** Streamlit

## 📁 Project Structure

```
Job Market Analysis Tool/
│
├── data/                          # Dataset directory
│   ├── raw/                       # Original datasets
│   └── processed/                 # Cleaned datasets
│
├── notebooks/                     # Jupyter notebooks
│   └── job_market_analysis.ipynb  # Main analysis notebook
│
├── src/                           # Source code (optional)
│   ├── data_collection.py
│   ├── data_cleaning.py
│   └── visualization.py
│
├── visualizations/                # Saved plots and charts
│
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## 🚀 Getting Started

### 1. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (run in Python)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 2. Download Dataset

1. Go to [Kaggle LinkedIn Job Postings](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)
2. Download the dataset
3. Extract to `data/raw/` folder

### 3. Run Analysis

```bash
# Start Jupyter Notebook
jupyter notebook

# Open notebooks/job_market_analysis.ipynb
```

## 📈 Analysis Pipeline

1. **Data Collection** - Load and explore raw job postings data
2. **Data Cleaning** - Handle missing values, normalize text, remove duplicates
3. **Exploratory Data Analysis** - Statistical summaries and initial insights
4. **Skill Extraction** - Parse job descriptions to extract technical skills
5. **Visualization** - Create charts, word clouds, and interactive plots
6. **Machine Learning** - Cluster similar jobs and predict job categories
7. **Insights & Recommendations** - Summarize findings

## 🎨 Key Visualizations

- Top 10 Most In-Demand Programming Languages
- Skill Frequency Word Cloud
- Salary Distribution by Job Role
- Geographic Distribution of Jobs
- Experience Level Requirements
- Skill Co-occurrence Heatmap

## 📝 Key Findings

(Results will be added after analysis)

## 🔮 Future Enhancements

- Real-time job scraping from multiple sources
- Time-series trend analysis
- Salary prediction model
- Interactive Streamlit dashboard
- Regional comparison (Saudi Arabia vs Global)

## 👤 Author

Computer Science Graduate
Portfolio Project - 2025

## 📄 License

This project is for educational and portfolio purposes.

