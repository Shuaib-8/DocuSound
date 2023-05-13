# Description: Transcribe audio file using whisper model

import ffmpeg
import numpy as np
import whisper


class WhisperModelTranscribe:

    # Hard code variable within class for now
    SAMPLE_RATE = 16000

    def __init__(self, file: str = None, model_type: str = "base"):
        if file.endswith() not in ["m4a", "mp3", "webm", "mp4", "mpga", "wav", "mpeg"]:
            raise ValueError(
                "File format must be either 'm4a'; 'mp3'; 'webm'; 'mp4'; \
                                 'mpga', 'wav', 'mpeg'"
            )
        self.file = file
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

    def transcribe(self, file_path: str = ""):
        model = whisper.models(self.model_type)
        result = model.transcribe(self.load_audio(file_path))
        return result["text"]
