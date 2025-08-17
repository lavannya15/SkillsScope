import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class MockJobData:
    """Generate realistic mock job posting data"""
    
    def __init__(self):
        np.random.seed(42)
        random.seed(42)
        
        # Define realistic company and industry data
        self.companies_by_industry = {
            "Technology": [
                "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Tesla",
                "Uber", "Airbnb", "Spotify", "Salesforce", "Adobe", "Intel", "Nvidia",
                "Oracle", "IBM", "Cisco", "VMware", "Dropbox", "Slack", "Zoom"
            ],
            "Finance": [
                "Goldman Sachs", "JPMorgan Chase", "Bank of America", "Citigroup",
                "Wells Fargo", "Morgan Stanley", "Credit Suisse", "Deutsche Bank",
                "BlackRock", "Vanguard", "Fidelity", "Charles Schwab", "American Express",
                "Visa", "Mastercard", "PayPal", "Square", "Stripe"
            ],
            "Healthcare": [
                "Johnson & Johnson", "Pfizer", "Moderna", "Novartis", "Roche",
                "Merck", "AbbVie", "Bristol Myers Squibb", "Eli Lilly", "GSK",
                "CVS Health", "UnitedHealth", "Anthem", "Humana", "Kaiser Permanente",
                "Mayo Clinic", "Cleveland Clinic", "Partners HealthCare"
            ],
            "Marketing": [
                "WPP", "Omnicom", "Publicis", "Interpublic Group", "Dentsu",
                "Havas", "Saatchi & Saatchi", "BBDO", "DDB", "Grey",
                "Ogilvy", "McCann", "Leo Burnett", "JWT", "Young & Rubicam",
                "Edelman", "Weber Shandwick", "Fleishman Hillard"
            ]
        }
        
        # Define job roles by industry
        self.job_roles_by_industry = {
            "Technology": [
                "Software Engineer", "Senior Software Engineer", "Staff Software Engineer",
                "Data Scientist", "Senior Data Scientist", "Machine Learning Engineer",
                "DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer",
                "Frontend Developer", "Backend Developer", "Full Stack Developer",
                "Product Manager", "Senior Product Manager", "Engineering Manager",
                "Data Analyst", "Business Analyst", "UX Designer", "UI Designer",
                "Security Engineer", "Platform Engineer", "Mobile Developer",
                "Quality Assurance Engineer", "Solutions Architect", "Technical Lead"
            ],
            "Finance": [
                "Financial Analyst", "Senior Financial Analyst", "Investment Banker",
                "Associate Investment Banker", "Vice President Investment Banking",
                "Risk Analyst", "Senior Risk Analyst", "Quantitative Analyst",
                "Portfolio Manager", "Asset Manager", "Wealth Manager",
                "Trading Analyst", "Equity Research Analyst", "Credit Analyst",
                "Compliance Officer", "Internal Auditor", "Financial Consultant",
                "Investment Advisor", "Treasury Analyst", "Corporate Finance Analyst",
                "Private Equity Associate", "Hedge Fund Analyst", "Financial Planner"
            ],
            "Healthcare": [
                "Clinical Data Analyst", "Healthcare Data Scientist", "Biostatistician",
                "Clinical Research Associate", "Clinical Research Coordinator",
                "Medical Affairs Specialist", "Regulatory Affairs Specialist",
                "Pharmacovigilance Specialist", "Clinical Data Manager",
                "Health Economics Analyst", "Market Access Analyst",
                "Medical Science Liaison", "Clinical Operations Manager",
                "Quality Assurance Specialist", "Compliance Specialist",
                "Healthcare Consultant", "Population Health Analyst",
                "Clinical Trial Manager", "Medical Writer", "Health Informatics Specialist"
            ],
            "Marketing": [
                "Digital Marketing Manager", "Marketing Analyst", "Brand Manager",
                "Product Marketing Manager", "Content Marketing Manager",
                "Social Media Manager", "SEO Specialist", "SEM Specialist",
                "Marketing Coordinator", "Campaign Manager", "Growth Marketing Manager",
                "Performance Marketing Manager", "Email Marketing Specialist",
                "Marketing Operations Manager", "Customer Acquisition Manager",
                "Marketing Data Analyst", "Creative Director", "Art Director",
                "Copywriter", "Public Relations Manager", "Event Marketing Manager",
                "Influencer Marketing Manager", "Affiliate Marketing Manager"
            ]
        }
        
        # Define skills by role
        self.skills_by_role = {
            # Technology roles
            "Software Engineer": ["Python", "Java", "JavaScript", "Git", "SQL", "REST APIs", "Agile", "Docker", "Linux", "Problem Solving"],
            "Senior Software Engineer": ["Python", "Java", "System Design", "Leadership", "Mentoring", "Architecture", "Code Review", "CI/CD", "Microservices", "Cloud Platforms"],
            "Data Scientist": ["Python", "R", "Machine Learning", "Statistics", "SQL", "Pandas", "NumPy", "Scikit-learn", "Data Visualization", "A/B Testing"],
            "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "Docker", "Kubernetes", "MLOps", "Git", "Linux", "Model Deployment", "Feature Engineering"],
            "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Linux", "Python", "Terraform", "Jenkins", "CI/CD", "Monitoring", "Infrastructure as Code"],
            "Frontend Developer": ["JavaScript", "React", "HTML", "CSS", "TypeScript", "Git", "Responsive Design", "Web APIs", "Testing", "UI/UX"],
            "Backend Developer": ["Python", "Java", "Node.js", "SQL", "NoSQL", "REST APIs", "Microservices", "Docker", "Git", "Database Design"],
            "Product Manager": ["Product Strategy", "Analytics", "SQL", "A/B Testing", "User Research", "Agile", "Roadmapping", "Stakeholder Management", "Market Research", "Data Analysis"],
            "Data Analyst": ["SQL", "Python", "Excel", "Tableau", "Power BI", "Statistics", "Data Visualization", "ETL", "Business Intelligence", "Report Writing"],
            
            # Finance roles
            "Financial Analyst": ["Excel", "Financial Modeling", "SQL", "VBA", "Bloomberg", "Financial Analysis", "Budgeting", "Forecasting", "Valuation", "PowerPoint"],
            "Investment Banker": ["Excel", "PowerPoint", "Financial Modeling", "Valuation", "M&A", "Bloomberg", "Pitch Books", "Due Diligence", "Client Management", "Market Analysis"],
            "Risk Analyst": ["Excel", "Python", "R", "SQL", "Risk Management", "Statistical Analysis", "Monte Carlo Simulation", "VaR", "Stress Testing", "Regulatory Knowledge"],
            "Quantitative Analyst": ["Python", "R", "C++", "MATLAB", "Statistics", "Machine Learning", "Financial Modeling", "Risk Management", "Algorithmic Trading", "Mathematical Modeling"],
            "Portfolio Manager": ["Excel", "Bloomberg", "Python", "Portfolio Management", "Asset Allocation", "Risk Management", "Performance Analysis", "Investment Research", "Client Relations", "Market Analysis"],
            
            # Healthcare roles
            "Clinical Data Analyst": ["SAS", "R", "SQL", "Clinical Data", "Statistical Analysis", "Clinical Trials", "GCP", "Regulatory Knowledge", "Data Management", "Report Writing"],
            "Healthcare Data Scientist": ["Python", "R", "Machine Learning", "Healthcare Data", "Statistics", "SQL", "Clinical Research", "Epidemiology", "Biostatistics", "Data Mining"],
            "Biostatistician": ["R", "SAS", "Python", "Clinical Statistics", "Study Design", "Statistical Analysis", "Clinical Trials", "Regulatory Submissions", "Medical Writing", "Data Interpretation"],
            "Clinical Research Associate": ["GCP", "Clinical Trials", "Monitoring", "Regulatory Knowledge", "Medical Terminology", "Data Management", "Site Management", "Protocol Development", "Audit", "Documentation"],
            
            # Marketing roles
            "Digital Marketing Manager": ["Google Analytics", "Google Ads", "Facebook Ads", "SEO", "SEM", "Email Marketing", "Social Media", "Content Marketing", "Marketing Automation", "A/B Testing"],
            "Marketing Analyst": ["SQL", "Python", "R", "Google Analytics", "Excel", "Tableau", "Statistics", "A/B Testing", "Market Research", "Data Visualization"],
            "Brand Manager": ["Brand Strategy", "Market Research", "Product Management", "Campaign Management", "Budget Management", "Creative Development", "Consumer Insights", "Competitive Analysis", "Project Management", "Presentation Skills"],
            "Content Marketing Manager": ["Content Strategy", "Content Creation", "SEO", "Social Media", "Email Marketing", "Analytics", "Project Management", "Brand Voice", "Editorial Calendar", "Performance Measurement"],
            "Social Media Manager": ["Social Media Strategy", "Content Creation", "Community Management", "Social Media Analytics", "Paid Social", "Influencer Marketing", "Brand Management", "Crisis Management", "Photography", "Video Editing"]
        }
        
        # Define salary ranges by role and experience
        self.salary_ranges = {
            # Technology
            "Software Engineer": {"entry": (80000, 120000), "mid": (100000, 150000), "senior": (130000, 200000)},
            "Senior Software Engineer": {"mid": (130000, 180000), "senior": (150000, 250000), "executive": (200000, 350000)},
            "Data Scientist": {"entry": (90000, 130000), "mid": (110000, 160000), "senior": (140000, 220000)},
            "Machine Learning Engineer": {"mid": (120000, 170000), "senior": (150000, 240000), "executive": (200000, 400000)},
            "Product Manager": {"mid": (110000, 160000), "senior": (140000, 220000), "executive": (180000, 350000)},
            
            # Finance
            "Financial Analyst": {"entry": (60000, 80000), "mid": (70000, 100000), "senior": (90000, 130000)},
            "Investment Banker": {"entry": (100000, 150000), "mid": (150000, 250000), "senior": (200000, 400000)},
            "Risk Analyst": {"entry": (70000, 90000), "mid": (80000, 120000), "senior": (100000, 160000)},
            "Quantitative Analyst": {"mid": (120000, 180000), "senior": (150000, 250000), "executive": (200000, 400000)},
            
            # Healthcare
            "Clinical Data Analyst": {"entry": (65000, 85000), "mid": (75000, 105000), "senior": (95000, 135000)},
            "Healthcare Data Scientist": {"mid": (100000, 140000), "senior": (125000, 180000), "executive": (160000, 250000)},
            "Biostatistician": {"mid": (95000, 130000), "senior": (115000, 170000), "executive": (150000, 220000)},
            
            # Marketing
            "Digital Marketing Manager": {"mid": (70000, 100000), "senior": (90000, 140000), "executive": (120000, 180000)},
            "Marketing Analyst": {"entry": (55000, 75000), "mid": (65000, 90000), "senior": (80000, 120000)},
            "Brand Manager": {"mid": (80000, 120000), "senior": (100000, 150000), "executive": (130000, 200000)}
        }
        
        # Locations with different cost of living adjustments
        self.locations_with_multipliers = {
            "San Francisco, CA": 1.4,
            "New York, NY": 1.3,
            "Seattle, WA": 1.2,
            "Boston, MA": 1.15,
            "Los Angeles, CA": 1.1,
            "Austin, TX": 1.0,
            "Chicago, IL": 0.95,
            "Denver, CO": 0.9,
            "Atlanta, GA": 0.85,
            "Remote": 1.0
        }
    
    def get_job_postings(self, num_jobs=1500):
        """Generate comprehensive mock job posting data"""
        job_postings = []
        
        for i in range(num_jobs):
            # Select industry
            industry = random.choice(list(self.companies_by_industry.keys()))
            
            # Select company from industry
            company = random.choice(self.companies_by_industry[industry])
            
            # Select role from industry
            job_title = random.choice(self.job_roles_by_industry[industry])
            
            # Determine experience level based on title
            if any(keyword in job_title.lower() for keyword in ['senior', 'sr.', 'lead', 'principal', 'staff']):
                experience_level = random.choices(
                    ["Mid Level", "Senior Level", "Executive Level"],
                    weights=[0.3, 0.6, 0.1]
                )[0]
            elif any(keyword in job_title.lower() for keyword in ['manager', 'director', 'vp', 'vice president']):
                experience_level = random.choices(
                    ["Senior Level", "Executive Level"],
                    weights=[0.4, 0.6]
                )[0]
            elif any(keyword in job_title.lower() for keyword in ['junior', 'associate', 'coordinator']):
                experience_level = random.choices(
                    ["Entry Level", "Mid Level"],
                    weights=[0.7, 0.3]
                )[0]
            else:
                experience_level = random.choices(
                    ["Entry Level", "Mid Level", "Senior Level"],
                    weights=[0.3, 0.5, 0.2]
                )[0]
            
            # Get location and salary
            location, location_multiplier = random.choice(list(self.locations_with_multipliers.items()))
            
            # Calculate salary based on role, experience, and location
            salary_min, salary_max = self._calculate_salary(job_title, experience_level, location_multiplier)
            
            # Get skills for role
            required_skills = self._get_skills_for_role(job_title, industry, experience_level)
            
            # Generate posting date (within last 90 days)
            posted_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            job_posting = {
                'id': i + 1,
                'title': job_title,
                'company': company,
                'industry': industry,
                'location': location,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'experience_level': experience_level,
                'required_skills': required_skills,
                'posted_date': posted_date,
                'description': self._generate_job_description(job_title, company, industry, required_skills),
                'benefits': self._generate_benefits(),
                'remote_option': random.choice([True, False]) if location != "Remote" else True,
                'company_size': random.choice(["Startup (1-50)", "Small (51-200)", "Medium (201-1000)", "Large (1001-5000)", "Enterprise (5000+)"]),
                'employment_type': random.choices(["Full-time", "Contract", "Part-time"], weights=[0.85, 0.12, 0.03])[0]
            }
            
            job_postings.append(job_posting)
        
        return pd.DataFrame(job_postings)
    
    def _calculate_salary(self, job_title, experience_level, location_multiplier):
        """Calculate salary based on role, experience, and location"""
        # Map experience levels to salary keys
        exp_mapping = {
            "Entry Level": "entry",
            "Mid Level": "mid", 
            "Senior Level": "senior",
            "Executive Level": "executive"
        }
        
        exp_key = exp_mapping.get(experience_level, "mid")
        
        # Get base salary range for role
        if job_title in self.salary_ranges:
            role_salaries = self.salary_ranges[job_title]
            if exp_key in role_salaries:
                base_min, base_max = role_salaries[exp_key]
            else:
                # Fallback to available experience level
                available_exp = list(role_salaries.keys())
                fallback_key = available_exp[0] if available_exp else "mid"
                base_min, base_max = role_salaries.get(fallback_key, (70000, 120000))
        else:
            # Default salary ranges by experience level
            default_ranges = {
                "entry": (60000, 90000),
                "mid": (80000, 130000),
                "senior": (110000, 180000),
                "executive": (150000, 300000)
            }
            base_min, base_max = default_ranges.get(exp_key, (70000, 120000))
        
        # Apply location multiplier
        salary_min = int(base_min * location_multiplier)
        salary_max = int(base_max * location_multiplier)
        
        # Add some randomization
        salary_min += random.randint(-5000, 5000)
        salary_max += random.randint(-5000, 10000)
        
        # Ensure min < max
        if salary_min >= salary_max:
            salary_max = salary_min + 20000
        
        return max(salary_min, 40000), salary_max  # Minimum floor of $40k
    
    def _get_skills_for_role(self, job_title, industry, experience_level):
        """Get skills based on role, industry, and experience level"""
        # Get base skills for role
        base_skills = self.skills_by_role.get(job_title, [])
        
        # Add industry-specific skills
        industry_skills = {
            "Technology": ["Agile", "Git", "Linux", "CI/CD", "Cloud Platforms"],
            "Finance": ["Excel", "Bloomberg", "Financial Analysis", "Risk Management", "Regulatory Knowledge"],
            "Healthcare": ["Healthcare Compliance", "HIPAA", "Clinical Knowledge", "Regulatory Affairs", "Medical Terminology"],
            "Marketing": ["Google Analytics", "Marketing Automation", "Brand Management", "Campaign Management", "Customer Insights"]
        }
        
        # Add experience-level specific skills
        experience_skills = {
            "Entry Level": ["Communication", "Time Management", "Attention to Detail"],
            "Mid Level": ["Project Management", "Team Collaboration", "Problem Solving"],
            "Senior Level": ["Leadership", "Strategic Planning", "Mentoring", "Decision Making"],
            "Executive Level": ["Executive Leadership", "Business Strategy", "Stakeholder Management", "Change Management"]
        }
        
        # Combine skills
        all_skills = list(base_skills)
        
        # Add industry skills (50% chance for each)
        for skill in industry_skills.get(industry, []):
            if skill not in all_skills and random.random() > 0.5:
                all_skills.append(skill)
        
        # Add experience skills (70% chance for each)
        for skill in experience_skills.get(experience_level, []):
            if skill not in all_skills and random.random() > 0.3:
                all_skills.append(skill)
        
        # Add some random technical skills based on industry
        if industry == "Technology":
            tech_pool = ["Docker", "Kubernetes", "AWS", "Python", "JavaScript", "SQL", "React", "Node.js", "Machine Learning", "Data Analysis"]
        elif industry == "Finance":
            tech_pool = ["Python", "R", "SQL", "VBA", "MATLAB", "Tableau", "Power BI", "SAS", "Statistical Analysis", "Data Modeling"]
        elif industry == "Healthcare":
            tech_pool = ["SAS", "R", "SQL", "Python", "Clinical Data Management", "Statistical Software", "Electronic Health Records", "Data Analysis"]
        else:  # Marketing
            tech_pool = ["Google Analytics", "SQL", "Python", "Tableau", "Adobe Creative Suite", "Marketing Automation Tools", "CRM Software", "Social Media Platforms"]
        
        # Randomly add 1-3 additional skills
        additional_count = random.randint(1, 3)
        additional_skills = random.sample(tech_pool, min(additional_count, len(tech_pool)))
        
        for skill in additional_skills:
            if skill not in all_skills:
                all_skills.append(skill)
        
        # Remove duplicates and return
        return list(set(all_skills))
    
    def _generate_job_description(self, job_title, company, industry, skills):
        """Generate a realistic job description"""
        descriptions = {
            "Software Engineer": f"We are looking for a talented Software Engineer to join our team at {company}. You will be responsible for developing high-quality software solutions and working collaboratively with cross-functional teams.",
            "Data Scientist": f"{company} is seeking a Data Scientist to analyze complex datasets and drive data-driven decision making across the organization. You will work with large-scale data and machine learning models.",
            "Product Manager": f"Join {company} as a Product Manager to lead product strategy and development. You will work closely with engineering, design, and business stakeholders to deliver innovative products.",
            "Marketing Analyst": f"We are hiring a Marketing Analyst at {company} to analyze marketing performance and provide insights for campaign optimization and growth strategies."
        }
        
        base_description = descriptions.get(job_title, f"We are looking for a {job_title} to join our team at {company}.")
        
        # Add responsibilities
        responsibilities = [
            f"Utilize {', '.join(skills[:3])} in daily work",
            "Collaborate with cross-functional teams",
            "Contribute to project planning and execution",
            "Maintain high standards of quality and performance"
        ]
        
        requirements = [
            f"Experience with {', '.join(skills[:5])}",
            "Strong analytical and problem-solving skills",
            "Excellent communication and teamwork abilities",
            "Bachelor's degree in relevant field"
        ]
        
        full_description = f"{base_description}\n\nResponsibilities:\n" + "\n".join([f"• {r}" for r in responsibilities])
        full_description += f"\n\nRequirements:\n" + "\n".join([f"• {r}" for r in requirements])
        
        return full_description
    
    def _generate_benefits(self):
        """Generate realistic benefits list"""
        possible_benefits = [
            "Health Insurance", "Dental Insurance", "Vision Insurance",
            "401(k) Matching", "Flexible PTO", "Remote Work Options",
            "Professional Development Budget", "Stock Options",
            "Life Insurance", "Disability Insurance", "Wellness Programs",
            "Flexible Hours", "Parental Leave", "Tuition Reimbursement",
            "Free Meals", "Gym Membership", "Transit Benefits"
        ]
        
        # Randomly select 5-10 benefits
        num_benefits = random.randint(5, 10)
        return random.sample(possible_benefits, num_benefits)
    
    def get_trending_skills(self, industry=None, days_back=30):
        """Get trending skills data (mock time series)"""
        job_data = self.get_job_postings()
        
        if industry:
            job_data = job_data[job_data['industry'] == industry]
        
        # Extract all skills
        all_skills = []
        for skills in job_data['required_skills']:
            all_skills.extend(skills)
        
        # Get top skills
        skill_counts = pd.Series(all_skills).value_counts().head(20)
        
        # Generate mock time series data
        dates = pd.date_range(end=datetime.now(), periods=days_back, freq='D')
        trend_data = []
        
        for skill in skill_counts.index:
            base_demand = skill_counts[skill]
            for date in dates:
                # Add some realistic variation
                daily_demand = base_demand + random.randint(-5, 10)
                trend_data.append({
                    'date': date,
                    'skill': skill,
                    'demand': max(daily_demand, 1)
                })
        
        return pd.DataFrame(trend_data)
