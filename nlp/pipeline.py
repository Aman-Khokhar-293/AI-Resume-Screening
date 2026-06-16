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
        try:
            from spacy.cli import download
            download(SPACY_MODEL)
            return spacy.load(SPACY_MODEL)
        except Exception as e:
            raise RuntimeError(
                f"spaCy model '{SPACY_MODEL}' not found and automatic download failed: {str(e)}"
            )


@lru_cache(maxsize=1)
def get_stopwords():
    try:
        return set(nltk.corpus.stopwords.words("english"))
    except LookupError:
        try:
            nltk.download("stopwords")
            nltk.download("punkt")
            return set(nltk.corpus.stopwords.words("english"))
        except Exception as e:
            raise RuntimeError(f"NLTK stopwords not found and automatic download failed: {str(e)}")
