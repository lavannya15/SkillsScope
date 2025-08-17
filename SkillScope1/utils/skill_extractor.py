import re
from collections import defaultdict
import pandas as pd

class SkillExtractor:
    """Advanced skill extraction from job descriptions and resumes"""
    
    def __init__(self):
        # Comprehensive skill database with variations
        self.skill_database = {
            # Programming Languages
            'python': ['python', 'py', 'python3', 'python2'],
            'java': ['java', 'java8', 'java11', 'openjdk'],
            'javascript': ['javascript', 'js', 'ecmascript', 'es6', 'es5'],
            'typescript': ['typescript', 'ts'],
            'c++': ['c++', 'cpp', 'c plus plus'],
            'c#': ['c#', 'csharp', 'c sharp'],
            'php': ['php', 'php7', 'php8'],
            'ruby': ['ruby', 'ruby on rails', 'ror'],
            'go': ['go', 'golang'],
            'swift': ['swift', 'swift ui'],
            'kotlin': ['kotlin'],
            'scala': ['scala'],
            'r': ['r programming', 'r language'],
            'sql': ['sql', 'mysql', 'postgresql', 'sqlite', 't-sql'],
            'html': ['html', 'html5'],
            'css': ['css', 'css3'],
            'matlab': ['matlab'],
            'perl': ['perl'],
            'shell': ['bash', 'shell scripting', 'powershell'],
            
            # Web Frameworks
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
            
            # Databases
            'mysql': ['mysql'],
            'postgresql': ['postgresql', 'postgres'],
            'mongodb': ['mongodb', 'mongo'],
            'redis': ['redis'],
            'elasticsearch': ['elasticsearch', 'elastic search'],
            'cassandra': ['cassandra'],
            'dynamodb': ['dynamodb', 'dynamo db'],
            'oracle': ['oracle database', 'oracle db'],
            'sql server': ['sql server', 'microsoft sql server'],
            'sqlite': ['sqlite'],
            
            # Cloud Platforms
            'aws': ['aws', 'amazon web services'],
            'azure': ['microsoft azure', 'azure'],
            'gcp': ['google cloud', 'gcp', 'google cloud platform'],
            'heroku': ['heroku'],
            'digital ocean': ['digital ocean', 'digitalocean'],
            
            # DevOps & Tools
            'docker': ['docker', 'containerization'],
            'kubernetes': ['kubernetes', 'k8s'],
            'jenkins': ['jenkins'],
            'git': ['git', 'github', 'gitlab', 'bitbucket'],
            'terraform': ['terraform'],
            'ansible': ['ansible'],
            'linux': ['linux', 'ubuntu', 'centos', 'rhel'],
            'unix': ['unix'],
            'ci/cd': ['ci/cd', 'continuous integration', 'continuous deployment'],
            
            # Data Science & ML
            'machine learning': ['machine learning', 'ml', 'artificial intelligence', 'ai'],
            'deep learning': ['deep learning', 'neural networks'],
            'tensorflow': ['tensorflow', 'tf'],
            'pytorch': ['pytorch'],
            'keras': ['keras'],
            'scikit-learn': ['scikit-learn', 'sklearn'],
            'pandas': ['pandas'],
            'numpy': ['numpy'],
            'matplotlib': ['matplotlib'],
            'seaborn': ['seaborn'],
            'jupyter': ['jupyter', 'jupyter notebook'],
            'spark': ['apache spark', 'pyspark'],
            'hadoop': ['hadoop'],
            'kafka': ['apache kafka', 'kafka'],
            
            # Business Intelligence
            'tableau': ['tableau'],
            'power bi': ['power bi', 'powerbi'],
            'qlik': ['qlikview', 'qlik sense'],
            'looker': ['looker'],
            'sas': ['sas'],
            'spss': ['spss'],
            
            # Design Tools
            'figma': ['figma'],
            'sketch': ['sketch'],
            'adobe xd': ['adobe xd', 'xd'],
            'photoshop': ['photoshop', 'adobe photoshop'],
            'illustrator': ['illustrator', 'adobe illustrator'],
            'indesign': ['indesign', 'adobe indesign'],
            
            # Project Management
            'agile': ['agile', 'agile methodology'],
            'scrum': ['scrum'],
            'kanban': ['kanban'],
            'jira': ['jira'],
            'confluence': ['confluence'],
            'trello': ['trello'],
            'asana': ['asana'],
            'project management': ['project management', 'pm'],
            
            # Microsoft Office
            'excel': ['excel', 'microsoft excel'],
            'powerpoint': ['powerpoint', 'microsoft powerpoint'],
            'word': ['microsoft word', 'ms word'],
            'outlook': ['outlook', 'microsoft outlook'],
            'sharepoint': ['sharepoint'],
            
            # Finance & Analytics
            'bloomberg': ['bloomberg terminal', 'bloomberg'],
            'reuters': ['reuters', 'refinitiv'],
            'factset': ['factset'],
            'matlab': ['matlab'],
            'r': ['r programming', 'r statistical'],
            'stata': ['stata'],
            'financial modeling': ['financial modeling', 'financial models'],
            'valuation': ['valuation', 'dcf', 'comparable analysis'],
            'risk management': ['risk management', 'var', 'stress testing'],
            
            # Soft Skills
            'leadership': ['leadership', 'team leadership', 'leading teams'],
            'communication': ['communication', 'verbal communication', 'written communication'],
            'problem solving': ['problem solving', 'analytical thinking'],
            'teamwork': ['teamwork', 'collaboration'],
            'time management': ['time management', 'organization'],
            'critical thinking': ['critical thinking', 'analytical skills'],
            'creativity': ['creativity', 'innovation'],
            'adaptability': ['adaptability', 'flexibility'],
            
            # Industry Specific
            'healthcare': ['hipaa', 'hl7', 'epic', 'cerner', 'clinical research'],
            'cybersecurity': ['cybersecurity', 'information security', 'penetration testing', 'ethical hacking'],
            'networking': ['networking', 'tcp/ip', 'vpn', 'firewall', 'routing'],
            'mobile development': ['ios development', 'android development', 'mobile apps'],
            'game development': ['unity', 'unreal engine', 'game development'],
            'blockchain': ['blockchain', 'ethereum', 'smart contracts', 'cryptocurrency']
        }
        
        # Create reverse mapping for faster lookup
        self.variation_to_skill = {}
        for skill, variations in self.skill_database.items():
            for variation in variations:
                self.variation_to_skill[variation.lower()] = skill
    
    def extract_skills_from_text(self, text):
        """Extract skills from text using pattern matching and NLP"""
        if not text:
            return []
        
        # Preprocess text
        text = self.preprocess_text(text)
        
        found_skills = set()
        
        # Method 1: Direct pattern matching
        skills_from_patterns = self._extract_by_patterns(text)
        found_skills.update(skills_from_patterns)
        
        # Method 2: Context-based extraction
        skills_from_context = self._extract_by_context(text)
        found_skills.update(skills_from_context)
        
        # Method 3: N-gram analysis
        skills_from_ngrams = self._extract_by_ngrams(text)
        found_skills.update(skills_from_ngrams)
        
        return list(found_skills)
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Handle special cases
        text = re.sub(r'\bc\+\+\b', 'c++', text)
        text = re.sub(r'\bc#\b', 'c#', text)
        text = re.sub(r'\bnode\.js\b', 'node.js', text)
        text = re.sub(r'\basp\.net\b', 'asp.net', text)
        
        return text
    
    def _extract_by_patterns(self, text):
        """Extract skills using direct pattern matching"""
        found_skills = set()
        
        for variation, skill in self.variation_to_skill.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(variation) + r'\b'
            if re.search(pattern, text):
                found_skills.add(skill)
        
        return found_skills
    
    def _extract_by_context(self, text):
        """Extract skills based on context clues"""
        found_skills = set()
        
        # Common contexts where skills appear
        context_patterns = [
            r'(?:experience (?:with|in)|skilled in|proficient in|knowledge of|familiar with|expertise in|worked with|using|utilize|implement|develop(?:ed|ing)?(?:\s+with)?)\s+([^,.\n]+)',
            r'(?:languages?|technologies?|tools?|frameworks?|platforms?|software|skills?)[:\s]+([^.\n]+)',
            r'(?:programming|coding|development)\s+(?:languages?|experience)\s*[:\s]+([^.\n]+)',
            r'(?:database|db)\s*[:\s]+([^.\n]+)',
            r'(?:cloud|hosting)\s*[:\s]+([^.\n]+)'
        ]
        
        for pattern in context_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Split by common delimiters and check each part
                parts = re.split(r'[,;/&\n\r]+', match)
                for part in parts:
                    part = part.strip()
                    if part and len(part) > 1:
                        # Check if this part contains any known skill variations
                        for variation, skill in self.variation_to_skill.items():
                            if variation in part.lower():
                                found_skills.add(skill)
        
        return found_skills
    
    def _extract_by_ngrams(self, text):
        """Extract skills using n-gram analysis"""
        found_skills = set()
        
        words = text.split()
        
        # Check unigrams, bigrams, and trigrams
        for n in range(1, 4):
            ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
            for ngram in ngrams:
                if ngram in self.variation_to_skill:
                    found_skills.add(self.variation_to_skill[ngram])
        
        return found_skills
    
    def extract_skills_with_confidence(self, text):
        """Extract skills with confidence scores"""
        if not text:
            return []
        
        text = self.preprocess_text(text)
        skill_scores = defaultdict(float)
        
        # Pattern matching (high confidence)
        pattern_skills = self._extract_by_patterns(text)
        for skill in pattern_skills:
            skill_scores[skill] += 0.8
        
        # Context-based (medium confidence)
        context_skills = self._extract_by_context(text)
        for skill in context_skills:
            skill_scores[skill] += 0.6
        
        # N-gram analysis (lower confidence)
        ngram_skills = self._extract_by_ngrams(text)
        for skill in ngram_skills:
            skill_scores[skill] += 0.4
        
        # Boost score for skills mentioned multiple times
        for skill in skill_scores:
            variations = self.skill_database.get(skill, [skill])
            mention_count = sum(text.count(var) for var in variations)
            if mention_count > 1:
                skill_scores[skill] += 0.2 * (mention_count - 1)
        
        # Return skills with confidence > 0.5
        result = [(skill, min(score, 1.0)) for skill, score in skill_scores.items() if score >= 0.5]
        result.sort(key=lambda x: x[1], reverse=True)
        
        return result
    
    def categorize_skills(self, skills):
        """Categorize skills into different types"""
        categories = {
            'Programming Languages': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'swift', 'kotlin', 'scala', 'r', 'matlab'],
            'Web Technologies': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'express', 'node.js', 'spring', 'laravel', 'asp.net', 'jquery', 'bootstrap'],
            'Databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'oracle', 'sql server', 'sqlite'],
            'Cloud & DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'terraform', 'ansible', 'linux', 'ci/cd'],
            'Data Science & ML': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'spark', 'hadoop'],
            'Business Intelligence': ['tableau', 'power bi', 'excel', 'qlik', 'looker', 'sas', 'spss'],
            'Design Tools': ['figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator'],
            'Project Management': ['agile', 'scrum', 'kanban', 'jira', 'project management'],
            'Soft Skills': ['leadership', 'communication', 'problem solving', 'teamwork', 'time management', 'critical thinking']
        }
        
        categorized = {}
        uncategorized = []
        
        for skill in skills:
            categorized_flag = False
            for category, category_skills in categories.items():
                if skill.lower() in [s.lower() for s in category_skills]:
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(skill)
                    categorized_flag = True
                    break
            
            if not categorized_flag:
                uncategorized.append(skill)
        
        if uncategorized:
            categorized['Other'] = uncategorized
        
        return categorized
    
    def get_skill_synonyms(self, skill):
        """Get synonyms/variations for a skill"""
        skill_lower = skill.lower()
        return self.skill_database.get(skill_lower, [skill])
    
    def suggest_related_skills(self, skills):
        """Suggest related skills based on current skill set"""
        suggestions = defaultdict(int)
        
        # Define skill relationships
        relationships = {
            'python': ['pandas', 'numpy', 'django', 'flask', 'machine learning', 'tensorflow'],
            'javascript': ['react', 'angular', 'vue', 'node.js', 'typescript'],
            'react': ['redux', 'next.js', 'javascript', 'typescript'],
            'machine learning': ['python', 'r', 'tensorflow', 'pytorch', 'scikit-learn'],
            'aws': ['docker', 'kubernetes', 'terraform', 'linux'],
            'sql': ['mysql', 'postgresql', 'database design', 'data analysis'],
            'docker': ['kubernetes', 'linux', 'ci/cd', 'aws'],
            'data analysis': ['python', 'r', 'sql', 'tableau', 'excel']
        }
        
        # Score related skills
        for skill in skills:
            related = relationships.get(skill.lower(), [])
            for related_skill in related:
                if related_skill not in [s.lower() for s in skills]:
                    suggestions[related_skill] += 1
        
        # Return top suggestions
        return sorted(suggestions.items(), key=lambda x: x[1], reverse=True)[:10]
