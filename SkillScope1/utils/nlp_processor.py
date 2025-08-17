import re
import string
from collections import Counter
import pandas as pd

class NLPProcessor:
    """Class to handle NLP processing for job descriptions and resumes"""
    
    def __init__(self):
        # Common stop words for skill extraction
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 
            'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been', 
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 
            'should', 'may', 'might', 'must', 'can', 'shall', 'this', 'that', 'these', 
            'those', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 
            'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 
            'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'whose', 
            'why', 'how', 'when', 'where', 'if', 'because', 'as', 'until', 'while', 
            'although', 'though', 'since', 'unless', 'than', 'so', 'but', 'however', 
            'therefore', 'thus', 'hence', 'moreover', 'furthermore', 'nevertheless',
            'work', 'job', 'position', 'role', 'candidate', 'team', 'company', 
            'experience', 'years', 'ability', 'skills', 'knowledge', 'required', 
            'preferred', 'plus', 'bonus', 'nice', 'strong', 'excellent', 'good'
        }
        
        # Programming languages and technologies
        self.tech_skills = {
            'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'swift', 
            'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'typescript',
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 
            'spring', 'laravel', 'rails', 'asp.net',
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'linux',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
            'tableau', 'power bi', 'excel', 'powerpoint', 'word', 'outlook',
            'photoshop', 'illustrator', 'figma', 'sketch', 'adobe xd'
        }
        
        # Business and soft skills
        self.business_skills = {
            'project management', 'agile', 'scrum', 'kanban', 'lean', 'six sigma',
            'leadership', 'communication', 'teamwork', 'problem solving',
            'analytical thinking', 'critical thinking', 'creativity', 'innovation',
            'time management', 'organization', 'attention to detail',
            'client management', 'stakeholder management', 'vendor management',
            'budget management', 'risk management', 'change management',
            'strategic planning', 'business analysis', 'market research',
            'financial modeling', 'data analysis', 'statistical analysis',
            'machine learning', 'deep learning', 'artificial intelligence',
            'data visualization', 'reporting', 'dashboard development'
        }
        
        # Industry-specific skills
        self.finance_skills = {
            'financial analysis', 'investment banking', 'portfolio management',
            'risk assessment', 'compliance', 'audit', 'taxation', 'accounting',
            'bloomberg terminal', 'reuters', 'factset', 'morningstar',
            'derivatives', 'equity research', 'fixed income', 'fx trading',
            'quantitative analysis', 'algorithmic trading', 'backtesting'
        }
        
        self.healthcare_skills = {
            'clinical research', 'medical coding', 'hipaa', 'fda regulations',
            'gcp', 'clinical trials', 'biostatistics', 'epidemiology',
            'health informatics', 'ehr systems', 'epic', 'cerner',
            'medical terminology', 'icd-10', 'cpt', 'pharmacovigilance'
        }
        
        # Combine all skill sets
        self.all_skills = (self.tech_skills | self.business_skills | 
                          self.finance_skills | self.healthcare_skills)
    
    def preprocess_text(self, text):
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important ones like + and #
        text = re.sub(r'[^\w\s\+\#\.\-]', ' ', text)
        
        # Handle common abbreviations and variations
        text = re.sub(r'\bc\+\+\b', 'c++', text)
        text = re.sub(r'\bc#\b', 'c#', text)
        text = re.sub(r'\bnode\.js\b', 'node.js', text)
        text = re.sub(r'\basp\.net\b', 'asp.net', text)
        
        return text.strip()
    
    def extract_skills_basic(self, text):
        """Basic skill extraction using keyword matching"""
        text = self.preprocess_text(text)
        
        found_skills = set()
        
        # Look for exact skill matches
        for skill in self.all_skills:
            if skill in text:
                found_skills.add(skill)
        
        # Look for variations and common patterns
        words = text.split()
        
        # Check for programming languages with common variations
        lang_patterns = {
            'python': ['python', 'py'],
            'javascript': ['javascript', 'js'],
            'typescript': ['typescript', 'ts'],
            'c++': ['c++', 'cpp'],
            'c#': ['c#', 'csharp'],
        }
        
        for lang, patterns in lang_patterns.items():
            if any(pattern in text for pattern in patterns):
                found_skills.add(lang)
        
        # Look for multi-word skills
        bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
        trigrams = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
        
        for skill in self.all_skills:
            if len(skill.split()) == 2 and skill in bigrams:
                found_skills.add(skill)
            elif len(skill.split()) == 3 and skill in trigrams:
                found_skills.add(skill)
        
        return list(found_skills)
    
    def extract_entities(self, text):
        """Extract named entities (simplified version)"""
        text = self.preprocess_text(text)
        
        entities = {
            'skills': [],
            'technologies': [],
            'companies': [],
            'education': []
        }
        
        # Extract skills
        entities['skills'] = self.extract_skills_basic(text)
        
        # Extract technology mentions
        tech_keywords = ['software', 'platform', 'framework', 'library', 'tool', 'system']
        for keyword in tech_keywords:
            pattern = rf'\b(\w+)\s+{keyword}\b'
            matches = re.findall(pattern, text)
            entities['technologies'].extend(matches)
        
        # Extract company mentions (simplified)
        company_patterns = [
            r'\bat\s+(\w+(?:\s+\w+)?)\b',
            r'\bworked\s+at\s+(\w+(?:\s+\w+)?)\b',
            r'\bemployed\s+by\s+(\w+(?:\s+\w+)?)\b'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['companies'].extend(matches)
        
        # Extract education mentions
        education_keywords = ['university', 'college', 'institute', 'school', 'degree', 'bachelor', 'master', 'phd']
        for keyword in education_keywords:
            pattern = rf'\b(\w+(?:\s+\w+)*)\s+{keyword}\b'
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['education'].extend(matches)
        
        # Clean up duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def analyze_text_complexity(self, text):
        """Analyze text complexity metrics"""
        if not text:
            return {}
        
        words = text.split()
        sentences = text.split('.')
        
        metrics = {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
            'unique_words': len(set(word.lower() for word in words)),
            'vocabulary_richness': len(set(word.lower() for word in words)) / len(words) if words else 0
        }
        
        return metrics
    
    def get_skill_frequency(self, texts):
        """Get frequency of skills across multiple texts"""
        all_skills = []
        
        for text in texts:
            skills = self.extract_skills_basic(text)
            all_skills.extend(skills)
        
        skill_freq = Counter(all_skills)
        
        return pd.DataFrame(list(skill_freq.items()), columns=['skill', 'frequency']).sort_values('frequency', ascending=False)
    
    def compare_texts(self, text1, text2):
        """Compare two texts and find similarities/differences"""
        skills1 = set(self.extract_skills_basic(text1))
        skills2 = set(self.extract_skills_basic(text2))
        
        comparison = {
            'common_skills': list(skills1 & skills2),
            'unique_to_text1': list(skills1 - skills2),
            'unique_to_text2': list(skills2 - skills1),
            'similarity_score': len(skills1 & skills2) / len(skills1 | skills2) if (skills1 | skills2) else 0
        }
        
        return comparison
    
    def suggest_skill_improvements(self, user_skills, target_skills):
        """Suggest skill improvements based on target requirements"""
        user_skills_set = set(skill.lower() for skill in user_skills)
        target_skills_set = set(skill.lower() for skill in target_skills)
        
        suggestions = {
            'missing_critical': list(target_skills_set - user_skills_set),
            'skill_match_rate': len(user_skills_set & target_skills_set) / len(target_skills_set) if target_skills_set else 0,
            'additional_skills': list(user_skills_set - target_skills_set)
        }
        
        return suggestions
