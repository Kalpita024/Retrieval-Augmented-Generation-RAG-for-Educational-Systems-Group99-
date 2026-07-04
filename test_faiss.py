from src.vectorstore.faiss_db import *

import numpy as np

index = create_index(384)

embeddings = np.random.rand(
    100,
    384
)

add_embeddings(
    index,
    embeddings
)

save_index(
    index,
    "exam_chatbot.faiss"
)

loaded_index = load_index(
    "exam_chatbot.faiss"
)

query = np.random.rand(
    384
)

distances, indices = search(
    loaded_index,
    query
)

print(indices)