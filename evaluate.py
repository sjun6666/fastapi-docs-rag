import time
from ingest import load_data
import bm25_search




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
    bm25 = bm25_search.build_index(data)
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