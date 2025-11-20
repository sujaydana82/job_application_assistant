import os
import re
from typing import Dict, List, Tuple
from fpdf import FPDF
from .file_processor import FileProcessor
from datetime import datetime

class AIJobAssistant:
    def __init__(self):
        self.file_processor = FileProcessor()
    
    def analyze_job_requirements(self, job_description: str) -> Dict[str, List[str]]:
        """Comprehensive job description analysis"""
        requirements = {
            'skills': [],
            'technologies': [],
            'experience': [],
            'qualifications': [],
            'responsibilities': [],
            'soft_skills': [],
            'tools': [],
            'all_detected_skills': []
        }
        
        text_lower = job_description.lower()
        
        # Comprehensive skill detection
        skill_categories = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'php', 'ruby', 'scala'],
            'web_frontend': ['html', 'css', 'react', 'angular', 'vue', 'svelte', 'bootstrap', 'tailwind', 'jquery', 'next.js', 'nuxt.js'],
            'web_backend': ['node.js', 'django', 'flask', 'spring', 'express', 'laravel', 'ruby on rails', 'asp.net', 'fastapi', 'graphql'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'dynamodb', 'cassandra', 'cosmos db', 'firebase'],
            'cloud': ['aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd', 'devops', 'serverless'],
            'data_science': ['pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'r', 'matplotlib', 'tableau', 'power bi', 'spark'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'swift', 'kotlin', 'xamarin'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'teams', 'docker', 'jenkins', 'ansible', 'puppet', 'chef', 'github', 'gitlab'],
            'methodologies': ['agile', 'scrum', 'kanban', 'waterfall', 'devops', 'cicd', 'tdd', 'bdd']
        }
        
        soft_skills = ['leadership', 'communication', 'teamwork', 'problem-solving', 'critical thinking', 
                      'adaptability', 'time management', 'creativity', 'collaboration', 'analytical',
                      'project management', 'stakeholder management', 'mentoring', 'presentation']
        
        # Extract ALL technical skills
        all_skills = []
        for category, skills in skill_categories.items():
            for skill in skills:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    requirements['skills'].append(skill)
                    all_skills.append(skill)
        
        # Extract ALL soft skills
        for skill in soft_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                requirements['soft_skills'].append(skill)
                all_skills.append(skill)
        
        requirements['all_detected_skills'] = all_skills
        
        # Enhanced experience extraction
        experience_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)[-+]?\s*to\s*(\d+)\s*years?',
            r'minimum\s+of\s+(\d+)\s*years?',
            r'at\s+least\s+(\d+)\s*years?',
            r'(\d+)\s*-\s*(\d+)\s*years?'
        ]
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                exp_text = match.group(0)
                if exp_text not in requirements['experience']:
                    requirements['experience'].append(exp_text)
        
        return requirements
    
    def analyze_cv_content(self, cv_text: str, requirements: Dict) -> Dict:
        """Analyze CV content against job requirements - COMPATIBILITY METHOD"""
        # This method maintains compatibility with the existing app
        cv_sections = self.file_processor.parse_cv_sections(cv_text)
        cv_skills = self._extract_all_skills_from_cv(cv_text)
        
        analysis = {
            'skills_found': [],
            'skills_missing': [],
            'skills_weak': [],
            'experience_alignment': [],
            'achievements_found': [],
            'summary_alignment': [],
            'cv_strengths': [],
            'cv_weaknesses': []
        }
        
        # Analyze skills
        for skill in requirements['skills']:
            if self._skill_exists_in_cv(skill, cv_text):
                analysis['skills_found'].append(skill)
            else:
                analysis['skills_missing'].append(skill)
        
        # Find skills that exist but need emphasis
        for skill in analysis['skills_found']:
            if not self._skill_is_strong_in_cv(skill, cv_text):
                analysis['skills_weak'].append(skill)
        
        # Analyze experience alignment
        analysis['experience_alignment'] = self._analyze_experience_alignment(cv_sections.get('experience', ''), requirements)
        
        # Extract achievements
        analysis['achievements_found'] = self.extract_achievements_from_cv(cv_text)
        
        # Analyze summary
        analysis['summary_alignment'] = self._analyze_summary_alignment(cv_sections.get('summary', ''), requirements)
        
        # Determine strengths and weaknesses
        analysis['cv_strengths'] = self._identify_strengths(analysis)
        analysis['cv_weaknesses'] = self._identify_weaknesses(analysis, requirements)
        
        return analysis
    
    def analyze_cv_vs_jd(self, cv_text: str, job_description: str) -> Dict:
        """Comprehensive analysis comparing CV with Job Description"""
        requirements = self.analyze_job_requirements(job_description)
        cv_skills = self._extract_all_skills_from_cv(cv_text)
        
        analysis = {
            'total_jd_skills': len(requirements['all_detected_skills']),
            'skills_matched': [],
            'skills_missing': [],
            'skills_partial_match': [],
            'match_percentage': 0,
            'cv_skills_found': cv_skills,
            'jd_skills_required': requirements['all_detected_skills'],
            'detailed_analysis': []
        }
        
        # Analyze each JD skill against CV
        for jd_skill in requirements['all_detected_skills']:
            jd_skill_lower = jd_skill.lower()
            matched = False
            partial_match = False
            
            for cv_skill in cv_skills:
                cv_skill_lower = cv_skill.lower()
                
                # Exact match
                if jd_skill_lower == cv_skill_lower:
                    analysis['skills_matched'].append({
                        'jd_skill': jd_skill,
                        'cv_skill': cv_skill,
                        'match_type': 'exact'
                    })
                    matched = True
                    break
                # Partial match (one contains the other)
                elif jd_skill_lower in cv_skill_lower or cv_skill_lower in jd_skill_lower:
                    analysis['skills_partial_match'].append({
                        'jd_skill': jd_skill,
                        'cv_skill': cv_skill,
                        'match_type': 'partial'
                    })
                    partial_match = True
                    break
            
            if not matched and not partial_match:
                analysis['skills_missing'].append(jd_skill)
        
        # Calculate match percentage
        total_matched = len(analysis['skills_matched']) + len(analysis['skills_partial_match'])
        analysis['match_percentage'] = int((total_matched / len(requirements['all_detected_skills'])) * 100) if requirements['all_detected_skills'] else 0
        
        return analysis
    
    def analyze_linkedin_vs_jd(self, linkedin_about: str, job_description: str) -> Dict:
        """Analyze LinkedIn About section against Job Description"""
        requirements = self.analyze_job_requirements(job_description)
        linkedin_skills = self._extract_skills_from_text(linkedin_about)
        
        analysis = {
            'linkedin_skills_found': linkedin_skills,
            'skills_matched': [],
            'skills_missing': [],
            'match_percentage': 0,
            'suggestions': []
        }
        
        # Analyze skill matching
        for jd_skill in requirements['all_detected_skills']:
            jd_skill_lower = jd_skill.lower()
            matched = False
            
            for li_skill in linkedin_skills:
                if jd_skill_lower in li_skill.lower() or li_skill.lower() in jd_skill_lower:
                    analysis['skills_matched'].append({
                        'jd_skill': jd_skill,
                        'linkedin_skill': li_skill
                    })
                    matched = True
                    break
            
            if not matched:
                analysis['skills_missing'].append(jd_skill)
        
        # Calculate match percentage
        analysis['match_percentage'] = int((len(analysis['skills_matched']) / len(requirements['all_detected_skills'])) * 100) if requirements['all_detected_skills'] else 0
        
        # Generate suggestions
        if analysis['skills_missing']:
            analysis['suggestions'].append(f"Add {len(analysis['skills_missing'])} missing skills to your LinkedIn About section")
        
        if analysis['match_percentage'] < 70:
            analysis['suggestions'].append("Consider optimizing your About section with more job-specific keywords")
        
        return analysis
    
    def generate_cv_improvements(self, original_cv: str, job_description: str, linkedin_url: str = "") -> str:
        """Generate comprehensive CV improvement suggestions"""
        analysis = self.analyze_cv_vs_jd(original_cv, job_description)
        
        cv_improvements = f"""COMPREHENSIVE CV vs JOB DESCRIPTION ANALYSIS
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 MATCH ANALYSIS:
• Overall Match: {analysis['match_percentage']}%
• JD Skills Required: {analysis['total_jd_skills']}
• Skills Matched: {len(analysis['skills_matched'])}
• Skills Partially Matched: {len(analysis['skills_partial_match'])}
• Skills Missing: {len(analysis['skills_missing'])}

✅ EXACT MATCHES ({len(analysis['skills_matched'])}):
{chr(10).join([f'• {match["jd_skill"]} → {match["cv_skill"]}' for match in analysis['skills_matched'][:15]]) if analysis['skills_matched'] else '• No exact matches found'}

🟡 PARTIAL MATCHES ({len(analysis['skills_partial_match'])}):
{chr(10).join([f'• {match["jd_skill"]} → {match["cv_skill"]}' for match in analysis['skills_partial_match'][:10]]) if analysis['skills_partial_match'] else '• No partial matches found'}

❌ MISSING SKILLS ({len(analysis['skills_missing'])}):
{chr(10).join([f'• {skill}' for skill in analysis['skills_missing'][:20]]) if analysis['skills_missing'] else '• All skills covered!'}

🎯 IMPROVEMENT STRATEGY:

1. PRIORITY SKILLS TO ADD:
{chr(10).join([f'• {skill}' for skill in analysis['skills_missing'][:10]]) if analysis['skills_missing'] else '• Your CV already covers all required skills!'}

2. SKILLS TO EMPHASIZE:
{chr(10).join([f'• {match["jd_skill"]} - Add specific project examples' for match in analysis['skills_partial_match'][:5]]) if analysis['skills_partial_match'] else '• All matched skills are well-emphasized'}

3. YOUR CV STRENGTHS:
• {len(analysis['cv_skills_found'])} total skills identified in your CV
• Strong alignment in {len(analysis['skills_matched'])} key areas

🚀 ACTION PLAN:
1. {f"Add top {min(5, len(analysis['skills_missing']))} missing skills to your CV" if analysis['skills_missing'] else "Maintain current skill coverage"}
2. {f"Strengthen {min(3, len(analysis['skills_partial_match']))} partial matches with specific examples" if analysis['skills_partial_match'] else "All skills are well-represented"}
3. "Highlight your strongest matches in your professional summary"
"""
        return cv_improvements
    
    def generate_linkedin_suggestions(self, linkedin_about: str, job_description: str, cv_text: str = "") -> str:
        """Generate LinkedIn optimization suggestions"""
        linkedin_analysis = self.analyze_linkedin_vs_jd(linkedin_about, job_description)
        cv_analysis = self.analyze_cv_vs_jd(cv_text, job_description) if cv_text else None
        
        # Generate headline suggestions
        headline_suggestions = self._generate_linkedin_headlines(cv_analysis, linkedin_analysis, job_description)
        
        linkedin_suggestions = f"""LINKEDIN PROFILE OPTIMIZATION
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 LINKEDIN vs JD ANALYSIS:
• Match Percentage: {linkedin_analysis['match_percentage']}%
• Skills in LinkedIn: {len(linkedin_analysis['linkedin_skills_found'])}
• Skills Matched: {len(linkedin_analysis['skills_matched'])}
• Skills Missing: {len(linkedin_analysis['skills_missing'])}

🎯 RECOMMENDED HEADLINES:
{chr(10).join([f'• {headline}' for headline in headline_suggestions[:3]])}

✅ SKILLS ALREADY IN YOUR LINKEDIN:
{chr(10).join([f'• {match["jd_skill"]}' for match in linkedin_analysis['skills_matched'][:10]]) if linkedin_analysis['skills_matched'] else '• No matching skills found in LinkedIn About section'}

❌ SKILLS MISSING FROM LINKEDIN:
{chr(10).join([f'• {skill}' for skill in linkedin_analysis['skills_missing'][:15]]) if linkedin_analysis['skills_missing'] else '• All key skills are already in your LinkedIn!'}

📝 ABOUT SECTION OPTIMIZATION:

CURRENT ANALYSIS:
{chr(10).join([f'• {suggestion}' for suggestion in linkedin_analysis['suggestions']]) if linkedin_analysis['suggestions'] else '• Your About section is well-optimized'}

RECOMMENDED UPDATES:
1. Add these missing skills: {', '.join(linkedin_analysis['skills_missing'][:8]) if linkedin_analysis['skills_missing'] else 'All key skills covered'}
2. Emphasize your expertise in: {', '.join([match['jd_skill'] for match in linkedin_analysis['skills_matched'][:3]]) if linkedin_analysis['skills_matched'] else 'key technical areas'}
3. Include quantifiable achievements from your CV

🚀 QUICK WINS:
✓ Update headline with job-specific keywords
✓ Add missing skills to About section
✓ Request endorsements for matched skills
✓ Share content related to missing skills
"""
        return linkedin_suggestions

    def generate_linkedin_improvements(self, cv_text: str, job_description: str, linkedin_url: str = "") -> str:
        """Generate LinkedIn improvements when no About section is provided"""
        analysis = self.analyze_cv_vs_jd(cv_text, job_description)
        requirements = self.analyze_job_requirements(job_description)
        
        linkedin_improvements = f"""LINKEDIN PROFILE OPTIMIZATION
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Based on your CV analysis against the job description:

📊 CV vs JD ANALYSIS:
• Overall Match: {analysis['match_percentage']}%
• Skills Matched: {len(analysis['skills_matched'])}
• Skills Missing: {len(analysis['skills_missing'])}

🎯 RECOMMENDED HEADLINES:
{chr(10).join([f'• {headline}' for headline in self._generate_linkedin_headlines(analysis, None, job_description)[:3]])}

🔧 KEY SKILLS TO FEATURE ON LINKEDIN:
{chr(10).join([f'• {match["jd_skill"]}' for match in analysis['skills_matched'][:10]]) if analysis['skills_matched'] else '• Focus on adding key skills from the job description'}

📝 ABOUT SECTION STRATEGY:
• Start with: "Experienced professional with expertise in {', '.join([match['jd_skill'] for match in analysis['skills_matched'][:3]]) if analysis['skills_matched'] else 'relevant technologies'}"
• Include keywords: {', '.join(requirements['skills'][:8])}
• Highlight your strongest matches from CV

🚀 IMMEDIATE ACTIONS:
✓ Update headline with your top matched skills
✓ Ensure all matched skills are listed in your LinkedIn Skills section
✓ Add missing key skills to your About section
✓ Request endorsements for your strongest skills
"""
        return linkedin_improvements
    
    def generate_motivation_letter(self, cv_text: str, job_description: str, linkedin_url: str = "") -> str:
        """Generate motivation letter using actual analysis"""
        analysis = self.analyze_cv_vs_jd(cv_text, job_description)
        requirements = self.analyze_job_requirements(job_description)
        
        company_name = self._extract_company_name(job_description)
        position_name = self._extract_position_name(job_description)
        
        # Use actual matched skills
        matched_skills = [match['jd_skill'] for match in analysis['skills_matched'][:5]]
        your_skills = ', '.join(matched_skills) if matched_skills else 'relevant technical skills'
        
        motivation_letter = f"""[Your Name]
[Your Address] • [Your Email] • [Your Phone] • {linkedin_url if linkedin_url else '[Your LinkedIn Profile]'}

{datetime.now().strftime('%B %d, %Y')}

Hiring Manager
{company_name}
[Company Address]

Subject: Application for {position_name} Position

Dear Hiring Manager,

I am writing to express my enthusiastic interest in the {position_name} position at {company_name}. With my expertise in {your_skills} and strong alignment with your requirements, I am confident in my ability to contribute significantly to your team.

What sets me apart for this role:

• Direct experience with {your_skills} as demonstrated in my previous roles
• {analysis['match_percentage']}% skill match with your requirements
• Proven track record of delivering measurable results

I am particularly excited about this opportunity at {company_name} because [specific reason related to company mission or projects]. My background in {your_skills} positions me perfectly to address your current needs and contribute to your team's success.

Thank you for considering my application. I have attached my CV for your review and would welcome the opportunity to discuss how my specific experience with {your_skills} can benefit {company_name}.

Sincerely,
[Your Name]
"""
        return motivation_letter
    
    def generate_interview_preparation(self, job_description: str, cv_text: str) -> str:
        """Generate interview preparation guide based on CV analysis"""
        requirements = self.analyze_job_requirements(job_description)
        analysis = self.analyze_cv_content(cv_text, requirements)
        
        interview_prep = f"""PERSONALIZED INTERVIEW PREPARATION GUIDE
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Based on your CV analysis, focus on these areas:

🎯 YOUR STRENGTHS TO EMPHASIZE:
• Expertise in: {', '.join(analysis['skills_found'][:5])}
• Key achievements: {chr(10).join([f'  - {achievement}' for achievement in analysis['achievements_found'][:3]])}
• Experience alignment: {analysis['experience_alignment'][0] if analysis['experience_alignment'] else 'Strong match with role requirements'}

📝 TECHNICAL QUESTIONS TO EXPECT:
1. "Can you elaborate on your experience with {analysis['skills_found'][0] if analysis['skills_found'] else 'key technologies'}?"
   - Prepare: Detailed examples from your CV showing {analysis['skills_found'][0] if analysis['skills_found'] else 'your expertise'}

2. "How have you used {analysis['skills_found'][1] if len(analysis['skills_found']) > 1 else 'relevant skills'} in previous projects?"
   - Focus on: {analysis['achievements_found'][0] if analysis['achievements_found'] else 'your most relevant project'}

💡 BEHAVIORAL PREPARATION:
• "Walk me through {analysis['achievements_found'][0] if analysis['achievements_found'] else 'a significant project'}" - Use STAR method
• "How do you handle challenges with {analysis['skills_weak'][0] if analysis['skills_weak'] else 'complex projects'}?" - Show learning ability

🎤 YOUR ACHIEVEMENT STORIES:
{chr(10).join([f'• {achievement}' for achievement in analysis['achievements_found'][:3]])}

✅ FINAL PREPARATION:
• Review your CV highlights: {', '.join(analysis['skills_found'][:3])}
• Practice explaining: {analysis['achievements_found'][0] if analysis['achievements_found'] else 'your key projects'}
• Research: {self._extract_company_name(job_description)}'s recent initiatives
"""
        return interview_prep
    
    # ===== SUPPORT METHODS =====
    
    def _extract_all_skills_from_cv(self, cv_text: str) -> List[str]:
        """Extract ALL skills from CV"""
        cv_sections = self.file_processor.parse_cv_sections(cv_text)
        skills_section = cv_sections.get('skills', '')
        
        # Comprehensive skill extraction
        all_skills = []
        
        # Extract from skills section
        if skills_section:
            # Split by common separators
            skills = re.split(r'[,•\-\n|]', skills_section)
            for skill in skills:
                skill_clean = skill.strip()
                if skill_clean and len(skill_clean) > 2:
                    all_skills.append(skill_clean)
        
        # Extract from entire CV using keyword matching
        technical_keywords = [
            'python', 'java', 'javascript', 'aws', 'azure', 'docker', 'kubernetes', 
            'terraform', 'ansible', 'git', 'jenkins', 'ci/cd', 'devops', 'sql',
            'react', 'angular', 'node.js', 'typescript', 'html', 'css', 'mongodb',
            'postgresql', 'mysql', 'redis', 'linux', 'unix', 'bash', 'shell'
        ]
        
        cv_lower = cv_text.lower()
        for keyword in technical_keywords:
            if keyword in cv_lower:
                all_skills.append(keyword)
        
        # Remove duplicates and return
        return list(set(all_skills))
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from any text (LinkedIn About, etc.)"""
        if not text:
            return []
        
        technical_keywords = [
            'python', 'java', 'javascript', 'aws', 'azure', 'docker', 'kubernetes', 
            'terraform', 'ansible', 'git', 'jenkins', 'ci/cd', 'devops', 'sql',
            'react', 'angular', 'node.js', 'typescript', 'html', 'css', 'mongodb',
            'postgresql', 'mysql', 'redis', 'linux', 'unix', 'bash', 'shell'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for keyword in technical_keywords:
            if keyword in text_lower:
                found_skills.append(keyword)
        
        return list(set(found_skills))
    
    def _generate_linkedin_headlines(self, cv_analysis: Dict, linkedin_analysis: Dict, job_description: str) -> List[str]:
        """Generate LinkedIn headline suggestions"""
        headlines = []
        requirements = self.analyze_job_requirements(job_description)
        
        # Get top matched skills
        top_skills = []
        if cv_analysis and cv_analysis['skills_matched']:
            top_skills = [match['jd_skill'] for match in cv_analysis['skills_matched'][:3]]
        elif linkedin_analysis and linkedin_analysis['skills_matched']:
            top_skills = [match['jd_skill'] for match in linkedin_analysis['skills_matched'][:3]]
        
        # Generate headline variations
        if top_skills:
            headlines.append(f"{top_skills[0].title()} | {top_skills[1] if len(top_skills) > 1 else 'Cloud'} Engineer | {requirements['skills'][0] if requirements['skills'] else 'Technology'}")
            headlines.append(f"Senior {top_skills[0].title()} Professional | {', '.join(top_skills[:2])} | Open to Opportunities")
            headlines.append(f"{top_skills[0].title()} Specialist | {top_skills[1] if len(top_skills) > 1 else 'Full Stack'} Developer | Cloud & DevOps")
        else:
            headlines.append("Technology Professional | Cloud Engineer | Software Development")
            headlines.append("Senior Technical Specialist | Open to New Challenges")
            headlines.append("IT Professional | Cloud & DevOps | Software Engineering")
        
        return headlines

    # ===== COMPATIBILITY METHODS =====
    
    def _skill_exists_in_cv(self, skill: str, cv_text: str) -> bool:
        """Check if skill exists in CV with context"""
        pattern = r'\b' + re.escape(skill) + r'\b'
        return bool(re.search(pattern, cv_text.lower()))
    
    def _skill_is_strong_in_cv(self, skill: str, cv_text: str) -> bool:
        """Check if skill is strongly represented in CV"""
        cv_sections = self.file_processor.parse_cv_sections(cv_text)
        skills_section = cv_sections.get('skills', '').lower()
        experience_section = cv_sections.get('experience', '').lower()
        
        pattern = r'\b' + re.escape(skill) + r'\b'
        
        in_skills = bool(re.search(pattern, skills_section))
        in_experience = bool(re.search(pattern, experience_section))
        multiple_mentions = len(re.findall(pattern, cv_text.lower())) > 1
        
        return in_skills and (in_experience or multiple_mentions)
    
    def _analyze_experience_alignment(self, experience_text: str, requirements: Dict) -> List[str]:
        """Analyze how well experience matches requirements"""
        alignment = []
        exp_lower = experience_text.lower()
        
        for skill in requirements['skills'][:5]:
            if re.search(r'\b' + re.escape(skill) + r'\b', exp_lower):
                alignment.append(f"✅ Experience with {skill} is well-documented")
        
        return alignment if alignment else ["✅ Experience section shows good alignment with requirements"]
    
    def _analyze_summary_alignment(self, summary_text: str, requirements: Dict) -> List[str]:
        """Analyze summary alignment with job requirements"""
        alignment = []
        summary_lower = summary_text.lower() if summary_text else ""
        
        for skill in requirements['skills'][:3]:
            if re.search(r'\b' + re.escape(skill) + r'\b', summary_lower):
                alignment.append(f"✅ {skill} mentioned in summary")
        
        return alignment if alignment else ["✅ Summary is well-structured"]
    
    def _identify_strengths(self, analysis: Dict) -> List[str]:
        """Identify CV strengths"""
        strengths = []
        
        if len(analysis['skills_found']) > len(analysis['skills_missing']):
            strengths.append(f"Strong skills match ({len(analysis['skills_found'])}/{len(analysis['skills_found']) + len(analysis['skills_missing'])} key skills)")
        
        if analysis['achievements_found']:
            strengths.append(f"Good quantifiable achievements ({len(analysis['achievements_found'])} found)")
        
        if analysis['experience_alignment']:
            strengths.append("Experience well-aligned with requirements")
        
        return strengths if strengths else ["Good CV structure and content organization"]
    
    def _identify_weaknesses(self, analysis: Dict, requirements: Dict) -> List[str]:
        """Identify CV weaknesses"""
        weaknesses = []
        
        if analysis['skills_missing']:
            weaknesses.append(f"Missing {len(analysis['skills_missing'])} key skills from job description")
        
        if analysis['skills_weak']:
            weaknesses.append(f"{len(analysis['skills_weak'])} skills need stronger emphasis")
        
        if not analysis['achievements_found']:
            weaknesses.append("Add more quantifiable achievements")
        
        return weaknesses
    
    def extract_achievements_from_cv(self, cv_text: str) -> List[str]:
        """Extract quantifiable achievements from CV"""
        achievements = []
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
    
    def _extract_company_name(self, job_description: str) -> str:
        """Extract company name from job description"""
        patterns = [
            r'at\s+([A-Z][a-zA-Z0-9\s&\.\-]+?)(?=\s|$|,)',
            r'for\s+([A-Z][a-zA-Z0-9\s&\.\-]+?)(?=\s|$|,)',
            r'company:\s*([^\n,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                # Clean the company name
                company = re.sub(r'\b(company|inc|llc|corp|ltd|position|role)\b', '', company, flags=re.IGNORECASE)
                company = re.sub(r'\s+', ' ', company).strip()
                if company and len(company) > 2:
                    return company
        
        return "[Company Name]"
    
    def _extract_position_name(self, job_description: str) -> str:
        """Extract position name from job description"""
        first_line = job_description.split('\n')[0].strip()
        if len(first_line) < 100 and not first_line.startswith(('http', 'www')):
            return first_line
        return "[Position Name]"
    
    def save_as_txt(self, content: str, filename: str) -> str:
        """Save content as text file"""
        os.makedirs('generated_files', exist_ok=True)
        filepath = os.path.join('generated_files', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def save_as_pdf(self, content: str, filename: str) -> str:
        """Save content as PDF file"""
        try:
            os.makedirs('generated_files', exist_ok=True)
            filepath = os.path.join('generated_files', filename)
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=10)
            
            clean_content = content.replace('•', '-').replace('✓', '[X]')
            
            lines = clean_content.split('\n')
            for line in lines:
                if pdf.get_string_width(line) > 190:
                    pdf.multi_cell(0, 5, line)
                else:
                    pdf.cell(0, 5, line, ln=True)
            
            pdf.output(filepath)
            return filepath
            
        except Exception as e:
            return self.save_as_txt(content, filename.replace('.pdf', '.txt'))