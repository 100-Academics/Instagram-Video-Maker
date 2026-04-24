import ffmpeg
import random

def get_audio_length(audio_file):
    try:
        probe = ffmpeg.probe(audio_file)
        duration = float(probe["format"]["duration"])
        print(f"Audio length: {duration:.2f} seconds")
        return duration

    except ffmpeg.Error as e:
        print("Failed to read audio duration.")
        print(e.stderr.decode() if hasattr(e, "stderr") and e.stderr else str(e))
        return None

    except Exception as e:
        print(f"Unexpected error while reading audio duration: {e}")
        return None


def get_random_section(input_video, output_video, audio_file):

    audio_length = get_audio_length(audio_file)

    if audio_length is None:
        print("Could not determine audio length. Aborting.")
        return

    try:
        probe = ffmpeg.probe(input_video)
        video_duration = float(probe["format"]["duration"])
        print(f"Video length: {video_duration:.2f} seconds")

        if audio_length >= video_duration:
            print("Audio is longer than (or equal to) the video.")
            print("Using the full video instead.")

            (
                ffmpeg
                .input(input_video)
                .output(output_video, c="copy")
                .run(overwrite_output=True)
            )
            return

        max_start_time = video_duration - audio_length
        start_time = random.uniform(0, max_start_time)

        print(f"Cutting from {start_time:.2f}s to {start_time + audio_length:.2f}s")

        (
            ffmpeg
            .input(input_video, ss=start_time)
            .output(
                output_video,
                t=audio_length,
                vcodec="libx264",
                an=None
            )
            .global_args("-hide_banner", "-loglevel", "error")
            .run(overwrite_output=True)
        )

        print(f"Finished. Saved to: {output_video}. Moving to overlay audio and subtitles...")

    except ffmpeg.Error as e:
        print("FFmpeg error while processing video.")
        print(e.stderr.decode() if hasattr(e, "stderr") and e.stderr else str(e))

    except Exception as e:
        print(f"Unexpected error: {e}")

def overlay_audio_onto_video(video, audio, srt, out):
    try:
        video_in = ffmpeg.input(video)
        audio_in = ffmpeg.input(audio)

        # Dark pill style: centered, white bold text, semi-transparent black background box
        subtitle_filter = (
            f"subtitles={srt}:force_style='"
            "Alignment=2,"          # centered horizontally, bottom-anchored
            "MarginV=60,"           # distance from bottom
            "Fontname=Arial,"
            "Fontsize=18,"
            "Bold=1,"
            "PrimaryColour=&H00FFFFFF,"   # white text
            "BackColour=&HBF000000,"      # semi-transparent black background (75% opacity)
            "BorderStyle=4,"              # opaque box (pill background)
            "Outline=0,"
            "Shadow=0,"
            "MarginL=20,"
            "MarginR=20"
            "'"
        )

        print("Beginning ffmpeg output.")
        (
            ffmpeg
            .output(
                video_in,
                audio_in,
                out,
                vcodec="libx264",
                acodec="aac",
                strict="experimental"
            )
            .global_args("-hide_banner", "-loglevel", "error")
            .run(overwrite_output=True)
        )

        print(f"Finished overlaying audio and subtitles. Saved to: {out}")

    except ffmpeg.Error as e:
        print("FFmpeg error while overlaying audio and subtitles.")
        print(e.stderr.decode() if e.stderr else str(e))

    except Exception as e:
        print(f"Unexpected error while overlaying audio and subtitles: {e}")

def start(NVIDIA_API_KEY):
    get_random_section("video/full/mc_clips.mp4", "video/clip/clip.mp4", "audio/voice.mp3")
    overlay_audio_onto_video("video/clip/clip.mp4", "audio/voice.mp3", "audio/voice.srt", "video/done/final.mp4")