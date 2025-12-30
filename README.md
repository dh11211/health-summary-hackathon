# AI Health Summarizer

A hackathon project leveraging Generative AI to translate complex medical transcripts into structured SOAP notes and patient-friendly summaries.

## Context & Problem Statement

Doctor-patient consultations are often dense, technical, and fast-paced. Patients can leave feeling confused about their diagnosis or care plan. Furthermore, doctors spend hours manually typing structured SOAP notes (Subjective, Objective, Assessment, Plan) into EHR systems.

This tool solves both sides of the equation:

*   **For Doctors:** Automates clinical documentation.
*   **For Patients:** Demystifies medical jargon into plain English.

## Architecture

This is a lightweight Flask application acting as an orchestration layer for the OpenAI API.

*   **Backend:** Python (Flask)
*   **AI Engine:** OpenAI GPT-4o (via openai Python SDK)
*   **Rendering:** Mistune (Markdown to HTML)
*   **Frontend:** HTML5, CSS3 (Responsive Flexbox Grid)

## Key Features

*   **SOAP Note Generation:** Automatically categorizes unstructured conversation text into standard clinical headers.
*   **Differential Diagnosis:** AI suggestions for potential diagnoses based only on the provided text, including safety disclaimers.
*   **Markdown Support:** Returns richly formatted text (bullet points, bold headers) for readability.

## Setup & Local Execution

### 1. Clone the repository

```bash
git clone https://github.com/dh11211/health-summary-hackathon.git
cd health-summary-hackathon
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=sk-your_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

Access the UI at `http://127.0.0.1:5000`.

## Author

**Zishan (Shannon) Chen**