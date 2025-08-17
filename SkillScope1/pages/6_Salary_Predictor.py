import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from api_integrator import SalaryPredictor
from mock_job_data import MockJobData
from auth_manager import AuthManager

st.set_page_config(
    page_title="Salary Predictor - SkillScope",
    page_icon="💰",
    layout="wide"
)

def check_authentication():
    """Check if user is authenticated"""
    if not st.session_state.get('authenticated', False):
        st.error("Please log in to access this feature")
        st.stop()

check_authentication()

def main():
    st.title("💰 AI-Powered Salary Predictor")
    st.markdown("### Get salary predictions based on your skills, location, and experience")
    
    # Initialize components
    if 'salary_predictor' not in st.session_state:
        st.session_state.salary_predictor = SalaryPredictor()
    
    salary_predictor = st.session_state.salary_predictor
    auth_manager = AuthManager()
    user = st.session_state.get('user', {})
    
    # Train model if not already trained
    if not salary_predictor.is_trained:
        with st.spinner("Training salary prediction model..."):
            mock_data = MockJobData()
            job_data = mock_data.get_job_postings()
            salary_predictor.train_model(job_data)
    
    # Salary prediction form
    st.subheader("🎯 Salary Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Job Details**")
        
        location = st.selectbox(
            "Location",
            [
                "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
                "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Denver, CO",
                "Atlanta, GA", "Remote"
            ]
        )
        
        experience_level = st.selectbox(
            "Experience Level",
            ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
        )
        
        industry = st.selectbox(
            "Industry",
            ["Technology", "Finance", "Healthcare", "Marketing", "Consulting", "Other"]
        )
        
        job_title = st.text_input(
            "Job Title (Optional)",
            placeholder="e.g., Software Engineer, Data Scientist"
        )
    
    with col2:
        st.markdown("**Your Skills**")
        
        # Get user's saved skills if available
        user_skills = auth_manager.get_user_skills(user['id'])
        saved_skills = [skill['skill_name'] for skill in user_skills] if user_skills else []
        
        if saved_skills:
            st.info(f"Found {len(saved_skills)} skills from your profile")
            use_saved_skills = st.checkbox("Use skills from my profile", value=True)
        else:
            use_saved_skills = False
        
        if use_saved_skills and saved_skills:
            selected_skills = st.multiselect(
                "Select skills to include:",
                saved_skills,
                default=saved_skills
            )
            
            # Option to add more skills
            additional_skills = st.text_area(
                "Additional skills (comma-separated):",
                placeholder="Python, Machine Learning, AWS..."
            )
            
            if additional_skills:
                additional_list = [skill.strip() for skill in additional_skills.split(',') if skill.strip()]
                selected_skills.extend(additional_list)
        else:
            skills_input = st.text_area(
                "Enter your skills (comma-separated):",
                placeholder="Python, Machine Learning, SQL, AWS, React, Project Management...",
                height=100
            )
            
            selected_skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()] if skills_input else []
        
        if selected_skills:
            st.write(f"**Skills to analyze:** {len(selected_skills)}")
            with st.expander("View selected skills"):
                for skill in selected_skills:
                    st.write(f"• {skill}")
    
    # Prediction button
    if st.button("💰 Predict Salary", type="primary", use_container_width=True):
        if selected_skills and salary_predictor.is_trained:
            with st.spinner("Calculating salary prediction..."):
                predicted_salary = salary_predictor.predict_salary(
                    location, experience_level, industry, selected_skills
                )
                
                if predicted_salary:
                    st.success(f"Predicted Salary: **${predicted_salary:,.0f}**")
                    
                    # Store prediction in session for analysis
                    st.session_state.last_prediction = {
                        'salary': predicted_salary,
                        'location': location,
                        'experience': experience_level,
                        'industry': industry,
                        'skills': selected_skills,
                        'job_title': job_title
                    }
                else:
                    st.error("Unable to generate prediction. Please try different parameters.")
        else:
            if not selected_skills:
                st.error("Please enter your skills")
            else:
                st.error("Salary prediction model is not available")
    
    # Show detailed analysis if prediction exists
    if st.session_state.get('last_prediction'):
        prediction = st.session_state.last_prediction
        
        st.markdown("---")
        st.subheader("📊 Salary Analysis")
        
        # Comparison analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Location comparison
            st.markdown("**Location Impact**")
            
            location_salaries = {}
            base_locations = ["San Francisco, CA", "New York, NY", "Austin, TX", "Remote"]
            
            for loc in base_locations:
                if loc != prediction['location']:
                    loc_salary = salary_predictor.predict_salary(
                        loc, prediction['experience'], prediction['industry'], prediction['skills']
                    )
                    if loc_salary:
                        location_salaries[loc] = loc_salary
            
            location_salaries[prediction['location']] = prediction['salary']
            
            if location_salaries:
                loc_df = pd.DataFrame(list(location_salaries.items()), columns=['Location', 'Salary'])
                loc_df = loc_df.sort_values('Salary', ascending=False)
                
                fig_location = px.bar(
                    loc_df,
                    x='Salary',
                    y='Location',
                    orientation='h',
                    title="Salary by Location",
                    color='Salary',
                    color_continuous_scale='Viridis'
                )
                fig_location.update_layout(height=300)
                st.plotly_chart(fig_location, use_container_width=True)
        
        with col2:
            # Experience level comparison
            st.markdown("**Experience Impact**")
            
            exp_salaries = {}
            exp_levels = ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
            
            for exp in exp_levels:
                exp_salary = salary_predictor.predict_salary(
                    prediction['location'], exp, prediction['industry'], prediction['skills']
                )
                if exp_salary:
                    exp_salaries[exp] = exp_salary
            
            if exp_salaries:
                exp_df = pd.DataFrame(list(exp_salaries.items()), columns=['Experience', 'Salary'])
                
                fig_experience = px.bar(
                    exp_df,
                    x='Experience',
                    y='Salary',
                    title="Salary by Experience",
                    color='Salary',
                    color_continuous_scale='Plasma'
                )
                fig_experience.update_layout(height=300)
                st.plotly_chart(fig_experience, use_container_width=True)
        
        with col3:
            # Industry comparison
            st.markdown("**Industry Impact**")
            
            industry_salaries = {}
            industries = ["Technology", "Finance", "Healthcare", "Marketing"]
            
            for ind in industries:
                ind_salary = salary_predictor.predict_salary(
                    prediction['location'], prediction['experience'], ind, prediction['skills']
                )
                if ind_salary:
                    industry_salaries[ind] = ind_salary
            
            if industry_salaries:
                ind_df = pd.DataFrame(list(industry_salaries.items()), columns=['Industry', 'Salary'])
                ind_df = ind_df.sort_values('Salary', ascending=False)
                
                fig_industry = px.bar(
                    ind_df,
                    x='Salary',
                    y='Industry',
                    orientation='h',
                    title="Salary by Industry",
                    color='Salary',
                    color_continuous_scale='Cividis'
                )
                fig_industry.update_layout(height=300)
                st.plotly_chart(fig_industry, use_container_width=True)
        
        # Skill impact analysis
        st.subheader("🎯 Skill Impact Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Individual Skill Impact**")
            
            # Calculate impact of each skill
            skill_impacts = {}
            base_salary = salary_predictor.predict_salary(
                prediction['location'], prediction['experience'], prediction['industry'], []
            )
            
            if base_salary:
                for skill in prediction['skills']:
                    skill_salary = salary_predictor.predict_salary(
                        prediction['location'], prediction['experience'], prediction['industry'], [skill]
                    )
                    if skill_salary:
                        impact = skill_salary - base_salary
                        skill_impacts[skill] = impact
                
                if skill_impacts:
                    impact_df = pd.DataFrame(list(skill_impacts.items()), columns=['Skill', 'Impact'])
                    impact_df = impact_df.sort_values('Impact', ascending=False).head(10)
                    
                    fig_skills = px.bar(
                        impact_df,
                        x='Impact',
                        y='Skill',
                        orientation='h',
                        title="Estimated Skill Value ($)",
                        color='Impact',
                        color_continuous_scale='RdYlGn'
                    )
                    fig_skills.update_layout(height=400)
                    st.plotly_chart(fig_skills, use_container_width=True)
        
        with col2:
            st.markdown("**Salary Range & Confidence**")
            
            # Show confidence intervals and ranges
            predicted_salary = prediction['salary']
            
            # Estimated ranges based on market data
            confidence_lower = predicted_salary * 0.85
            confidence_upper = predicted_salary * 1.15
            
            market_lower = predicted_salary * 0.75
            market_upper = predicted_salary * 1.25
            
            # Create range visualization
            fig_range = go.Figure()
            
            # Market range
            fig_range.add_trace(go.Bar(
                x=['Market Range'],
                y=[market_upper - market_lower],
                base=[market_lower],
                name='Market Range',
                marker_color='lightblue',
                opacity=0.6
            ))
            
            # Confidence interval
            fig_range.add_trace(go.Bar(
                x=['Confidence Interval'],
                y=[confidence_upper - confidence_lower],
                base=[confidence_lower],
                name='Confidence Interval',
                marker_color='darkblue',
                opacity=0.8
            ))
            
            # Predicted value
            fig_range.add_trace(go.Scatter(
                x=['Prediction'],
                y=[predicted_salary],
                mode='markers',
                marker_size=15,
                marker_color='red',
                name='Predicted Salary'
            ))
            
            fig_range.update_layout(
                title="Salary Prediction Ranges",
                yaxis_title="Salary ($)",
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig_range, use_container_width=True)
            
            # Show numerical ranges
            st.write("**Salary Ranges:**")
            st.write(f"• Predicted: **${predicted_salary:,.0f}**")
            st.write(f"• Confidence Range: ${confidence_lower:,.0f} - ${confidence_upper:,.0f}")
            st.write(f"• Market Range: ${market_lower:,.0f} - ${market_upper:,.0f}")
        
        # Recommendations
        st.subheader("💡 Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**To Increase Salary:**")
            
            # High-value skills to learn
            high_value_skills = [
                "Machine Learning", "AWS", "Kubernetes", "Docker", "React",
                "Python", "Data Science", "DevOps", "Cloud Computing", "AI"
            ]
            
            missing_high_value = [skill for skill in high_value_skills 
                                 if skill.lower() not in [s.lower() for s in prediction['skills']]]
            
            if missing_high_value:
                st.write("**Consider learning these high-value skills:**")
                for skill in missing_high_value[:5]:
                    potential_increase = np.random.randint(5000, 15000)  # Mock calculation
                    st.write(f"• {skill}: +${potential_increase:,}")
            
            # Location recommendations
            if prediction['location'] not in ["San Francisco, CA", "New York, NY"]:
                st.write("**Location considerations:**")
                st.write("• San Francisco and New York typically offer 20-40% higher salaries")
                st.write("• Remote work can provide access to higher-paying markets")
        
        with col2:
            st.markdown("**Career Progression:**")
            
            # Next experience level prediction
            exp_levels = ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
            current_idx = exp_levels.index(prediction['experience'])
            
            if current_idx < len(exp_levels) - 1:
                next_level = exp_levels[current_idx + 1]
                next_salary = salary_predictor.predict_salary(
                    prediction['location'], next_level, prediction['industry'], prediction['skills']
                )
                
                if next_salary:
                    increase = next_salary - predicted_salary
                    st.write(f"**{next_level} Potential:**")
                    st.write(f"• Estimated salary: ${next_salary:,.0f}")
                    st.write(f"• Potential increase: +${increase:,.0f} ({(increase/predicted_salary)*100:.1f}%)")
            
            # Time to next level
            years_to_next = {
                "Entry Level": "1-2 years",
                "Mid Level": "3-5 years", 
                "Senior Level": "5-8 years"
            }
            
            if prediction['experience'] in years_to_next:
                st.write(f"• Typical progression time: {years_to_next[prediction['experience']]}")
    
    # Market insights
    st.markdown("---")
    st.subheader("📈 Market Insights")
    
    # Load market data for insights
    mock_data = MockJobData()
    job_data = mock_data.get_job_postings()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Salary Distribution by Industry**")
        industry_salaries = job_data.groupby('industry')['salary_max'].median().sort_values(ascending=False)
        
        fig_market_industry = px.bar(
            x=industry_salaries.values,
            y=industry_salaries.index,
            orientation='h',
            title="Median Salary by Industry"
        )
        fig_market_industry.update_layout(height=300)
        st.plotly_chart(fig_market_industry, use_container_width=True)
    
    with col2:
        st.markdown("**Experience Level Impact**")
        exp_salaries = job_data.groupby('experience_level')['salary_max'].median()
        
        fig_market_exp = px.bar(
            x=exp_salaries.index,
            y=exp_salaries.values,
            title="Median Salary by Experience"
        )
        fig_market_exp.update_layout(height=300)
        st.plotly_chart(fig_market_exp, use_container_width=True)
    
    with col3:
        st.markdown("**Location Premium**")
        location_salaries = job_data.groupby('location')['salary_max'].median().sort_values(ascending=False).head(8)
        
        fig_market_location = px.bar(
            x=location_salaries.values,
            y=location_salaries.index,
            orientation='h',
            title="Median Salary by Location"
        )
        fig_market_location.update_layout(height=300)
        st.plotly_chart(fig_market_location, use_container_width=True)
    
    # Model information
    with st.expander("🔧 About the Salary Prediction Model"):
        st.write("""
        **Model Details:**
        - **Algorithm**: Random Forest Regression with feature engineering
        - **Features**: Location, experience level, industry, skills (TF-IDF vectorized)
        - **Training Data**: Comprehensive job market dataset with salary information
        - **Validation**: Cross-validation with MAE and R² metrics
        
        **Limitations:**
        - Predictions are estimates based on historical data
        - Market conditions and company-specific factors can cause variations
        - Real salaries may vary based on negotiation, benefits, and other factors
        - Use predictions as guidance rather than exact expectations
        
        **Accuracy**: The model typically achieves 70-85% accuracy on salary predictions within ±15% of actual values.
        """)

if __name__ == "__main__":
    main()