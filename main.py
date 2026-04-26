import os
from dotenv import load_dotenv
from gen.gentext import run
from video.edit import start
import time
import argparse

parser = argparse.ArgumentParser(description="Setup for the Instagram Video Maker.")
parser.add_argument("--additional_prompt", required=False, type=str, help="Additonal prompt for the LLM.")

args = parser.parse_args()
additional_prompt = args.additional_prompt if args.additional_prompt else "\n"
additional_prompt = str(additional_prompt) ## for safety

def is_dir_empty(path):
    with os.scandir(path) as it:
        return not any(it)

def run_checks(path, NVIDIA_API_KEY):
    if is_dir_empty(path): ## check to make sure your main footage exists.
        raise (Exception(
            "No footage found in video/full! Please a file named \"mc_clips.mp4\" to the \"video/full\" directory and try again."))

    if not os.path.exists(".env"): ## create .env if it doesn't exist.
        with open(".env", "w") as f:
            f.write("NVIDIA_API_KEY = PUTKEYHERE ## Put your NVIDIA API key here. You can get one at https://build.nvidia.com/")

    if NVIDIA_API_KEY == "" or NVIDIA_API_KEY == None or NVIDIA_API_KEY == "PUTKEYHERE": ## check to make sure NVIDIA_API_KEY exists.
        raise (Exception(
            "NVIDIA_API_KEY not found in environment variables. Please set NVIDIA_API_KEY in your .env file and try again."))
# List of required directories
required_dirs = [
    "audio",
    "saved-audio",
    "video",
    os.path.join("video", "clip"),
    os.path.join("video", "done"),
    os.path.join("video", "full"),
]

time_start = time.time()

load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

print("Making directories...")
for d in required_dirs: ## make directories as necessary.
    os.makedirs(d, exist_ok=True)

print("Now checking \"video/full\" for footage, and ensuring your NVIDIA_API_KEY exists...")
run_checks("video/full", NVIDIA_API_KEY)

print("Beginning story generation script...")
run(NVIDIA_API_KEY, additional_prompt) # always pass through NVIDIA_API_KEY, in case it is needed
time_mid = time.time()

print("\nTime to generate text and audio: {:.2f} seconds. Moving to the ffmpeg side.".format(time_mid - time_start))
start(NVIDIA_API_KEY) # always pass through NVIDIA_API_KEY, in case it is needed




time_end = time.time()
print("\nVideo generated.")
print(f"It took {time_end - time_start:.2f} seconds to complete.")