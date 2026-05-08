import os
from dotenv import load_dotenv

load_dotenv()

# Use absolute path for SQLite to avoid working directory issues on Render
_default_db = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")
DATABASE_URL = os.getenv("DATABASE_URL", _default_db)
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")
