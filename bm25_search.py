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
def search(query, k=5):
    chunks = load_data("data/chunks.json")

    # 1. 整理书库：每个文本块的正文分词
    tokenized_corpus = []
    for chunk in chunks:
        tokenized_corpus.append(tokenize(chunk["text"]))

    # 2. 建索引（循环结束后，只建一次）
    bm25 = BM25Okapi(tokenized_corpus)

    # 3. 问题分词，打分
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)

    # 4. 取分数最高的 k 个下标
    top_ids = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    # 5. 返回这 k 个文本块，并附上分数
    results = []
    for i in top_ids:
        results.append({"chunk_id":chunks[i]["chunk_id"] , "doc_id": chunks[i]["doc_id"],"score": scores[i], "text":chunks[i]["text"]})
    return results


if __name__ == '__main__':
    data = load_data("data/chunks.json")

    test = load_data("data/eval_questions.json")
    results = []
    originally_count = 0
    change_count = 0
    for q in test:
        result=search(q["question"])
        if any(r["doc_id"] == q["expected_doc"]for r in result):
            print("命中成功","类型是",q["type"],"问题",q["question"])
            if q["type"] =="原词":
                originally_count +=1
            elif q["type"] =="换说法":
                change_count +=1
        else:
            print("没命中的题目",q["question"])

    print("总命中数",originally_count+change_count,"原词命中数",originally_count,"换说法命中数",change_count)





