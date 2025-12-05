"""File utility functions for finding and filtering audio files."""

import os
from pathlib import Path
from typing import List, Optional, Union


def find_audio_files(
    directory: Union[str, Path],
    timestamp: Optional[float] = None
) -> List[Path]:
    """
    Find all M4A and QTA files in a directory, optionally filtered by creation time.
    
    Args:
        directory: Path to the directory to search
        timestamp: Optional Unix timestamp. If provided, only return files created after this time.
                  If None, return all M4A and QTA files.
        
    Returns:
        List[Path]: List of Path objects for M4A and QTA files found
        
    Raises:
        FileNotFoundError: If the directory doesn't exist
        NotADirectoryError: If the path is not a directory
        PermissionError: If access to the directory is denied by the system
    """
    directory = Path(directory)
    
    # Validate directory exists
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    # Validate it's a directory
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")
    
    # Extensions to search for (case-insensitive)
    audio_extensions = {'.m4a', '.qta'}
    
    found_files = []
    
    # Iterate through all files in directory
    try:
        items = list(directory.iterdir())
    except PermissionError as e:
        # Provide helpful error message for permission issues
        error_msg = (
            f"Permission denied: Cannot access '{directory}'\n\n"
            f"This directory is protected by macOS security policies.\n"
        )
        
        # Check if it's Voice Memos directory
        if "VoiceMemos" in str(directory):
            error_msg += (
                "\nFor Voice Memos access:\n"
                "1. Export voice memos from the Voice Memos app (File > Export)\n"
                "2. Or copy files manually to an accessible location\n"
                "3. Grant Full Disk Access: System Settings > Privacy & Security > Full Disk Access\n"
                "   (Note: This requires adding Python or your terminal app)\n"
            )
        else:
            error_msg += (
                "\nTo resolve:\n"
                "1. Check directory permissions: ls -la <directory>\n"
                "2. Copy files to an accessible location\n"
                "3. Grant necessary permissions in System Settings > Privacy & Security\n"
            )
        
        raise PermissionError(error_msg) from e
    
    for item in items:
        # Skip if not a file
        if not item.is_file():
            continue
        
        # Check if file has one of the target extensions (case-insensitive)
        if item.suffix.lower() in audio_extensions:
            # If timestamp is provided, check creation time
            if timestamp is not None:
                try:
                    # Get file creation time (or modification time as fallback)
                    file_ctime = os.path.getctime(item)
                    
                    # Only include if file was created after the timestamp
                    if file_ctime > timestamp:
                        found_files.append(item)
                except OSError:
                    # Skip files we can't access
                    continue
            else:
                # No timestamp filter, include all matching files
                found_files.append(item)
    
    # Sort by creation time (newest first)
    found_files.sort(key=lambda f: os.path.getctime(f), reverse=True)
    
    return found_files

if __name__ == '__main__':

    voice_memos_dir = "/Users/Oleksii_Shapovalov/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
    files = find_audio_files(voice_memos_dir)
    for f in files:
        print(f"  - {f.name}")