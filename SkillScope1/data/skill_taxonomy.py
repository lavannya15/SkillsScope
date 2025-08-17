from collections import defaultdict
import re

class SkillTaxonomy:
    """Class to categorize and organize skills into meaningful taxonomies"""
    
    def __init__(self):
        # Define comprehensive skill categories with variations and synonyms
        self.skill_categories = {
            'Programming Languages': {
                'python': ['python', 'py', 'python3', 'python2'],
                'java': ['java', 'java8', 'java11', 'openjdk'],
                'javascript': ['javascript', 'js', 'ecmascript', 'es6', 'es5'],
                'typescript': ['typescript', 'ts'],
                'c++': ['c++', 'cpp', 'c plus plus'],
                'c#': ['c#', 'csharp', 'c sharp'],
                'php': ['php', 'php7', 'php8'],
                'ruby': ['ruby'],
                'go': ['go', 'golang'],
                'swift': ['swift'],
                'kotlin': ['kotlin'],
                'scala': ['scala'],
                'r': ['r', 'r programming', 'r language'],
                'sql': ['sql', 't-sql'],
                'html': ['html', 'html5'],
                'css': ['css', 'css3'],
                'matlab': ['matlab'],
                'perl': ['perl'],
                'rust': ['rust'],
                'dart': ['dart'],
                'lua': ['lua'],
                'shell': ['bash', 'shell scripting', 'powershell', 'zsh']
            },
            
            'Web Frameworks & Libraries': {
                'react': ['react', 'reactjs', 'react.js'],
                'angular': ['angular', 'angularjs'],
                'vue': ['vue', 'vuejs', 'vue.js'],
                'django': ['django'],
                'flask': ['flask'],
                'express': ['express', 'express.js', 'expressjs'],
                'node.js': ['node.js', 'nodejs', 'node js'],
                'spring': ['spring', 'spring boot', 'spring framework'],
                'laravel': ['laravel'],
                'asp.net': ['asp.net', 'aspnet'],
                'jquery': ['jquery'],
                'bootstrap': ['bootstrap'],
                'next.js': ['next.js', 'nextjs'],
                'nuxt.js': ['nuxt.js', 'nuxtjs'],
                'svelte': ['svelte'],
                'ember': ['ember', 'ember.js'],
                'backbone': ['backbone', 'backbone.js'],
                'rails': ['ruby on rails', 'rails', 'ror']
            },
            
            'Databases': {
                'mysql': ['mysql'],
                'postgresql': ['postgresql', 'postgres'],
                'mongodb': ['mongodb', 'mongo'],
                'redis': ['redis'],
                'elasticsearch': ['elasticsearch', 'elastic search'],
                'cassandra': ['cassandra'],
                'dynamodb': ['dynamodb', 'dynamo db'],
                'oracle': ['oracle database', 'oracle db', 'oracle'],
                'sql server': ['sql server', 'microsoft sql server'],
                'sqlite': ['sqlite'],
                'couchdb': ['couchdb'],
                'neo4j': ['neo4j'],
                'influxdb': ['influxdb'],
                'mariadb': ['mariadb'],
                'firebase': ['firebase', 'firestore']
            },
            
            'Cloud Platforms & Services': {
                'aws': ['aws', 'amazon web services'],
                'azure': ['microsoft azure', 'azure'],
                'gcp': ['google cloud', 'gcp', 'google cloud platform'],
                'heroku': ['heroku'],
                'digital ocean': ['digital ocean', 'digitalocean'],
                'linode': ['linode'],
                'vultr': ['vultr'],
                'cloudflare': ['cloudflare'],
                'netlify': ['netlify'],
                'vercel': ['vercel']
            },
            
            'DevOps & Infrastructure': {
                'docker': ['docker', 'containerization'],
                'kubernetes': ['kubernetes', 'k8s'],
                'jenkins': ['jenkins'],
                'git': ['git', 'github', 'gitlab', 'bitbucket'],
                'terraform': ['terraform'],
                'ansible': ['ansible'],
                'puppet': ['puppet'],
                'chef': ['chef'],
                'vagrant': ['vagrant'],
                'linux': ['linux', 'ubuntu', 'centos', 'rhel', 'debian'],
                'unix': ['unix'],
                'ci/cd': ['ci/cd', 'continuous integration', 'continuous deployment'],
                'monitoring': ['monitoring', 'observability'],
                'nginx': ['nginx'],
                'apache': ['apache', 'apache http server']
            },
            
            'Data Science & Analytics': {
                'machine learning': ['machine learning', 'ml'],
                'deep learning': ['deep learning', 'neural networks'],
                'artificial intelligence': ['artificial intelligence', 'ai'],
                'data analysis': ['data analysis', 'data analytics'],
                'statistics': ['statistics', 'statistical analysis'],
                'data mining': ['data mining'],
                'predictive modeling': ['predictive modeling'],
                'feature engineering': ['feature engineering'],
                'model deployment': ['model deployment'],
                'nlp': ['natural language processing', 'nlp'],
                'computer vision': ['computer vision', 'cv'],
                'time series': ['time series analysis'],
                'a/b testing': ['a/b testing', 'ab testing', 'split testing']
            },
            
            'ML/AI Frameworks & Tools': {
                'tensorflow': ['tensorflow', 'tf'],
                'pytorch': ['pytorch'],
                'keras': ['keras'],
                'scikit-learn': ['scikit-learn', 'sklearn'],
                'pandas': ['pandas'],
                'numpy': ['numpy'],
                'matplotlib': ['matplotlib'],
                'seaborn': ['seaborn'],
                'plotly': ['plotly'],
                'jupyter': ['jupyter', 'jupyter notebook'],
                'spark': ['apache spark', 'pyspark', 'spark'],
                'hadoop': ['hadoop'],
                'kafka': ['apache kafka', 'kafka'],
                'airflow': ['apache airflow', 'airflow'],
                'mlflow': ['mlflow'],
                'kubeflow': ['kubeflow']
            },
            
            'Business Intelligence & Visualization': {
                'tableau': ['tableau'],
                'power bi': ['power bi', 'powerbi'],
                'qlik': ['qlikview', 'qlik sense', 'qlik'],
                'looker': ['looker'],
                'sas': ['sas'],
                'spss': ['spss'],
                'excel': ['excel', 'microsoft excel'],
                'google sheets': ['google sheets'],
                'r shiny': ['shiny', 'r shiny'],
                'dash': ['plotly dash', 'dash'],
                'streamlit': ['streamlit']
            },
            
            'Design & Creative Tools': {
                'figma': ['figma'],
                'sketch': ['sketch'],
                'adobe xd': ['adobe xd', 'xd'],
                'photoshop': ['photoshop', 'adobe photoshop'],
                'illustrator': ['illustrator', 'adobe illustrator'],
                'indesign': ['indesign', 'adobe indesign'],
                'after effects': ['after effects', 'adobe after effects'],
                'premiere pro': ['premiere pro', 'adobe premiere'],
                'canva': ['canva'],
                'invision': ['invision']
            },
            
            'Project Management & Collaboration': {
                'agile': ['agile', 'agile methodology'],
                'scrum': ['scrum'],
                'kanban': ['kanban'],
                'waterfall': ['waterfall'],
                'lean': ['lean', 'lean methodology'],
                'six sigma': ['six sigma'],
                'jira': ['jira'],
                'confluence': ['confluence'],
                'trello': ['trello'],
                'asana': ['asana'],
                'monday': ['monday.com', 'monday'],
                'slack': ['slack'],
                'microsoft teams': ['microsoft teams', 'teams'],
                'zoom': ['zoom'],
                'notion': ['notion']
            },
            
            'Microsoft Office Suite': {
                'excel': ['excel', 'microsoft excel'],
                'powerpoint': ['powerpoint', 'microsoft powerpoint'],
                'word': ['microsoft word', 'ms word', 'word'],
                'outlook': ['outlook', 'microsoft outlook'],
                'sharepoint': ['sharepoint'],
                'onenote': ['onenote'],
                'access': ['microsoft access', 'access'],
                'visio': ['microsoft visio', 'visio']
            },
            
            'Finance & Trading Tools': {
                'bloomberg': ['bloomberg terminal', 'bloomberg'],
                'reuters': ['reuters', 'refinitiv'],
                'factset': ['factset'],
                'eikon': ['eikon'],
                'capital iq': ['capital iq'],
                'morningstar': ['morningstar'],
                'quickbooks': ['quickbooks'],
                'sap': ['sap'],
                'oracle financials': ['oracle financials']
            },
            
            'Security & Compliance': {
                'cybersecurity': ['cybersecurity', 'information security'],
                'penetration testing': ['penetration testing', 'pen testing'],
                'ethical hacking': ['ethical hacking'],
                'network security': ['network security'],
                'application security': ['application security'],
                'security frameworks': ['security frameworks'],
                'compliance': ['compliance'],
                'audit': ['audit', 'auditing'],
                'risk management': ['risk management'],
                'incident response': ['incident response'],
                'vulnerability assessment': ['vulnerability assessment'],
                'siem': ['siem']
            },
            
            'Soft Skills': {
                'leadership': ['leadership', 'team leadership', 'leading teams'],
                'communication': ['communication', 'verbal communication', 'written communication'],
                'problem solving': ['problem solving', 'analytical thinking'],
                'teamwork': ['teamwork', 'collaboration'],
                'time management': ['time management', 'organization'],
                'critical thinking': ['critical thinking', 'analytical skills'],
                'creativity': ['creativity', 'innovation'],
                'adaptability': ['adaptability', 'flexibility'],
                'emotional intelligence': ['emotional intelligence', 'eq'],
                'negotiation': ['negotiation', 'negotiation skills'],
                'presentation': ['presentation skills', 'public speaking'],
                'mentoring': ['mentoring', 'coaching'],
                'decision making': ['decision making'],
                'strategic thinking': ['strategic thinking', 'strategic planning']
            },
            
            'Industry Knowledge': {
                'healthcare': ['healthcare', 'medical', 'clinical'],
                'finance': ['finance', 'financial services', 'banking'],
                'e-commerce': ['e-commerce', 'ecommerce', 'retail'],
                'manufacturing': ['manufacturing', 'industrial'],
                'telecommunications': ['telecommunications', 'telecom'],
                'education': ['education', 'edtech'],
                'real estate': ['real estate', 'property'],
                'automotive': ['automotive', 'automotive industry'],
                'energy': ['energy', 'oil and gas', 'renewable energy'],
                'logistics': ['logistics', 'supply chain'],
                'gaming': ['gaming', 'game development'],
                'media': ['media', 'entertainment']
            },
            
            'Specialized Skills': {
                'blockchain': ['blockchain', 'cryptocurrency', 'bitcoin', 'ethereum'],
                'iot': ['iot', 'internet of things'],
                'ar/vr': ['augmented reality', 'virtual reality', 'ar', 'vr'],
                'robotics': ['robotics', 'automation'],
                'quantum computing': ['quantum computing'],
                'edge computing': ['edge computing'],
                'microservices': ['microservices', 'service oriented architecture'],
                'api development': ['api development', 'rest apis', 'graphql'],
                'mobile development': ['mobile development', 'ios development', 'android development'],
                'game development': ['game development', 'unity', 'unreal engine']
            }
        }
        
        # Create reverse mapping for faster lookup
        self.skill_to_category = {}
        self.variation_to_skill = {}
        
        for category, skills in self.skill_categories.items():
            for main_skill, variations in skills.items():
                self.skill_to_category[main_skill] = category
                for variation in variations:
                    self.variation_to_skill[variation.lower()] = main_skill
    
    def categorize_skills(self, skills):
        """Categorize a list of skills into their respective categories"""
        categorized = defaultdict(list)
        uncategorized = []
        
        for skill in skills:
            skill_lower = skill.lower().strip()
            
            # Try to find the skill or its variations
            main_skill = self.variation_to_skill.get(skill_lower)
            
            if main_skill:
                category = self.skill_to_category[main_skill]
                categorized[category].append(skill)
            else:
                # Try partial matching for compound skills
                found_category = self._find_partial_match(skill_lower)
                if found_category:
                    categorized[found_category].append(skill)
                else:
                    uncategorized.append(skill)
        
        # Convert to regular dict and add uncategorized if any
        result = dict(categorized)
        if uncategorized:
            result['Other'] = uncategorized
        
        return result
    
    def _find_partial_match(self, skill):
        """Find category through partial matching"""
        skill_words = skill.split()
        
        for category, skills in self.skill_categories.items():
            for main_skill, variations in skills.items():
                for variation in variations:
                    variation_words = variation.split()
                    
                    # Check if any word from skill matches any word from variation
                    if any(word in skill for word in variation_words if len(word) > 2):
                        return category
                    
                    # Check if skill contains the variation
                    if variation in skill or skill in variation:
                        return category
        
        return None
    
    def get_category_for_skill(self, skill):
        """Get the category for a specific skill"""
        skill_lower = skill.lower().strip()
        main_skill = self.variation_to_skill.get(skill_lower)
        
        if main_skill:
            return self.skill_to_category[main_skill]
        else:
            return self._find_partial_match(skill_lower)
    
    def get_skills_in_category(self, category):
        """Get all skills in a specific category"""
        if category in self.skill_categories:
            return list(self.skill_categories[category].keys())
        return []
    
    def get_all_categories(self):
        """Get all available categories"""
        return list(self.skill_categories.keys())
    
    def get_related_skills(self, skill, limit=10):
        """Get skills related to the given skill (same category)"""
        category = self.get_category_for_skill(skill)
        if category:
            related_skills = self.get_skills_in_category(category)
            # Remove the input skill itself
            related_skills = [s for s in related_skills if s.lower() != skill.lower()]
            return related_skills[:limit]
        return []
    
    def analyze_skill_distribution(self, skills):
        """Analyze the distribution of skills across categories"""
        categorized = self.categorize_skills(skills)
        
        analysis = {
            'total_skills': len(skills),
            'categories_covered': len(categorized),
            'category_distribution': {},
            'category_percentages': {}
        }
        
        for category, category_skills in categorized.items():
            count = len(category_skills)
            analysis['category_distribution'][category] = count
            analysis['category_percentages'][category] = round((count / len(skills)) * 100, 1)
        
        return analysis
    
    def suggest_skill_gaps(self, current_skills, target_role_skills):
        """Suggest skill gaps organized by category"""
        current_categorized = self.categorize_skills(current_skills)
        target_categorized = self.categorize_skills(target_role_skills)
        
        gaps = {}
        
        for category, target_skills in target_categorized.items():
            current_in_category = set(skill.lower() for skill in current_categorized.get(category, []))
            target_in_category = set(skill.lower() for skill in target_skills)
            
            missing_skills = target_in_category - current_in_category
            if missing_skills:
                gaps[category] = list(missing_skills)
        
        return gaps
    
    def get_skill_progression_path(self, current_skills, target_category):
        """Get a suggested learning path for a specific category"""
        if target_category not in self.skill_categories:
            return []
        
        current_categorized = self.categorize_skills(current_skills)
        current_in_target = set(skill.lower() for skill in current_categorized.get(target_category, []))
        
        # Define skill progression within categories
        progression_paths = {
            'Programming Languages': ['python', 'javascript', 'sql', 'java', 'typescript'],
            'Web Frameworks & Libraries': ['html', 'css', 'javascript', 'react', 'node.js'],
            'Data Science & Analytics': ['statistics', 'python', 'pandas', 'machine learning', 'deep learning'],
            'Cloud Platforms & Services': ['aws', 'docker', 'kubernetes', 'terraform'],
            'DevOps & Infrastructure': ['linux', 'git', 'docker', 'kubernetes', 'ci/cd'],
            'Business Intelligence & Visualization': ['excel', 'sql', 'tableau', 'power bi']
        }
        
        suggested_path = progression_paths.get(target_category, list(self.skill_categories[target_category].keys())[:5])
        
        # Filter out skills already known
        learning_path = [skill for skill in suggested_path if skill not in current_in_target]
        
        return learning_path[:5]  # Return top 5 suggestions
    
    def normalize_skill_name(self, skill):
        """Normalize skill name to its canonical form"""
        skill_lower = skill.lower().strip()
        main_skill = self.variation_to_skill.get(skill_lower)
        return main_skill if main_skill else skill
    
    def get_skill_synonyms(self, skill):
        """Get all synonyms/variations for a skill"""
        skill_lower = skill.lower().strip()
        main_skill = self.variation_to_skill.get(skill_lower, skill_lower)
        
        # Find the category and variations
        for category, skills in self.skill_categories.items():
            if main_skill in skills:
                return skills[main_skill]
        
        return [skill]
