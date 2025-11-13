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
        if 'job_title_clean' in df.columns:
            top_jobs = df['job_title_clean'].value_counts().head(10)
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
    
    with col_right:
        # Top Locations
        st.subheader("🌍 Top 10 Locations")
        if 'location' in df.columns:
            top_locations = df['location'].value_counts().head(10)
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
    
    st.markdown("---")
    
    # Experience Level Distribution
    st.subheader("📊 Experience Level Distribution")
    if 'experience_level' in df.columns:
        exp_dist = df['experience_level'].value_counts()
        
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
    
    # Raw Data Explorer
    with st.expander("📋 View Raw Data"):
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

