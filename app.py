import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request
import mistune

# --- Configuration & Setup ---
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Verify API Key
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    logger.error("No OPENAI_API_KEY found. Please set it in your .env file.")
    raise ValueError("No OPENAI_API_KEY found")

client = OpenAI(api_key=api_key)

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    diagnosis = ""
    transcript = ""
    
    if request.method == 'POST':
        transcript = request.form.get('transcript', '')
        action = request.form.get('action')

        if transcript:
            if action == 'summarize':
                summary = generate_summary(transcript)
            elif action == 'diagnose':
                diagnosis = generate_diagnosis(transcript)
            
    return render_template('index.html', summary=summary, diagnosis=diagnosis, transcript=transcript)

# --- Business Logic ---
def generate_summary(text):
    """Generates a SOAP note summary using GPT-4o."""
    system_prompt = (
        "You are an expert medical assistant. Your task is to summarize the following "
        "doctor-patient consultation transcript into a structured SOAP note. "
        "Format it clearly under the headings: **Subjective**, **Objective**, **Assessment**, and **Plan**."
    )

    logger.info("Requesting summary from OpenAI...")
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            model="gpt-4o",
        )
        response_text = completion.choices[0].message.content
        # Convert Markdown response to HTML
        return mistune.html(response_text)
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return f"<p class='error'>An error occurred while generating the summary. Please try again.</p>"

def generate_diagnosis(text):
    """Generates differential diagnoses with a disclaimer."""
    system_prompt = (
        "You are an expert medical diagnostic assistant AI. Analyze the transcript and "
        "provide a list of possible differential diagnoses, starting with the most likely one. "
        "For each, provide a brief rationale citing evidence from the text. "
        "\n\nIMPORTANT: End with a clear disclaimer that this is AI-generated and not professional medical advice."
    )

    logger.info("Requesting diagnosis from OpenAI...")
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            model="gpt-4o",
        )
        response_text = completion.choices[0].message.content
        return mistune.html(response_text)
    except Exception as e:
        logger.error(f"Error generating diagnosis: {e}")
        return f"<p class='error'>An error occurred while generating the diagnosis.</p>"

if __name__ == '__main__':
    # Disable debug mode in production context
    app.run(debug=True)