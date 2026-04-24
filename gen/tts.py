import asyncio
import edge_tts

OUTPUT_FILE = "voice.mp3"
SRT_FILE = "voice.srt"

def begin(NVIDIA_API_KEY, TEXT):
    asyncio.run(amain(TEXT))

async def amain(TEXT) -> None:
    voices = await VoicesManger.create()
    voice = voices.find(Gender = "Male", Language = "en-US")
    print(f"Generating mp3/srt using voice: {voice.Name}")

    tts = edge_tts.Communicate(TEXT, voice.Name)