import os
import smtplib
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from docusound.whisper_model_transcribe import WhisperModelTranscribe

root = Path(__file__).resolve().parents[1]
dotenv_path = os.path.join(root, ".env")
load_dotenv(dotenv_path)

st.title("🎤 Audio Transcription App")
st.write("---")


def send_email(subject, message, to, gmail_user, gmail_password):
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to, text)
        server.close()

        return "Email sent!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


def main():

    # Upload audio file.
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "flac", "m4a"])

    model_type = "small"

    if uploaded_file is not None:
        # Create a temporary file and save the uploaded file's content to this temporary file.
        # By default converts to mp4, then this file will be deleted when this context exits.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
            temp.write(uploaded_file.getvalue())
            temp_path = temp.name

        st.audio(temp_path, format="audio/wav")  # Display audio and Change format as needed.

        if st.button("Transcribe"):
            # Transcribe audio file using whisper model and display transcript.
            transcriber = WhisperModelTranscribe(temp_path, model_type)
            st.markdown("**Transcribing...**")
            st.markdown(f"**:blue[{transcriber.transcribe()}]**")

        # Send email with transcript.
        if st.checkbox("Send email with transcript"):

            # Get email address from user.
            email = st.text_input("Enter email address")

            # Get gmail username and password from environment variables.
            gmail_user = os.environ.get("GMAIL")
            gmail_password = os.environ.get("GMAIL_APP_PASS")

            if st.button("Send"):
                # Send email with transcript.
                subject = "Transcript"
                message = WhisperModelTranscribe(temp_path, model_type).transcribe()
                to = email
                st.markdown("**Sending email...**")
                st.markdown(f"**:blue[{send_email(subject, message, to, gmail_user, gmail_password)}]**")

            else:
                st.write("Click the 'Send' button to send email.")


if __name__ == "__main__":
    main()
