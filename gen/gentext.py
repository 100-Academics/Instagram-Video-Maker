import requests, base64
import json
import re
from gen.tts import begin as tts_begin

NVIDIA_API_KEY = None
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False

## formatted weird because I moved it up from the run function
PROMPT = "Follow these instructions carefully: " + "You are to generate an entertaining Reddit \"Am I the Asshole\" (AITA) story. " + "Make it as believable or unbelievable as you want, be sure to make it unique. " + "It must remain grounded in realism, however. " + "That is not say, nothing supernatural, for example. Make as crazy as you see fit." + "Make sure whatever you write is maximally entertaining for short-form (instagram reels) content. Be sure to include your/someone else's gender and age (whomever it may pertain to) in the form M(AGE) or F(AGE) whenever you introduce yourself or other people." +  "However, while writing, you MUST follow some specific rules: \n " + "First: You must NOT generate a title or original poster. \n" + "Second: You are to denote when the story starts by saying \"pSTORY_BEGINp\" exactly as typed.\n" + "Third: You do not have to include post comments, but you can. If you do, you must first list " + "the user (i.e \"u/exampleusername\"), and then the comment. " +  "You MUST come up with convincing usernames for the commentors, something that sounds real. " + "The comments must also be realistic.\n" + "Fourth: You must denote when the FIRST comment starts by saying \"pCOMMENT_BEGINp\" exactly as I have. \n " + "Fifth: Do not be too shocking. For example, do not write about a woman leaving her dog in a freezer. The story does not have to be about dogs. Only go to them if you can think of nothing else.\n\n" + "Now please generate the story following the above instructions. " + "Remember to follow the instructions carefully and to denote the " + "beginning of the story and comments as specified. \n\nFinally, make sure to end the story with a verdict of either \"YTA\", \"NTA\", \"ESH\", or \"NAH\". " + "This should be the last thing in the story. " + "This is important because I want the outcome known and I want it to be accurate. " + "If you do not end the story with one of these verdicts, I will assume the verdict is NAH. " + "If you do not follow these instructions, I will be very sad and disappointed in you. " + "So please follow them carefully. Thank you!"
additional_prompt = "\nThe story should be about something." ## change this out if you want it to be about something specific

strings_to_remove = ["pSTORY_BEGINp", "pCOMMENT_BEGINp"]

def read_b64(path):
  with open(path, "rb") as f:
    return base64.b64encode(f.read()).decode()

def cleanFile(data):
    with open("response.txt", "w") as f:
        
        cleaned_data = re.sub(r'\n{2,}', '\n', data)
        cleaned_data = cleaned_data.replace(strings_to_remove[0], "")
        cleaned_data = cleaned_data.replace(strings_to_remove[1], "Here's some top comments:")
        cleaned_data = re.sub(r'\bu/([A-Za-z0-9_-]+)\b(?!\s+says\b)', r'u/\1 says', cleaned_data)
        
        f.write(cleaned_data) ## hard copy for later.
        
        


    next(NVIDIA_API_KEY)

def saveResponse(headers, payload):
    response = requests.post(invoke_url, headers=headers, json=payload, stream=stream)
    response_data = None
    stillGoing = True
    while(stillGoing):
        if response.status_code != 200:
            print("Error: " + str(response.status_code) + " - " + response.text)
            break

        if stream:
            for line in response.iter_lines():
                if line:
                    print(line.decode("utf-8"))
        else:
            response_data = response.json()
            print(response_data)
            stillGoing = False
            break
        
    
    if response_data is None:
        return

    print("Done generating story. Cleaning story of uneccesary characters...")
    with open("response.json", "w") as j:
        json.dump(response_data, j, indent=2)

    data = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
    cleanFile(data)
            

def next(NVIDIA_API_KEY):
    print("Done cleaning file, begin TTS generation...")
    tts_begin(NVIDIA_API_KEY)


def run(NVIDIA_API_KEY):
   NVIDIA_API_KEY = NVIDIA_API_KEY
   headers = {
  "Authorization": f"Bearer {NVIDIA_API_KEY}",
  "Accept": "text/event-stream" if stream else "application/json"
   }

   payload = {
    "model": "qwen/qwen3.5-122b-a10b",
    "messages": [{"role":"user","content": PROMPT + additional_prompt
                    }],
    "max_tokens": 16384,
    "temperature": 0.60,
    "top_p": 0.95,
    "stream": stream,
    "chat_template_kwargs": {"enable_thinking":False},
    }
   print("Generating story...")
   saveResponse(headers, payload)

