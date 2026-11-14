#读 data/regression_code.json
#写 无
#预期 纯向量 3 道，BM25 5 道 # 实际：BM25 13，向量 11
#预期 向量块9  bm25块12
from ingest import load_data
import bm25_search
import vector_search
from sentence_transformers import SentenceTransformer

if __name__ == "__main__":
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
    data = load_data("data/regression_code.json")
    chunks = load_data("data/chunks.json")
    bm25 = bm25_search.build_index(chunks)
    vectors = vector_search.get_vectors(chunks, model)
    questions = data
    bm_25_right = 0
    bm_block=0
    ve_right=0
    ve_block=0

    for q in questions:
        bm_r=False
        ve_r=False
        bm_r_block=False
        ve_r_block=False
        result_bm = bm25_search.search(q["question"],bm25,chunks,k=5)
        result_ve = vector_search.vector_search(q["question"], model, vectors, chunks,k=5)
        if any(r["doc_id"] == q["expected_doc"] for r in result_bm):
            bm_r = True
        if any(q["identifier"] in r["text"] for r in result_bm):
            bm_r_block = True
        if any(r["doc_id"] == q["expected_doc"] for r in result_ve):
            ve_r = True
        if any(q["identifier"] in r["text"] for r in result_ve):
            ve_r_block = True
        if bm_r: bm_25_right += 1
        if ve_r: ve_right += 1
        if bm_r_block: bm_block += 1
        if ve_r_block: ve_block += 1

        print(q["identifier"], "BM25:", bm_r, "向量:", ve_r)
        print(q["identifier"],"bm_block",bm_r_block,"ve_block",ve_r_block,)

    print("BM25:", bm_25_right, "/", len(data))
    print("Ve:", ve_right, "/", len(data))
    print("BM_block:", bm_block, "/", len(data))
    print("VE_block:", ve_block, "/", len(data))