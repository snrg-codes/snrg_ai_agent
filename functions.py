import base64
import os
from google import genai
from google.genai import types

# from dotenv import load_dotenv                    #
# load_dotenv()                                     #
from config import GEMINI_API_TOKEN                 #

with open("main.json", "r") as f:
    data = f.read()

def generate(savol):
    client = genai.Client(
        # api_key=os.getenv("GEMINI_API_TOKEN"),
        api_key=GEMINI_API_TOKEN,                   #
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{savol}"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=f"""tasavvur qil sen sotuv menedjerisan
            {data} - ma'lumotlaridan foydalan
            va savollarga javob ber. agar ushbu mavzuda qo'shimcha ma'lumot
            bera olsang ma'lumotni faqat tanishish maqsadida taqdim 
            etishing mumkin"""),
        ],
    )

    javob =  client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
        )
    return javob.text

with open("ponchiki_namangan.json", "r") as f:
    ponchiki_namangan = f.read()

def generate_ponchiki_namangan(savol):
    client = genai.Client(
        # api_key=os.getenv("GEMINI_API_TOKEN"),
        api_key=GEMINI_API_TOKEN,                   #
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{savol}"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=f"""tasavvur qil sen sotuv menedjerisan
            {ponchiki_namangan} - ma'lumotlaridan foydalan
            va savollarga javob ber. agar ushbu mavzuda qo'shimcha ma'lumot
            bera olsang ma'lumotni faqat tanishish maqsadida taqdim 
            etishing mumkin"""),
        ],
    )

    javob =  client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
        )
    return javob.text



if __name__ == "__main__":
    a = generate_ponchiki_namangan("Qanday ponchik turlari mavjud?")
    print(a)

