import os
import logging
from google import genai
from google.generativeai import types # tiplar uchun import to'g'irlandi.

# Ushbu modul uchun loglashni sozlash
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Generate:
    """
    Google Gemini API bilan o'zaro aloqa qilish uchun mo'ljallangan sinf bo'lib, 
    taqdim etilgan JSON bilimlar bazasiga asoslanib savollarga javob beradigan savdo menejeri vazifasini bajaradi.
    """

    def __init__(self, api_token: str, json_file_path: str):
        """
        Generate klassini Gemini API tokeni va bilimlar bazasi fayli bilan ishga tushiradi.

        Argumentlar:
            api_token (str): Sizning Google Gemini API kalitingiz.
            json_file_path (str): Bilimlar bazasini o'z ichiga olgan JSON faylga yo'l.

        Xatoliklar:
            ValueError: Agar API tokeni topilmasa.
            IOError: Agar JSON fayli topilmasa yoki o'qib bo'lmasa.
        """
        if not api_token:
            logging.error("GEMINI_API_TOKEN topilmadi. Iltimos, Google Gemini API tokenini kiriting.")
            raise ValueError("Gemini klienti uchun API tokeni talab qilinadi.")
        
        self.client = genai.Client(api_key=api_token)
        self.model = "gemini-2.0-flash-lite"
        self.json_file_path = json_file_path
        
        # Ma'lumotlar JSON faylidan ishga tushirish (initialization) vaqtida yuklanadi
        self.data = self._load_data_from_json()

        # Gemini modelining tizim ko'rsatmalari sozlanadi
        self.generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text=f"""Tasavvur qiling, siz sotuv menejerisiz.
                Quyidagi ma'lumotlardan foydalaning:
                {self.data}
                Faqat ushbu ma'lumotlarga asoslanib savollarga javob bering. Agar savol berilgan mavzuga aloqador bo'lmasa yoki sizda javob berish uchun yetarli ma'lumot bo'lmasa, buni ochiq ayting va javob bermang. Agar ushbu mavzuda qo'shimcha ma'lumot bera olsangiz, uni faqat tanishish maqsadida taqdim etishingiz mumkin."""),
            ],
        )
        logging.info(f"{self.model} modeli va {self.json_file_path} bilimlar bazasi bilan Generate ishga tushirildi: ")

    def _load_data_from_json(self) -> str:
        """
        Belgilangan JSON fayldan ma'lumotni yuklaydi va qaytaradi.
        Bu yordamchi (private helper) metod.

        Qaytaradi:
            str: JSON fayl mazmuni qator (string) ko'rinishida.
        Xatoliklar:
            IOError: Agar fayl topilmasa yoki o'qib bo'lmasa.

        """
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logging.critical(f"JSON bilimlar bazasi mavjud emas: {self.json_file_path}. Please ensure it exists.")
            raise IOError(f"Bilimlar bazasi fayli '{self.json_file_path}' mavjud emas.")
        except Exception as e:
            logging.critical(f"JSON faylni o'qishda xatolik yuzaga keldi: '{self.json_file_path}': {e}")
            raise IOError(f"Bilimlar bazasi faylini o'qishda xatolik yuzaga keldi: '{self.json_file_path}'. Fayl formati va o'qish huquqini tekshiring.")

    def generate(self, question: str) -> str:
        """
        Konfiguratsiya qilingan Gemini modeli yordamida foydalanuvchi savoliga javob yaratadi.

        Argumentlar:
            question (str): Foydalanuvchining savoli.

        Qaytaradi:
            str: Gemini modelidan yaratilgan javob, yoki muammo yuzaga kelsa, xato xabari.
        """
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=question),
                ],
            ),
        ]
        
        try:
            logging.info(f"Geminiga savol yuborildi: '{question[:50]}...'") # So'rovning dastlabki 50 ta belgisi logga yoziladi
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=self.generate_content_config,
            )
            
            # Bo'sh javob bor-yo'qligi tekshiriladi va agar bo'lsa, logga yoziladi.
            if not response.text:
                logging.warning(f"Gemini API returned an empty text response for question: '{question}'")
                return "Kechirasiz, men savolingizga aniq javob topa olmadim. Boshqa savol berib ko'rishingiz mumkin."
                
            logging.info(f"Received response from Gemini: '{response.text[:50]}...'")
            return response.text
        except types.core.GeminiAPIError as e:
            logging.error(f"Gemini API error occurred: {e}")
            return "Kechirasiz, hozirda sun'iy intellekt xizmatida texnik muammo yuzaga keldi. Iltimos, keyinroq urinib ko'ring."
        except Exception as e:
            logging.error(f"An unexpected error occurred during content generation: {e}")
            return "Kechirasiz, so'rovingizni bajarishda kutilmagan xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."

# Ushbu blok Generate klassini mustaqil ravishda tekshirish (test qilish) uchun mo'ljallangan.
if __name__ == "__main__":
    # GEMINI_API_TOKEN .env faylidan tekshirish uchun
    from dotenv import load_dotenv
    load_dotenv()
    test_gemini_api_token = os.getenv("GEMINI_API_TOKEN")

    if not test_gemini_api_token:
        print("Error: GEMINI_API_TOKEN topilmadi. Testni ishga tushirib bo'lmaydi.")
    else:
        # Agar mavjud bo'lmasa, test qilish uchun soxta namdu.json fayli yaratiladi
        if not os.path.exists("namdu.json"):
            print("Test maqsadida 'namdu.json' fayli yaratilmoqda...")
            with open("namdu.json", "w", encoding="utf-8") as f:
                f.write("""
                {
                    "university_name": "Namangan Davlat Universiteti",
                    "faculties": [
                        {"name": "Kimyo Texnologiya", "description": "Kimyo fanlari va texnologiyalariga oid ta'lim beradi."},
                        {"name": "Fizika", "description": "Fizika qonuniyatlari va ularni amaliyotga tatbiq qilishni o'rgatadi."}
                    ],
                    "contacts": "Veb-sayt: namdu.uz, Tel: +998991234567"
                }
                """)
        
        try:
            namdu_generator = Generate(test_gemini_api_token, "namdu.json")
            
            print("\n--- Test Case 1: Tegishli savol ---")
            question1 = "Kimyoni o'rganib qaysi yo'nalishga kirsam bo'ladi?"
            response1 = namdu_generator.generate(question1)
            print(f"Savol: {question1}\nJavob: {response1}")

            print("\n--- Test Case 2: Yana bir tegishli savol ---")
            question2 = "Namangan Davlat Universitetining aloqa ma'lumotlari qanday?"
            response2 = namdu_generator.generate(question2)
            print(f"Savol: {question2}\nJavob: {response2}")

            print("\n--- Test Case 3: Aloqasi yo'q savol ---")
            question3 = "Eng yaxshi mashina qaysi?"
            response3 = namdu_generator.generate(question3)
            print(f"Savol: {question3}\nJavob: {response3}")

        except (ValueError, IOError) as e:
            print(f"\nIshga tushirish xatosi: {e}")
        except Exception as e:
            print(f"\nTest o'tkazish vaqtida kutilmagan xatolik: {e}")