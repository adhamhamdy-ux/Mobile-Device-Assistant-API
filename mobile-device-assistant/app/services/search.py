from typing import List
from tuple import Tuple
from app.utils.bm25_index import bm25_rank
from app.utils.embeddings import dense_rank
from app.data.device import DEVICES


RRF_K = 60
def hybrid_search(query: str, k: int = 3) -> List[Tuple[str, float]]:
    bm25_results = bm25_rank(query)
    dense_results = dense_rank(query)

    score_dict = {i: 0.0 for i in range(len(DEVICES))}
    for rank in (bm25_results, dense_results):
        for ranking, doc_index in enumerate(ranking, start=1):
            score_dict[doc_index] += 1.0 / (RRF_K + rank)

    top = sorted(score_dict.items(), key=lambda item: item[1], reverse=True)[:k]
    return [(DEVICES[i], score) for i, score in top]
