import os
from dotenv import load_dotenv
from gen.gentext import run
from video.edit import start
import time

time_start = time.time()

load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

run(NVIDIA_API_KEY) # always pass through NVIDIA_API_KEY, in case it is needed
time_mid = time.time()
print("Time to generate text and audio: {:.2f} seconds. Moving to the ffmpeg side".format(time_mid - time_start))
start(NVIDIA_API_KEY) # always pass through NVIDIA_API_KEY, in case it is needed




time_end = time.time()
print("Video generated.")
print(f"It took {time_end - time_start:.2f} seconds to complete.")
