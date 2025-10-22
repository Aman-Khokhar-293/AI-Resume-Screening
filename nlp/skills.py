from __future__ import annotations
import csv
import os
from typing import Iterable, Set
from .pipeline import get_nlp, get_stopwords

_SKILLS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "skills.csv")


def _load_skill_vocab() -> Set[str]:
    vocab: set[str] = set()
    if os.path.exists(_SKILLS_PATH):
        with open(_SKILLS_PATH, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                skill = row[0].strip().lower()
                if skill:
                    vocab.add(skill)
    return vocab

_SKILL_VOCAB = _load_skill_vocab()


def extract_skills(text: str) -> Set[str]:
    if not text:
        return set()
    doc = get_nlp()(text)
    stops = get_stopwords()

    # Simple candidates: tokens and noun chunks intersected with known vocab
    tokens = {t.lemma_.lower() for t in doc if not t.is_space}
    tokens |= {t.text.lower() for t in doc if not t.is_space}

    noun_chunks = {chunk.text.strip().lower() for chunk in doc.noun_chunks}

    candidates = set()
    for tok in tokens | noun_chunks:
        tok_norm = tok.strip().lower()
        if not tok_norm or tok_norm in stops:
            continue
        if tok_norm in _SKILL_VOCAB:
            candidates.add(tok_norm)
        # handle simple punctuation variants
        tok_norm2 = tok_norm.replace(" ", "-")
        if tok_norm2 in _SKILL_VOCAB:
            candidates.add(tok_norm2)
    return candidates
