import base64
import os
from google import genai
from google.genai import types
                              
from config import GEMINI_API_TOKEN                 

class Generate:
    def __init__(self, GEMINI_API_TOKEN, json_file):

        self.client = genai.Client(
            api_key=GEMINI_API_TOKEN,
        )
        self.model = "gemini-2.0-flash-lite"
        self.json_file = json_file
        with open(self.json_file, 'r', encoding='utf-8') as f:
            self.data = f.read()
    
        self.generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text=f"""tasavvur qil sen sotuv menedjerisan
                {self.data} - ma'lumotlaridan foydalan
                va savollarga javob ber. agar ushbu mavzuda qo'shimcha ma'lumot
                bera olsang ma'lumotni faqat tanishish maqsadida taqdim 
                etishing mumkin"""),
            ],
        )
    
    def generate(self, savol):
        self.contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=f"""{savol}"""),
                ],
            ),
        ]
        javob =  self.client.models.generate_content(
                model=self.model,
                contents=self.contents,
                config=self.generate_content_config,
        )
        return javob.text

if __name__ == "__main__":  

    namdu = Generate(GEMINI_API_TOKEN, "namdu.json")
    savol = "Kimyoni o'rganib qaysi yo'nalishga kirsam bo'ladi"
    javob = namdu.generate(savol)
    print(javob)
       
