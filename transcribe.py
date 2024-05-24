import whisper
from datetime import timedelta

def transcribe_audio_whisper(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["segments"]

def generate_srt_whisper(segments, srt_file):
    with open(srt_file, 'w', encoding='utf-8') as f:
        previous_end = 0
        for idx, segment in enumerate(segments):
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text']

            # Handle zero time codes
            if start_time == 0 or end_time == 0:
                if idx > 0 and idx < len(segments) - 1:
                    next_start = segments[idx + 1]['start']
                    if start_time == 0:
                        start_time = (previous_end + next_start) / 2
                    if end_time == 0:
                        end_time = (start_time + next_start) / 2
            
            # Offset the first subtitle to start at 0:00:00,001
            if idx == 0 and start_time == 0:
                start_time = 0.001
            
            # Write to SRT file
            f.write(f"{idx + 1}\n")
            f.write(f"{str(timedelta(seconds=start_time))[:-3].replace('.', ',')} --> {str(timedelta(seconds=end_time))[:-3}.replace('.', ',')}\n")
            f.write(f"{text.strip()}\n\n")
            
            previous_end = end_time

    print(f"SRT file saved as {srt_file}")

def correct_zero_timecodes(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    corrected_lines = []
    for i, line in enumerate(lines):
        if '--> 0:00' in line or '0:00 -->' in line:
            prev_end = None
            next_start = None

            if i > 2 and '-->' in lines[i-2]:
                prev_end = lines[i-2].split(' --> ')[1].strip()
            if i < len(lines) - 4 and '-->' in lines[i+2]:
                next_start = lines[i+2].split(' --> ')[0].strip()

            if prev_end and next_start:
                prev_end_td = timedelta(hours=int(prev_end.split(':')[0]), minutes=int(prev_end.split(':')[1]), seconds=float(prev_end.split(':')[2].replace(',', '.')))
                next_start_td = timedelta(hours=int(next_start.split(':')[0]), minutes=int(next_start.split(':')[1]), seconds=float(next_start.split(':')[2].replace(',', '.')))
                mid_point_td = prev_end_td + (next_start_td - prev_end_td) / 2

                if '0:00 -->' in line:
                    new_start = str(mid_point_td)[:-3].replace('.', ',')
                    corrected_lines.append(new_start + ' --> ' + lines[i].split(' --> ')[1])
                elif '--> 0:00' in line:
                    new_end = str(mid_point_td)[:-3].replace('.', ',')
                    corrected_lines.append(lines[i].split(' --> ')[0] + ' --> ' + new_end)
            else:
                corrected_lines.append(line)
        else:
            corrected_lines.append(line)

    with open(srt_file, 'w', encoding='utf-8') as f:
        f.writelines(corrected_lines)
    print(f"Zero timecodes corrected in {srt_file}")
