# Description: Transcribe audio file using whisper model

import os
import warnings

import ffmpeg
import numpy as np
import whisper

warnings.filterwarnings("ignore")


class WhisperModelTranscribe:

    # Hard code sample rate for now
    SAMPLE_RATE = 16000

    # Hard code accepted file formats for now
    ACCEPTED_FILE_FORMATS = [".m4a", ".mp3", ".webm", ".mp4", ".mpga", ".wav", ".mpeg"]

    def __init__(self, file_path: str = None, model_type: str = "base"):
        if os.path.splitext(file_path)[1] not in self.ACCEPTED_FILE_FORMATS:
            raise ValueError(
                "File format must be either 'm4a'; 'mp3'; 'webm'; 'mp4'; \
                              'mpga'; 'wav'; 'mpeg'"
            )
        self.file_path = file_path
        if model_type not in ["tiny", "base", "small", "medium", "large"]:
            raise ValueError(
                "Model type must be either 'tiny'; \
                                 'base'; 'small'; 'medium'; 'large'"
            )
        self.model_type = model_type

    @staticmethod
    def load_audio(file_path: str, sr: int = SAMPLE_RATE):
        """
        Use file's bytes and transform to mono waveform, resampling as necessary
        Parameters.

        Taken from https://github.com/openai/whisper/discussions/908.
        ----------
        file: bytes
            The bytes of the audio file
        sr: int
            The sample rate to resample the audio if necessary
        Returns
        -------
        A NumPy array containing the audio waveform, in float32 dtype.
        """
        try:
            # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
            # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
            out, _ = (
                ffmpeg.input("pipe:", threads=0)
                .output("pipe:", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
                .run_async(pipe_stdin=True, pipe_stdout=True)
            ).communicate(input=file_path)

        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

    def transcribe(self):
        model = whisper.load_model(self.model_type)
        result = model.transcribe(self.file_path, fp16=False, language="en")
        return result["text"]


if __name__ == "__main__":
    from pathlib import Path

    # get location of file path on desktop
    file_path = str(Path.home() / "Desktop" / "audio-test.wav")

    model_type = "small"
    transcriber = WhisperModelTranscribe(file_path, model_type)
    print(transcriber.transcribe())
