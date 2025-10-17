#importing all the needed packages
import os
from groq import Groq
from flask import Flask, request, render_template, redirect, url_for, flash
import tempfile

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret")


#api key is protected I have mentioned it in the render website 
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
    
#post method to send the audio to the backend
@app.route("/upload", methods=["POST"])
def upload():
    if "audio_file" not in request.files:
        flash("No file uploaded")
        return redirect(url_for("index"))

    file = request.files["audio_file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Groq transcription with the api key 
        with open(tmp_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo", # using this to convert the audio to text 
                file=(file.filename, audio_file.read()),
                language="en",
                response_format="verbose_json"
            )
            transcript = response.text # storing the text

        # Groq summarization with api key for llm
        prompt = f"Summarize this meeting transcript:\n{transcript}\nReturn SUMMARY, DECISIONS, and ACTION ITEMS."
        # giving proper promt to get in a specific format
        summary_resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a meeting summarizer."},
                {"role": "user", "content": prompt}
            ],
        )
        summary_output = summary_resp.choices[0].message.content
        
        #this is the output to be displayed

        return render_template("result.html", transcript=transcript, summary=summary_output, filename=file.filename)

    finally:
        try:
            os.remove(tmp_path)
        except:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
