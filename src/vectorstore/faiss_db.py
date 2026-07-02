import faiss
import numpy as np

def create_index(dimension):
    return faiss.IndexFlatL2(dimension)

def add_embeddings(index, embeddings):
    embeddings = np.array(
        embeddings,
        dtype="float32"
    )
    index.add(embeddings)

def save_index(index, filename):
    faiss.write_index(index, filename)

def load_index(filename):
    return faiss.read_index(filename)

def search(index, query_embedding, k=5):
    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    return distances, indices