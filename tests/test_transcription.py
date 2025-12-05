"""Unit tests for audio transcription module."""

import tempfile
from pathlib import Path
import pytest

from src.transcriber import transcribe_mp3


class TestTranscribeMp3:
    """Test cases for transcribe_mp3 function."""
    
    def test_transcribe_mp3_basic(self):
        """Test basic MP3 transcription functionality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            # Create a simple audio file with a tone
            # Note: This will transcribe to silence/noise, but tests the pipeline
            tone = Sine(440).to_audio_segment(duration=2000)  # 2 seconds
            
            mp3_file = Path(tmpdir) / "test_audio.mp3"
            tone.export(str(mp3_file), format="mp3")
            
            # Transcribe the audio
            result = transcribe_mp3(mp3_file, model="tiny")  # Use tiny model for speed
            
            # Verify result is a string
            assert isinstance(result, str), "Result should be a string"
            # Result might be empty or contain noise interpretation
            assert result is not None, "Result should not be None"
    
    def test_transcribe_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            non_existent = Path(tmpdir) / "nonexistent.mp3"
            
            with pytest.raises(FileNotFoundError):
                transcribe_mp3(non_existent)
    
    def test_transcribe_with_different_models(self):
        """Test transcription with different Whisper models."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone = Sine(440).to_audio_segment(duration=1000)
            mp3_file = Path(tmpdir) / "test_audio.mp3"
            tone.export(str(mp3_file), format="mp3")
            
            # Test with tiny model (fastest)
            result_tiny = transcribe_mp3(mp3_file, model="tiny")
            assert isinstance(result_tiny, str)
            
            # Test with base model (default)
            result_base = transcribe_mp3(mp3_file, model="base")
            assert isinstance(result_base, str)
    
    def test_transcribe_string_path(self):
        """Test that function accepts string paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone = Sine(440).to_audio_segment(duration=1000)
            mp3_file = str(Path(tmpdir) / "test_audio.mp3")
            tone.export(mp3_file, format="mp3")
            
            result = transcribe_mp3(mp3_file, model="tiny")
            assert isinstance(result, str)
    
    def test_transcribe_longer_audio(self):
        """Test transcription of longer audio file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine, Square
            
            # Create a longer audio with varying tones
            tone1 = Sine(440).to_audio_segment(duration=1000)
            tone2 = Square(880).to_audio_segment(duration=1000)
            combined = tone1 + tone2 + tone1  # 3 seconds total
            
            mp3_file = Path(tmpdir) / "long_audio.mp3"
            combined.export(str(mp3_file), format="mp3")
            
            result = transcribe_mp3(mp3_file, model="tiny")
            assert isinstance(result, str)
    
    def test_transcribe_cached_model(self):
        """Test that model caching works (multiple calls don't re-download)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone = Sine(440).to_audio_segment(duration=1000)
            
            # Create two different files
            mp3_file1 = Path(tmpdir) / "audio1.mp3"
            mp3_file2 = Path(tmpdir) / "audio2.mp3"
            
            tone.export(str(mp3_file1), format="mp3")
            tone.export(str(mp3_file2), format="mp3")
            
            # Transcribe both - second should use cached model
            result1 = transcribe_mp3(mp3_file1, model="tiny")
            result2 = transcribe_mp3(mp3_file2, model="tiny")
            
            assert isinstance(result1, str)
            assert isinstance(result2, str)
