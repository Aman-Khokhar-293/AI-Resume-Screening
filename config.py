import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")
