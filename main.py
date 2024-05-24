import os
from extract_audio import extract_audio
from transcribe import transcribe_audio_whisper, generate_srt_whisper, correct_zero_timecodes
from synchronize import synchronize_subtitles

def main_process(video_file, run_subsync, keep_intermediate, video_lang, sub_lang, output_path):
    audio_file = "extracted_audio.wav"
    srt_file = os.path.join(output_path, os.path.splitext(os.path.basename(video_file))[0] + "_whisper.srt")

    # Extract audio from video
    if not extract_audio(video_file, audio_file):
        return

    # Transcribe audio
    segments = transcribe_audio_whisper(audio_file)

    # Generate SRT file from transcription
    generate_srt_whisper(segments, srt_file)

    # Correct zero timecodes in SRT file
    correct_zero_timecodes(srt_file)

    # Synchronize subtitles with the video
    if run_subsync:
        synchronize_subtitles(video_file, srt_file, video_lang, sub_lang)

    # Clean up extracted audio file
    if not keep_intermediate:
        os.remove(audio_file)
        print(f"Temporary audio file {audio_file} removed")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Extract audio, transcribe, and synchronize subtitles for a video file.')
    parser.add_argument('video_file', type=str, nargs='?', help='Path to the video file')
    parser.add_argument('--sync', action='store_true', help='Run subsync after processing to further synchronize subtitles')
    parser.add_argument('--keep-intermediate', action='store_true', help='Keep intermediate files')
    parser.add_argument('--cli', action='store_true', help='Run in command-line mode')
    parser.add_argument('--video-lang', type=str, default='eng', help='Language of the video')
    parser.add_argument('--sub-lang', type=str, default='eng', help='Language of the subtitles')
    parser.add_argument('--output-path', type=str, default='.', help='Output path for the subtitles')

    args = parser.parse_args()

    if args.cli:
        if not args.video_file:
            print("Error: video_file argument is required in CLI mode.")
            exit(1)
        main_process(args.video_file, args.sync, args.keep_intermediate, args.video_lang, args.sub_lang, args.output_path)
    else:
        from gui import run_gui
        run_gui()
