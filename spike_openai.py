import io
import os

from openai import OpenAI

OPEN_API_KEY = os.environ["OPENAI_KEY"]

client = OpenAI(api_key=OPEN_API_KEY)
import requests
from dotenv import load_dotenv
from PIL import Image
from resizeimage import resizeimage

load_dotenv()


# engines = openai.Engine.list()
# print(engines)
# for engine in engines["data"]:
#     print(engine["id"])

good_engines = "text-davinci-003"


CHAT_SETTINGS = {
    "engine": "text-davinci-003",
    "max_tokens": 1500,
    "temperature": 0.9,
    "top_p": 1,
}

# completion = openai.Completion.create(
#     prompt="Give me a patriotic quote from Donald Trump.", **CHAT_SETTINGS
# )
# print(completion)
# print(completion["choices"][0]["text"])

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=1500,
    temperature=0.9,
    messages=[{"role": "user", "content": "Give me a new inspirational bible verse."}],
)
print(completion.choices[0].message.content)


# Example of generating a image from a prompt
# response = openai.Image.create(
#     prompt="an armchair in the shape of an avocado",
#     n=1,
#     size="1024x1024",
# )

# image_url = response["data"][0]["url"]
# print(f"Response: {response}")
# print(f"Image: {image_url}")


def square_image(filename, save_copy=False):
    with open(filename, "r+b") as fp:
        with Image.open(fp) as image:
            if image.height != image.width:
                image_dimension = min(max(image.width, image.height), 1024)
                cover = resizeimage.resize_contain(
                    image,
                    [image_dimension, image_dimension],
                    bg_color=(0, 0, 0, 0),
                )

                bytes_array = io.BytesIO()
                cover.save(bytes_array, format="PNG")
                if save_copy:
                    cover.save(open("book-cover-copy.png", "wb"), format="PNG")
                bytes_array = bytes_array.getvalue()
                return bytes_array
            else:
                fp.seek(0)
                return fp


# Example of making changes to an uploaded image
# with open("book_cover.png", "r+b") as fp:
#     with Image.open(fp) as image:
#         image_dimension = min(max(image.width, image.height), 1024)
#         cover = resizeimage.resize_contain(
#             image,
#             [image_dimension, image_dimension],
#             bg_color=(0, 0, 0, 0),
#         )

#         bytes_array = io.BytesIO()
#         cover.save(bytes_array, format="PNG")
#         cover.save(open("book-cover-resized.png", "wb"), format="PNG")
#         bytes_array = bytes_array.getvalue()
#         response = openai.Image.create_edit(
#             image=bytes_array,
#             prompt="change yellow to green",
#             n=2,
#             size="1024x1024",
#         )
#         print(f"Response: {response}")


# Example of making a variation of image
# response = openai.Image.create_variation(
#     image=square_image("Work-Profile-small.jpg"), n=1, size="1024x1024"
# )
# print(f"RESPONSE: {response}")


def upload_image(image_url):
    image_string = requests.get(image_url)

    response = requests.post(
        url="https://image.groupme.com/pictures",
        data=image_string,
        headers={
            "Content-Type": "image/png",
            "X-Access-Token": os.environ["GROUPME_ACCESS_TOKEN"],
        },
    )
    print(response)
    print(response.json())
    return response.json()["payload"]["picture_url"]


def post_message(picture_url):
    response = requests.post(
        "https://api.groupme.com/v3/bots/post",
        json={
            "text": "This is my best guess:",
            "picture_url": picture_url,
            "bot_id": os.environ["GROUPME_BOT_ID"],
        },
    )
    print(response)
    print(response.json())


# picture_url = upload_image(image_url)
# post_message(picture_url)
