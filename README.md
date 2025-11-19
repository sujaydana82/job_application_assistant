# 🧠 AI Job Application Assistant

A comprehensive local application that helps you tailor your job application materials — including CV enhancement, motivation letters, and interview preparation guides — based on job descriptions.


## 📁 Project Structure
```
job_application_assistant/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── utils/
│   ├── __init__.py                # Package initialization
│   ├── ai_helpers.py              # Core AI assistance logic
│   └── file_processor.py          # File processing utilities
└── generated_files/               # Output directory for saved files
```

### ✨ Features

- 📝 **CV Enhancement**: Analyze your current CV and job description to generate specific modification recommendations  
- 💌 **Motivation Letter Generation**: Create tailored motivation letters for specific job applications  
- 🎯 **Interview Preparation**: Generate comprehensive interview cheatsheets with questions and answers  
- 📁 **Multiple Format Support**: Upload PDF, DOCX, and TXT files  
- 💾 **Export Options**: Save generated content as both TXT and PDF files  
- ✏️ **Editable Content**: Modify generated content before saving  
- 🔒 **Local Processing**: All processing happens locally on your machine  

---

## 🧰 Technology Stack

| Layer         | Tools Used                          |
|--------------|-------------------------------------|
| **Frontend**  | Streamlit                           |
| **Backend**   | Python 3.11                         |
| **File I/O**  | PyPDF2, python-docx                 |
| **PDF Output**| FPDF2                               |
| **Text Logic**| Regular expressions, pattern matching |


---

## ⚙️ Installation & Setup

### 🔧 Prerequisites
- Python 3.11 or higher  
- pip (Python package manager)

### 📦 Step-by-Step Installation

#### 1. Clone or create the project directory
```bash
mkdir job_application_assistant
cd job_application_assistant
```

#### 2. Create a virtual environment
Windows
```bash
python -m venv job_venv
source job_venv\Scripts\activate
```
macOS/Linux
```bash
python -m venv job_venv
source job_venv/bin/activate
```

#### 3. Install dependencies
```Bash
pip install -r requirements.txt
```

#### 4. Run the Streamlit application
```bash
streamlit run app.py
```
#### 5. Application will launch on browser http://localhost:8501
#### 6. Update your documents(CV,JD), give linkedin profile URL  OR paste job decription and click on Generate Application Materials
