import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "./chroma_db"

SQLITE_DB = "./cease_desist.db"

CONFIDENCE_THRESHOLD = 0.80

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = os.getenv("POPPLER_PATH")
