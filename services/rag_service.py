"""Lightweight RAG service using ChromaDB for semantic retrieval.

Pipeline: Chunk → Embed → Store → Retrieve → Pass to LLM
"""

import chromadb
import os
import re
from typing import List

CHROMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "chroma_db"
)


def _get_client() -> chromadb.PersistentClient:
    os.makedirs(CHROMA_PATH, exist_ok=True)
    return chromadb.PersistentClient(path=CHROMA_PATH)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks using sentence-aware splitting."""
    if not text or not text.strip():
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks: List[str] = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) <= chunk_size:
            current += (" " + sentence) if current else sentence
        else:
            if current:
                chunks.append(current.strip())
            current = sentence

    if current:
        chunks.append(current.strip())

    # Fallback: character-based splitting when no sentence boundaries exist
    if not chunks:
        for i in range(0, len(text), chunk_size - overlap):
            piece = text[i : i + chunk_size]
            if piece.strip():
                chunks.append(piece.strip())

    return chunks


def store_and_retrieve(
    resume_text: str, jd_text: str, top_k: int = 5
) -> dict:
    """Full RAG pipeline: chunk, embed, store in ChromaDB, and retrieve.

    Returns dict with retrieved context strings and chunk statistics.
    """
    client = _get_client()

    # Reset collections for a fresh analysis
    for name in ("resume_chunks", "jd_chunks"):
        try:
            client.delete_collection(name)
        except Exception:
            pass

    resume_col = client.create_collection(
        name="resume_chunks", metadata={"hnsw:space": "cosine"}
    )
    jd_col = client.create_collection(
        name="jd_chunks", metadata={"hnsw:space": "cosine"}
    )

    resume_chunks = chunk_text(resume_text)
    jd_chunks = chunk_text(jd_text)

    # Store resume chunks with auto-generated embeddings
    if resume_chunks:
        resume_col.add(
            documents=resume_chunks,
            ids=[f"resume_{i}" for i in range(len(resume_chunks))],
            metadatas=[
                {"source": "resume", "chunk_index": i}
                for i in range(len(resume_chunks))
            ],
        )

    # Store JD chunks
    if jd_chunks:
        jd_col.add(
            documents=jd_chunks,
            ids=[f"jd_{i}" for i in range(len(jd_chunks))],
            metadatas=[
                {"source": "jd", "chunk_index": i}
                for i in range(len(jd_chunks))
            ],
        )

    # Retrieve: query resume with JD to find relevant experience
    retrieved_resume: List[str] = []
    if resume_chunks and jd_chunks:
        res = resume_col.query(
            query_texts=[jd_text[:1000]],
            n_results=min(top_k, len(resume_chunks)),
        )
        retrieved_resume = res["documents"][0] if res["documents"] else []

    # Retrieve: query JD with resume to find relevant requirements
    retrieved_jd: List[str] = []
    if jd_chunks and resume_chunks:
        res = jd_col.query(
            query_texts=[resume_text[:1000]],
            n_results=min(top_k, len(jd_chunks)),
        )
        retrieved_jd = res["documents"][0] if res["documents"] else []

    return {
        "resume_chunks_total": len(resume_chunks),
        "jd_chunks_total": len(jd_chunks),
        "retrieved_resume_chunks": retrieved_resume,
        "retrieved_jd_chunks": retrieved_jd,
        "resume_context": "\n\n".join(retrieved_resume),
        "jd_context": "\n\n".join(retrieved_jd),
    }
