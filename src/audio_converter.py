"""Audio file conversion module using pydub."""

from pathlib import Path
from typing import Union

from pydub import AudioSegment



def convert_to_mp3(input_path: Union[str, Path], output_path: Union[str, Path]) -> None:
    """
    Convert any audio file to MP3 format.
    
    Args:
        input_path: Path to the input audio file (supports various formats like wav, flac, m4a, etc.)
        output_path: Path where the output MP3 file will be saved
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the output path is invalid
        Exception: If conversion fails (e.g., unsupported format, codec issues)
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    # Validate input file exists
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Validate output directory exists or can be created
    output_dir = output_path.parent
    if output_dir and not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ValueError(f"Cannot create output directory: {output_dir}") from e
    
    # Load audio file (pydub auto-detects format from extension)
    try:
        audio = AudioSegment.from_file(str(input_path))
    except Exception as e:
        raise Exception(f"Failed to load audio file: {e}") from e
    
    # Export as MP3
    try:
        audio.export(str(output_path), format="mp3")
    except Exception as e:
        raise Exception(f"Failed to export as MP3: {e}") from e





if __name__ == '__main__':
    convert_to_mp3("1.m4a", "1.mp3")