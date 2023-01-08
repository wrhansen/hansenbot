import os

import openai
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.environ["OPENAI_KEY"]

openai.api_key = OPEN_API_KEY

engines = openai.Engine.list()
print(engines)
for engine in engines["data"]:
    print(engine["id"])

good_engines = "text-davinci-003"


CHAT_SETTINGS = {
    "engine": "text-davinci-003",
    "max_tokens": 1500,
    "temperature": 0.9,
    "top_p": 1,
}

completion = openai.Completion.create(
    prompt="Will AI rise up and destroy the human race?", **CHAT_SETTINGS
)

print(completion)
print(completion["choices"][0]["text"])
