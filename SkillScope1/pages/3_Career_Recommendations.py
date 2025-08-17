import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from mock_job_data import MockJobData
from skill_taxonomy import SkillTaxonomy

st.set_page_config(
    page_title="Career Recommendations - SkillScope",
    page_icon="🚀",
    layout="wide"
)

def get_career_path_data():
    """Generate career path progression data"""
    career_paths = {
        "Data Science": {
            "entry": ["Data Analyst", "Junior Data Scientist"],
            "mid": ["Data Scientist", "Senior Data Analyst", "Machine Learning Engineer"],
            "senior": ["Senior Data Scientist", "Principal Data Scientist", "Data Science Manager"],
            "executive": ["Head of Data Science", "Chief Data Officer", "VP of Analytics"]
        },
        "Software Engineering": {
            "entry": ["Junior Developer", "Software Engineer I"],
            "mid": ["Software Engineer", "Full Stack Developer", "Backend Developer"],
            "senior": ["Senior Software Engineer", "Tech Lead", "Staff Engineer"],
            "executive": ["Principal Engineer", "Engineering Manager", "VP of Engineering"]
        },
        "Product Management": {
            "entry": ["Associate Product Manager", "Product Analyst"],
            "mid": ["Product Manager", "Senior Product Analyst"],
            "senior": ["Senior Product Manager", "Principal Product Manager"],
            "executive": ["Director of Product", "VP of Product", "Chief Product Officer"]
        },
        "DevOps Engineering": {
            "entry": ["DevOps Engineer I", "Junior Site Reliability Engineer"],
            "mid": ["DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer"],
            "senior": ["Senior DevOps Engineer", "Principal SRE", "DevOps Architect"],
            "executive": ["Engineering Manager", "Director of Infrastructure", "VP of Engineering"]
        },
        "Cybersecurity": {
            "entry": ["Security Analyst I", "Junior Security Engineer"],
            "mid": ["Security Analyst", "Security Engineer", "Penetration Tester"],
            "senior": ["Senior Security Engineer", "Security Architect", "Lead Security Analyst"],
            "executive": ["Security Manager", "Director of Security", "Chief Information Security Officer"]
        }
    }
    return career_paths

def get_skill_requirements_by_role():
    """Get skill requirements for different roles"""
    skill_taxonomy = SkillTaxonomy()
    
    role_skills = {
        # Data Science roles
        "Data Analyst": ["Python", "SQL", "Excel", "Tableau", "Power BI", "Statistics", "Data Visualization"],
        "Junior Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Statistics", "Pandas", "Numpy"],
        "Data Scientist": ["Python", "R", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "SQL", "Statistics", "Git"],
        "Senior Data Scientist": ["Python", "R", "Machine Learning", "Deep Learning", "MLOps", "Docker", "Kubernetes", "Cloud Platforms", "Team Leadership"],
        "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "MLOps", "Docker", "Kubernetes", "Cloud Platforms", "CI/CD", "Model Deployment"],
        
        # Software Engineering roles
        "Junior Developer": ["Python", "JavaScript", "Git", "HTML", "CSS", "Basic Algorithms", "Database Fundamentals"],
        "Software Engineer": ["Python", "JavaScript", "Git", "React", "Node.js", "SQL", "REST APIs", "Testing"],
        "Full Stack Developer": ["JavaScript", "React", "Node.js", "Python", "SQL", "MongoDB", "REST APIs", "Docker", "Cloud Platforms"],
        "Senior Software Engineer": ["System Design", "Architecture", "Microservices", "Docker", "Kubernetes", "Cloud Platforms", "Team Leadership", "Code Review"],
        "Backend Developer": ["Python", "Java", "Node.js", "SQL", "NoSQL", "REST APIs", "Microservices", "Docker", "Cloud Platforms"],
        
        # Product Management roles
        "Associate Product Manager": ["Product Strategy", "Market Research", "Analytics", "SQL", "A/B Testing", "User Research", "Agile"],
        "Product Manager": ["Product Strategy", "Market Research", "Analytics", "SQL", "A/B Testing", "User Research", "Agile", "Roadmapping", "Stakeholder Management"],
        "Senior Product Manager": ["Product Strategy", "Market Research", "Advanced Analytics", "Data Analysis", "Leadership", "Cross-functional Collaboration", "Go-to-Market Strategy"],
        
        # DevOps roles
        "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform", "Ansible", "Linux", "Python", "Monitoring"],
        "Site Reliability Engineer": ["Kubernetes", "Docker", "Monitoring", "Alerting", "Python", "Go", "Linux", "Cloud Platforms", "Infrastructure as Code"],
        "Cloud Engineer": ["AWS", "Azure", "GCP", "Terraform", "Docker", "Kubernetes", "CI/CD", "Infrastructure as Code", "Networking"],
        
        # Cybersecurity roles
        "Security Analyst": ["Network Security", "Incident Response", "SIEM", "Vulnerability Assessment", "Security Frameworks", "Risk Analysis"],
        "Security Engineer": ["Network Security", "Application Security", "Penetration Testing", "Security Architecture", "Cryptography", "Security Tools"],
        "Penetration Tester": ["Ethical Hacking", "Vulnerability Assessment", "Penetration Testing Tools", "Network Security", "Web Application Security", "Report Writing"]
    }
    
    return role_skills

def calculate_skill_gap(current_skills, required_skills):
    """Calculate skill gap between current and required skills"""
    current_skills_lower = [skill.lower() for skill in current_skills]
    required_skills_lower = [skill.lower() for skill in required_skills]
    
    matching = [skill for skill in required_skills_lower if skill in current_skills_lower]
    missing = [skill for skill in required_skills_lower if skill not in current_skills_lower]
    
    return {
        'matching': matching,
        'missing': missing,
        'match_percentage': len(matching) / len(required_skills_lower) * 100 if required_skills_lower else 0
    }

def main():
    st.title("🚀 Career Recommendations")
    st.markdown("### Discover your ideal career path and skill development roadmap")
    
    # Load job data
    mock_data = MockJobData()
    job_data = mock_data.get_job_postings()
    
    # Career exploration section
    st.subheader("🎯 Career Path Explorer")
    
    # Two modes: explore careers or get specific recommendations
    mode = st.radio(
        "Choose your approach:",
        ["Explore Career Paths", "Get Personalized Recommendations"]
    )
    
    if mode == "Explore Career Paths":
        career_paths = get_career_path_data()
        
        st.subheader("📈 Career Progression Paths")
        
        # Career path selector
        selected_career = st.selectbox(
            "Select a career path to explore:",
            list(career_paths.keys())
        )
        
        if selected_career:
            path_data = career_paths[selected_career]
            role_skills = get_skill_requirements_by_role()
            
            # Display career progression
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(f"🛤️ {selected_career} Career Path")
                
                # Create progression visualization
                levels = ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
                level_keys = ["entry", "mid", "senior", "executive"]
                
                for i, (level, key) in enumerate(zip(levels, level_keys)):
                    st.markdown(f"### {level}")
                    
                    roles = path_data[key]
                    for role in roles:
                        with st.expander(f"👤 {role}"):
                            # Get skills for this role
                            skills = role_skills.get(role, ["Skills data not available"])
                            
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                st.write("**Key Skills Required:**")
                                for skill in skills[:10]:  # Show first 10 skills
                                    st.write(f"• {skill}")
                                if len(skills) > 10:
                                    st.write(f"... and {len(skills) - 10} more")
                            
                            with col_b:
                                # Find related jobs in our dataset
                                related_jobs = job_data[job_data['title'].str.contains(role, case=False, na=False)]
                                if not related_jobs.empty:
                                    avg_salary = related_jobs['salary_max'].mean()
                                    job_count = len(related_jobs)
                                    st.metric("Average Max Salary", f"${avg_salary:,.0f}")
                                    st.metric("Available Positions", job_count)
                                else:
                                    st.info("No current job postings found")
                    
                    if i < len(levels) - 1:
                        st.markdown("⬇️")
            
            with col2:
                st.subheader("📊 Path Overview")
                
                # Calculate total roles per level
                level_counts = {level: len(path_data[key]) for level, key in zip(levels, level_keys)}
                
                fig_levels = px.funnel(
                    x=list(level_counts.values()),
                    y=list(level_counts.keys()),
                    title="Roles per Career Level"
                )
                st.plotly_chart(fig_levels, use_container_width=True)
                
                # Skills frequency analysis
                all_path_skills = []
                for key in level_keys:
                    for role in path_data[key]:
                        skills = role_skills.get(role, [])
                        all_path_skills.extend(skills)
                
                if all_path_skills:
                    skill_counts = pd.Series(all_path_skills).value_counts().head(10)
                    
                    fig_skills = px.bar(
                        x=skill_counts.values,
                        y=skill_counts.index,
                        orientation='h',
                        title="Most Important Skills"
                    )
                    st.plotly_chart(fig_skills, use_container_width=True)
    
    else:  # Personalized recommendations mode
        st.subheader("🎯 Get Personalized Career Recommendations")
        
        # Input current information
        col1, col2 = st.columns(2)
        
        with col1:
            current_role = st.selectbox(
                "What's your current role?",
                ["Select your current role"] + sorted(job_data['title'].unique())
            )
            
            experience_level = st.selectbox(
                "Your experience level:",
                ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
            )
        
        with col2:
            target_industry = st.selectbox(
                "Target industry:",
                ["Any Industry"] + sorted(job_data['industry'].unique())
            )
            
            career_goal = st.selectbox(
                "Your career goal:",
                ["Higher salary", "More responsibility", "Technical leadership", "Management", "Specialization", "Industry change"]
            )
        
        # Current skills input
        st.subheader("📝 Your Current Skills")
        current_skills_input = st.text_area(
            "List your current skills (comma-separated):",
            placeholder="Python, SQL, Machine Learning, Project Management, etc."
        )
        
        current_skills = []
        if current_skills_input:
            current_skills = [skill.strip() for skill in current_skills_input.split(',') if skill.strip()]
        
        # Generate recommendations
        if st.button("🔍 Get My Career Recommendations", type="primary"):
            if current_skills and current_role != "Select your current role":
                with st.spinner("Analyzing career opportunities..."):
                    # Filter jobs based on criteria
                    recommended_jobs = job_data.copy()
                    
                    if target_industry != "Any Industry":
                        recommended_jobs = recommended_jobs[recommended_jobs['industry'] == target_industry]
                    
                    # Calculate skill matches for each job
                    job_recommendations = []
                    role_skills = get_skill_requirements_by_role()
                    
                    for _, job in recommended_jobs.iterrows():
                        job_required_skills = job['required_skills']
                        gap_analysis = calculate_skill_gap(current_skills, job_required_skills)
                        
                        # Get additional role-specific skills if available
                        role_specific_skills = role_skills.get(job['title'], [])
                        if role_specific_skills:
                            combined_gap = calculate_skill_gap(current_skills, job_required_skills + role_specific_skills)
                        else:
                            combined_gap = gap_analysis
                        
                        job_recommendations.append({
                            'title': job['title'],
                            'company': job['company'],
                            'industry': job['industry'],
                            'salary_max': job['salary_max'],
                            'experience_level': job['experience_level'],
                            'match_percentage': combined_gap['match_percentage'],
                            'missing_skills': combined_gap['missing'],
                            'required_skills': job_required_skills
                        })
                    
                    # Sort by match percentage and salary
                    job_recommendations.sort(key=lambda x: (x['match_percentage'], x['salary_max']), reverse=True)
                    
                    # Display recommendations
                    st.subheader("🏆 Recommended Career Opportunities")
                    
                    if job_recommendations:
                        # Show top 15 recommendations
                        for i, rec in enumerate(job_recommendations[:15]):
                            with st.expander(f"#{i+1} {rec['title']} - {rec['match_percentage']:.1f}% match"):
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.write("**Opportunity Details:**")
                                    st.write(f"• Company: {rec['company']}")
                                    st.write(f"• Industry: {rec['industry']}")
                                    st.write(f"• Experience: {rec['experience_level']}")
                                    st.write(f"• Max Salary: ${rec['salary_max']:,.0f}")
                                
                                with col2:
                                    st.write("**Why It's a Good Fit:**")
                                    st.write(f"• {rec['match_percentage']:.1f}% skill match")
                                    
                                    if rec['match_percentage'] > 70:
                                        st.write("🟢 Excellent match - you're ready to apply!")
                                    elif rec['match_percentage'] > 50:
                                        st.write("🟡 Good match - minimal skill gap")
                                    else:
                                        st.write("🔵 Growth opportunity - learn key skills")
                                
                                with col3:
                                    st.write("**Skills to Develop:**")
                                    if rec['missing_skills']:
                                        priority_skills = rec['missing_skills'][:5]  # Top 5 missing skills
                                        for skill in priority_skills:
                                            st.write(f"📚 {skill.title()}")
                                        if len(rec['missing_skills']) > 5:
                                            st.write(f"... and {len(rec['missing_skills']) - 5} more")
                                    else:
                                        st.write("🎉 You have all required skills!")
                    
                    # Skill development roadmap
                    st.markdown("---")
                    st.subheader("📚 Your Skill Development Roadmap")
                    
                    # Aggregate missing skills from top opportunities
                    all_missing_skills = []
                    for rec in job_recommendations[:10]:  # Top 10 opportunities
                        all_missing_skills.extend(rec['missing_skills'])
                    
                    if all_missing_skills:
                        skill_priority = pd.Series(all_missing_skills).value_counts().head(15)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Priority Skills to Learn:**")
                            for i, (skill, count) in enumerate(skill_priority.items()):
                                priority_level = "🔥 High" if count >= 5 else "🟡 Medium" if count >= 3 else "🔵 Low"
                                st.write(f"{i+1}. **{skill.title()}** - {priority_level}")
                                st.write(f"   📊 Needed for {count} opportunities")
                                st.write("")
                        
                        with col2:
                            fig_priorities = px.bar(
                                x=skill_priority.values,
                                y=skill_priority.index,
                                orientation='h',
                                title="Skills by Priority (# of opportunities)"
                            )
                            st.plotly_chart(fig_priorities, use_container_width=True)
                    
                    # Learning resources suggestions
                    st.subheader("🎓 Recommended Learning Resources")
                    
                    learning_resources = {
                        'python': 'Codecademy Python Course, Real Python, Python.org tutorial',
                        'machine learning': 'Coursera ML Course (Andrew Ng), Kaggle Learn, Fast.ai',
                        'sql': 'SQLBolt, W3Schools SQL, MySQL Tutorial',
                        'javascript': 'freeCodeCamp, MDN Web Docs, JavaScript.info',
                        'react': 'React Official Tutorial, freeCodeCamp React, Scrimba React',
                        'docker': 'Docker Official Tutorial, Docker Mastery Course, Play with Docker',
                        'aws': 'AWS Free Tier, A Cloud Guru, AWS Training',
                        'data analysis': 'Kaggle Learn, DataCamp, Coursera Data Analysis',
                        'project management': 'PMI, Coursera Project Management, Trello Academy'
                    }
                    
                    if all_missing_skills:
                        top_missing = skill_priority.head(5).index.tolist()
                        
                        for skill in top_missing:
                            skill_lower = skill.lower()
                            resources = learning_resources.get(skill_lower, f"Search for '{skill}' courses on Coursera, edX, or Udemy")
                            
                            with st.expander(f"📖 Learning {skill.title()}"):
                                st.write(f"**Recommended resources for {skill}:**")
                                st.write(resources)
                                st.write(f"\n**Estimated time to learn:** 2-8 weeks depending on depth")
                                st.write(f"**Difficulty:** Beginner to Intermediate")
            
            else:
                st.warning("Please provide your current skills and select your current role to get recommendations.")

if __name__ == "__main__":
    main()
