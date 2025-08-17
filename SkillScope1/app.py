import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Import configuration
try:
    import config
except ImportError:
    st.warning("Config file not found. Using default settings.")

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from data_loader import DataLoader
from nlp_processor import NLPProcessor
from mock_job_data import MockJobData
try:
    from auth_manager import AuthManager
except ImportError:
    from simple_auth import SimpleAuthManager as AuthManager
from api_integrator import JobAPIIntegrator, SalaryPredictor

# Page configuration
st.set_page_config(
    page_title="SkillScope - Job Market Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check
def check_authentication():
    """Check if user is authenticated"""
    if not st.session_state.get('authenticated', False):
        # Show login interface directly in the main app
        show_login_interface()
        st.stop()

def show_login_interface():
    """Show login/signup interface"""
    st.title("🎯 SkillScope")
    st.markdown("### Job Market Skill Trend Analyzer")
    st.markdown("""
    Discover trending skills, analyze job markets, and optimize your career path with 
    real-time data and personalized recommendations.
    """)
    
    st.markdown("---")
    
    # Show appropriate form
    if st.session_state.get('show_signup', False):
        show_signup_form()
    else:
        show_login_form()

def show_login_form():
    """Display login form"""
    st.subheader("Sign In to SkillScope")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("Sign In", type="primary", use_container_width=True)
        with col2:
            if st.form_submit_button("Create Account", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()
        
        if login_button:
            if email and password:
                auth_manager = AuthManager()
                user = auth_manager.authenticate_user(email, password)
                
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.success(f"Welcome back, {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.error("Please enter both email and password")

def show_signup_form():
    """Display signup form"""
    st.subheader("Create Your SkillScope Account")
    
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", help="Minimum 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        # Optional profile information
        st.markdown("**Optional Profile Information:**")
        current_role = st.text_input("Current Role", placeholder="e.g., Software Engineer")
        experience_level = st.selectbox("Experience Level", 
                                      ["Entry Level", "Mid Level", "Senior Level", "Executive Level"])
        industry = st.selectbox("Industry", 
                               ["Technology", "Finance", "Healthcare", "Marketing", "Other"])
        
        col1, col2 = st.columns(2)
        with col1:
            signup_button = st.form_submit_button("Create Account", type="primary", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Sign In", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
        
        if signup_button:
            if not all([name, email, password, confirm_password]):
                st.error("Please fill in all required fields")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email address")
            else:
                auth_manager = AuthManager()
                
                if auth_manager.create_user(email, name, password):
                    # Create profile data
                    profile_data = {
                        'current_role': current_role,
                        'experience_level': experience_level,
                        'industry': industry,
                        'signup_date': datetime.now().isoformat()
                    }
                    
                    # Authenticate the new user
                    user = auth_manager.authenticate_user(email, password)
                    if user:
                        # Update profile
                        auth_manager.update_user_profile(user['id'], profile_data)
                        
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.session_state.user['profile_data'] = profile_data
                        st.success(f"Account created successfully! Welcome, {name}!")
                        st.rerun()
                else:
                    st.error("Account creation failed. Email might already be registered.")

# Check authentication first
check_authentication()

# Initialize session state
if 'data_loader' not in st.session_state:
    st.session_state.data_loader = DataLoader()
if 'nlp_processor' not in st.session_state:
    st.session_state.nlp_processor = NLPProcessor()
if 'api_integrator' not in st.session_state:
    st.session_state.api_integrator = JobAPIIntegrator()
if 'salary_predictor' not in st.session_state:
    st.session_state.salary_predictor = SalaryPredictor()

def main():
    # User info in sidebar
    user = st.session_state.get('user', {})
    st.sidebar.title(f"Welcome, {user.get('name', 'User')}!")
    st.sidebar.markdown("---")
    
    # Logout button
    if st.sidebar.button("Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("login.py")
    
    st.sidebar.markdown("---")
    
    # API Status
    st.sidebar.subheader("Data Sources")
    if st.sidebar.button("Refresh Live Data", type="secondary"):
        st.session_state.refresh_data = True
    
    st.title("🎯 SkillScope - Job Market Analyzer")
    st.markdown("### Discover trending skills and optimize your career path")
    
    # Load both mock and real data
    mock_data = MockJobData()
    mock_job_data = mock_data.get_job_postings()
    
    # Try to get live data
    api_integrator = st.session_state.api_integrator
    live_jobs = []
    
    with st.spinner("Loading real-time job data..."):
        if st.session_state.get('refresh_data', False):
            # Get trending jobs from APIs
            trending_queries = ["software engineer", "data scientist", "product manager", "devops engineer"]
            for query in trending_queries[:2]:  # Limit to prevent rate limiting
                jobs = api_integrator.search_all_sources(query, max_results_per_source=10)
                live_jobs.extend(jobs)
            
            if live_jobs:
                st.sidebar.success(f"✅ Live data: {len(live_jobs)} jobs")
                # Convert to DataFrame format
                live_df = pd.DataFrame(live_jobs)
                # Standardize column names
                if not live_df.empty:
                    live_df['required_skills'] = live_df.apply(lambda x: 
                        api_integrator.extract_skills_from_job_data([x.to_dict()]), axis=1)
                    live_df['industry'] = live_df.get('category', 'Technology')
                    live_df['experience_level'] = 'Mid Level'  # Default for API data
                    # Combine with mock data
                    job_data = pd.concat([mock_job_data.head(1000), live_df], ignore_index=True)
                else:
                    job_data = mock_job_data
            else:
                st.sidebar.info("📊 Using comprehensive mock data")
                job_data = mock_job_data
        else:
            st.sidebar.info("📊 Using comprehensive mock data")
            job_data = mock_job_data
    
    # Main dashboard overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Job Postings", f"{len(job_data):,}")
    
    with col2:
        unique_skills = set()
        for skills in job_data['required_skills']:
            unique_skills.update(skills)
        st.metric("Unique Skills Tracked", len(unique_skills))
    
    with col3:
        st.metric("Industries Covered", job_data['industry'].nunique())
    
    with col4:
        avg_salary = job_data['salary_max'].mean()
        st.metric("Avg. Max Salary", f"${avg_salary:,.0f}")
    
    st.markdown("---")
    
    # Quick insights section
    st.subheader("📊 Quick Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top industries by job count
        industry_counts = job_data['industry'].value_counts()
        fig_industry = px.bar(
            x=industry_counts.index,
            y=industry_counts.values,
            title="Job Postings by Industry",
            labels={'x': 'Industry', 'y': 'Number of Jobs'}
        )
        fig_industry.update_layout(height=400)
        st.plotly_chart(fig_industry, use_container_width=True)
    
    with col2:
        # Salary distribution by industry
        fig_salary = px.box(
            job_data,
            x='industry',
            y='salary_max',
            title="Salary Distribution by Industry"
        )
        fig_salary.update_xaxes(tickangle=45)
        fig_salary.update_layout(height=400)
        st.plotly_chart(fig_salary, use_container_width=True)
    
    # Top trending skills
    st.subheader("🔥 Trending Skills Across All Industries")
    
    # Extract and count all skills
    all_skills = []
    for skills in job_data['required_skills']:
        all_skills.extend(skills)
    
    skill_counts = pd.Series(all_skills).value_counts().head(20)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_skills = px.bar(
            x=skill_counts.values,
            y=skill_counts.index,
            orientation='h',
            title="Top 20 Most Demanded Skills",
            labels={'x': 'Number of Job Postings', 'y': 'Skills'}
        )
        fig_skills.update_layout(height=600)
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with col2:
        st.subheader("Skills Growth")
        # Mock growth data for demonstration
        growth_data = pd.DataFrame({
            'skill': skill_counts.head(10).index,
            'growth': np.random.uniform(5, 25, 10)
        })
        
        for idx, row in growth_data.iterrows():
            growth_color = "green" if row['growth'] > 15 else "orange" if row['growth'] > 10 else "red"
            st.metric(
                label=row['skill'],
                value=f"+{row['growth']:.1f}%",
                delta=f"{row['growth']:.1f}% vs last quarter"
            )
    
    # Recent job postings
    st.subheader("📋 Recent Job Postings")
    
    # Display recent jobs
    recent_jobs = job_data.head(10)[['title', 'company', 'industry', 'location', 'salary_max']]
    recent_jobs['salary_max'] = recent_jobs['salary_max'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(
        recent_jobs,
        column_config={
            "title": "Job Title",
            "company": "Company",
            "industry": "Industry",
            "location": "Location",
            "salary_max": "Max Salary"
        },
        use_container_width=True
    )
    
    # Footer with navigation hints
    st.markdown("---")
    st.markdown("""
    ### 🚀 Explore More Features:
    
    - **Industry Trends**: Analyze specific industry trends and skill demands
    - **Resume Analyzer**: Upload your resume to identify skill gaps
    - **Career Recommendations**: Get personalized career path suggestions
    
    Use the navigation in the sidebar to explore these features!
    """)

if __name__ == "__main__":
    main()
