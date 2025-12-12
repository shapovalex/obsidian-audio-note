#!/usr/bin/env python3
"""Process voice memos: convert to MP3 and transcribe."""
import time
from src.file_utils import find_audio_files, read_timestamp, write_timestamp, write_string_to_file
from src.audio_converter import convert_to_mp3
from src.transcriber import transcribe_mp3
import os

def generate_timestamp():
    return str(int(time.time()))

def main():
    home_directory_env = os.getenv("HOME")
    """Main processing function."""
    # Use accessible directory for voice memos
    voice_memos_dir = f"{home_directory_env}/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
    output_dir = f"{home_directory_env}/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal/01_Audio inbox"

    timestamp = read_timestamp("last_timestamp.txt")
    audio_files = find_audio_files(voice_memos_dir, timestamp)

    for audio_file in audio_files:
        print(f"Processing {audio_file.name}")
        convert_to_mp3(audio_file, "temp.mp3")
        transcription = transcribe_mp3("temp.mp3")
        write_string_to_file(output_dir, generate_timestamp() + ".md", transcription)

    write_timestamp("last_timestamp.txt")


if __name__ == "__main__":
    main()
