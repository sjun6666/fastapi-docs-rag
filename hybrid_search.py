from bm25_search import build_index, search
from vector_search import get_vectors,vector_search
from ingest import load_data
from sentence_transformers import SentenceTransformer


def hybrid_search(query,bm25,model,vectors,chunks,k=5,n=20):
    results_bm=search(query,bm25,chunks,n)
    results_ve=vector_search(query,model,vectors,chunks,n)
    score={}
    table = {}
    for chunk in chunks:
        table[chunk["chunk_id"]] = chunk
    for rank,r in enumerate(results_bm,start=1):
        if r['chunk_id'] not in score:
            score[r['chunk_id']] = 0
        score[r['chunk_id']] += 1/(60+rank)
    for rank,r in enumerate(results_ve,start=1):
        if r['chunk_id'] not in score:
            score[r['chunk_id']] = 0
        score[r['chunk_id']] += 1/(60+rank)
    top_ids = sorted(score,key = lambda cid : score[cid], reverse=True)[:k]
    result = []
    for i in top_ids:
        result.append({"chunk_id": table[i]["chunk_id"], "doc_id": table[i]["doc_id"], "score": score[i],
                        "text": table[i]["text"]})
    return result











if __name__=="__main__":
    query = "怎么声明路径"
    chunks = load_data("data/chunks.json")
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
    vectors = get_vectors(chunks,model)
    bm25 = build_index(chunks)
    print(hybrid_search(query,bm25,model,vectors,chunks))