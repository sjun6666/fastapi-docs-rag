from ingest import load_data,save_data
from vector_search import vector_search,get_vectors
from sentence_transformers import SentenceTransformer
import sys
import os
from rag import answer




if __name__ == "__main__":
    if os.path.exists("data/dev_answers.json"):
        print("文件已存在，请检查")
        sys.exit()
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
    chunks = load_data("data/chunks.json")
    vectors = get_vectors(chunks, model)
    questions = load_data("data/eval_questions.json")
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
            "expected_doc": q["expected_doc"],
            "answer": result["answer"],
            "sources": sources,
        })
        print("打印到第{}题了一共{}题".format(i, len(questions)))
    save_data(records,"data/dev_answers.json")# ② 在这里用 save_data 存到 data/dev_answers.json，并打印一共存了几道
    print("已保存", len(records), "道")




