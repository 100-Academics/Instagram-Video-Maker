import ffmpeg
import random

def getAudioLength(file):
    try:
        probe = ffmpeg.probe(file)
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"An error occurred while probing the audio file: {e}")
        return None

def get_random_section(input_file, output_file):
    audio_length = getAudioLength(input_file)
    if audio_length is None:
        print("Could not determine audio length. Skipping random section extraction.")
        return
    
    probe = ffmpeg.probe(input_file)
    duration = float(probe['format']['duration'])
    max_start_time = max(0, duration - audio_length)
    start_time = random.uniform(0, max_start_time)

    (
        ffmpeg
        .input(input_file, ss=start_time)
        .output(output_file, t=audio_length, c='copy')
        .run(overwrite_output=True)
    )
    
