import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure AI Model
if api_key:
    genai.configure(api_key=api_key)
    # Using the most stable model name for your environment
    model = genai.GenerativeModel('models/gemini-2.5-flash')

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def check_sponsorship(jd_text):
    # Phrases that usually indicate no H-1B/CPT/OPT sponsorship
    no_sponsorship_terms = [
        "not provide sponsorship", "no sponsorship", "citizens only",
        "authorized to work in the US without", "will not employ those",
        "temporary visas", "not eligible for hire"
    ]
    found = [term for term in no_sponsorship_terms if term.lower() in jd_text.lower()]
    return found

# --- UI LAYOUT ---
st.set_page_config(page_title="Career Copilot", layout="wide")
st.title("🎯 AI Career Copilot & Interview Prep")

# Inputs defined at the top to prevent NameErrors
with st.sidebar:
    st.header("1. Upload Documents")
    res_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    st.info("Tip: Use your USC Master's resume for best results.")

st.header("2. Job Details")
jd_text = st.text_area("Paste Job Description here:", height=200)

# --- ANALYSIS LOGIC ---
if st.button("Run Full Analysis & Interview Prep"):
    if res_file and jd_text:
        with st.spinner("Analyzing your profile..."):
            resume_text = extract_text(res_file)
            
            # Feature 1: Sponsorship Radar
            sponsorship_warnings = check_sponsorship(jd_text)
            if sponsorship_warnings:
                st.error("⚠️ SPONSORSHIP WARNING: This company may not support F-1/H-1B visas.")
                st.write(f"Detected: *'{sponsorship_warnings[0]}'*")
            
            # Feature 2 & 3: Match Score & Interview Prep
            master_prompt = f"""
            System: You are a Senior Technical Recruiter. Format your response using clean Markdown with bold headers, tables, and bullet points for high scannability.

            User Resume: {resume_text}
            Job Description: {jd_text}

            Provide:
            1. ### **Match Overview**
            - **Match Score**: [Percentage]%
            - **Status**: [Strong Match / Potential / Gap Heavy]
            - **Key Advantage**: (One sentence on why the candidate fits, e.g., USC MSCS background)

            2. ### **Technical Gap Analysis**
            | Category | Missing Skill/Keyword | Priority |
            | :--- | :--- | :--- |
            | Industry | [Skill 1] | High |
            | Framework | [Skill 2] | Med |
            | Concept | [Skill 3] | Med |

            3. ### **Behavioral Interview Prep**
            * **Question 1**: [Question Text]
                - **Suggested Project**: [Project Name from Resume]
                - **Focus**: (e.g., Leadership on your {resume_text} projects)

            * **Question 2**: [Question Text]
                - **Suggested Project**: [Project Name from Resume]
                - **Focus**: (e.g., Solving bugs in {resume_text})

            * **Question 3**: [Question Text]
                - **Suggested Project**: [Project Name from Resume]
                - **Focus**: (e.g., Learning Unity or AI for your {resume_text} projects)
            """
            
            try:
                response = model.generate_content(master_prompt)
                st.divider()
                st.markdown(response.text)
                
                # Download Button for the report
                st.download_button("Download Analysis", response.text, "career_report.txt")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload a resume and paste a job description first.")