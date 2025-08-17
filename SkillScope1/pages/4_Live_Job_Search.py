import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from api_integrator import JobAPIIntegrator, SalaryPredictor
from auth_manager import AuthManager
from skill_extractor import SkillExtractor

st.set_page_config(
    page_title="Live Job Search - SkillScope",
    page_icon="🔍",
    layout="wide"
)

def check_authentication():
    """Check if user is authenticated"""
    if not st.session_state.get('authenticated', False):
        st.error("Please log in to access this feature")
        st.stop()

check_authentication()

def main():
    st.title("🔍 Live Job Search")
    st.markdown("### Search real-time job postings from multiple sources")
    
    # Initialize components
    if 'api_integrator' not in st.session_state:
        st.session_state.api_integrator = JobAPIIntegrator()
    
    if 'salary_predictor' not in st.session_state:
        st.session_state.salary_predictor = SalaryPredictor()
    
    api_integrator = st.session_state.api_integrator
    salary_predictor = st.session_state.salary_predictor
    auth_manager = AuthManager()
    user = st.session_state.get('user', {})
    
    # Search interface
    st.subheader("🎯 Job Search")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "Job Title or Keywords",
            placeholder="e.g., Software Engineer, Data Scientist, Python Developer"
        )
    
    with col2:
        location = st.text_input(
            "Location",
            placeholder="e.g., San Francisco, Remote"
        )
    
    with col3:
        max_results = st.selectbox(
            "Max Results",
            [10, 25, 50, 100],
            index=1
        )
    
    # Advanced filters
    with st.expander("🔧 Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            salary_min = st.number_input("Minimum Salary ($)", min_value=0, value=0, step=5000)
        
        with col2:
            salary_max = st.number_input("Maximum Salary ($)", min_value=0, value=0, step=5000)
        
        with col3:
            job_type = st.selectbox("Job Type", ["Any", "Full-time", "Contract", "Part-time"])
    
    # Search button
    if st.button("🔍 Search Jobs", type="primary", use_container_width=True):
        if search_query:
            with st.spinner("Searching job postings..."):
                # Search from all sources
                jobs = api_integrator.search_all_sources(
                    query=search_query,
                    location=location,
                    max_results_per_source=max_results // 2
                )
                
                if jobs:
                    st.session_state.search_results = jobs
                    st.session_state.search_query = search_query
                    st.session_state.search_location = location
                    
                    # Save search to database
                    filters = {
                        'location': location,
                        'salary_min': salary_min if salary_min > 0 else None,
                        'salary_max': salary_max if salary_max > 0 else None,
                        'job_type': job_type if job_type != "Any" else None
                    }
                    
                    auth_manager.save_job_search(
                        user['id'], 
                        search_query, 
                        filters, 
                        len(jobs)
                    )
                    
                    st.success(f"Found {len(jobs)} job postings!")
                else:
                    st.warning("No job postings found. Try different search terms.")
        else:
            st.error("Please enter a search query")
    
    # Display search results
    if st.session_state.get('search_results'):
        jobs = st.session_state.search_results
        
        st.markdown("---")
        st.subheader(f"📋 Search Results for '{st.session_state.get('search_query', '')}'")
        
        # Filter results based on advanced filters
        filtered_jobs = jobs.copy()
        
        if salary_min > 0:
            filtered_jobs = [job for job in filtered_jobs 
                           if job.get('salary_min') and job['salary_min'] >= salary_min]
        
        if salary_max > 0:
            filtered_jobs = [job for job in filtered_jobs 
                           if job.get('salary_max') and job['salary_max'] <= salary_max]
        
        if job_type != "Any":
            filtered_jobs = [job for job in filtered_jobs 
                           if job.get('contract_type', '').lower() == job_type.lower()]
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", len(filtered_jobs))
        
        with col2:
            companies = set(job.get('company', '') for job in filtered_jobs if job.get('company'))
            st.metric("Unique Companies", len(companies))
        
        with col3:
            salaries = [job.get('salary_max') for job in filtered_jobs if job.get('salary_max')]
            avg_salary = np.mean(salaries) if salaries else 0
            st.metric("Avg Max Salary", f"${avg_salary:,.0f}" if avg_salary > 0 else "N/A")
        
        with col4:
            remote_jobs = len([job for job in filtered_jobs if 'remote' in job.get('location', '').lower()])
            st.metric("Remote Jobs", remote_jobs)
        
        # Charts
        if len(filtered_jobs) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Jobs by company
                company_counts = {}
                for job in filtered_jobs:
                    company = job.get('company', 'Unknown')
                    company_counts[company] = company_counts.get(company, 0) + 1
                
                if company_counts:
                    company_df = pd.DataFrame(list(company_counts.items()), columns=['Company', 'Jobs'])
                    company_df = company_df.sort_values('Jobs', ascending=False).head(10)
                    
                    fig_companies = px.bar(
                        company_df,
                        x='Jobs',
                        y='Company',
                        orientation='h',
                        title="Top Hiring Companies"
                    )
                    fig_companies.update_layout(height=400)
                    st.plotly_chart(fig_companies, use_container_width=True)
            
            with col2:
                # Salary distribution
                salary_data = [job.get('salary_max') for job in filtered_jobs if job.get('salary_max')]
                if salary_data:
                    fig_salary = px.histogram(
                        salary_data,
                        nbins=20,
                        title="Salary Distribution"
                    )
                    fig_salary.update_layout(
                        xaxis_title="Maximum Salary ($)",
                        yaxis_title="Number of Jobs",
                        height=400
                    )
                    st.plotly_chart(fig_salary, use_container_width=True)
        
        # Job listings
        st.subheader("📝 Job Listings")
        
        # Pagination
        jobs_per_page = 10
        total_pages = (len(filtered_jobs) + jobs_per_page - 1) // jobs_per_page
        
        if total_pages > 1:
            page = st.selectbox("Page", range(1, total_pages + 1))
        else:
            page = 1
        
        start_idx = (page - 1) * jobs_per_page
        end_idx = start_idx + jobs_per_page
        page_jobs = filtered_jobs[start_idx:end_idx]
        
        for i, job in enumerate(page_jobs):
            with st.expander(f"{job.get('title', 'Unknown Title')} at {job.get('company', 'Unknown Company')}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write("**Job Details:**")
                    st.write(f"📍 Location: {job.get('location', 'Not specified')}")
                    st.write(f"🏢 Company: {job.get('company', 'Unknown')}")
                    st.write(f"📅 Posted: {job.get('created_date', 'Recently')}")
                    st.write(f"🔗 Source: {job.get('source', 'API')}")
                    
                    if job.get('description'):
                        st.write("**Description:**")
                        description = job['description']
                        if len(description) > 300:
                            description = description[:300] + "..."
                        st.write(description)
                
                with col2:
                    st.write("**Compensation:**")
                    if job.get('salary_min') and job.get('salary_max'):
                        st.write(f"💰 ${job['salary_min']:,} - ${job['salary_max']:,}")
                    elif job.get('salary_max'):
                        st.write(f"💰 Up to ${job['salary_max']:,}")
                    else:
                        st.write("💰 Salary not specified")
                    
                    if job.get('contract_type'):
                        st.write(f"⏰ {job['contract_type']}")
                    
                    # Salary prediction if we have user skills
                    user_skills = auth_manager.get_user_skills(user['id'])
                    if user_skills and salary_predictor.is_trained:
                        skills_list = [skill['skill_name'] for skill in user_skills]
                        predicted_salary = salary_predictor.predict_salary(
                            job.get('location', ''),
                            'Mid Level',
                            job.get('category', 'Technology'),
                            skills_list
                        )
                        
                        if predicted_salary:
                            st.write(f"🎯 Predicted for you: ${predicted_salary:,.0f}")
                
                with col3:
                    st.write("**Actions:**")
                    
                    # Save job button
                    if st.button(f"💾 Save Job", key=f"save_{job.get('id', i)}"):
                        job_data = {
                            'job_id': job.get('id', f"job_{i}"),
                            'title': job.get('title'),
                            'company': job.get('company'),
                            'salary_min': job.get('salary_min'),
                            'salary_max': job.get('salary_max'),
                            'location': job.get('location')
                        }
                        
                        if auth_manager.save_job(user['id'], job_data):
                            st.success("Job saved!")
                        else:
                            st.error("Failed to save job")
                    
                    # Apply button (external link)
                    if job.get('url'):
                        st.markdown(f"[🚀 Apply Now]({job['url']})")
                    
                    # Skills extraction
                    if st.button(f"🔍 Extract Skills", key=f"skills_{job.get('id', i)}"):
                        skill_extractor = SkillExtractor()
                        job_text = f"{job.get('title', '')} {job.get('description', '')}"
                        extracted_skills = skill_extractor.extract_skills_from_text(job_text)
                        
                        if extracted_skills:
                            st.write("**Required Skills:**")
                            for skill in extracted_skills[:10]:  # Show top 10
                                st.write(f"• {skill}")
                            if len(extracted_skills) > 10:
                                st.write(f"... and {len(extracted_skills) - 10} more")
                        else:
                            st.write("No specific skills detected")
    
    # Saved jobs section
    st.markdown("---")
    st.subheader("💾 Your Saved Jobs")
    
    saved_jobs = auth_manager.get_saved_jobs(user['id'])
    
    if saved_jobs:
        saved_df = pd.DataFrame(saved_jobs)
        saved_df['saved_date'] = pd.to_datetime(saved_df['saved_date'])
        saved_df = saved_df.sort_values('saved_date', ascending=False)
        
        st.dataframe(
            saved_df[['job_title', 'company', 'location', 'salary_max', 'saved_date']],
            column_config={
                'job_title': 'Job Title',
                'company': 'Company',
                'location': 'Location',
                'salary_max': st.column_config.NumberColumn('Max Salary', format='$%d'),
                'saved_date': st.column_config.DatetimeColumn('Saved Date')
            },
            use_container_width=True
        )
    else:
        st.info("No saved jobs yet. Search and save jobs that interest you!")
    
    # API Status and Configuration
    st.sidebar.subheader("🔧 API Configuration")
    
    # Check if API keys are configured
    adzuna_configured = bool(os.getenv('ADZUNA_APP_ID') and os.getenv('ADZUNA_API_KEY'))
    indeed_configured = bool(os.getenv('INDEED_API_KEY'))
    
    if adzuna_configured:
        st.sidebar.success("✅ Adzuna API: Configured")
    else:
        st.sidebar.warning("⚠️ Adzuna API: Not configured")
        st.sidebar.info("Add ADZUNA_APP_ID and ADZUNA_API_KEY to environment secrets for live data")
    
    if indeed_configured:
        st.sidebar.success("✅ Indeed API: Configured")
    else:
        st.sidebar.warning("⚠️ Indeed API: Not configured")
        st.sidebar.info("Add INDEED_API_KEY to environment secrets for Indeed integration")
    
    if not adzuna_configured and not indeed_configured:
        st.sidebar.info("📊 Currently using enhanced mock data with realistic job postings")

if __name__ == "__main__":
    main()