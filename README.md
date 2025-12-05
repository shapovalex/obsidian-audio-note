# Audio Converter & Transcription

A Python project for audio file conversion and transcription using pydub and OpenAI Whisper.

## Features

- **Audio Conversion**: Convert any audio file format to MP3 using pydub
- **Audio Transcription**: Transcribe MP3 files to text using OpenAI Whisper

## Installation

This project uses `uv` for dependency management. Install dependencies with:

```bash
uv sync
```

## Requirements

- Python 3.12
- FFmpeg (required by pydub for audio processing)

## Usage

### Convert Audio to MP3

```python
from src.audio_converter import convert_to_mp3

# Convert any audio file to MP3
convert_to_mp3("input.wav", "output.mp3")
convert_to_mp3("input.flac", "output.mp3")
convert_to_mp3("input.m4a", "output.mp3")
```

### Transcribe MP3 to Text

```python
from src.audio_converter import transcribe_mp3

# Transcribe using default "base" model
text = transcribe_mp3("audio.mp3")
print(text)

# Use a different Whisper model for better accuracy
text = transcribe_mp3("audio.mp3", model="small")

# Use "tiny" model for faster processing
text = transcribe_mp3("audio.mp3", model="tiny")
```

### Whisper Model Options

- **tiny**: Fastest, least accurate (~39M parameters)
- **base**: Good balance of speed and accuracy (~74M parameters, default)
- **small**: Better accuracy, slower (~244M parameters)
- **medium**: High accuracy, slow (~769M parameters)
- **large**: Best accuracy, slowest (~1550M parameters)

### Combined Example

```python
from src.audio_converter import convert_to_mp3, transcribe_mp3

# Convert audio file to MP3
convert_to_mp3("recording.wav", "recording.mp3")

# Transcribe the MP3
transcription = transcribe_mp3("recording.mp3", model="base")
print(f"Transcription: {transcription}")
```

## Running Tests

Run all tests:

```bash
uv run pytest tests/ -v
```

Run specific test file:

```bash
uv run pytest tests/test_audio_converter.py -v
uv run pytest tests/test_transcription.py -v
```

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   └── audio_converter.py      # Main module with conversion and transcription functions
├── tests/
│   ├── __init__.py
│   ├── test_audio_converter.py # Tests for audio conversion
│   └── test_transcription.py   # Tests for audio transcription
├── pyproject.toml              # Project dependencies and configuration
└── README.md                   # This file
```

## Functions

### `convert_to_mp3(input_path, output_path)`

Convert any audio file to MP3 format.

**Parameters:**
- `input_path` (str | Path): Path to input audio file
- `output_path` (str | Path): Path where MP3 will be saved

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `ValueError`: If output directory cannot be created
- `Exception`: If conversion fails

### `transcribe_mp3(mp3_path, model="base")`

Transcribe an MP3 file to text using OpenAI Whisper.

**Parameters:**
- `mp3_path` (str | Path): Path to MP3 file
- `model` (str): Whisper model to use ("tiny", "base", "small", "medium", "large")

**Returns:**
- `str`: Transcribed text from the audio

**Raises:**
- `FileNotFoundError`: If MP3 file doesn't exist
- `Exception`: If transcription fails

## Test Results

- **Audio Conversion Tests**: 6 passed, 2 skipped
- **Transcription Tests**: 6 passed
- **Total**: 12 passed, 2 skipped

Skipped tests require additional FFmpeg codecs for M4A and QuickTime formats.
