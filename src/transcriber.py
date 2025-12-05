import whisper
from pathlib import Path
from typing import Union

whisper_model = whisper.load_model("large")

def transcribe_mp3(mp3_path: Union[str, Path], model: str = "large") -> str:
    """
    Transcribe an MP3 file to text using OpenAI Whisper.

    Args:
        mp3_path: Path to the MP3 file to transcribe
        model: Whisper model to use. Options: "tiny", "base", "small", "medium", "large"
               Default is "base" which provides a good balance of speed and accuracy.

    Returns:
        str: Transcribed text from the audio file

    Raises:
        FileNotFoundError: If the MP3 file doesn't exist
        Exception: If transcription fails
    """
    mp3_path = Path(mp3_path)

    # Validate input file exists
    if not mp3_path.exists():
        raise FileNotFoundError(f"MP3 file not found: {mp3_path}")

    try:

        # Transcribe the audio file
        result = whisper_model.transcribe(str(mp3_path))

        return result["text"]
    except Exception as e:
        raise Exception(f"Failed to transcribe audio: {e}") from e