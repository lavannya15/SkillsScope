import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional, Any
import os

class JobAPIIntegrator:
    """Integrate with real-time job APIs like Indeed and Adzuna"""
    
    def __init__(self):
        # API credentials would be stored as secrets
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID')
        self.adzuna_api_key = os.getenv('ADZUNA_API_KEY')
        self.indeed_api_key = os.getenv('INDEED_API_KEY')
        
        # API endpoints
        self.adzuna_base_url = "https://api.adzuna.com/v1/api/jobs/us"
        self.indeed_base_url = "https://api.indeed.com/ads/apisearch"
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum seconds between requests
    
    def rate_limit(self):
        """Implement rate limiting for API requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        
        self.last_request_time = time.time()
    
    def search_adzuna_jobs(self, 
                          query: str = "", 
                          location: str = "", 
                          category: str = "",
                          salary_min: int = None,
                          salary_max: int = None,
                          max_results: int = 50) -> List[Dict[str, Any]]:
        """Search jobs using Adzuna API"""
        
        if not self.adzuna_app_id or not self.adzuna_api_key:
            st.warning("Adzuna API credentials not configured. Please add ADZUNA_APP_ID and ADZUNA_API_KEY to your secrets.")
            return self._get_mock_api_data(query, location, max_results)
        
        try:
            self.rate_limit()
            
            # Build search parameters
            params = {
                'app_id': self.adzuna_app_id,
                'app_key': self.adzuna_api_key,
                'results_per_page': min(max_results, 50),  # API limit
                'what': query,
                'where': location,
                'content-type': 'application/json'
            }
            
            if salary_min:
                params['salary_min'] = salary_min
            if salary_max:
                params['salary_max'] = salary_max
            if category:
                params['category'] = category
            
            # Make API request
            url = f"{self.adzuna_base_url}/search/1"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = []
            
            for job in data.get('results', []):
                job_data = {
                    'id': job.get('id'),
                    'title': job.get('title', ''),
                    'company': job.get('company', {}).get('display_name', ''),
                    'location': job.get('location', {}).get('display_name', ''),
                    'description': job.get('description', ''),
                    'salary_min': job.get('salary_min'),
                    'salary_max': job.get('salary_max'),
                    'created_date': job.get('created'),
                    'url': job.get('redirect_url', ''),
                    'source': 'Adzuna',
                    'contract_type': job.get('contract_type'),
                    'category': job.get('category', {}).get('label', '')
                }
                jobs.append(job_data)
            
            return jobs
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching jobs from Adzuna: {e}")
            return self._get_mock_api_data(query, location, max_results)
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return self._get_mock_api_data(query, location, max_results)
    
    def search_indeed_jobs(self, 
                          query: str = "", 
                          location: str = "",
                          job_type: str = "",
                          salary: str = "",
                          max_results: int = 25) -> List[Dict[str, Any]]:
        """Search jobs using Indeed API (Note: Indeed has restricted API access)"""
        
        if not self.indeed_api_key:
            st.warning("Indeed API credentials not configured. Using enhanced mock data.")
            return self._get_mock_api_data(query, location, max_results, source="Indeed")
        
        try:
            self.rate_limit()
            
            params = {
                'publisher': self.indeed_api_key,
                'q': query,
                'l': location,
                'sort': 'date',
                'radius': 25,
                'st': 'jobsite',
                'jt': job_type,
                'start': 0,
                'limit': min(max_results, 25),  # API limit
                'format': 'json',
                'v': '2'
            }
            
            if salary:
                params['salary'] = salary
            
            response = requests.get(self.indeed_base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = []
            
            for job in data.get('results', []):
                job_data = {
                    'id': job.get('jobkey'),
                    'title': job.get('jobtitle', ''),
                    'company': job.get('company', ''),
                    'location': job.get('formattedLocation', ''),
                    'description': job.get('snippet', ''),
                    'salary_min': None,  # Indeed doesn't provide structured salary data
                    'salary_max': None,
                    'created_date': job.get('date'),
                    'url': job.get('url', ''),
                    'source': 'Indeed',
                    'contract_type': job.get('formattedRelativeTime'),
                    'category': ''
                }
                jobs.append(job_data)
            
            return jobs
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching jobs from Indeed: {e}")
            return self._get_mock_api_data(query, location, max_results, source="Indeed")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return self._get_mock_api_data(query, location, max_results, source="Indeed")
    
    def _get_mock_api_data(self, query: str, location: str, max_results: int, source: str = "API") -> List[Dict[str, Any]]:
        """Generate realistic mock API data when real APIs are not available"""
        
        # Enhanced mock companies by industry
        tech_companies = ["Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Uber", "Airbnb", "Spotify", "Salesforce", "Adobe", "Nvidia"]
        finance_companies = ["Goldman Sachs", "JPMorgan", "Bank of America", "Citigroup", "Wells Fargo", "Morgan Stanley", "BlackRock", "Vanguard"]
        healthcare_companies = ["Johnson & Johnson", "Pfizer", "Moderna", "Novartis", "Roche", "Merck", "CVS Health", "UnitedHealth"]
        consulting_companies = ["McKinsey", "BCG", "Deloitte", "PwC", "EY", "Accenture", "Bain & Company"]
        
        # Job titles based on query
        tech_roles = ["Software Engineer", "Data Scientist", "DevOps Engineer", "Product Manager", "Frontend Developer", "Backend Developer", "ML Engineer"]
        finance_roles = ["Financial Analyst", "Investment Banker", "Risk Analyst", "Quantitative Analyst", "Portfolio Manager"]
        healthcare_roles = ["Clinical Data Analyst", "Healthcare Data Scientist", "Biostatistician", "Medical Affairs Specialist"]
        consulting_roles = ["Management Consultant", "Strategy Consultant", "Business Analyst", "Operations Consultant"]
        
        # Determine industry based on query
        if any(term in query.lower() for term in ['software', 'developer', 'engineer', 'tech', 'data scientist', 'python', 'javascript']):
            companies = tech_companies
            roles = tech_roles
            industry = "Technology"
        elif any(term in query.lower() for term in ['finance', 'analyst', 'banking', 'investment', 'trading']):
            companies = finance_companies
            roles = finance_roles
            industry = "Finance"
        elif any(term in query.lower() for term in ['healthcare', 'clinical', 'medical', 'pharma', 'biostat']):
            companies = healthcare_companies
            roles = healthcare_roles
            industry = "Healthcare"
        elif any(term in query.lower() for term in ['consultant', 'consulting', 'strategy', 'management']):
            companies = consulting_companies
            roles = consulting_roles
            industry = "Consulting"
        else:
            companies = tech_companies + finance_companies[:3]
            roles = tech_roles + finance_roles[:3]
            industry = "Technology"
        
        # Generate locations
        locations = [
            "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
            "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Denver, CO",
            "Atlanta, GA", "Remote", "Hybrid"
        ]
        
        if location:
            locations = [location] + [loc for loc in locations if loc != location]
        
        jobs = []
        np.random.seed(42)  # For consistent results
        
        for i in range(min(max_results, 50)):
            company = np.random.choice(companies)
            role = np.random.choice(roles)
            job_location = np.random.choice(locations[:5])  # Prefer top locations
            
            # Generate realistic salary based on role and location
            base_salaries = {
                "Software Engineer": (100000, 180000),
                "Data Scientist": (110000, 190000),
                "DevOps Engineer": (105000, 175000),
                "Product Manager": (120000, 200000),
                "Financial Analyst": (70000, 120000),
                "Investment Banker": (120000, 250000),
                "Clinical Data Analyst": (75000, 130000),
                "Management Consultant": (100000, 160000)
            }
            
            salary_range = base_salaries.get(role, (80000, 140000))
            location_multiplier = 1.3 if "San Francisco" in job_location or "New York" in job_location else 1.0
            
            salary_min = int(salary_range[0] * location_multiplier)
            salary_max = int(salary_range[1] * location_multiplier)
            
            # Generate realistic job description
            descriptions = [
                f"We are seeking a talented {role} to join our growing team at {company}. The ideal candidate will have experience with relevant technologies and a passion for innovation.",
                f"Join {company} as a {role} and help shape the future of {industry.lower()}. This role offers excellent growth opportunities and competitive compensation.",
                f"Exciting opportunity for a {role} at {company}. Work on cutting-edge projects with a collaborative team in a fast-paced environment.",
                f"{company} is looking for an experienced {role} to drive our {industry.lower()} initiatives forward. Remote and hybrid options available."
            ]
            
            created_date = datetime.now() - timedelta(days=np.random.randint(1, 30))
            
            job_data = {
                'id': f"mock_{source.lower()}_{i+1}_{int(time.time())}",
                'title': role,
                'company': company,
                'location': job_location,
                'description': np.random.choice(descriptions),
                'salary_min': salary_min,
                'salary_max': salary_max,
                'created_date': created_date.isoformat(),
                'url': f"https://example.com/jobs/{company.lower().replace(' ', '-')}-{role.lower().replace(' ', '-')}-{i+1}",
                'source': f"{source} (Mock Data)",
                'contract_type': np.random.choice(['Full-time', 'Contract', 'Part-time']),
                'category': industry
            }
            
            jobs.append(job_data)
        
        return jobs
    
    def extract_skills_from_job_data(self, jobs: List[Dict[str, Any]]) -> Dict[str, int]:
        """Extract and count skills from job descriptions"""
        from .skill_extractor import SkillExtractor
        
        skill_extractor = SkillExtractor()
        skill_counts = {}
        
        for job in jobs:
            description = job.get('description', '') + ' ' + job.get('title', '')
            skills = skill_extractor.extract_skills_from_text(description)
            
            for skill in skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        return skill_counts
    
    def search_all_sources(self, 
                          query: str = "", 
                          location: str = "",
                          max_results_per_source: int = 25) -> List[Dict[str, Any]]:
        """Search jobs from all available sources"""
        
        all_jobs = []
        
        # Search Adzuna
        adzuna_jobs = self.search_adzuna_jobs(query, location, max_results=max_results_per_source)
        all_jobs.extend(adzuna_jobs)
        
        # Search Indeed
        indeed_jobs = self.search_indeed_jobs(query, location, max_results=max_results_per_source)
        all_jobs.extend(indeed_jobs)
        
        # Remove duplicates based on title and company
        seen = set()
        unique_jobs = []
        
        for job in all_jobs:
            job_key = (job.get('title', '').lower(), job.get('company', '').lower())
            if job_key not in seen:
                seen.add(job_key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def get_trending_skills(self, timeframe_days: int = 30) -> Dict[str, Any]:
        """Get trending skills based on recent job postings"""
        
        # Search for recent jobs across popular queries
        trending_queries = [
            "software engineer", "data scientist", "product manager", 
            "devops engineer", "machine learning", "python developer",
            "financial analyst", "marketing manager"
        ]
        
        all_skills = {}
        total_jobs = 0
        
        for query in trending_queries:
            jobs = self.search_all_sources(query, max_results_per_source=10)
            skills = self.extract_skills_from_job_data(jobs)
            
            for skill, count in skills.items():
                all_skills[skill] = all_skills.get(skill, 0) + count
            
            total_jobs += len(jobs)
        
        # Calculate trend scores
        trending_skills = {
            'skills': dict(sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:20]),
            'total_jobs_analyzed': total_jobs,
            'analysis_date': datetime.now().isoformat(),
            'timeframe_days': timeframe_days
        }
        
        return trending_skills


class SalaryPredictor:
    """Predict salaries based on skills, location, and experience"""
    
    def __init__(self):
        self.model = None
        self.feature_encoder = None
        self.is_trained = False
        
    def prepare_training_data(self, job_data: pd.DataFrame) -> tuple:
        """Prepare data for salary prediction model"""
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        # Extract features
        features = []
        salaries = []
        
        for _, job in job_data.iterrows():
            if job['salary_max'] and job['salary_max'] > 0:
                # Create feature vector
                feature_dict = {
                    'location': job.get('location', ''),
                    'experience_level': job.get('experience_level', 'Mid Level'),
                    'industry': job.get('industry', ''),
                    'company_size': job.get('company_size', 'Medium'),
                    'skills': ' '.join(job.get('required_skills', []))
                }
                
                features.append(feature_dict)
                salaries.append(job['salary_max'])
        
        return features, salaries
    
    def train_model(self, job_data: pd.DataFrame):
        """Train salary prediction model"""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import LabelEncoder
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_absolute_error, r2_score
        
        try:
            features, salaries = self.prepare_training_data(job_data)
            
            if len(features) < 10:
                st.warning("Insufficient data for training salary prediction model")
                return
            
            # Create feature matrix
            feature_matrix = []
            location_encoder = LabelEncoder()
            experience_encoder = LabelEncoder()
            industry_encoder = LabelEncoder()
            
            # Encode categorical features
            locations = [f['location'] for f in features]
            experiences = [f['experience_level'] for f in features]
            industries = [f['industry'] for f in features]
            skills_text = [f['skills'] for f in features]
            
            location_encoded = location_encoder.fit_transform(locations)
            experience_encoded = experience_encoder.fit_transform(experiences)
            industry_encoded = industry_encoder.fit_transform(industries)
            
            # Vectorize skills
            skills_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            skills_matrix = skills_vectorizer.fit_transform(skills_text).toarray()
            
            # Combine features
            for i in range(len(features)):
                feature_vector = [
                    location_encoded[i],
                    experience_encoded[i], 
                    industry_encoded[i]
                ] + list(skills_matrix[i])
                feature_matrix.append(feature_vector)
            
            # Train model
            X = np.array(feature_matrix)
            y = np.array(salaries)
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Store encoders for prediction
            self.encoders = {
                'location': location_encoder,
                'experience': experience_encoder,
                'industry': industry_encoder,
                'skills': skills_vectorizer
            }
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            st.success(f"Salary prediction model trained successfully! MAE: ${mae:,.0f}, R²: {r2:.3f}")
            self.is_trained = True
            
        except Exception as e:
            st.error(f"Error training salary model: {e}")
    
    def predict_salary(self, location: str, experience_level: str, industry: str, skills: List[str]) -> Optional[float]:
        """Predict salary based on features"""
        if not self.is_trained or not self.model:
            return None
        
        try:
            # Encode features
            location_encoded = self.encoders['location'].transform([location])[0]
            experience_encoded = self.encoders['experience'].transform([experience_level])[0]
            industry_encoded = self.encoders['industry'].transform([industry])[0]
            
            skills_text = ' '.join(skills)
            skills_encoded = self.encoders['skills'].transform([skills_text]).toarray()[0]
            
            # Create feature vector
            feature_vector = [location_encoded, experience_encoded, industry_encoded] + list(skills_encoded)
            feature_vector = np.array(feature_vector).reshape(1, -1)
            
            # Predict
            predicted_salary = self.model.predict(feature_vector)[0]
            return max(predicted_salary, 30000)  # Minimum salary floor
            
        except Exception as e:
            st.error(f"Error predicting salary: {e}")
            return None