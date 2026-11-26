from ingest import load_data
from vector_search import get_vectors,vector_search
from sentence_transformers import SentenceTransformer



chunks = load_data("data/chunks.json")
model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
vectors = get_vectors(chunks,model)
file = load_data("data/eval_questions.json")
misses = []
print(len(file))
counts = {
    "原词":   {"前5": 0, "6-20": 0, "20后": 0},
    "换说法": {"前5": 0, "6-20": 0, "20后": 0},
}
def rank_of(results,chunk_id):
    for i,result in enumerate(results,start=1):
        if result["chunk_id"] == chunk_id:
            return i
    return None
def rank_of_doc(results,doc_id):
    for i,result in enumerate(results,start=1):
        if result["doc_id"] == doc_id:
            return i
    return None

if __name__=="__main__":

    for f in file:
        result=vector_search(f["question"],model,vectors,chunks,k=50)
        count=rank_of_doc(result,f["expected_doc"])
        if count is not None and count <= 5:
            bucket = "前5"
        elif count is not None and 5<count<=20:
            bucket = "6-20"
        else:
            bucket = "20后"
        if f["type"] == "换说法" and bucket != "前5":
            misses.append((count, f["question"]))
        counts[f["type"]][bucket] += 1  # 题型本身就是字典的键
    print(counts)
    for count, q in misses:
        print(count, q)





