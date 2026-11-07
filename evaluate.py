import time
from ingest import load_data
import bm25_search
from sentence_transformers import SentenceTransformer
import vector_search
import hybrid_search


if __name__=="__main__":
    t0 = time.perf_counter()
    data = load_data("data/chunks.json")
    test = load_data("data/eval_questions.json")
    chunks = load_data("data/chunks.json")
    hit_original = 0
    hit__change_original=0
    miss_count = 0
    bm25 = bm25_search.build_index(data)
    for q in test:
        result = bm25_search.search(q["question"], bm25,chunks)
        if any(r["doc_id"] == q["expected_doc"]for r in result):
            if q["type"]=="原词":
                hit_original += 1
            elif q["type"]=="换说法":
                hit__change_original += 1
        else:
            miss_count += 1
    print("一共有多少数据",len(test),"命中数据",hit_original+hit__change_original,"类型是原词的有：",hit_original,"类型是换说法的有",hit__change_original,
          "出错的有",miss_count)


    print("耗时", round(time.perf_counter() - t0, 2))
    hit_original = 0
    hit__change_original=0
    miss_count = 0
    index = bm25_search.build_overlap_index(data)
    for q in test:
        result = bm25_search.overlap_search(q["question"],index, chunks)
        if any(r["doc_id"] == q["expected_doc"] for r in result):
            if q["type"] == "原词":
                hit_original += 1
            elif q["type"] == "换说法":
                hit__change_original += 1
        else:
            miss_count += 1
    print("一共有多少数据", len(test), "命中数据", hit_original + hit__change_original, "类型是原词的有：", hit_original,
          "类型是换说法的有", hit__change_original,
          "出错的有", miss_count)
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")  # 只加载一次
    chunks = load_data("data/chunks.json")
    vectors = vector_search.get_vectors(chunks, model)
    hit_original = 0
    hit__change_original = 0

    all_right=0
    for q in test:
        result_v = vector_search.vector_search(q["question"], model, vectors, chunks)
        result_bm = bm25_search.search(q["question"], bm25, chunks)
        hit_vec = any(r["doc_id"] == q["expected_doc"] for r in result_v)
        hit_bm = any(r["doc_id"] == q["expected_doc"] for r in result_bm)
        top_2=bm25_search.search(q["question"], bm25, chunks, 2)
        s1 = top_2[0]["score"]
        s2 = top_2[1]["score"]
        if s2>0:
            ratio=s1/s2
        else:
            ratio=99

        if hit_vec ==hit_bm == True:
            all_right += 1
        if hit_vec == hit_bm == False:
            print("两个都错：",q["question"])
        if hit_vec == True and hit_bm == False:
            print("bm25错：", q["question"],"比值是",ratio)
        if hit_vec == False and hit_bm == True:
            print("v错误", q["question"],"比值是",ratio)
    print("两个都对",all_right)

    weights = [(1, 0),(0, 1),(1, 1),(1, 3),(1, 5),(1, 10)]
    for w_bm, w_ve in weights:
        hit_original = 0
        hit__change_original = 0
        miss_count = 0
        w_bm = w_bm
        w_ve = w_ve
        for q in test:
            result = hybrid_search.hybrid_search(q["question"],bm25,model,vectors,chunks,k=5,n=20,w_bm=w_bm,w_ve=w_ve)
            if any(r["doc_id"] == q["expected_doc"] for r in result):
                if q["type"] == "原词":
                    hit_original += 1
                elif q["type"] == "换说法":
                    hit__change_original += 1
            else:
                miss_count += 1
        print("一共有多少数据", len(test), "权重w_bm,w_ve",w_bm,w_ve,"命中数据", hit_original + hit__change_original, "类型是原词的有：", hit_original,
            "类型是换说法的有", hit__change_original,
            "出错的有", miss_count)





