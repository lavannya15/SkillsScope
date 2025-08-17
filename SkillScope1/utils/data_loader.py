import pandas as pd
import numpy as np
import os
import sys

class DataLoader:
    """Class to handle loading and processing of job market data"""
    
    def __init__(self):
        self.job_data = None
        self.skills_data = None
        self.processed = False
    
    def load_mock_data(self):
        """Load mock job posting data for demonstration"""
        # This would normally load from Kaggle datasets or APIs
        # For now, we'll create realistic mock data
        
        np.random.seed(42)  # For reproducible results
        
        # Define realistic job data structure
        companies = [
            "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Tesla",
            "Goldman Sachs", "JPMorgan", "Bank of America", "Citigroup",
            "Johnson & Johnson", "Pfizer", "Moderna", "CVS Health",
            "McKinsey", "BCG", "Deloitte", "PwC", "EY"
        ]
        
        industries = ["Technology", "Finance", "Healthcare", "Consulting"]
        
        tech_roles = [
            "Software Engineer", "Data Scientist", "Machine Learning Engineer",
            "DevOps Engineer", "Frontend Developer", "Backend Developer",
            "Full Stack Developer", "Data Analyst", "Product Manager",
            "UI/UX Designer", "Security Engineer", "Cloud Engineer"
        ]
        
        finance_roles = [
            "Financial Analyst", "Investment Banker", "Risk Analyst",
            "Quantitative Analyst", "Portfolio Manager", "Trading Analyst",
            "Credit Analyst", "Financial Consultant", "Compliance Officer"
        ]
        
        healthcare_roles = [
            "Data Analyst", "Healthcare Consultant", "Clinical Research Associate",
            "Biostatistician", "Health Informatics Specialist", "Medical Coder",
            "Healthcare Data Scientist", "Clinical Data Manager"
        ]
        
        consulting_roles = [
            "Management Consultant", "Strategy Consultant", "Business Analyst",
            "Operations Consultant", "IT Consultant", "Digital Transformation Consultant"
        ]
        
        # Create job postings
        job_postings = []
        
        for i in range(1000):  # Generate 1000 job postings
            # Select industry and corresponding roles
            industry = np.random.choice(industries)
            
            if industry == "Technology":
                role = np.random.choice(tech_roles)
                company = np.random.choice(companies[:7])  # Tech companies
            elif industry == "Finance":
                role = np.random.choice(finance_roles)
                company = np.random.choice(companies[7:11])  # Finance companies
            elif industry == "Healthcare":
                role = np.random.choice(healthcare_roles)
                company = np.random.choice(companies[11:15])  # Healthcare companies
            else:  # Consulting
                role = np.random.choice(consulting_roles)
                company = np.random.choice(companies[15:])  # Consulting companies
            
            # Generate realistic salary ranges based on role and industry
            base_salary = self._get_base_salary(role, industry)
            salary_min = base_salary + np.random.randint(-20000, 10000)
            salary_max = salary_min + np.random.randint(20000, 60000)
            
            # Generate location
            locations = ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
                        "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Remote"]
            location = np.random.choice(locations)
            
            # Generate experience level
            experience_levels = ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
            experience_weights = [0.3, 0.4, 0.25, 0.05]
            experience = np.random.choice(experience_levels, p=experience_weights)
            
            job_postings.append({
                'id': i + 1,
                'title': role,
                'company': company,
                'industry': industry,
                'location': location,
                'salary_min': max(salary_min, 40000),  # Minimum floor
                'salary_max': salary_max,
                'experience_level': experience,
                'required_skills': self._get_skills_for_role(role, industry),
                'posted_date': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(1, 90))
            })
        
        self.job_data = pd.DataFrame(job_postings)
        self.processed = True
        return self.job_data
    
    def _get_base_salary(self, role, industry):
        """Get base salary for role and industry combination"""
        salary_mapping = {
            # Technology roles
            "Software Engineer": 120000,
            "Data Scientist": 130000,
            "Machine Learning Engineer": 140000,
            "DevOps Engineer": 125000,
            "Frontend Developer": 110000,
            "Backend Developer": 115000,
            "Full Stack Developer": 120000,
            "Data Analyst": 85000,
            "Product Manager": 140000,
            "UI/UX Designer": 95000,
            "Security Engineer": 130000,
            "Cloud Engineer": 125000,
            
            # Finance roles
            "Financial Analyst": 80000,
            "Investment Banker": 150000,
            "Risk Analyst": 90000,
            "Quantitative Analyst": 160000,
            "Portfolio Manager": 180000,
            "Trading Analyst": 140000,
            "Credit Analyst": 85000,
            "Financial Consultant": 100000,
            "Compliance Officer": 95000,
            
            # Healthcare roles
            "Data Analyst": 75000,
            "Healthcare Consultant": 110000,
            "Clinical Research Associate": 85000,
            "Biostatistician": 120000,
            "Health Informatics Specialist": 95000,
            "Medical Coder": 45000,
            "Healthcare Data Scientist": 125000,
            "Clinical Data Manager": 100000,
            
            # Consulting roles
            "Management Consultant": 120000,
            "Strategy Consultant": 130000,
            "Business Analyst": 85000,
            "Operations Consultant": 110000,
            "IT Consultant": 105000,
            "Digital Transformation Consultant": 125000
        }
        
        base = salary_mapping.get(role, 80000)
        
        # Industry multipliers
        if industry == "Technology":
            base *= 1.1
        elif industry == "Finance":
            base *= 1.15
        elif industry == "Healthcare":
            base *= 0.95
        # Consulting stays at base
        
        return int(base)
    
    def _get_skills_for_role(self, role, industry):
        """Get realistic skills for a given role and industry"""
        skill_mapping = {
            # Technology roles
            "Software Engineer": ["Python", "Java", "JavaScript", "Git", "SQL", "React", "Node.js", "Docker", "AWS"],
            "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Statistics"],
            "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "Docker", "Kubernetes", "MLOps", "Git", "Linux", "Cloud Platforms"],
            "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Linux", "Python", "Terraform", "Jenkins", "Monitoring", "CI/CD"],
            "Frontend Developer": ["JavaScript", "React", "HTML", "CSS", "TypeScript", "Vue.js", "Webpack", "Git"],
            "Backend Developer": ["Python", "Java", "Node.js", "SQL", "NoSQL", "REST APIs", "Microservices", "Docker"],
            "Full Stack Developer": ["JavaScript", "React", "Node.js", "Python", "SQL", "MongoDB", "Git", "AWS"],
            "Data Analyst": ["SQL", "Python", "Excel", "Tableau", "Power BI", "Statistics", "Data Visualization"],
            "Product Manager": ["Analytics", "SQL", "A/B Testing", "Product Strategy", "Agile", "User Research"],
            "UI/UX Designer": ["Figma", "Adobe XD", "Sketch", "Prototyping", "User Research", "Design Thinking"],
            "Security Engineer": ["Network Security", "Penetration Testing", "SIEM", "Incident Response", "Risk Assessment"],
            "Cloud Engineer": ["AWS", "Azure", "GCP", "Terraform", "Docker", "Kubernetes", "Linux", "Networking"],
            
            # Finance roles
            "Financial Analyst": ["Excel", "SQL", "Financial Modeling", "VBA", "Bloomberg", "Python", "Statistics"],
            "Investment Banker": ["Excel", "PowerPoint", "Financial Modeling", "Valuation", "M&A", "Bloomberg"],
            "Risk Analyst": ["Excel", "SQL", "Python", "R", "Risk Management", "Statistics", "Monte Carlo"],
            "Quantitative Analyst": ["Python", "R", "C++", "MATLAB", "Statistics", "Machine Learning", "Financial Modeling"],
            "Portfolio Manager": ["Excel", "Bloomberg", "Python", "Risk Management", "Asset Allocation", "Performance Analysis"],
            "Trading Analyst": ["Excel", "Bloomberg", "Python", "Market Analysis", "Technical Analysis", "Risk Management"],
            "Credit Analyst": ["Excel", "SQL", "Credit Analysis", "Financial Modeling", "Risk Assessment"],
            "Financial Consultant": ["Excel", "Financial Planning", "Client Management", "Investment Analysis"],
            "Compliance Officer": ["Regulatory Knowledge", "Risk Assessment", "Audit", "Documentation"],
            
            # Healthcare roles
            "Data Analyst": ["SQL", "Python", "R", "Excel", "Tableau", "Healthcare Data", "Statistics"],
            "Healthcare Consultant": ["Healthcare Knowledge", "Data Analysis", "Process Improvement", "Project Management"],
            "Clinical Research Associate": ["Clinical Trials", "GCP", "Data Management", "Regulatory Knowledge"],
            "Biostatistician": ["R", "SAS", "Python", "Clinical Statistics", "Study Design", "Statistical Analysis"],
            "Health Informatics Specialist": ["Healthcare IT", "EHR Systems", "Data Analysis", "SQL", "Healthcare Standards"],
            "Medical Coder": ["ICD-10", "CPT", "Medical Terminology", "Healthcare Documentation"],
            "Healthcare Data Scientist": ["Python", "R", "Machine Learning", "Healthcare Data", "Statistics", "SQL"],
            "Clinical Data Manager": ["Clinical Data", "EDC Systems", "Data Quality", "Regulatory Standards"],
            
            # Consulting roles
            "Management Consultant": ["Strategy", "Business Analysis", "PowerPoint", "Excel", "Problem Solving"],
            "Strategy Consultant": ["Strategic Planning", "Market Analysis", "Financial Modeling", "PowerPoint", "Excel"],
            "Business Analyst": ["Business Analysis", "SQL", "Excel", "Process Mapping", "Requirements Gathering"],
            "Operations Consultant": ["Operations Management", "Process Improvement", "Lean Six Sigma", "Data Analysis"],
            "IT Consultant": ["IT Strategy", "System Analysis", "Project Management", "Technology Assessment"],
            "Digital Transformation Consultant": ["Digital Strategy", "Change Management", "Technology Assessment", "Business Analysis"]
        }
        
        base_skills = skill_mapping.get(role, ["Communication", "Problem Solving", "Teamwork"])
        
        # Add some randomization and industry-specific skills
        skills = base_skills.copy()
        
        # Add common industry skills
        if industry == "Technology":
            additional_skills = ["Agile", "Scrum", "Git", "Linux"]
        elif industry == "Finance":
            additional_skills = ["Excel", "Financial Analysis", "Bloomberg", "Risk Management"]
        elif industry == "Healthcare":
            additional_skills = ["Healthcare Compliance", "HIPAA", "Medical Knowledge"]
        else:  # Consulting
            additional_skills = ["Client Management", "Presentation Skills", "Strategic Thinking"]
        
        # Randomly add some additional skills
        for skill in additional_skills:
            if skill not in skills and np.random.random() > 0.5:
                skills.append(skill)
        
        # Add some general professional skills randomly
        general_skills = ["Communication", "Leadership", "Project Management", "Analytical Thinking", "Problem Solving"]
        for skill in general_skills:
            if skill not in skills and np.random.random() > 0.7:
                skills.append(skill)
        
        return skills
    
    def get_job_data(self):
        """Get processed job data"""
        if not self.processed:
            return self.load_mock_data()
        return self.job_data
    
    def get_skills_summary(self):
        """Get summary of skills across all jobs"""
        if not self.processed:
            self.load_mock_data()
        
        all_skills = []
        for skills in self.job_data['required_skills']:
            all_skills.extend(skills)
        
        skills_df = pd.Series(all_skills).value_counts().reset_index()
        skills_df.columns = ['skill', 'count']
        skills_df['percentage'] = skills_df['count'] / len(self.job_data) * 100
        
        return skills_df
    
    def get_industry_skills(self, industry):
        """Get skills specific to an industry"""
        if not self.processed:
            self.load_mock_data()
        
        industry_data = self.job_data[self.job_data['industry'] == industry]
        
        industry_skills = []
        for skills in industry_data['required_skills']:
            industry_skills.extend(skills)
        
        skills_df = pd.Series(industry_skills).value_counts().reset_index()
        skills_df.columns = ['skill', 'count']
        skills_df['percentage'] = skills_df['count'] / len(industry_data) * 100
        
        return skills_df
