"""
Job Market Analysis Dashboard
Interactive Streamlit Dashboard for Job Market Insights

To run: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="Job Market Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Job Market Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    """Load the processed dataset"""
    try:
        df = pd.read_csv('data/processed/job_market_clean.csv')
        return df
    except FileNotFoundError:
        st.error("⚠️ Dataset not found! Please run the Jupyter notebook first to generate processed data.")
        st.info("Path: data/processed/job_market_clean.csv")
        return None

df = load_data()

if df is not None:
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Location filter
    if 'location' in df.columns:
        all_locations = ["All"] + sorted(df['location'].unique().tolist())
        selected_location = st.sidebar.selectbox("Select Location", all_locations)
        
        if selected_location != "All":
            df = df[df['location'] == selected_location]
    
    # Job title filter
    if 'job_title_clean' in df.columns:
        all_jobs = ["All"] + sorted(df['job_title_clean'].unique().tolist())
        selected_job = st.sidebar.selectbox("Select Job Title", all_jobs)
        
        if selected_job != "All":
            df = df[df['job_title_clean'] == selected_job]
    
    # Experience level filter
    if 'experience_level' in df.columns:
        all_exp = ["All"] + sorted(df['experience_level'].unique().tolist())
        selected_exp = st.sidebar.selectbox("Select Experience Level", all_exp)
        
        if selected_exp != "All":
            df = df[df['experience_level'] == selected_exp]
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 Showing {len(df):,} job postings")
    
    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs", f"{len(df):,}")
    
    with col2:
        if 'company' in df.columns:
            st.metric("Unique Companies", f"{df['company'].nunique():,}")
    
    with col3:
        if 'location' in df.columns:
            st.metric("Locations", f"{df['location'].nunique():,}")
    
    with col4:
        if 'job_title' in df.columns:
            st.metric("Job Titles", f"{df['job_title'].nunique():,}")
    
    st.markdown("---")
    
    # Two column layout
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Top Job Titles
        st.subheader("💼 Top 10 Job Titles")
        # Use job_title_clean if available, otherwise use job_title
        title_col = 'job_title_clean' if 'job_title_clean' in df.columns else 'job_title'
        
        if title_col in df.columns:
            top_jobs = df[title_col].value_counts().head(10)
            
            if len(top_jobs) > 0:
                fig = px.bar(
                    x=top_jobs.values,
                    y=top_jobs.index,
                    orientation='h',
                    labels={'x': 'Number of Jobs', 'y': 'Job Title'},
                    color=top_jobs.values,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No job title data available")
        else:
            st.warning("Job title column not found in data")
    
    with col_right:
        # Top Locations
        st.subheader("🌍 Top 10 Locations")
        if 'location' in df.columns:
            top_locations = df['location'].value_counts().head(10)
            
            if len(top_locations) > 0:
                fig = px.bar(
                    x=top_locations.values,
                    y=top_locations.index,
                    orientation='h',
                    labels={'x': 'Number of Jobs', 'y': 'Location'},
                    color=top_locations.values,
                    color_continuous_scale='Greens'
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No location data available")
        else:
            st.warning("Location column not found in data")
    
    st.markdown("---")
    
    # Experience Level Distribution
    st.subheader("📊 Experience Level Distribution")
    if 'experience_level' in df.columns:
        exp_dist = df['experience_level'].value_counts()
        
        if len(exp_dist) > 0:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.dataframe(
                    pd.DataFrame({
                        'Experience Level': exp_dist.index,
                        'Count': exp_dist.values,
                        'Percentage': [f"{(v/len(df)*100):.1f}%" for v in exp_dist.values]
                    }),
                    hide_index=True
                )
            
            with col2:
                fig = px.pie(
                    values=exp_dist.values,
                    names=exp_dist.index,
                    title="",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No experience level data available")
    else:
        st.warning("Experience level column not found in data")
    
    st.markdown("---")
    
    # Top Companies
    st.subheader("🏢 Top Hiring Companies")
    if 'company' in df.columns:
        top_companies = df['company'].value_counts().head(10)
        
        if len(top_companies) > 0:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.bar(
                    x=top_companies.values,
                    y=top_companies.index,
                    orientation='h',
                    labels={'x': 'Number of Job Postings', 'y': 'Company'},
                    color=top_companies.values,
                    color_continuous_scale='Purples'
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(
                    pd.DataFrame({
                        'Company': top_companies.index,
                        'Jobs': top_companies.values,
                        'Share': [f"{(v/len(df)*100):.1f}%" for v in top_companies.values]
                    }),
                    hide_index=True,
                    height=400
                )
        else:
            st.info("No company data available")
    else:
        st.warning("Company column not found in data")
    
    st.markdown("---")
    
    # Skills Analysis
    st.subheader("🔥 Most In-Demand Skills")
    
    if 'skills' in df.columns:
        # Extract all skills
        try:
            import ast
            all_skills = []
            for skills_str in df['skills'].dropna():
                try:
                    if isinstance(skills_str, str):
                        skills_list = ast.literal_eval(skills_str)
                        if isinstance(skills_list, list):
                            all_skills.extend(skills_list)
                except:
                    pass
            
            if all_skills:
                skill_counts = Counter(all_skills)
                top_skills = pd.DataFrame(
                    skill_counts.most_common(20),
                    columns=['Skill', 'Count']
                )
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(
                        top_skills,
                        x='Count',
                        y='Skill',
                        orientation='h',
                        title="Top 20 Skills",
                        color='Count',
                        color_continuous_scale='Viridis'
                    )
                    fig.update_layout(showlegend=False, height=600)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(
                        top_skills.head(20),
                        hide_index=True,
                        height=600
                    )
                
                # Word Cloud
                st.subheader("☁️ Skills Word Cloud")
                skills_text = ' '.join(all_skills)
                
                wordcloud = WordCloud(
                    width=1600,
                    height=400,
                    background_color='white',
                    colormap='viridis'
                ).generate(skills_text)
                
                fig, ax = plt.subplots(figsize=(16, 4))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.warning("No skills data available after filtering")
        except Exception as e:
            st.error(f"Error processing skills: {str(e)}")
    else:
        st.info("Skills column not found in dataset. Run the Jupyter notebook to extract skills.")
    
    st.markdown("---")
    
    # Job Listings Section
    st.subheader("📄 Job Postings")
    
    # Display mode selector
    view_mode = st.radio("View Mode:", ["Cards", "Table"], horizontal=True)
    
    # Number of jobs to display
    num_jobs = st.slider("Number of jobs to display:", 5, 50, 10)
    
    if view_mode == "Cards":
        # Card view - more visual
        for idx, row in df.head(num_jobs).iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {row.get('job_title', 'N/A')}")
                    st.markdown(f"**Company:** {row.get('company', 'N/A')}")
                    st.markdown(f"**Location:** {row.get('location', 'N/A')}")
                    
                with col2:
                    if 'experience_level' in row and pd.notna(row['experience_level']):
                        st.metric("Experience", row['experience_level'])
                    if 'salary' in row and pd.notna(row['salary']) and row['salary'] != '':
                        st.metric("Salary", row['salary'])
                
                # Description
                if 'description' in row and pd.notna(row['description']):
                    with st.expander("📝 Job Description"):
                        st.write(row['description'])
                
                st.markdown("---")
    else:
        # Table view - more compact
        display_cols = []
        if 'job_title' in df.columns:
            display_cols.append('job_title')
        if 'company' in df.columns:
            display_cols.append('company')
        if 'location' in df.columns:
            display_cols.append('location')
        if 'experience_level' in df.columns:
            display_cols.append('experience_level')
        if 'salary' in df.columns:
            display_cols.append('salary')
        
        if display_cols:
            st.dataframe(
                df[display_cols].head(num_jobs),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No display columns found")
    
    st.markdown("---")
    
    # Raw Data Explorer
    with st.expander("📋 View All Raw Data"):
        st.dataframe(df.head(100), use_container_width=True)
        st.info(f"Showing first 100 of {len(df):,} rows")
    
    # Download section
    st.markdown("---")
    st.subheader("💾 Download Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name="filtered_job_data.csv",
            mime="text/csv"
        )
    
    with col2:
        if 'skills' in df.columns and len(all_skills) > 0:
            skills_csv = top_skills.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Top Skills (CSV)",
                data=skills_csv,
                file_name="top_skills.csv",
                mime="text/csv"
            )

else:
    st.warning("Please run the Jupyter notebook first to generate the processed dataset.")
    st.info("Steps:\n1. Open `notebooks/job_market_analysis.ipynb`\n2. Run all cells\n3. Come back to this dashboard")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📊 Job Market Analysis Dashboard | Built with Streamlit & Python</p>
        <p>Computer Science Graduate Portfolio Project | 2025</p>
    </div>
""", unsafe_allow_html=True)

