#读data/chunks.json data/eval_ambiguous.json
#写data/ambiguous_answers.json
#预期检索覆盖 23 / 23
#回答覆盖 15 / 23
#拒答 3 / 8

from ingest import load_data,save_data
from vector_search import get_vectors
from sentence_transformers import SentenceTransformer
from rag import answer
import sys
import os

OUT_PATH = "data/ambiguous_answers.json"
if __name__ == "__main__":
    if os.path.exists(OUT_PATH):
        print("文件已存在，请检查")
        sys.exit()
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
    chunks = load_data("data/chunks.json")
    vectors = get_vectors(chunks, model)
    questions = load_data("data/eval_ambiguous.json")
    table = {}
    for c in chunks:
        table[c["chunk_id"]] = c["doc_id"]

    records = []
    for i, q in enumerate(questions, start=1):
        result = answer(q["question"], model, vectors, chunks)
        sources = []
        for cid in result["sources"]:
            sources.append({"chunk_id": cid, "doc_id": table[cid]})
        records.append({
            "question": q["question"],
            "type": q["type"],
            "expected_docs": q["expected_docs"],
            "answer": result["answer"],
            "sources": sources,
        })
        print("打印到第{}题了一共{}题".format(i, len(questions)))
    save_data(records,OUT_PATH)
    print("已保存", len(records), "道")



