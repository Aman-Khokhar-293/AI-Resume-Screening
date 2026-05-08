import os
import sys
import subprocess

SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")

def run(cmd: list[str]):
    print("$", " ".join(cmd))
    subprocess.check_call(cmd)

if __name__ == "__main__":
    # Download spaCy model
    run([sys.executable, "-m", "spacy", "download", SPACY_MODEL])

    # Download NLTK data
    import nltk
    nltk.download("stopwords")
    nltk.download("punkt")
    print("NLP setup complete.")
