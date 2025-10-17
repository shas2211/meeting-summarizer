from flask import Flask, request, render_template
from pydub import AudioSegment
from groq import Groq
from gensim.summarization import summarize
import os

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def transcribe_audio(file_path):
    # Send audio file to Groq for transcription
    with open(file_path, "rb") as f:
        response = client.transcribe(file=f)
    return response.text

def summarize_text(text):
    try:
        return summarize(text, word_count=100)
    except:
        return text  # fallback if text too short

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    summary = ""
    if request.method == "POST":
        audio = request.files["audio_file"]
        audio_path = f"temp_{audio.filename}"
        audio.save(audio_path)

        # Convert to WAV if needed
        if not audio.filename.endswith(".wav"):
            sound = AudioSegment.from_file(audio_path)
            audio_path = audio_path.rsplit(".", 1)[0] + ".wav"
            sound.export(audio_path, format="wav")

        transcript = transcribe_audio(audio_path)
        summary = summarize_text(transcript)

    return render_template("index.html", transcript=transcript, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
