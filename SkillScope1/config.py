import os

# Database Configuration
# For development, you can use SQLite or set up PostgreSQL
# Option 1: Use SQLite (simpler for development)
DATABASE_URL = "sqlite:///skillscope.db"

# Option 2: Use PostgreSQL (production ready)
# DATABASE_URL = "postgresql://username:password@localhost:5432/skillscope_db"

# Set environment variable
os.environ['DATABASE_URL'] = DATABASE_URL

# API Keys (if you have them)
# os.environ['LINKEDIN_API_KEY'] = 'your_linkedin_api_key'
# os.environ['INDEED_API_KEY'] = 'your_indeed_api_key'

# App Configuration
APP_TITLE = "SkillScope - Job Market Analyzer"
APP_ICON = "🎯"
