from flask import Flask, request, render_template, redirect, url_for, flash
import whisper
import tempfile
import os
from groq import Groq

app = Flask(__name__)
app.secret_key = "super-secret"  # later replace with env var if hosting

# Initialize Whisper model
model = whisper.load_model("small")  # small is good balance speed/accuracy

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "audio_file" not in request.files:
        flash("No file uploaded")
        return redirect(url_for("index"))

    file = request.files["audio_file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    # Save temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # 1️⃣ Whisper transcription
        transcript = model.transcribe(tmp_path)["text"]

        # 2️⃣ Groq summarization
        prompt = f"Summarize this meeting transcript:\n{transcript}\nReturn SUMMARY, DECISIONS, and ACTION ITEMS."
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a meeting summarizer."},
                {"role": "user", "content": prompt}
            ],
        )
        summary_output = response.choices[0].message.content

        return render_template("result.html", transcript=transcript, summary=summary_output, filename=file.filename)

    except Exception as e:
        flash(f"Error processing file: {e}")
        return redirect(url_for("index"))
    finally:
        try:
            os.remove(tmp_path)
        except:
            pass

if __name__ == "__main__":
    app.run(debug=True)
