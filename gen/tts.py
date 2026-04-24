import asyncio
import sys
import edge_tts
from edge_tts import VoicesManager
import random

OUTPUT_FILE = "audio/voice.mp3"
SRT_FILE = "audio/voice.srt"
TEXT = ""
POSSIBLE_VOICES = ["en-AU-WilliamMultilingualNeural", "en-AU-NatashaNeural", "en-CA-ClaraNeural", "en-CA-LiamNeural", "en-GB-LibbyNeural", "en-GB-MaisieNeural", "en-GB-RyanNeural", "en-GB-SoniaNeural", "en-GB-ThomasNeural", "en-US-AvaNeural", "en-US-AndrewNeural", "en-US-EmmaNeural", "en-US-BrianNeural", "en-US-AnaNeural", "en-US-AndrewMultilingualNeural", "en-US-AriaNeural", "en-US-AvaMultilingualNeural", "en-US-BrianMultilingualNeural", "en-US-ChristopherNeural", "en-US-EmmaMultilingualNeural", "en-US-EricNeural", "en-US-GuyNeural", "en-US-JennyNeural", "en-US-MichelleNeural", "en-US-RogerNeural", "en-US-SteffanNeural"]

def begin(NVIDIA_API_KEY,): ## pass down API key in case we need it later.
    print("Beginning TTS generation...")
    with open ("response.txt", "r") as f:
        TEXT = f.read()
    asyncio.run(amain(str(TEXT)))

async def amain(TEXT) -> None:
    # drawn from 
    # https://github.com/rany2/edge-tts/blob/master/examples/sync_audio_streaming_with_predefined_voice_subtitles_print2stdout.py
    # https://github.com/rany2/edge-tts/blob/master/examples/async_audio_gen_with_dynamic_voice_selection.p
    print("Finding right voice...")
    voices = await VoicesManager.create()
    voice_for_tts = "en-US-AndrewNeural"
    print("Voice found. I am " + voice_for_tts + " for this run. Beginning generation...")

    communicate = edge_tts.Communicate(TEXT, "en-US-AndrewNeural", rate="+100%")
    submaker = edge_tts.SubMaker()
    stdout = sys.stdout
    audio_bytes = []
    
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    print("Done generating audio and subtitles. Saving subtitles to file...")
    with open(SRT_FILE, "w", encoding="utf-8") as file:
        file.write(submaker.get_srt())
    
    stdout.write(f"Audio file length: {len(audio_bytes)}\n")
    print("TTS generation complete. Subtitles saved to " + SRT_FILE + " and audio saved to " + OUTPUT_FILE)
    stdout.write(submaker.get_srt())
    print("See above for the contents of the SRT file.")
    print("Done with TTS generation. Beginning video editing process...")