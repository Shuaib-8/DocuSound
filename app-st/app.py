import tempfile

import streamlit as st

from docusound.whisper_model_transcribe import WhisperModelTranscribe

st.title("🎤 Audio Transcription App")
st.write("---")


def main():

    # Upload audio file.
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "flac", "m4a"])

    if uploaded_file is not None:
        # Create a temporary file and save the uploaded file's content to this temporary file.
        # By default converts to mp4, then this file will be deleted when this context exits.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
            temp.write(uploaded_file.getvalue())
            temp_path = temp.name

        st.audio(temp_path, format="audio/wav")  # Display audio and Change format as needed.

        if st.button("Transcribe"):
            # Transcribe audio file using whisper model and display transcript.
            model_type = "small"
            transcriber = WhisperModelTranscribe(temp_path, model_type)
            st.markdown("**Transcribing...**")
            st.markdown(f"**:blue[{transcriber.transcribe(temp_path)}]**")


if __name__ == "__main__":
    main()
