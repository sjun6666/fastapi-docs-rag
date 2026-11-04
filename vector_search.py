from sentence_transformers import SentenceTransformer
from ingest import load_data
import os
import numpy as np
def get_vectors(chunks,model):
    if os.path.exists("data/chunk_vectors.npy"):
        vectors= np.load("data/chunk_vectors.npy")
        return vectors
    else:
        texts =build_vector_index(chunks,model)
        np.save("data/chunk_vectors.npy",texts)
        vectors = np.load("data/chunk_vectors.npy")
        return vectors

def build_vector_index(chunks, model):
    texts = []
    for chunk in chunks:
        texts.append(chunk["text"])
    vectors = model.encode(texts,normalize_embeddings=True)
    return vectors


# 返回 NumPy 数组，1093 × 512
def vector_search(query, model, vectors, chunks, k=5):
    q_vectors = model.encode(query, normalize_embeddings=True)
    scores=q_vectors @ vectors.T

    top_ids = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    # 5. 返回这 k 个文本块，并附上分数
    results = []
    for i in top_ids:
        results.append({"chunk_id": chunks[i]["chunk_id"], "doc_id": chunks[i]["doc_id"], "score": scores[i],
                        "text": chunks[i]["text"]})
    return results
if __name__ == "__main__":
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")   # 只加载一次
    chunks = load_data("data/chunks.json")
    vectors = get_vectors(chunks,model)

    for query in ["怎么声明路径参数", "URL 里的变量怎么获取"]:
        results = vector_search(query, model, vectors, chunks)
        print("问题：", query)
        for r in results:
            print(r["chunk_id"], round(float(r["score"]), 3))
