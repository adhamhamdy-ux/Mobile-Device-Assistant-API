from sentence_transformers import SentenceTransformer
import numpy as np
from app.data.device import DEVICES

model = SentenceTransformer('BAAI/bge-small-en-v1.5')
doc = model.encode(DEVICES, normalize_embeddings=True)

def dense_rank(query:str)->list[int]:
    query_embedding = model.encode(query, normalize_embeddings=True)
    scores = doc @ query_embedding
    return list (np.argsort(-scores))

