# Instagram Brainrot Video Maker
Using the free [NVIDIA BUILD API](https://build.nvidia.com/blueprints) as well as [edge-tts](https://github.com/rany2/edge-tts), this software can create a fake Reddit story, and then create audio for it, and then overlay it onto a clip from a longer video. It can do this almost fully in the cloud by hooking into these APIS. It is designed to get views on Instagram, but it may or may not be good depending on how things go idk I haven't tested it and it's almost midnight as I write this I'll fix this later.

It does what it does by calling the NVIDIA [Qwen3.5-122b-a10b endpoint](https://build.nvidia.com/qwen/qwen3.5-122b-a10b) with the prompt, and then passing the response edge-tts, which uses Microsoft Edge's TTS system to return an audio. **YOU DO NOT NEED WINDOWS OR EDGE FOR THIS TO WORK.** It then uses ffmpeg-python to overlay this onto a random clip from a video that you provide.

**Importantly, it does not post videos on Instagram automatically (yet). That is a fully user thing.**

# SETUP
First, clone the project:

```sh
git clone https://github.com/100-Academics/Instagram-Brainrot-Video-Maker
```

Then, navigate to the folder, and install the necessary requirements:

```sh
cd "Instagram-Video-Maker"
```

```python
pip install -r requirements.txt
```


Hook into the .venv:

```sh
.venv\Scripts\activate
```
on **Windows** (**command line**) or 
```bash
source .venv/bin/activate
``` 
on **Linux**.

Then, run main.py:

```
python main.py
```
if you're on **Windows**, or
```
python3 main.py
```
if you are on **Linux**. **It will generate a ``.env`` file, as well as any directories necessary and then raise an error, on a first run.**

**In your .env file, place your NVIDIA API key (``nvapi-``) at the ``NVIDIA_API_KEY=`` variable.**

Then, run main.py again:

```
python main.py
```
if you're on Windows, or 
```
python3 main.py
```
if you are on Linux.
This time, it will run fully (it may take several minutes), and will save your final clip to ``video/final/videoXXX``

# OTHER STUFF
If you feel the need to change the prompt in some way, navigate to ``gen/prompt.txt`` and edit the file. You can also pass the argument ``--additional_prompt "[ADDITIONAL PROMPT]"`` in order to make the story about something specific, without changing the general prompt.
