import streamlit as st
import os
import tempfile
from datetime import datetime
from utils.ai_helpers import AIJobAssistant
from utils.file_processor import FileProcessor

# Initialize assistants
assistant = AIJobAssistant()
file_processor = FileProcessor()

def main():
    st.set_page_config(
        page_title="AI Job Application Assistant",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .stTextArea textarea {
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">💼 AI Job Application Assistant</h1>', unsafe_allow_html=True)
    st.markdown("Upload your documents to generate tailored application materials")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("""
        This tool helps you:
        - 📝 Improve your CV for specific jobs
        - 🔗 Optimize your LinkedIn profile
        - 💌 Generate motivation letters
        - 🎯 Prepare for interviews
        """)
        
        st.header("Instructions")
        st.write("""
        1. Upload your current CV
        2. Provide the job description
        3. Add your LinkedIn profile URL
        4. Paste your LinkedIn About section (optional)
        5. Generate improvement suggestions
        6. Download the results
        """)
    
    # Initialize session state
    if 'edited_content' not in st.session_state:
        st.session_state.edited_content = {
            'cv_improvements': '',
            'linkedin_suggestions': '',
            'motivation_letter': '',
            'interview_preparation': ''
        }
    
    if 'last_saved_files' not in st.session_state:
        st.session_state.last_saved_files = {
            'cv_improvements_txt': None,
            'cv_improvements_pdf': None,
            'linkedin_suggestions_txt': None,
            'linkedin_suggestions_pdf': None,
            'motivation_letter_txt': None,
            'motivation_letter_pdf': None,
            'interview_preparation_txt': None,
            'interview_preparation_pdf': None
        }
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📄 Document Upload", "🛠️ Improvement Suggestions", "⚙️ Settings"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Upload Your Documents")
            
            # CV Upload
            cv_file = st.file_uploader(
                "Upload Your CV", 
                type=['pdf', 'docx', 'txt'],
                help="Supported formats: PDF, DOCX, TXT",
                key="cv_uploader"
            )
            
            # Job Description Upload
            jd_file = st.file_uploader(
                "Upload Job Description", 
                type=['pdf', 'docx', 'txt'],
                help="The job description you're applying for",
                key="jd_uploader"
            )
            
            # LinkedIn URL
            linkedin_url = st.text_input(
                "LinkedIn Profile URL",
                placeholder="https://linkedin.com/in/yourprofile",
                help="For LinkedIn profile improvement suggestions",
                key="linkedin_url"
            )
            
            # LinkedIn About Section
            st.subheader("LinkedIn About Section (Optional)")
            linkedin_about = st.text_area(
                "Paste your LinkedIn About section for optimization:",
                height=150,
                placeholder="Paste your current LinkedIn About section here for personalized optimization suggestions...",
                key="linkedin_about"
            )
            
            # Direct JD input
            st.subheader("Or Paste Job Description")
            jd_text = st.text_area(
                "Paste job description here:",
                height=200,
                placeholder="Copy and paste the job description text here...",
                label_visibility="collapsed",
                key="jd_text_area"
            )
            
            # Generate button
            generate_btn = st.button(
                "🚀 Generate Improvement Suggestions", 
                type="primary",
                use_container_width=True,
                key="generate_btn"
            )
        
        with col2:
            st.subheader("📊 Document Preview")
            
            if cv_file:
                st.write(f"**CV Uploaded:** {cv_file.name}")
                try:
                    cv_preview = file_processor.process_uploaded_file(cv_file)
                    with st.expander("CV Preview (First 500 characters)"):
                        st.text(cv_preview[:500] + "..." if len(cv_preview) > 500 else cv_preview)
                except Exception as e:
                    st.error(f"Error reading CV: {str(e)}")
            
            if jd_file or jd_text:
                if jd_file:
                    st.write(f"**JD Uploaded:** {jd_file.name}")
                    try:
                        jd_preview = file_processor.process_uploaded_file(jd_file)
                        with st.expander("Job Description Preview (First 500 characters)"):
                            st.text(jd_preview[:500] + "..." if len(jd_preview) > 500 else jd_preview)
                    except Exception as e:
                        st.error(f"Error reading job description: {str(e)}")
                else:
                    st.write("**Job Description:** Text input")
                    with st.expander("Job Description Preview (First 500 characters)"):
                        st.text(jd_text[:500] + "..." if len(jd_text) > 500 else jd_text)
            
            if linkedin_url:
                st.write(f"**LinkedIn URL:** {linkedin_url}")
            
            if linkedin_about:
                st.write(f"**LinkedIn About:** {len(linkedin_about)} characters provided")
                with st.expander("LinkedIn About Preview"):
                    st.text(linkedin_about[:300] + "..." if len(linkedin_about) > 300 else linkedin_about)
    
    with tab2:
        if 'generated_materials' not in st.session_state:
            st.session_state.generated_materials = None
        
        if generate_btn and (cv_file or jd_file or jd_text):
            with st.spinner("🔄 Analyzing documents and generating improvement suggestions..."):
                try:
                    # Process files
                    cv_text = ""
                    jd_text_final = jd_text
                    
                    if cv_file:
                        cv_text = file_processor.process_uploaded_file(cv_file)
                    
                    if jd_file and not jd_text:
                        jd_text_final = file_processor.process_uploaded_file(jd_file)
                    
                    # Generate improvement suggestions using NEW methods
                    cv_improvements = assistant.generate_cv_improvements(cv_text, jd_text_final, linkedin_url)
                    
                    # Generate LinkedIn suggestions if About section is provided
                    if linkedin_about:
                        linkedin_suggestions = assistant.generate_linkedin_suggestions(linkedin_about, jd_text_final, cv_text)
                    else:
                        linkedin_suggestions = assistant.generate_linkedin_improvements(cv_text, jd_text_final, linkedin_url)
                    
                    motivation_letter = assistant.generate_motivation_letter(cv_text, jd_text_final, linkedin_url)
                    interview_preparation = assistant.generate_interview_preparation(jd_text_final, cv_text)
                    
                    # Store in session state
                    st.session_state.generated_materials = {
                        'cv_improvements': cv_improvements,
                        'linkedin_suggestions': linkedin_suggestions,
                        'motivation_letter': motivation_letter,
                        'interview_preparation': interview_preparation,
                        'timestamp': datetime.now()
                    }
                    
                    # Initialize edited content with generated materials
                    st.session_state.edited_content = {
                        'cv_improvements': cv_improvements,
                        'linkedin_suggestions': linkedin_suggestions,
                        'motivation_letter': motivation_letter,
                        'interview_preparation': interview_preparation
                    }
                    
                    st.success("✅ Improvement suggestions generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating materials: {str(e)}")
        
        # Display improvement suggestions with editing capability
        if st.session_state.generated_materials:
            doc_tab1, doc_tab2, doc_tab3, doc_tab4 = st.tabs([
                "📝 CV Improvements", 
                "🔗 LinkedIn Suggestions",
                "💌 Motivation Letter", 
                "🎯 Interview Prep"
            ])
            
            with doc_tab1:
                st.subheader("CV Improvement Suggestions")
                
                # Editable text area for CV improvements
                edited_cv_improvements = st.text_area(
                    "Edit your CV improvement suggestions:",
                    value=st.session_state.edited_content['cv_improvements'],
                    height=400,
                    key="cv_improvements_editor"
                )
                
                # Update session state with edited content
                st.session_state.edited_content['cv_improvements'] = edited_cv_improvements
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save CV Improvements as TXT", key="save_cv_improvements_txt"):
                        filename = f"cv_improvements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        filepath = assistant.save_as_txt(st.session_state.edited_content['cv_improvements'], filename)
                        st.session_state.last_saved_files['cv_improvements_txt'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                with col2:
                    if st.button("💾 Save CV Improvements as PDF", key="save_cv_improvements_pdf"):
                        filename = f"cv_improvements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        filepath = assistant.save_as_pdf(st.session_state.edited_content['cv_improvements'], filename)
                        st.session_state.last_saved_files['cv_improvements_pdf'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                # Show last saved files
                if st.session_state.last_saved_files['cv_improvements_txt'] or st.session_state.last_saved_files['cv_improvements_pdf']:
                    with st.expander("📁 Last Saved Files"):
                        if st.session_state.last_saved_files['cv_improvements_txt']:
                            st.write(f"TXT: `{st.session_state.last_saved_files['cv_improvements_txt']}`")
                        if st.session_state.last_saved_files['cv_improvements_pdf']:
                            st.write(f"PDF: `{st.session_state.last_saved_files['cv_improvements_pdf']}`")
            
            with doc_tab2:
                st.subheader("LinkedIn Optimization Suggestions")
                
                # Editable text area for LinkedIn suggestions
                edited_linkedin_suggestions = st.text_area(
                    "Edit your LinkedIn suggestions:",
                    value=st.session_state.edited_content['linkedin_suggestions'],
                    height=400,
                    key="linkedin_suggestions_editor"
                )
                
                # Update session state with edited content
                st.session_state.edited_content['linkedin_suggestions'] = edited_linkedin_suggestions
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save LinkedIn Suggestions as TXT", key="save_linkedin_suggestions_txt"):
                        filename = f"linkedin_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        filepath = assistant.save_as_txt(st.session_state.edited_content['linkedin_suggestions'], filename)
                        st.session_state.last_saved_files['linkedin_suggestions_txt'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                with col2:
                    if st.button("💾 Save LinkedIn Suggestions as PDF", key="save_linkedin_suggestions_pdf"):
                        filename = f"linkedin_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        filepath = assistant.save_as_pdf(st.session_state.edited_content['linkedin_suggestions'], filename)
                        st.session_state.last_saved_files['linkedin_suggestions_pdf'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                # Show last saved files
                if st.session_state.last_saved_files['linkedin_suggestions_txt'] or st.session_state.last_saved_files['linkedin_suggestions_pdf']:
                    with st.expander("📁 Last Saved Files"):
                        if st.session_state.last_saved_files['linkedin_suggestions_txt']:
                            st.write(f"TXT: `{st.session_state.last_saved_files['linkedin_suggestions_txt']}`")
                        if st.session_state.last_saved_files['linkedin_suggestions_pdf']:
                            st.write(f"PDF: `{st.session_state.last_saved_files['linkedin_suggestions_pdf']}`")
            
            with doc_tab3:
                st.subheader("Tailored Motivation Letter")
                
                # Editable text area for motivation letter
                edited_letter = st.text_area(
                    "Edit your motivation letter:",
                    value=st.session_state.edited_content['motivation_letter'],
                    height=400,
                    key="letter_editor"
                )
                
                # Update session state with edited content
                st.session_state.edited_content['motivation_letter'] = edited_letter
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Letter as TXT", key="save_letter_txt"):
                        filename = f"motivation_letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        filepath = assistant.save_as_txt(st.session_state.edited_content['motivation_letter'], filename)
                        st.session_state.last_saved_files['motivation_letter_txt'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                with col2:
                    if st.button("💾 Save Letter as PDF", key="save_letter_pdf"):
                        filename = f"motivation_letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        filepath = assistant.save_as_pdf(st.session_state.edited_content['motivation_letter'], filename)
                        st.session_state.last_saved_files['motivation_letter_pdf'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                # Show last saved files
                if st.session_state.last_saved_files['motivation_letter_txt'] or st.session_state.last_saved_files['motivation_letter_pdf']:
                    with st.expander("📁 Last Saved Files"):
                        if st.session_state.last_saved_files['motivation_letter_txt']:
                            st.write(f"TXT: `{st.session_state.last_saved_files['motivation_letter_txt']}`")
                        if st.session_state.last_saved_files['motivation_letter_pdf']:
                            st.write(f"PDF: `{st.session_state.last_saved_files['motivation_letter_pdf']}`")
            
            with doc_tab4:
                st.subheader("Interview Preparation Guide")
                
                # Editable text area for interview preparation
                edited_interview_prep = st.text_area(
                    "Edit your interview preparation guide:",
                    value=st.session_state.edited_content['interview_preparation'],
                    height=400,
                    key="interview_prep_editor"
                )
                
                # Update session state with edited content
                st.session_state.edited_content['interview_preparation'] = edited_interview_prep
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Interview Prep as TXT", key="save_interview_prep_txt"):
                        filename = f"interview_preparation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        filepath = assistant.save_as_txt(st.session_state.edited_content['interview_preparation'], filename)
                        st.session_state.last_saved_files['interview_preparation_txt'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                with col2:
                    if st.button("💾 Save Interview Prep as PDF", key="save_interview_prep_pdf"):
                        filename = f"interview_preparation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        filepath = assistant.save_as_pdf(st.session_state.edited_content['interview_preparation'], filename)
                        st.session_state.last_saved_files['interview_preparation_pdf'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                # Show last saved files
                if st.session_state.last_saved_files['interview_preparation_txt'] or st.session_state.last_saved_files['interview_preparation_pdf']:
                    with st.expander("📁 Last Saved Files"):
                        if st.session_state.last_saved_files['interview_preparation_txt']:
                            st.write(f"TXT: `{st.session_state.last_saved_files['interview_preparation_txt']}`")
                        if st.session_state.last_saved_files['interview_preparation_pdf']:
                            st.write(f"PDF: `{st.session_state.last_saved_files['interview_preparation_pdf']}`")
            
            # Add a reset button to revert to original generated content
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Reset to Original Generated Content", type="secondary", key="reset_content"):
                    st.session_state.edited_content = {
                        'cv_improvements': st.session_state.generated_materials['cv_improvements'],
                        'linkedin_suggestions': st.session_state.generated_materials['linkedin_suggestions'],
                        'motivation_letter': st.session_state.generated_materials['motivation_letter'],
                        'interview_preparation': st.session_state.generated_materials['interview_preparation']
                    }
                    st.success("Content reset to original generated versions!")
    
    with tab3:
        st.subheader("Configuration & Enhancements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Current Features:**
            - Comprehensive CV vs JD skill matching
            - LinkedIn About section optimization
            - Personalized headline suggestions
            - Motivation letter generation
            - Interview preparation guide
            - File export (TXT/PDF)
            """)
        
        with col2:
            st.warning("""
            **Future Enhancements:**
            - AI integration (OpenAI/Ollama)
            - LinkedIn profile scraping
            - Advanced templates
            - Application tracking
            """)
        
        # File management section
        st.subheader("File Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Generated Files", key="clear_files"):
                import shutil
                try:
                    if os.path.exists('generated_files'):
                        shutil.rmtree('generated_files')
                    os.makedirs('generated_files', exist_ok=True)
                    st.session_state.last_saved_files = {
                        'cv_improvements_txt': None, 'cv_improvements_pdf': None,
                        'linkedin_suggestions_txt': None, 'linkedin_suggestions_pdf': None,
                        'motivation_letter_txt': None, 'motivation_letter_pdf': None,
                        'interview_preparation_txt': None, 'interview_preparation_pdf': None
                    }
                    st.success("Generated files cleared!")
                except Exception as e:
                    st.error(f"Error clearing files: {e}")
        
        with col2:
            if st.button("Clear All Data", type="secondary", key="clear_all_data"):
                st.session_state.clear()
                st.success("All data cleared!")

if __name__ == "__main__":
    main()