import streamlit as st
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from auth_manager import AuthManager

# Page configuration
st.set_page_config(
    page_title="SkillScope - Login",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
                        'signup_date': st.session_state.get('signup_date', None)
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

def main():
    """Main login page"""
    
    # Check if user is already authenticated
    if st.session_state.get('authenticated', False):
        # Redirect to main app
        st.success("You are already logged in!")
        if st.button("Go to Dashboard", type="primary"):
            # Since this is already the main dashboard logic, just rerun
            st.rerun()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Logout", use_container_width=True):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        return
    
    # Show app title and description
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
    
    # Features section
    st.markdown("---")
    st.markdown("### ✨ Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📊 Industry Trends**
        - Real-time job market analysis
        - Skill demand tracking
        - Salary insights
        """)
    
    with col2:
        st.markdown("""
        **📄 Resume Analysis**
        - Skill gap identification
        - Job matching
        - Personalized recommendations
        """)
    
    with col3:
        st.markdown("""
        **🚀 Career Guidance**
        - Career path exploration
        - Skill development roadmap
        - Market predictions
        """)

if __name__ == "__main__":
    main()