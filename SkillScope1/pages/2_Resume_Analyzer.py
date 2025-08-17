import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from io import StringIO
import re

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from nlp_processor import NLPProcessor
from skill_extractor import SkillExtractor
from mock_job_data import MockJobData
from skill_taxonomy import SkillTaxonomy

st.set_page_config(
    page_title="Resume Analyzer - SkillScope",
    page_icon="📄",
    layout="wide"
)

def extract_text_from_uploaded_file(uploaded_file):
    """Extract text from uploaded file"""
    if uploaded_file.type == "text/plain":
        return str(uploaded_file.read(), "utf-8")
    elif uploaded_file.type == "application/pdf":
        try:
            # For PDF files, we'll provide a simple text extraction
            # In a real implementation, you'd use PyPDF2 or similar
            st.warning("PDF parsing is simplified for this demo. Please copy and paste your resume text instead.")
            return ""
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
    else:
        st.error("Unsupported file type. Please upload a .txt or .pdf file, or paste your resume text.")
        return ""

def analyze_resume_skills(resume_text):
    """Analyze resume and extract skills"""
    skill_extractor = SkillExtractor()
    nlp_processor = NLPProcessor()
    
    # Extract skills from resume
    extracted_skills = skill_extractor.extract_skills_from_text(resume_text)
    
    # Get skill categories
    skill_taxonomy = SkillTaxonomy()
    categorized_skills = skill_taxonomy.categorize_skills(extracted_skills)
    
    return extracted_skills, categorized_skills

def get_skill_gap_analysis(user_skills, target_job_skills):
    """Analyze skill gaps between user and target job"""
    user_skills_set = set([skill.lower() for skill in user_skills])
    target_skills_set = set([skill.lower() for skill in target_job_skills])
    
    matching_skills = user_skills_set.intersection(target_skills_set)
    missing_skills = target_skills_set - user_skills_set
    additional_skills = user_skills_set - target_skills_set
    
    return {
        'matching': list(matching_skills),
        'missing': list(missing_skills),
        'additional': list(additional_skills),
        'match_percentage': len(matching_skills) / len(target_skills_set) * 100 if target_skills_set else 0
    }

def main():
    st.title("📄 Resume Analyzer")
    st.markdown("### Upload your resume and discover skill gaps and opportunities")
    
    # Resume input section
    st.subheader("📤 Submit Your Resume")
    
    input_method = st.radio(
        "Choose input method:",
        ["Paste resume text", "Upload file"]
    )
    
    resume_text = ""
    
    if input_method == "Upload file":
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'pdf'],
            help="Upload your resume in .txt or .pdf format"
        )
        
        if uploaded_file is not None:
            resume_text = extract_text_from_uploaded_file(uploaded_file)
    else:
        resume_text = st.text_area(
            "Paste your resume text here:",
            height=300,
            placeholder="Copy and paste your resume content here..."
        )
    
    if resume_text and len(resume_text.strip()) > 50:
        st.success("✅ Resume loaded successfully!")
        
        # Analyze button
        if st.button("🔍 Analyze Resume", type="primary"):
            with st.spinner("Analyzing your resume..."):
                # Extract skills from resume
                user_skills, categorized_skills = analyze_resume_skills(resume_text)
                
                if user_skills:
                    st.session_state.user_skills = user_skills
                    st.session_state.categorized_skills = categorized_skills
                    st.session_state.resume_analyzed = True
                else:
                    st.warning("No skills detected in your resume. Please check your resume content.")
                    return
    
    # Display analysis results if available
    if hasattr(st.session_state, 'resume_analyzed') and st.session_state.resume_analyzed:
        st.markdown("---")
        st.subheader("🎯 Your Skills Analysis")
        
        user_skills = st.session_state.user_skills
        categorized_skills = st.session_state.categorized_skills
        
        # Display extracted skills
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Detected Skills")
            
            if categorized_skills:
                for category, skills in categorized_skills.items():
                    if skills:
                        st.write(f"**{category}:**")
                        for skill in skills:
                            st.write(f"• {skill}")
                        st.write("")
            else:
                st.write("Skills detected:")
                for skill in user_skills:
                    st.write(f"• {skill}")
        
        with col2:
            st.subheader("📊 Skills Overview")
            
            # Skills count by category
            if categorized_skills:
                category_counts = {cat: len(skills) for cat, skills in categorized_skills.items() if skills}
                
                if category_counts:
                    import plotly.express as px
                    fig = px.pie(
                        values=list(category_counts.values()),
                        names=list(category_counts.keys()),
                        title="Skills Distribution by Category"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Total skills metric
            st.metric("Total Skills Detected", len(user_skills))
        
        # Job matching section
        st.markdown("---")
        st.subheader("🎯 Job Matching & Skill Gap Analysis")
        
        # Load job data for matching
        mock_data = MockJobData()
        job_data = mock_data.get_job_postings()
        
        # Industry and job title filters
        col1, col2 = st.columns(2)
        
        with col1:
            selected_industry = st.selectbox(
                "Select target industry:",
                ["All Industries"] + sorted(job_data['industry'].unique())
            )
        
        with col2:
            # Filter jobs by industry
            if selected_industry != "All Industries":
                filtered_jobs = job_data[job_data['industry'] == selected_industry]
            else:
                filtered_jobs = job_data
            
            job_titles = sorted(filtered_jobs['title'].unique())
            selected_job_title = st.selectbox(
                "Select target job title:",
                ["Any Job Title"] + job_titles
            )
        
        # Perform job matching
        if st.button("🔍 Find Matching Jobs", type="secondary"):
            with st.spinner("Analyzing job matches..."):
                # Filter jobs based on selection
                target_jobs = filtered_jobs.copy()
                if selected_job_title != "Any Job Title":
                    target_jobs = target_jobs[target_jobs['title'] == selected_job_title]
                
                # Calculate match scores for each job
                job_matches = []
                for _, job in target_jobs.iterrows():
                    gap_analysis = get_skill_gap_analysis(user_skills, job['required_skills'])
                    job_matches.append({
                        'title': job['title'],
                        'company': job['company'],
                        'industry': job['industry'],
                        'location': job['location'],
                        'salary_max': job['salary_max'],
                        'experience_level': job['experience_level'],
                        'match_percentage': gap_analysis['match_percentage'],
                        'matching_skills': gap_analysis['matching'],
                        'missing_skills': gap_analysis['missing'],
                        'required_skills': job['required_skills']
                    })
                
                # Sort by match percentage
                job_matches.sort(key=lambda x: x['match_percentage'], reverse=True)
                
                # Display top matches
                st.subheader("🏆 Top Job Matches")
                
                if job_matches:
                    # Show top 10 matches
                    for i, match in enumerate(job_matches[:10]):
                        with st.expander(f"#{i+1} {match['title']} at {match['company']} - {match['match_percentage']:.1f}% match"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write("**Job Details:**")
                                st.write(f"• Industry: {match['industry']}")
                                st.write(f"• Location: {match['location']}")
                                st.write(f"• Experience: {match['experience_level']}")
                                st.write(f"• Max Salary: ${match['salary_max']:,.0f}")
                            
                            with col2:
                                st.write("**Matching Skills:**")
                                if match['matching_skills']:
                                    for skill in match['matching_skills'][:10]:  # Show top 10
                                        st.write(f"✅ {skill.title()}")
                                    if len(match['matching_skills']) > 10:
                                        st.write(f"... and {len(match['matching_skills']) - 10} more")
                                else:
                                    st.write("No direct skill matches found")
                            
                            with col3:
                                st.write("**Skills to Learn:**")
                                if match['missing_skills']:
                                    for skill in match['missing_skills'][:10]:  # Show top 10
                                        st.write(f"📚 {skill.title()}")
                                    if len(match['missing_skills']) > 10:
                                        st.write(f"... and {len(match['missing_skills']) - 10} more")
                                else:
                                    st.write("🎉 You have all required skills!")
                            
                            # Progress bar for match percentage
                            st.progress(match['match_percentage'] / 100)
                else:
                    st.info("No matching jobs found with your current criteria.")
        
        # Skill recommendations section
        st.markdown("---")
        st.subheader("📚 Skill Recommendations")
        
        # Get industry-specific skill recommendations
        if selected_industry != "All Industries":
            industry_jobs = job_data[job_data['industry'] == selected_industry]
        else:
            industry_jobs = job_data
        
        # Extract all skills from target industry
        industry_skills = []
        for skills in industry_jobs['required_skills']:
            industry_skills.extend(skills)
        
        # Count skill frequency
        skill_counts = pd.Series(industry_skills).value_counts()
        
        # Find skills user doesn't have but are popular in target industry
        user_skills_lower = [skill.lower() for skill in user_skills]
        recommended_skills = []
        
        for skill, count in skill_counts.items():
            if skill.lower() not in user_skills_lower:
                recommended_skills.append({
                    'skill': skill,
                    'demand': count,
                    'percentage': (count / len(industry_jobs)) * 100
                })
        
        # Sort by demand
        recommended_skills.sort(key=lambda x: x['demand'], reverse=True)
        
        if recommended_skills:
            st.write(f"**Top skills to learn for {selected_industry if selected_industry != 'All Industries' else 'the job market'}:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top recommended skills
                for i, rec in enumerate(recommended_skills[:15]):
                    priority = "🔥 High" if rec['percentage'] > 30 else "🟡 Medium" if rec['percentage'] > 15 else "🔵 Low"
                    st.write(f"{i+1}. **{rec['skill']}** - {priority} Priority")
                    st.write(f"   📊 Found in {rec['demand']} jobs ({rec['percentage']:.1f}%)")
                    st.write("")
            
            with col2:
                # Visualization of skill demand
                import plotly.express as px
                
                top_recommendations = recommended_skills[:10]
                skills = [r['skill'] for r in top_recommendations]
                demands = [r['demand'] for r in top_recommendations]
                
                fig = px.bar(
                    x=demands,
                    y=skills,
                    orientation='h',
                    title="Top Skills to Learn (by Demand)",
                    labels={'x': 'Number of Job Postings', 'y': 'Skills'}
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("You already have most of the in-demand skills for this industry!")
    
    elif resume_text and len(resume_text.strip()) <= 50:
        st.warning("⚠️ Please provide a more detailed resume (at least 50 characters)")
    
    else:
        # Instructions when no resume is provided
        st.info("👆 Please upload your resume or paste your resume text to get started with the analysis.")
        
        st.markdown("### 💡 Tips for better analysis:")
        st.markdown("""
        - Include your technical skills, programming languages, and tools
        - Mention your work experience and projects
        - Add education and certifications
        - Use clear formatting and avoid special characters
        - Include both hard skills (technical) and soft skills
        """)

if __name__ == "__main__":
    main()
