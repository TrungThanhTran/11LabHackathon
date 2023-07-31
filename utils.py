import os

def write_audio_file(audio: bytes, file_path: str):
    with open(file_path, "wb") as f:
        f.write(audio)