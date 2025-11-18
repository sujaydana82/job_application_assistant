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
        - 📝 Tailor your CV to specific jobs
        - 💌 Generate motivation letters
        - 🎯 Create interview preparation guides
        """)
        
        st.header("Instructions")
        st.write("""
        1. Upload your current CV
        2. Provide the job description
        3. Generate tailored materials
        4. Edit the generated content if needed
        5. Download the results
        """)
    
    # Initialize session state
    if 'edited_content' not in st.session_state:
        st.session_state.edited_content = {
            'updated_cv': '',
            'motivation_letter': '',
            'interview_cheatsheet': ''
        }
    
    if 'last_saved_files' not in st.session_state:
        st.session_state.last_saved_files = {
            'cv_txt': None,
            'cv_pdf': None,
            'letter_txt': None,
            'letter_pdf': None,
            'cheatsheet_txt': None,
            'cheatsheet_pdf': None
        }
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📄 Document Upload", "🛠️ Generated Materials", "⚙️ Settings"])
    
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
                "LinkedIn Profile URL (Optional)",
                placeholder="https://linkedin.com/in/yourprofile",
                help="For additional context (future enhancement)",
                key="linkedin_url"
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
                "🚀 Generate Application Materials", 
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
    
    with tab2:
        if 'generated_materials' not in st.session_state:
            st.session_state.generated_materials = None
        
        if generate_btn and (cv_file or jd_file or jd_text):
            with st.spinner("🔄 Analyzing documents and generating materials..."):
                try:
                    # Process files
                    cv_text = ""
                    jd_text_final = jd_text
                    
                    if cv_file:
                        cv_text = file_processor.process_uploaded_file(cv_file)
                    
                    if jd_file and not jd_text:
                        jd_text_final = file_processor.process_uploaded_file(jd_file)
                    
                    # Generate materials
                    updated_cv = assistant.generate_updated_cv(cv_text, jd_text_final, linkedin_url)
                    motivation_letter = assistant.generate_motivation_letter(cv_text, jd_text_final, linkedin_url)
                    interview_cheatsheet = assistant.generate_interview_cheatsheet(jd_text_final, cv_text)
                    
                    # Store in session state
                    st.session_state.generated_materials = {
                        'updated_cv': updated_cv,
                        'motivation_letter': motivation_letter,
                        'interview_cheatsheet': interview_cheatsheet,
                        'timestamp': datetime.now()
                    }
                    
                    # Initialize edited content with generated materials
                    st.session_state.edited_content = {
                        'updated_cv': updated_cv,
                        'motivation_letter': motivation_letter,
                        'interview_cheatsheet': interview_cheatsheet
                    }
                    
                    st.success("✅ Materials generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating materials: {str(e)}")
        
        # Display generated materials with editing capability
        if st.session_state.generated_materials:
            doc_tab1, doc_tab2, doc_tab3 = st.tabs([
                "📝 Enhanced CV", 
                "💌 Motivation Letter", 
                "🎯 Interview Cheatsheet"
            ])
            
            with doc_tab1:
                st.subheader("Enhanced CV Recommendations")
                
                # Editable text area for CV
                edited_cv = st.text_area(
                    "Edit your enhanced CV content:",
                    value=st.session_state.edited_content['updated_cv'],
                    height=400,
                    key="cv_editor"
                )
                
                # Update session state with edited content
                st.session_state.edited_content['updated_cv'] = edited_cv
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save CV as TXT", key="save_cv_txt"):
                        filename = f"enhanced_cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        filepath = assistant.save_as_txt(st.session_state.edited_content['updated_cv'], filename)
                        st.session_state.last_saved_files['cv_txt'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                with col2:
                    if st.button("💾 Save CV as PDF", key="save_cv_pdf"):
                        filename = f"enhanced_cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        filepath = assistant.save_as_pdf(st.session_state.edited_content['updated_cv'], filename)
                        st.session_state.last_saved_files['cv_pdf'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                # Show last saved files
                if st.session_state.last_saved_files['cv_txt'] or st.session_state.last_saved_files['cv_pdf']:
                    with st.expander("📁 Last Saved Files"):
                        if st.session_state.last_saved_files['cv_txt']:
                            st.write(f"TXT: `{st.session_state.last_saved_files['cv_txt']}`")
                        if st.session_state.last_saved_files['cv_pdf']:
                            st.write(f"PDF: `{st.session_state.last_saved_files['cv_pdf']}`")
            
            with doc_tab2:
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
                        st.session_state.last_saved_files['letter_txt'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                with col2:
                    if st.button("💾 Save Letter as PDF", key="save_letter_pdf"):
                        filename = f"motivation_letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        filepath = assistant.save_as_pdf(st.session_state.edited_content['motivation_letter'], filename)
                        st.session_state.last_saved_files['letter_pdf'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                # Show last saved files
                if st.session_state.last_saved_files['letter_txt'] or st.session_state.last_saved_files['letter_pdf']:
                    with st.expander("📁 Last Saved Files"):
                        if st.session_state.last_saved_files['letter_txt']:
                            st.write(f"TXT: `{st.session_state.last_saved_files['letter_txt']}`")
                        if st.session_state.last_saved_files['letter_pdf']:
                            st.write(f"PDF: `{st.session_state.last_saved_files['letter_pdf']}`")
            
            with doc_tab3:
                st.subheader("Interview Preparation Guide")
                
                # Editable text area for interview cheatsheet
                edited_cheatsheet = st.text_area(
                    "Edit your interview cheatsheet:",
                    value=st.session_state.edited_content['interview_cheatsheet'],
                    height=400,
                    key="cheatsheet_editor"
                )
                
                # Update session state with edited content
                st.session_state.edited_content['interview_cheatsheet'] = edited_cheatsheet
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Cheatsheet as TXT", key="save_cheatsheet_txt"):
                        filename = f"interview_cheatsheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        filepath = assistant.save_as_txt(st.session_state.edited_content['interview_cheatsheet'], filename)
                        st.session_state.last_saved_files['cheatsheet_txt'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                with col2:
                    if st.button("💾 Save Cheatsheet as PDF", key="save_cheatsheet_pdf"):
                        filename = f"interview_cheatsheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        filepath = assistant.save_as_pdf(st.session_state.edited_content['interview_cheatsheet'], filename)
                        st.session_state.last_saved_files['cheatsheet_pdf'] = filepath
                        st.success(f"Saved as: {filepath}")
                
                # Show last saved files
                if st.session_state.last_saved_files['cheatsheet_txt'] or st.session_state.last_saved_files['cheatsheet_pdf']:
                    with st.expander("📁 Last Saved Files"):
                        if st.session_state.last_saved_files['cheatsheet_txt']:
                            st.write(f"TXT: `{st.session_state.last_saved_files['cheatsheet_txt']}`")
                        if st.session_state.last_saved_files['cheatsheet_pdf']:
                            st.write(f"PDF: `{st.session_state.last_saved_files['cheatsheet_pdf']}`")
            
            # Add a reset button to revert to original generated content
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Reset to Original Generated Content", type="secondary", key="reset_content"):
                    st.session_state.edited_content = {
                        'updated_cv': st.session_state.generated_materials['updated_cv'],
                        'motivation_letter': st.session_state.generated_materials['motivation_letter'],
                        'interview_cheatsheet': st.session_state.generated_materials['interview_cheatsheet']
                    }
                    st.success("Content reset to original generated versions!")
    
    with tab3:
        st.subheader("Configuration & Enhancements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Current Features:**
            - Local file processing
            - Basic text analysis
            - Template-based generation
            - File export (TXT/PDF)
            - Editable content before saving
            """)
        
        with col2:
            st.warning("""
            **Future Enhancements:**
            - AI integration (OpenAI/Ollama)
            - LinkedIn profile parsing
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
                        'cv_txt': None, 'cv_pdf': None,
                        'letter_txt': None, 'letter_pdf': None,
                        'cheatsheet_txt': None, 'cheatsheet_pdf': None
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