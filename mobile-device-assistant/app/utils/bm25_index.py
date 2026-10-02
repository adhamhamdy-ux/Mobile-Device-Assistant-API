import BM25Okapi
from app.data.devices import DEVICES
def tokenize(text):
    return text.lower().split()

_bm25 = BM25Okapi([tokenize(doc) for doc in DEVICES])

def bm25_rank(query:str)->list[int]:
    tokenized_query = tokenize(query)
    scores = _bm25.get_scores(tokenized_query)

    return sorted(range(len(DEVICES)), key=lambda i: scores[i], reverse=True)
