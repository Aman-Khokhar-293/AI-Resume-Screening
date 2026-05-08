from __future__ import annotations
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _build_vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=20000,
    )


def cosine_match_score(query_text: str, doc_text: str) -> float:
    vec = _build_vectorizer()
    X = vec.fit_transform([query_text or "", doc_text or ""])
    sim = cosine_similarity(X[0], X[1])[0][0]
    return float(sim)


def batch_recommend(candidate_text: str, jobs: List[Tuple[int, str]], top_k: int = 5) -> List[Tuple[int, float]]:
    # jobs: list of (job_id, job_description)
    texts = [candidate_text or ""] + [desc or "" for _, desc in jobs]
    vec = _build_vectorizer()
    X = vec.fit_transform(texts)
    sims = cosine_similarity(X[0], X[1:]).ravel()
    pairs = [(jobs[i][0], float(sims[i])) for i in range(len(jobs))]
    pairs.sort(key=lambda x: x[1], reverse=True)
    return pairs[:top_k]
