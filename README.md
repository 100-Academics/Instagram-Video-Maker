# Instagram Brainrot Video Maker
Using the free [NVIDIA BUILD API](https://build.nvidia.com/blueprints) as well as [edge-tts](https://github.com/rany2/edge-tts), this software can create a fake Reddit story, and then create audio for it, and then overlay it onto a clip from a longer video. It can do this almost fully in the cloud by hooking into these APIS. It is designed to get views on Instagram, but it may or may not be good depending on how things go idk I haven't tested it and it's almost midnight as I write this I'll fix this later.
Importantly, it does not post videos on Instagram automatically (yet). That is a fully user thing.

# SETUP
First, clone the project:
``git clone https://github.com/100-Academics/Instagram-Brainrot-Video-Maker``

Then, navigate to the folder, and install the necessary requirements:
``cd "Instagram-Video-Maker"``
``pip install -r requirements.txt``

Hook into the .venv:
``.venv\Scripts\activate`` on Windows (command line) or ``source .venv/bin/activate`` on Linux.

Then, run main.py:
``python main.py`` if you're on Windows, or ``python3 main.py`` if you are on Linux. It will generate a ``.env`` file, as well as any directories necessary, and then raise an error.
In your .env file, place your NVIDIA API key (``nvapi-``) at the ``NVIDIA_API_KEY=`` variable.

Then, run main.py again:
``python main.py`` if you're on Windows, or ``python3 main.py`` if you are on Linux.
This time, it will run fully (it may take several minutes), and will save your final clip to ``video/final/videoXXX``

# OTHER STUFF
If you feel the need to change the prompt in some way, navigate to ``gen/prompt.txt`` and edit the file. You can also pass the argument ``--additional_prompt "[ADDITIONAL PROMPT]"`` in order to make the story about something specific, without changing the general prompt.
