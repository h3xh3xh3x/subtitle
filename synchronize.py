import subprocess
import configparser
from utils import check_file_exists

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get paths from config or fallback to PATH
subsync_path = config['paths'].get('subsync', 'subsync')

def synchronize_subtitles(video_file, srt_file, video_lang, sub_lang):
    if not check_file_exists(subsync_path):
        print(f"Error: subsync executable not found at {subsync_path}")
        return
    resynced_srt_file = srt_file.replace(".srt", "_resync.srt")
    command = [
        subsync_path,
        'sync',
        '--sub', srt_file,
        '--ref', video_file,
        '--out', resynced_srt_file,
        '--sub-lang', video_lang,
        '--ref-lang', sub_lang
    ]
    subprocess.run(command, check=True)
    print(f"Subtitles synchronized and saved as {resynced_srt_file}")
