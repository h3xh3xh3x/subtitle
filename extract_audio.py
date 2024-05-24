import subprocess
import os
import configparser
from utils import gui_prompt_overwrite

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get paths from config or fallback to PATH
ffmpeg_path = config['paths'].get('ffmpeg', 'ffmpeg')

def extract_audio(video_file, output_audio_file):
    if os.path.exists(output_audio_file):
        if not gui_prompt_overwrite(f"{output_audio_file} already exists. Overwrite?"):
            return False
    command = [
        ffmpeg_path,
        '-i', video_file,
        '-q:a', '0',
        '-map', 'a',
        output_audio_file
    ]
    subprocess.run(command, check=True)
    print(f"Audio extracted and saved as {output_audio_file}")
    return True
