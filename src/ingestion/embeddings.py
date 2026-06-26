import os
import voyageai
import logging
import numpy as np
from groq import Groq
from dotenv import load_dotenv
from typing import List
from functools import lru_cache
from langchain.schema import Document

# Load all variables from .env
load_dotenv()

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

VOYAGE_API_KEY         = os.getenv("VOYAGE_API_KEY")
GROQ_API_KEY           = os.getenv("GROQ_API_KEY")
VOYAGE_EMBEDDING_MODEL = os.getenv("VOYAGE_EMBEDDING_MODEL")
GROQ_LLM_MODEL         = os.getenv("GROQ_LLM_MODEL")

if not VOYAGE_API_KEY:
    raise ValueError("VOYAGE_API_KEY is missing — add it to your .env file")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing — add it to your .env file")
if not VOYAGE_EMBEDDING_MODEL:
    raise ValueError("VOYAGE_EMBEDDING_MODEL is missing — add it to your .env file")
if not GROQ_LLM_MODEL:
    raise ValueError("GROQ_LLM_MODEL is missing — add it to your .env file")
    
# CACHED CLIENTS 

@lru_cache(maxsize=1)
def get_voyage_client():
    """Return a cached Voyage AI client using VOYAGE_API_KEY from .env"""
    return voyageai.Client(api_key=VOYAGE_API_KEY)
 
 
@lru_cache(maxsize=1)
def get_groq_client():
    """Return a cached Groq client using GROQ_API_KEY from .env"""
    return Groq(api_key=GROQ_API_KEY)

#Generate Voyage embeddings for all document chunks.

def generate_embeddings(
    chunks: List[Document],
    batch_size: int = 128,
) -> np.ndarray:
   
    if not chunks:
        logger.warning("generate_embeddings() got empty chunk list.")
        return np.empty((0, 0), dtype="float32")
 
    vo    = get_voyage_client()
    texts = [c.page_content for c in chunks]
    all_embeddings = []
 
    logger.info(f"Calling Voyage API to embed {len(texts)} chunks "
                f"(model={VOYAGE_EMBEDDING_MODEL}) …")
 
    for i in range(0, len(texts), batch_size):
        batch = texts[i: i + batch_size]

        try:
            result = vo.embed(
                batch,
                model=VOYAGE_EMBEDDING_MODEL,
                input_type="document"
            )

            all_embeddings.extend(result.embeddings)
            logger.info(
              f"Embedded {min(i + batch_size, len(texts))}/{len(texts)} chunks"
            )

        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            raise

    embeddings = np.array(all_embeddings, dtype="float32")
 
 # L2-normalise → cosine similarity == dot product (needed for FAISS)

    norms      = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / np.clip(norms, 1e-10, None)
 
    logger.info(f"Embeddings shape: {embeddings.shape}")
    return embeddings
 
 
def get_query_embedding(query: str) -> np.ndarray:
    vo = get_voyage_client()

    try:
        result = vo.embed(
            [query],
            model=VOYAGE_EMBEDDING_MODEL,
            input_type="query"
        )

        vec = np.array(result.embeddings[0], dtype="float32")
        vec = vec / max(np.linalg.norm(vec), 1e-10)

        return vec.reshape(1, -1)

    except Exception as e:
        logger.error(f"Query embedding failed: {e}")
        raise

