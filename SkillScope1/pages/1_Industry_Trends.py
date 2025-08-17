import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from data_loader import DataLoader
from mock_job_data import MockJobData

st.set_page_config(
    page_title="Industry Trends - SkillScope",
    page_icon="📈",
    layout="wide"
)

def main():
    st.title("📈 Industry Skill Trends")
    st.markdown("### Analyze trending skills and market demands by industry")
    
    # Load data
    mock_data = MockJobData()
    job_data = mock_data.get_job_postings()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Industry selector
    industries = sorted(job_data['industry'].unique())
    selected_industries = st.sidebar.multiselect(
        "Select Industries",
        industries,
        default=industries[:2]
    )
    
    # Experience level filter
    experience_levels = sorted(job_data['experience_level'].unique())
    selected_experience = st.sidebar.multiselect(
        "Experience Level",
        experience_levels,
        default=experience_levels
    )
    
    # Salary range filter
    min_salary, max_salary = st.sidebar.slider(
        "Salary Range ($)",
        min_value=int(job_data['salary_min'].min()),
        max_value=int(job_data['salary_max'].max()),
        value=(int(job_data['salary_min'].min()), int(job_data['salary_max'].max())),
        step=5000
    )
    
    # Filter data
    filtered_data = job_data[
        (job_data['industry'].isin(selected_industries)) &
        (job_data['experience_level'].isin(selected_experience)) &
        (job_data['salary_max'] >= min_salary) &
        (job_data['salary_min'] <= max_salary)
    ]
    
    if filtered_data.empty:
        st.warning("No data matches your current filters. Please adjust your selection.")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Filtered Job Postings", f"{len(filtered_data):,}")
    
    with col2:
        avg_salary = filtered_data['salary_max'].mean()
        st.metric("Avg. Max Salary", f"${avg_salary:,.0f}")
    
    with col3:
        unique_companies = filtered_data['company'].nunique()
        st.metric("Companies Hiring", unique_companies)
    
    with col4:
        # Calculate skill diversity
        all_skills = []
        for skills in filtered_data['required_skills']:
            all_skills.extend(skills)
        unique_skills = len(set(all_skills))
        st.metric("Unique Skills", unique_skills)
    
    st.markdown("---")
    
    # Industry comparison
    if len(selected_industries) > 1:
        st.subheader("🔍 Industry Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Job count by industry
            industry_counts = filtered_data['industry'].value_counts()
            fig_industry = px.pie(
                values=industry_counts.values,
                names=industry_counts.index,
                title="Job Distribution by Industry"
            )
            st.plotly_chart(fig_industry, use_container_width=True)
        
        with col2:
            # Average salary by industry
            salary_by_industry = filtered_data.groupby('industry')['salary_max'].mean().reset_index()
            fig_salary = px.bar(
                salary_by_industry,
                x='industry',
                y='salary_max',
                title="Average Maximum Salary by Industry",
                labels={'salary_max': 'Average Max Salary ($)', 'industry': 'Industry'}
            )
            fig_salary.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_salary, use_container_width=True)
    
    # Top skills analysis
    st.subheader("🎯 Top Skills by Industry")
    
    # Create tabs for each industry
    if selected_industries:
        tabs = st.tabs(selected_industries)
        
        for i, industry in enumerate(selected_industries):
            with tabs[i]:
                industry_data = filtered_data[filtered_data['industry'] == industry]
                
                # Extract skills for this industry
                industry_skills = []
                for skills in industry_data['required_skills']:
                    industry_skills.extend(skills)
                
                if industry_skills:
                    skill_counts = pd.Series(industry_skills).value_counts().head(15)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        fig_skills = px.bar(
                            x=skill_counts.values,
                            y=skill_counts.index,
                            orientation='h',
                            title=f"Top Skills in {industry}",
                            labels={'x': 'Number of Job Postings', 'y': 'Skills'}
                        )
                        fig_skills.update_layout(height=500)
                        st.plotly_chart(fig_skills, use_container_width=True)
                    
                    with col2:
                        st.subheader("Industry Insights")
                        
                        # Job count
                        st.metric("Jobs in Industry", len(industry_data))
                        
                        # Average salary
                        avg_industry_salary = industry_data['salary_max'].mean()
                        st.metric("Avg. Max Salary", f"${avg_industry_salary:,.0f}")
                        
                        # Top companies
                        top_companies = industry_data['company'].value_counts().head(5)
                        st.subheader("Top Hiring Companies")
                        for company, count in top_companies.items():
                            st.write(f"• {company}: {count} jobs")
                        
                        # Experience level distribution
                        exp_dist = industry_data['experience_level'].value_counts()
                        st.subheader("Experience Level Demand")
                        for level, count in exp_dist.items():
                            st.write(f"• {level}: {count} jobs")
                else:
                    st.info("No skills data available for this industry selection.")
    
    # Skill trend analysis (mock time series data)
    st.subheader("📊 Skill Trend Analysis")
    
    if selected_industries:
        # Generate mock time series data for top skills
        all_filtered_skills = []
        for skills in filtered_data['required_skills']:
            all_filtered_skills.extend(skills)
        
        top_skills = pd.Series(all_filtered_skills).value_counts().head(8).index.tolist()
        
        # Create mock time series data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        trend_data = []
        
        for skill in top_skills:
            for date in dates:
                # Generate realistic trend data with some noise
                base_demand = np.random.randint(10, 100)
                seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
                growth_factor = 1 + 0.1 * (date.month - 1) / 12
                demand = int(base_demand * seasonal_factor * growth_factor)
                
                trend_data.append({
                    'date': date,
                    'skill': skill,
                    'demand': demand
                })
        
        trend_df = pd.DataFrame(trend_data)
        
        # Plot trends
        fig_trends = px.line(
            trend_df,
            x='date',
            y='demand',
            color='skill',
            title="Skill Demand Trends Over Time (2024)",
            labels={'demand': 'Job Postings Count', 'date': 'Month'}
        )
        fig_trends.update_layout(height=500)
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Growth analysis
        st.subheader("📈 Skill Growth Analysis")
        
        # Calculate growth rates (mock data)
        growth_data = []
        for skill in top_skills:
            skill_data = trend_df[trend_df['skill'] == skill]
            if len(skill_data) >= 2:
                start_demand = skill_data.iloc[0]['demand']
                end_demand = skill_data.iloc[-1]['demand']
                growth_rate = ((end_demand - start_demand) / start_demand) * 100
                growth_data.append({
                    'skill': skill,
                    'growth_rate': growth_rate,
                    'start_demand': start_demand,
                    'end_demand': end_demand
                })
        
        if growth_data:
            growth_df = pd.DataFrame(growth_data).sort_values('growth_rate', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Growth rate chart
                colors = ['green' if x > 0 else 'red' for x in growth_df['growth_rate']]
                fig_growth = px.bar(
                    growth_df,
                    x='skill',
                    y='growth_rate',
                    title="Year-over-Year Skill Growth (%)",
                    labels={'growth_rate': 'Growth Rate (%)', 'skill': 'Skill'}
                )
                fig_growth.update_traces(marker_color=colors)
                fig_growth.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_growth, use_container_width=True)
            
            with col2:
                st.subheader("Growth Leaders")
                for _, row in growth_df.head(10).iterrows():
                    delta_color = "normal" if row['growth_rate'] > 0 else "inverse"
                    st.metric(
                        label=row['skill'],
                        value=f"{row['end_demand']:.0f} jobs",
                        delta=f"{row['growth_rate']:+.1f}%"
                    )
    
    # Salary insights
    st.subheader("💰 Salary Insights by Skills")
    
    # Calculate average salary by skill
    skill_salary_data = []
    for _, row in filtered_data.iterrows():
        for skill in row['required_skills']:
            skill_salary_data.append({
                'skill': skill,
                'salary_max': row['salary_max'],
                'industry': row['industry']
            })
    
    if skill_salary_data:
        skill_salary_df = pd.DataFrame(skill_salary_data)
        
        # Get top skills by salary
        top_salary_skills = skill_salary_df.groupby('skill')['salary_max'].agg(['mean', 'count']).reset_index()
        top_salary_skills = top_salary_skills[top_salary_skills['count'] >= 3]  # Filter skills with at least 3 occurrences
        top_salary_skills = top_salary_skills.sort_values('mean', ascending=False).head(15)
        
        if not top_salary_skills.empty:
            fig_salary_skills = px.bar(
                top_salary_skills,
                x='mean',
                y='skill',
                orientation='h',
                title="Highest Paying Skills (Average Max Salary)",
                labels={'mean': 'Average Max Salary ($)', 'skill': 'Skill'}
            )
            fig_salary_skills.update_layout(height=500)
            st.plotly_chart(fig_salary_skills, use_container_width=True)
        else:
            st.info("Not enough data to show salary insights for skills.")

if __name__ == "__main__":
    main()
