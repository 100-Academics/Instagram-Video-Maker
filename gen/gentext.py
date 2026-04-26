import requests, base64
import json
import re
from gen.tts import begin as tts_begin

NVIDIA_API_KEY = None
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False

## read from text file to prevent overwrites when pushing and pulling this file.
PROMPT = "" ## probably unnecessary, but I'm doing it anyways cause it feels better
with open("gen/prompt.txt", "r") as f:
    PROMPT = str(f.read()) ## ensure string type just in case. idk.

strings_to_remove = ["pSTORY_BEGINp", "pCOMMENT_BEGINp"] ## Idfk why I did this there was no need. Not touching it.

def read_b64(path): ## copy pasted from the "view code" button @ https://build.nvidia.com/qwen/qwen3.5-122b-a10b
  with open(path, "rb") as f:
    return base64.b64encode(f.read()).decode()

def cleanFile(data): ## file cleaning to make it slightly prettier in ways I don't trust the AI to correctly generate, or can't fix based on json parsing
    with open("response.txt", "w") as f:

        cleaned_data = re.sub(r'\n{2,}', '\n', data) ## remove weird extra newlines. Thanks json.
        cleaned_data = cleaned_data.replace(strings_to_remove[0], "") ## clear the title header
        cleaned_data = cleaned_data.replace(strings_to_remove[1], "Here's some top comments:") ## replace comments header
        cleaned_data = re.sub(r'\bu/([A-Za-z0-9_-]+)\b(?!\s+says\b)', r'u/\1 says', cleaned_data) ## add something nice to the end of the usernames so it's not just "[USERNAME]: [COMMENT]" for every comment.

        f.write(cleaned_data) ## hard copy for later.

    next(NVIDIA_API_KEY) ## always pass through API key.

def saveResponse(headers, payload): ## basically copy pasted from the show code button @ https://build.nvidia.com/qwen/qwen3.5-122b-a10b but with some changes, as well as being moved into its own function.
    response = requests.post(invoke_url, headers=headers, json=payload, stream=stream)
    response_data = None
    stillGoing = True
    while(stillGoing): ## don't move to the next stuff while its still generating the story.
        if response.status_code != 200:
            print("Error: " + str(response.status_code) + " - " + response.text)
            break

        if stream:
            for line in response.iter_lines():
                if line:
                    print(line.decode("utf-8"))
        else:
            response_data = response.json()
            print(f"Response is: {response_data}")
            stillGoing = False ## break once story is done
            break


    if response_data is None:
        return ## break if you get nothing back.

    print("Done generating story. Cleaning story of uneccesary characters...")
    with open("response.json", "w") as j:
        json.dump(response_data, j, indent=2) ## To make it easier to see the structure of the response.

    data = response_data.get("choices", [{}])[0].get("message", {}).get("content", "") ## get just the story.
    cleanFile(data)


def next(NVIDIA_API_KEY):
    print("Done cleaning file, begin TTS generation...")
    tts_begin(NVIDIA_API_KEY) ## move to next thing.



def run(NVIDIA_API_KEY, additional_prompt): ## basically copy pasted from the show code button @ https://build.nvidia.com/qwen/qwen3.5-122b-a10b

   if (additional_prompt is not None or additional_prompt is not "\n"):
       print(f"Additional prompt provided. Adding \"{additional_prompt}\" to Qwen generation prompt.")

   headers = {
  "Authorization": f"Bearer {NVIDIA_API_KEY}",
  "Accept": "text/event-stream" if stream else "application/json"
   }

   payload = {
       "model": "qwen/qwen3.5-122b-a10b",
       "messages": [{"role": "user", "content": PROMPT + additional_prompt}],
       "max_tokens": 16384,
       "temperature": 0.60,
       "top_p": 0.95,
       "stream": stream,
       "chat_template_kwargs": {"enable_thinking": True},
   }

   print("Generating story...")
   saveResponse(headers, payload)