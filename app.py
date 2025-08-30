import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request
import mistune

# --- Block 1: Setup ---
load_dotenv()
app = Flask(__name__)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# --- Block 2: The Main Web Page ---
@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    diagnosis = ""
    if request.method == 'POST':
        transcript = request.form.get('transcript', '') # Get transcript, default to empty string
        action = request.form.get('action') # Get which button was clicked

        if transcript:
            if action == 'summarize':
                summary = generate_summary(transcript)
            elif action == 'diagnose':
                diagnosis = generate_diagnosis(transcript)
            
    return render_template('index.html', summary=summary, diagnosis=diagnosis)

# --- Block 3: The AI Logic for Summary ---
def generate_summary(conversation_transcript):
    system_prompt = "You are an expert medical assistant. Your task is to summarize the following doctor-patient consultation transcript into a structured SOAP note. Format it clearly under the headings: Subjective, Objective, Assessment, and Plan."

    print("Asking the AI to generate a summary...")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation_transcript}
            ],
            model="gpt-4o",
        )
        ai_response = chat_completion.choices[0].message.content
        return mistune.html(ai_response)
    except Exception as e:
        return f"An error occurred: {e}"

# --- Block 4: The AI Logic for Diagnosis ---
def generate_diagnosis(conversation_transcript):
    system_prompt = """
    You are an expert medical diagnostic assistant AI. Your task is to analyze the following doctor-patient consultation transcript.
    Based ONLY on the information provided in the transcript, provide a list of possible differential diagnoses, starting with the most likely one.
    For each diagnosis, provide a brief rationale citing evidence from the text.
    IMPORTANT: You must include a disclaimer at the end that this is an AI-generated suggestion for informational purposes only and is not a substitute for a professional medical opinion.
    """

    print("Asking the AI to suggest a diagnosis...")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation_transcript}
            ],
            model="gpt-4o",
        )
        diagnosis_response = chat_completion.choices[0].message.content
        return mistune.html(diagnosis_response)
    except Exception as e:
        return f"An error occurred: {e}"

# --- This makes the web server run when you execute the script ---
if __name__ == '__main__':
    app.run(debug=True)