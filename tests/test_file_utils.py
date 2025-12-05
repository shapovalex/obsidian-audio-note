"""Unit tests for file utility functions."""

import tempfile
import time
import os
from pathlib import Path
import pytest

from src.file_utils import find_audio_files


class TestFindAudioFiles:
    """Test cases for find_audio_files function."""
    
    def test_find_all_m4a_files(self):
        """Test finding all M4A files without timestamp filter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create test files
            (tmpdir_path / "audio1.m4a").touch()
            (tmpdir_path / "audio2.m4a").touch()
            (tmpdir_path / "audio3.mp3").touch()  # Should not be included
            (tmpdir_path / "document.txt").touch()  # Should not be included
            
            result = find_audio_files(tmpdir_path)
            
            assert len(result) == 2
            assert all(f.suffix == '.m4a' for f in result)
    
    def test_find_all_qta_files(self):
        """Test finding all QTA files without timestamp filter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create test files
            (tmpdir_path / "audio1.qta").touch()
            (tmpdir_path / "audio2.qta").touch()
            (tmpdir_path / "audio3.m4a").touch()
            
            result = find_audio_files(tmpdir_path)
            
            assert len(result) == 3
            qta_files = [f for f in result if f.suffix == '.qta']
            assert len(qta_files) == 2
    
    def test_find_mixed_audio_files(self):
        """Test finding both M4A and QTA files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create test files
            (tmpdir_path / "audio1.m4a").touch()
            (tmpdir_path / "audio2.qta").touch()
            (tmpdir_path / "video.mp4").touch()  # Should not be included
            
            result = find_audio_files(tmpdir_path)
            
            assert len(result) == 2
            extensions = {f.suffix for f in result}
            assert extensions == {'.m4a', '.qta'}
    
    def test_case_insensitive_extensions(self):
        """Test that file extensions are matched case-insensitively."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create files with various case extensions
            (tmpdir_path / "audio1.M4A").touch()
            (tmpdir_path / "audio2.m4a").touch()
            (tmpdir_path / "audio3.QTA").touch()
            (tmpdir_path / "audio4.Qta").touch()
            
            result = find_audio_files(tmpdir_path)
            
            assert len(result) == 4
    
    def test_with_timestamp_filter(self):
        """Test filtering files by creation timestamp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create files with slight delays
            old_file = tmpdir_path / "old.m4a"
            old_file.touch()
            
            # Record timestamp
            time.sleep(0.1)
            cutoff_time = time.time()
            time.sleep(0.1)
            
            # Create new files
            new_file1 = tmpdir_path / "new1.m4a"
            new_file2 = tmpdir_path / "new2.qta"
            new_file1.touch()
            new_file2.touch()
            
            # Find files created after cutoff
            result = find_audio_files(tmpdir_path, timestamp=cutoff_time)
            
            # Should only return the new files
            assert len(result) == 2
            result_names = {f.name for f in result}
            assert result_names == {"new1.m4a", "new2.qta"}
    
    def test_empty_directory(self):
        """Test behavior with empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = find_audio_files(tmpdir)
            assert result == []
    
    def test_directory_not_found(self):
        """Test that FileNotFoundError is raised for non-existent directory."""
        with pytest.raises(FileNotFoundError):
            find_audio_files("/nonexistent/directory")
    
    def test_path_is_not_directory(self):
        """Test that NotADirectoryError is raised when path is a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            file_path.touch()
            
            with pytest.raises(NotADirectoryError):
                find_audio_files(file_path)
    
    def test_string_path_accepted(self):
        """Test that function accepts string paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            (Path(tmpdir) / "audio.m4a").touch()
            
            # Pass string instead of Path
            result = find_audio_files(tmpdir)
            
            assert len(result) == 1
            assert result[0].suffix == '.m4a'
    
    def test_files_sorted_by_time(self):
        """Test that files are sorted by creation time (newest first)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create files with delays to ensure different creation times
            file1 = tmpdir_path / "first.m4a"
            file1.touch()
            time.sleep(0.1)
            
            file2 = tmpdir_path / "second.m4a"
            file2.touch()
            time.sleep(0.1)
            
            file3 = tmpdir_path / "third.m4a"
            file3.touch()
            
            result = find_audio_files(tmpdir_path)
            
            # Should be sorted newest first
            assert len(result) == 3
            assert result[0].name == "third.m4a"
            assert result[2].name == "first.m4a"
    
    def test_no_subdirectories_searched(self):
        """Test that subdirectories are not searched (non-recursive)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create file in main directory
            (tmpdir_path / "audio1.m4a").touch()
            
            # Create subdirectory with files
            subdir = tmpdir_path / "subdir"
            subdir.mkdir()
            (subdir / "audio2.m4a").touch()
            
            result = find_audio_files(tmpdir_path)
            
            # Should only find file in main directory
            assert len(result) == 1
            assert result[0].name == "audio1.m4a"
    
    def test_permission_error_handling(self):
        """Test that PermissionError is raised with helpful message."""
        # This test checks that we handle permission errors properly
        # We can't easily create a directory with no permissions in a temp dir,
        # so we'll test with the actual error case if it exists
        
        # Test with Voice Memos directory (will fail with permission error)
        voice_memos_dir = Path.home() / "Library" / "Group Containers" / "group.com.apple.VoiceMemos.shared" / "Recordings"
        
        if voice_memos_dir.exists():
            with pytest.raises(PermissionError) as exc_info:
                find_audio_files(voice_memos_dir)
            
            # Check that error message contains helpful information
            error_message = str(exc_info.value)
            assert "Permission denied" in error_message
            assert "Voice Memos" in error_message or "protected" in error_message
