#读 test_questions.json chunks.json test_unanswerable.json
#写 data/test_answers.json
#预期 文档级 Hit@5：28/36
#块级 Hit@5：28/36
#拒答：8/36，其中误拒 3
#引用文档命中率：80%
#无答案题拒答：10/10

from ingest import load_data,save_data
from vector_search import vector_search,get_vectors
from sentence_transformers import SentenceTransformer
import sys
import os
from rag import answer




if __name__ == "__main__":
    TRIAL = False  # 试跑时为 True；正式跑之前改成 False
    if TRIAL:
        QUESTIONS_PATH = "data/eval_questions.json"  # 换成你开发集题目文件的真实名字
        UNANSWERABLE_PATH = None  # 试跑不用无答案题
        OUT_PATH = "data/trial_answers.json"
        question = load_data(QUESTIONS_PATH)[:3]
        unanswerable_question = []
    else:
        QUESTIONS_PATH = "data/test_questions.json"
        UNANSWERABLE_PATH = "data/test_unanswerable.json"
        OUT_PATH = "data/test_answers.json"
        question = load_data(QUESTIONS_PATH)
        unanswerable_question = load_data(UNANSWERABLE_PATH)
    if os.path.exists(OUT_PATH):
        print("文件已存在，请检查")
        sys.exit()
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
    test_candidates=load_data("data/test_candidates.json")
    chunks = load_data("data/chunks.json")
    vectors = get_vectors(chunks, model)

    table = {}
    table_candidates={}
    for q in test_candidates:
        table_candidates[q["question"]]=q["source_chunk"]
    questions=[]
    for q in question:
        q["answerable"]=True
        if q["question"] in table_candidates:
            q["source_chunk"]=table_candidates[q["question"]]
        questions.append(q)
    for q in unanswerable_question:
        q["answerable"]=False
        q["source_chunk"]=None
        questions.append(q)
    if not TRIAL:
        for q in questions:
            if q["answerable"]:
                assert q.get("source_chunk"), q["question"]

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
            "expected_doc": q.get("expected_doc"),
            "answerable":q["answerable"],
            "source_chunk":q.get("source_chunk"),
            "answer": result["answer"],
            "sources": sources,
        })
        print("打印到第{}题了一共{}题".format(i, len(questions)))
    save_data(records,OUT_PATH)
    if not TRIAL: assert len(records) == 46




