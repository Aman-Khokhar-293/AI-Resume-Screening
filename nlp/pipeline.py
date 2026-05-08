import os
import spacy
import nltk
from functools import lru_cache
from config import SPACY_MODEL


@lru_cache(maxsize=1)
def get_nlp():
    try:
        return spacy.load(SPACY_MODEL)
    except OSError:
        raise RuntimeError(
            f"spaCy model '{SPACY_MODEL}' not found. Run: python scripts/setup_nlp.py"
        )


@lru_cache(maxsize=1)
def get_stopwords():
    try:
        return set(nltk.corpus.stopwords.words("english"))
    except LookupError:
        raise RuntimeError("NLTK stopwords not found. Run: python scripts/setup_nlp.py")
