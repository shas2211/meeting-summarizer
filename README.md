# meeting-summarizer

<img width="360" height="343" alt="image" src="https://github.com/user-attachments/assets/a02ebed7-a9ce-4d51-bcb8-083a23d6e3e9" />



A web application that transcribes meeting audio and generates action-oriented summaries using **Groq ASR** and **Groq LLM**.

---

## Features

- Upload audio files (.wav / .mp3)
- Fast transcription using Groq Whisper API
- Summarization into:
  - **Summary**
  - **Decisions**
  - **Action Items**
- User-friendly web interface built with Flask
- Secure environment variables for API keys

---

## Demo

Upload an audio file on the homepage, and get:

- Full transcript
- Structured summary including decisions and action items

---

## Tech Stack

- Python 3.11+
- Flask
- Groq API (Whisper + LLM)
- HTML/CSS (frontend)
- Gunicorn (production server)

---

## Installation (Local)

1. Clone the repo:

```bash
git clone https://github.com/<your-username>/meeting-summarizer.git
cd meeting-summarizer
