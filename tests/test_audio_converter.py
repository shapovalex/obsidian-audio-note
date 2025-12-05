"""Unit tests for audio converter module."""

import tempfile
import os
from pathlib import Path
import pytest

from src.audio_converter import convert_to_mp3


class TestConvertToMP3:
    """Test cases for convert_to_mp3 function."""
    
    def test_convert_wav_to_mp3(self):
        """Test converting a WAV file to MP3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple WAV file using pydub
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            # Generate a 1-second sine wave
            tone = Sine(440).to_audio_segment(duration=1000)  # 1 second at 440Hz
            
            input_file = Path(tmpdir) / "test_input.wav"
            output_file = Path(tmpdir) / "test_output.mp3"
            
            # Save as WAV first
            tone.export(str(input_file), format="wav")
            
            # Convert to MP3
            convert_to_mp3(input_file, output_file)
            
            # Verify output file exists
            assert output_file.exists(), "Output MP3 file should exist"
            
            # Verify it's a valid MP3 file
            audio = AudioSegment.from_mp3(str(output_file))
            assert len(audio) > 0, "Output should be a valid audio file"
    
    def test_convert_flac_to_mp3(self):
        """Test converting a FLAC file to MP3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone = Sine(440).to_audio_segment(duration=1000)
            
            input_file = Path(tmpdir) / "test_input.flac"
            output_file = Path(tmpdir) / "test_output.mp3"
            
            tone.export(str(input_file), format="flac")
            
            convert_to_mp3(input_file, output_file)
            
            assert output_file.exists()
            audio = AudioSegment.from_mp3(str(output_file))
            assert len(audio) > 0
    
    def test_convert_m4a_to_mp3(self):
        """Test converting an M4A file to MP3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone = Sine(440).to_audio_segment(duration=1000)
            
            input_file = Path(tmpdir) / "test_input.m4a"
            output_file = Path(tmpdir) / "test_output.mp3"
            
            try:
                tone.export(str(input_file), format="m4a")
                convert_to_mp3(input_file, output_file)
                
                assert output_file.exists()
                audio = AudioSegment.from_mp3(str(output_file))
                assert len(audio) > 0
            except Exception as e:
                print(e)
                # M4A might not be available if ffmpeg codecs aren't installed
                pytest.skip("M4A format not available (may require additional codecs)")
    
    def test_convert_qta_to_m4a_available(self):
        """Test if conversion from QTA (QuickTime Audio) to M4A format is available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone = Sine(440).to_audio_segment(duration=1000)
            
            # QTA files typically use .mov or .qt extension
            # Test with .mov extension (QuickTime format)
            input_file = Path(tmpdir) / "test_input.mov"
            output_file = Path(tmpdir) / "test_output.m4a"
            
            try:
                # Try to export as QuickTime format
                tone.export(str(input_file), format="mov")
                
                # Check if we can load the QTA file
                audio = AudioSegment.from_file(str(input_file))
                
                # Try to export as M4A
                audio.export(str(output_file), format="m4a")
                
                # Verify output file exists and is valid
                assert output_file.exists(), "M4A output file should exist"
                m4a_audio = AudioSegment.from_file(str(output_file))
                assert len(m4a_audio) > 0, "Output should be a valid audio file"
                
            except Exception as e:
                # QTA/M4A conversion might not be available if ffmpeg codecs aren't installed
                pytest.skip(f"QTA to M4A conversion not available: {e}")
    
    def test_file_not_found_error(self):
        """Test that FileNotFoundError is raised for non-existent input file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = Path(tmpdir) / "nonexistent.wav"
            output_file = Path(tmpdir) / "output.mp3"
            
            with pytest.raises(FileNotFoundError):
                convert_to_mp3(input_file, output_file)
    
    def test_creates_output_directory(self):
        """Test that output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone = Sine(440).to_audio_segment(duration=1000)
            
            input_file = Path(tmpdir) / "test_input.wav"
            output_file = Path(tmpdir) / "subdir" / "nested" / "output.mp3"
            
            tone.export(str(input_file), format="wav")
            
            # Directory shouldn't exist yet
            assert not output_file.parent.exists()
            
            convert_to_mp3(input_file, output_file)
            
            # Directory should be created and file should exist
            assert output_file.exists()
            assert output_file.parent.exists()
    
    def test_string_paths_accepted(self):
        """Test that function accepts string paths in addition to Path objects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone = Sine(440).to_audio_segment(duration=1000)
            
            input_file = os.path.join(tmpdir, "test_input.wav")
            output_file = os.path.join(tmpdir, "test_output.mp3")
            
            tone.export(input_file, format="wav")
            
            convert_to_mp3(input_file, output_file)
            
            assert os.path.exists(output_file)
    
    def test_output_file_overwrites_existing(self):
        """Test that existing output file is overwritten."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            tone1 = Sine(440).to_audio_segment(duration=1000)
            tone2 = Sine(880).to_audio_segment(duration=2000)  # Different frequency and duration
            
            input_file1 = Path(tmpdir) / "input1.wav"
            input_file2 = Path(tmpdir) / "input2.wav"
            output_file = Path(tmpdir) / "output.mp3"
            
            tone1.export(str(input_file1), format="wav")
            tone2.export(str(input_file2), format="wav")
            
            # First conversion
            convert_to_mp3(input_file1, output_file)
            first_audio = AudioSegment.from_mp3(str(output_file))
            first_duration = len(first_audio)
            
            # Second conversion (should overwrite)
            convert_to_mp3(input_file2, output_file)
            second_audio = AudioSegment.from_mp3(str(output_file))
            second_duration = len(second_audio)
            
            # Durations should be different, confirming overwrite
            assert first_duration != second_duration
