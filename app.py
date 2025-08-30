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
    if request.method == 'POST':
        # Get the transcript from the website's text box
        transcript = request.form['transcript']
        
        # If the user submitted something, ask the AI
        if transcript:
            summary = generate_summary(transcript)
            
    # Show the main webpage and pass the summary to it
    return render_template('index.html', summary=summary)

# --- Block 3: The AI Logic (Moved into a function) ---
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
        # If there is an error, show it
        return f"An error occurred: {e}"

# --- This makes the web server run when you execute the script ---
if __name__ == '__main__':
    app.run(debug=True)