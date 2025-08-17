# SkillScope - Job Market Analyzer

## Overview

SkillScope is a comprehensive job market analysis application built with Streamlit that helps users discover trending skills and optimize their career paths. The application provides industry-specific skill trend analysis, resume skill assessment, and personalized career recommendations. It features an interactive dashboard with data visualizations using Plotly, mock job market data generation, and advanced NLP processing for skill extraction from resumes and job descriptions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit with multi-page application structure
- **Visualization**: Plotly Express and Plotly Graph Objects for interactive charts and dashboards
- **Layout**: Wide layout with expandable sidebar navigation
- **Pages**: Main dashboard plus dedicated pages for Industry Trends, Resume Analyzer, and Career Recommendations

### Backend Architecture
- **Core Application**: Python-based with modular utility classes
- **Data Processing**: Object-oriented design with specialized classes for different functionalities:
  - `DataLoader`: Handles job market data loading and processing
  - `NLPProcessor`: Text processing and skill extraction from natural language
  - `SkillExtractor`: Advanced skill identification with comprehensive skill database
  - `MockJobData`: Realistic job posting data generation for demonstration
  - `SkillTaxonomy`: Skill categorization and organization system

### Data Management
- **Mock Data Generation**: Comprehensive mock job posting system with realistic company, industry, and role data
- **Skill Database**: Extensive skill taxonomy covering programming languages, frameworks, databases, cloud platforms, and business skills
- **Session State**: Streamlit session state management for persistent data across page navigation

### NLP and Skill Processing
- **Text Processing**: Custom NLP pipeline for extracting skills from job descriptions and resumes
- **Skill Matching**: Advanced pattern matching with synonym and variation handling
- **Categorization**: Hierarchical skill organization by technology domains and experience levels

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework and UI components
- **plotly**: Interactive data visualization (plotly.express and plotly.graph_objects)
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing and array operations
- **datetime**: Date and time handling for temporal analysis

### File Processing
- **Text Files**: Native text file reading for resume uploads
- **PDF Support**: Placeholder implementation for PDF resume processing (would require PyPDF2 or similar)

### Data Sources
- **Mock Data**: Self-contained realistic job market data generation
- **Extensible Design**: Architecture supports integration with external job APIs (LinkedIn, Indeed, Glassdoor) and resume parsing services