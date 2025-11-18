import os
import re
from typing import Dict, List
from fpdf import FPDF
from .file_processor import FileProcessor
from datetime import datetime

class AIJobAssistant:
    def __init__(self):
        self.file_processor = FileProcessor()
    
    def analyze_job_requirements(self, job_description: str) -> Dict[str, List[str]]:
        """Comprehensive job description analysis - FIXED VERSION"""
        requirements = {
            'skills': [],
            'technologies': [],
            'experience': [],
            'qualifications': [],
            'responsibilities': [],
            'soft_skills': [],
            'tools': []
        }
        
        text_lower = job_description.lower()
        
        # More conservative skill detection - only add if clearly mentioned
        skill_categories = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'php', 'ruby'],
            'web_frontend': ['html', 'css', 'react', 'angular', 'vue', 'svelte', 'bootstrap', 'tailwind', 'jquery'],
            'web_backend': ['node.js', 'django', 'flask', 'spring', 'express', 'laravel', 'ruby on rails', 'asp.net'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'dynamodb', 'cassandra'],
            'cloud': ['aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd', 'devops'],
            'data_science': ['pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'r', 'matplotlib', 'tableau'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'swift', 'kotlin'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'teams', 'docker', 'jenkins', 'ansible']
        }
        
        soft_skills = ['leadership', 'communication', 'teamwork', 'problem-solving', 'critical thinking', 
                      'adaptability', 'time management', 'creativity', 'collaboration', 'analytical']
        
        # Extract technical skills with context awareness
        for category, skills in skill_categories.items():
            for skill in skills:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    requirements['skills'].append(skill)
        
        # Extract soft skills with context awareness
        for skill in soft_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                requirements['soft_skills'].append(skill)
        
        # Enhanced experience extraction
        experience_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)[-+]?\s*to\s*(\d+)\s*years?',
            r'minimum\s+of\s+(\d+)\s*years?',
            r'at\s+least\s+(\d+)\s*years?'
        ]
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                exp_text = match.group(0)
                if exp_text not in requirements['experience']:
                    requirements['experience'].append(exp_text)
        
        # Extract qualifications
        qualification_keywords = [
            'bachelor', "bachelor's", 'master', "master's", 'phd', 'doctorate', 
            'degree', 'certification', 'diploma', 'bsc', 'msc', 'mba'
        ]
        for qual in qualification_keywords:
            pattern = r'\b' + re.escape(qual) + r'\b'
            if re.search(pattern, text_lower):
                requirements['qualifications'].append(qual)
        
        return requirements
    
    def extract_achievements_from_cv(self, cv_text: str) -> List[str]:
        """Extract quantifiable achievements from CV"""
        achievements = []
        
        # Patterns for quantifiable achievements
        patterns = [
            r'increased\s+[^.]*\s+by\s+(\d+%|\$\d+)',
            r'reduced\s+[^.]*\s+by\s+(\d+%|\$\d+)',
            r'improved\s+[^.]*\s+by\s+(\d+%)',
            r'saved\s+[^.]*\s+(\d+%|\$\d+)',
            r'achieved\s+[^.]*\s+(\d+%)',
            r'led\s+[^.]*\s+team',
            r'managed\s+[^.]*\s+project',
            r'developed\s+[^.]*\s+system',
            r'implemented\s+[^.]*\s+solution'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, cv_text.lower())
            for match in matches:
                achievement = match.group(0).capitalize()
                if achievement not in achievements:
                    achievements.append(achievement)
        
        return achievements[:10]
    
    def generate_updated_cv(self, original_cv: str, job_description: str, linkedin_data: str = "") -> str:
        """Generate SPECIFIC MODIFICATIONS needed for CV based on job description analysis"""
        requirements = self.analyze_job_requirements(job_description)
        cv_sections = self.file_processor.parse_cv_sections(original_cv)
        achievements = self.extract_achievements_from_cv(original_cv)
        
        # Analyze gaps and specific modifications needed
        missing_skills = self._find_missing_skills(cv_sections.get('skills', ''), requirements)
        experience_gaps = self._analyze_experience_gaps(cv_sections.get('experience', ''), requirements)
        summary_improvements = self._analyze_summary_improvements(cv_sections.get('summary', ''), requirements)
        
        updated_cv = f"""CV MODIFICATION REQUIREMENTS FOR JOB APPLICATION
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

JOB REQUIREMENTS SUMMARY:
- Must-have Skills: {', '.join(requirements['skills'][:8])}
- Experience Required: {', '.join(requirements['experience']) if requirements['experience'] else 'Not specified'}
- Qualifications: {', '.join(requirements['qualifications']) if requirements['qualifications'] else 'Not specified'}

IMMEDIATE MODIFICATIONS REQUIRED:

1. SKILLS SECTION UPDATES:
{self._format_skills_modifications(cv_sections.get('skills', ''), requirements, missing_skills)}

2. EXPERIENCE SECTION ENHANCEMENTS:
{self._format_experience_modifications(cv_sections.get('experience', ''), requirements, experience_gaps)}

3. PROFESSIONAL SUMMARY REWRITE:
{self._format_summary_modifications(cv_sections.get('summary', ''), requirements, summary_improvements)}

4. ACHIEVEMENTS TO HIGHLIGHT:
{self._format_achievements_modifications(achievements, requirements)}

5. KEYWORDS TO ADD THROUGHOUT CV:
{', '.join(requirements['skills'][:10])}

ACTION PLAN:
[X] Update skills section with missing keywords
[X] Rewrite professional summary to match job requirements
[X] Enhance experience descriptions with relevant technologies
[X] Add quantifiable achievements in bullet points
[X] Ensure all job description keywords are included

MODIFIED SECTIONS TEMPLATE:

PROFESSIONAL SUMMARY (Rewrite):
{self._generate_summary_template(requirements, len(requirements['experience']))}

SKILLS SECTION (Add these):
Technical: {', '.join(missing_skills[:5])}
Tools: {', '.join([skill for skill in requirements['skills'] if skill in ['git', 'docker', 'jenkins', 'jira']][:3])}

EXPERIENCE BULLET POINTS (Add these examples):
- Developed solutions using {requirements['skills'][0] if requirements['skills'] else 'relevant technologies'} to achieve business objectives
- Collaborated with cross-functional teams to deliver projects on time
- Implemented best practices for {requirements['skills'][1] if len(requirements['skills']) > 1 else 'key technologies'}
"""
        return updated_cv
    
    def _find_missing_skills(self, current_skills: str, requirements: Dict) -> List[str]:
        """Find skills in job description missing from CV - FIXED VERSION"""
        current_skills_lower = current_skills.lower()
        missing = []
        for skill in requirements['skills']:
            # More precise matching - check if skill is actually in the skills section
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if not re.search(pattern, current_skills_lower):
                missing.append(skill)
        return missing[:10]
    
    def _get_existing_relevant_skills(self, current_skills: str, requirements: Dict) -> List[str]:
        """Get skills that are actually in the CV and relevant to the job - FIXED VERSION"""
        current_skills_lower = current_skills.lower()
        existing = []
        for skill in requirements['skills']:
            # More precise matching with word boundaries
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, current_skills_lower):
                existing.append(skill)
        return existing
    
    def _analyze_experience_gaps(self, current_experience: str, requirements: Dict) -> List[str]:
        """Analyze experience gaps between CV and job requirements"""
        gaps = []
        current_exp_lower = current_experience.lower()
        
        for skill in requirements['skills'][:5]:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if not re.search(pattern, current_exp_lower):
                gaps.append(f"Add experience with {skill}")
        
        if requirements['experience'] and not any(exp in current_exp_lower for exp in ['year', 'experience']):
            gaps.append(f"Highlight {requirements['experience'][0]} of relevant experience")
        
        return gaps
    
    def _analyze_summary_improvements(self, current_summary: str, requirements: Dict) -> List[str]:
        """Identify summary section improvements needed"""
        improvements = []
        current_summary_lower = current_summary.lower()
        
        # Check if key skills are mentioned in summary
        for skill in requirements['skills'][:3]:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if not re.search(pattern, current_summary_lower):
                improvements.append(f"Include '{skill}' in summary")
        
        if requirements['experience']:
            if not any(exp in current_summary_lower for exp in ['year', 'experience', 'experienced']):
                improvements.append(f"Add experience level: {requirements['experience'][0]}")
        
        return improvements
    
    def _format_skills_modifications(self, current_skills: str, requirements: Dict, missing_skills: List[str]) -> str:
        """Format skills modification recommendations - FIXED VERSION"""
        existing_relevant_skills = self._get_existing_relevant_skills(current_skills, requirements)
        
        modifications = f"""CURRENT SKILLS LENGTH: {len(current_skills)} characters

ADD THESE SKILLS (Missing from your CV):
{chr(10).join([f'- {skill}' for skill in missing_skills[:8]])}

EMPHASIZE THESE EXISTING SKILLS (Already in your CV):
{chr(10).join([f'- {skill}' for skill in existing_relevant_skills[:5]]) if existing_relevant_skills else '- No matching skills found in your current CV'}

REMOVE OR DEPRIORITIZE:
- Skills not mentioned in job description
- Outdated or irrelevant technologies"""
        
        return modifications
    
    def _format_experience_modifications(self, current_experience: str, requirements: Dict, experience_gaps: List[str]) -> str:
        """Format experience modification recommendations"""
        modifications = f"""CURRENT EXPERIENCE LENGTH: {len(current_experience)} characters

IMMEDIATE UPDATES NEEDED:
{chr(10).join([f'- {gap}' for gap in experience_gaps])}

ADD QUANTIFIABLE METRICS:
- Include numbers, percentages, and specific outcomes
- Use action verbs: Developed, Led, Implemented, Optimized
- Focus on results rather than responsibilities

TECHNOLOGY SPECIFIC UPDATES:
- Mention specific technologies from job description
- Add context about how you used each technology
- Include project scope and impact"""
        
        return modifications
    
    def _format_summary_modifications(self, current_summary: str, requirements: Dict, summary_improvements: List[str]) -> str:
        """Format summary modification recommendations"""
        modifications = f"""CURRENT SUMMARY LENGTH: {len(current_summary)} characters

REQUIRED IMPROVEMENTS:
{chr(10).join([f'- {improvement}' for improvement in summary_improvements])}

NEW SUMMARY SHOULD INCLUDE:
- Years of experience matching job requirements
- Key technical skills from job description
- Relevant industry keywords
- Career objectives aligned with position"""
        
        return modifications
    
    def _format_achievements_modifications(self, achievements: List[str], requirements: Dict) -> str:
        """Format achievements modification recommendations"""
        if not achievements:
            return "- ADD: Quantifiable achievements with metrics\n- INCLUDE: Specific projects and outcomes\n- HIGHLIGHT: Business impact of your work"
        
        return f"""EXISTING ACHIEVEMENTS TO EMPHASIZE:
{chr(10).join([f'- {achievement}' for achievement in achievements[:3]])}

ADDITIONAL ACHIEVEMENTS TO INCLUDE:
- Projects using {requirements['skills'][0] if requirements['skills'] else 'relevant technologies'}
- Leadership experiences
- Problem-solving examples"""
    
    def _generate_summary_template(self, requirements: Dict, experience_years: int) -> str:
        """Generate a summary template based on requirements"""
        experience_text = requirements['experience'][0] if requirements['experience'] else "X"
        top_skills = requirements['skills'][:3]
        
        return f"""Results-driven professional with {experience_text} years of experience in {', '.join(top_skills)}. 
Proven track record of delivering successful projects and solutions. 
Seeking to leverage expertise in {top_skills[0] if top_skills else 'relevant technologies'} 
to contribute to challenging opportunities at target organization."""
    
    def generate_motivation_letter(self, cv_text: str, job_description: str, linkedin_data: str = "") -> str:
        """Generate detailed motivation letter"""
        requirements = self.analyze_job_requirements(job_description)
        achievements = self.extract_achievements_from_cv(cv_text)
        
        # Extract company and position details
        company_match = re.search(r'(?:at|for|in)\s+([A-Z][a-zA-Z0-9\s&\.]+)', job_description, re.IGNORECASE)
        company_name = company_match.group(1) if company_match else "[Company Name]"
        
        position_match = re.search(r'(position|role|job)\s+of\s+([A-Z][a-zA-Z0-9\s&]+)', job_description, re.IGNORECASE)
        position_name = position_match.group(2) if position_match else "[Position Name]"
        
        motivation_letter = f"""MOTIVATION LETTER
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

[Your Name]
[Your Address] - [Your Email] - [Your Phone] - [LinkedIn Profile]

{datetime.now().strftime('%B %d, %Y')}

Hiring Manager
{company_name}
[Company Address]

Subject: Application for {position_name} Position

Dear Hiring Manager,

I am writing with great enthusiasm to apply for the {position_name} position at {company_name}. With my extensive experience in {', '.join(requirements['skills'][:3])} and proven track record in delivering successful projects, I am confident that I possess the skills and expertise necessary to excel in this role.

WHAT I BRING TO {company_name.upper()}:

Technical Expertise:
- Proficient in {', '.join(requirements['skills'][:5])}
- Experience with {requirements['skills'][5] if len(requirements['skills']) > 5 else 'relevant technologies'}
- Strong background in {requirements['responsibilities'][0] if requirements['responsibilities'] else 'key responsibilities mentioned'}

Key Achievements Relevant to This Role:
{chr(10).join([f'- {achievement}' for achievement in achievements[:3]])}

Why I'm Excited About This Opportunity:
- The chance to work with cutting-edge technologies like {requirements['skills'][0] if requirements['skills'] else 'your technology stack'}
- The opportunity to contribute to {company_name}'s mission and projects
- Alignment between the role's requirements and my professional background

My experience has prepared me to:
- {requirements['responsibilities'][0] if requirements['responsibilities'] else 'Handle key responsibilities effectively'}
- Collaborate effectively with cross-functional teams
- Deliver high-quality solutions under tight deadlines

I am particularly impressed by {company_name}'s [mention something specific about the company - research this] and believe my skills in {requirements['skills'][1] if len(requirements['skills']) > 1 else 'relevant areas'} would be valuable for your team.

Thank you for considering my application. I have attached my CV for your review and would welcome the opportunity to discuss how my experience and skills align with your needs.

Sincerely,
[Your Name]
"""
        return motivation_letter
    
    def generate_interview_cheatsheet(self, job_description: str, cv_text: str) -> str:
        """Generate comprehensive interview cheatsheet with answers"""
        requirements = self.analyze_job_requirements(job_description)
        achievements = self.extract_achievements_from_cv(cv_text)
        cv_sections = self.file_processor.parse_cv_sections(cv_text)
        
        cheatsheet = f"""COMPREHENSIVE INTERVIEW PREPARATION CHEATSHEET
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

SECTION 1: ROLE ANALYSIS
--------------------------------------------------

TECHNICAL REQUIREMENTS:
{chr(10).join([f'- {skill.upper()}: Must-have skill' for skill in requirements['skills'][:8]])}

EXPERIENCE LEVEL: {', '.join(requirements['experience'])}
QUALIFICATIONS: {', '.join(requirements['qualifications'])}
SOFT SKILLS REQUIRED: {', '.join(requirements['soft_skills'][:5])}

SECTION 2: TECHNICAL INTERVIEW PREPARATION
--------------------------------------------------

EXPECTED TECHNICAL QUESTIONS & SUGGESTED ANSWERS:

1. "Describe your experience with {requirements['skills'][0] if requirements['skills'] else 'key technologies'}"
   SUGGESTED ANSWER:
   "In my previous role, I extensively worked with {requirements['skills'][0] if requirements['skills'] else 'relevant technologies'} 
   to develop [mention specific project]. I used it for [specific functionality] which resulted in [quantifiable outcome]."

2. "How do you approach problem-solving in technical projects?"
   SUGGESTED ANSWER:
   "I follow a structured approach: First, I analyze requirements and break down the problem. Then I research solutions, 
   prototype if needed, implement the best approach, and finally test thoroughly. For example, when facing [specific challenge], 
   I used this method to [achievement]."

3. "What are the best practices for {requirements['skills'][1] if len(requirements['skills']) > 1 else 'your primary technology'}?"
   SUGGESTED ANSWER:
   "Key best practices include: [mention 3-4 specific best practices]. In my experience at [previous company], 
   implementing these practices helped us achieve [specific positive outcome]."

SECTION 3: BEHAVIORAL INTERVIEW PREPARATION
--------------------------------------------------

STAR METHOD TEMPLATES:

1. "Tell me about a challenging project"
   - SITUATION: "At [Company], we faced [specific challenge]..."
   - TASK: "My responsibility was to [specific task]..."
   - ACTION: "I implemented [specific actions] using [technologies]..."
   - RESULT: "This resulted in [quantifiable achievement]..."

2. "Describe a time you had to learn new technology quickly"
   - SITUATION: "When we adopted [new technology] at [Company]..."
   - TASK: "I needed to become proficient within [timeframe]..."
   - ACTION: "I studied [resources], built [practice project], collaborated with [team]..."
   - RESULT: "Successfully delivered [project] using the new technology, resulting in [benefit]..."

YOUR SPECIFIC ACHIEVEMENTS TO DISCUSS:
{chr(10).join([f'- {achievement}' for achievement in achievements[:5]])}

SECTION 4: YOUR CV-BASED QUESTIONS
--------------------------------------------------

EXPECTED QUESTIONS ABOUT YOUR CV:

1. "Can you tell me more about your experience at [most recent company]?"
   PREPARED ANSWER: [Prepare 2-minute summary highlighting key achievements]

2. "I see you worked on [specific project from CV]. What was your role?"
   PREPARED ANSWER: [Detail your specific contributions and technologies used]

3. "Why are you looking to leave your current position?"
   PREPARED ANSWER: "I'm seeking new challenges in [specific area] and this role at your company perfectly aligns with my career goals."

SECTION 5: QUESTIONS TO ASK THE INTERVIEWER
--------------------------------------------------

TECHNICAL QUESTIONS:
- "What are the current biggest technical challenges the team is facing?"
- "What does the typical development workflow look like?"
- "How does the team handle technical debt?"

CULTURE & GROWTH QUESTIONS:
- "What opportunities for professional development are available?"
- "How does the company support continuous learning?"
- "Can you describe the team dynamics and collaboration style?"

ROLE-SPECIFIC QUESTIONS:
- "What would success look like in the first 6 months in this role?"
- "What are the key projects I would be working on initially?"

SECTION 6: TECHNICAL ASSESSMENT PREPARATION
--------------------------------------------------

KEY CONCEPTS TO REVIEW:
{chr(10).join([f'- {skill.upper()}: Review fundamentals, advanced concepts, and practical applications' for skill in requirements['skills'][:5]])}

PRACTICE EXERCISES:
- Whiteboard coding: Practice explaining your thought process
- System design: Be prepared to design a [relevant system type]
- Code review: Practice reviewing sample code for best practices

FINAL PREPARATION CHECKLIST:
[X] Research company recent news and projects
[X] Review job description thoroughly
[X] Practice explaining your key achievements
[X] Prepare 5+ intelligent questions to ask
[X] Review technical fundamentals
[X] Prepare examples of past successes
"""
        return cheatsheet
    
    def save_as_txt(self, content: str, filename: str) -> str:
        """Save content as text file"""
        os.makedirs('generated_files', exist_ok=True)
        filepath = os.path.join('generated_files', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def save_as_pdf(self, content: str, filename: str) -> str:
        """Save content as PDF file - FIXED VERSION"""
        try:
            os.makedirs('generated_files', exist_ok=True)
            filepath = os.path.join('generated_files', filename)
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=10)
            
            # Replace problematic Unicode characters
            clean_content = content.replace('•', '-').replace('✓', '[X]')
            
            # Simple line-by-line addition
            lines = clean_content.split('\n')
            for line in lines:
                if pdf.get_string_width(line) > 190:
                    # Use multi_cell for long lines
                    pdf.multi_cell(0, 5, line)
                else:
                    pdf.cell(0, 5, line, ln=True)
            
            pdf.output(filepath)
            return filepath
            
        except Exception as e:
            print(f"PDF generation failed, using TXT: {e}")
            return self.save_as_txt(content, filename.replace('.pdf', '.txt'))