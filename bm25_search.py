import jieba
from ingest import load_data
from rank_bm25 import BM25Okapi

STOPWORDS={"的", "了", "是", "在", "和", "你", "我", "这", "一个", "可以","怎么"}
def tokenize(text):
    result = jieba.lcut(text)
    result_no_blank=[]
    for word in result:
        word = word.lower()
        if not word.strip():
            continue
        elif not word.isalnum():
            continue
        elif word in STOPWORDS:
            continue
        result_no_blank.append(word)


    return result_no_blank
def search(query,bm25,chunks,k=5):
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)

    # 4. 取分数最高的 k 个下标
    top_ids = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    # 5. 返回这 k 个文本块，并附上分数
    results = []
    for i in top_ids:
        results.append({"chunk_id":chunks[i]["chunk_id"] , "doc_id": chunks[i]["doc_id"],"score": scores[i], "text":chunks[i]["text"]})
    return results
def build_index(chunks):
    tokenized_corpus = []
    for chunk in chunks:
        tokenized_corpus.append(tokenize(chunk["text"]))
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25
def build_overlap_index(chunks):
    overlap_list = []
    for chunk in chunks:
        overlap_list.append(set(tokenize(chunk["text"])))
    return overlap_list
def overlap_search(query, index, chunks, k=5):
    query_tokens = tokenize(query)

    scores=[]
    for t in index:
        count = 0
        for q in query_tokens:
            if q in t:
                count+=1
        scores.append(count)

    top_ids = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    results = []
    for i in top_ids:
        results.append({"chunk_id":chunks[i]["chunk_id"] , "doc_id": chunks[i]["doc_id"],"score": scores[i], "text":chunks[i]["text"]})
    return results


if __name__ == '__main__':
    chunks = load_data("data/chunks.json")
    test = load_data("data/eval_questions.json")
    query="怎么声明路径参数"
    index = build_overlap_index(chunks)
    results = overlap_search(query, index, chunks)
    for r in results:
        print(r["chunk_id"], r["score"])






