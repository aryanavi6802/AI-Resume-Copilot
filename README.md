# AI Resume Copilot

AI Resume Copilot is a Streamlit app that helps analyze a resume against a job description and generate interview prep guidance.

## Features

- Upload a resume in PDF format
- Paste a job description
- Detect common sponsorship-related warning phrases
- Generate a match overview and gap analysis
- Create behavioral interview prep prompts
- Download the generated analysis as a text file

## Tech Stack

- Python
- Streamlit
- PyPDF2
- Google Generative AI
- python-dotenv

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
```

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Add your Google API key.
5. Run the Streamlit app.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

You can also copy from `.env.example`.

## Run Locally

```bash
streamlit run app.py
```

After startup, open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## How It Works

1. The app reads the uploaded PDF resume.
2. It checks the job description for common sponsorship restriction phrases.
3. It sends the resume and job description to the Gemini model.
4. It returns a formatted analysis with match insights and interview prep.

## Notes

- Keep `.env` private and do not commit real API keys.
- The current app uses `google.generativeai`, which shows a deprecation warning in newer environments.

## Future Improvements

- Support DOCX resumes
- Add resume keyword suggestions
- Improve sponsorship detection coverage
- Export reports as PDF
- Migrate to the newer Google Gen AI SDK
