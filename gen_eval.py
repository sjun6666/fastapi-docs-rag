import json
import random
from llm import ask_llm
from ingest import load_data,save_data
chunks = load_data("data/chunks.json")
random.seed(40)
save_path="data/eval_candidates2.json"

count=0
c_num=0
records = []
used_id=set()
used_file= load_data("data/eval_questions.json")
for f in used_file:
    used_id.add(f["expected_doc"])
used_file= load_data("data/eval_candidates.json")
for f in used_file:
    used_id.add(f["expected_doc"])
new_chunks = []
for chunk in chunks:
    if chunk["doc_id"]  not in used_id:
        new_chunks.append(chunk)


sample = random.sample(new_chunks,25)


for chunk in sample:
    c_num+=1
    print("第{}/{}块".format(c_num,len(sample)))
    prompt = f"""下面是 FastAPI 中文文档的一段内容。请根据它出两道题，模拟用户可能会问的问题，答案必须能在这段内容里找到。

    要求：
    1. 第一道题可以使用原文里的关键词
    2. 第二道题意思相同，但尽量不用原文里的关键词，换成普通用户的说法
    3. 如果这段内容主要是代码、目录或没有实质信息，两道题都返回空字符串
    4. 只输出 JSON，不要输出任何其他文字，格式如下：
    {{"original": "第一道题", "paraphrase": "第二道题"}}

    文档内容：
    {chunk["text"]}
    """
    answer = ask_llm(prompt)
    try:
        item = json.loads(answer)
    except json.decoder.JSONDecodeError:
        count += 1
        continue

    if item["original"]:
        records.append({
            "question": item["original"],
            "expected_doc": chunk["doc_id"],
            "type": "原词",
            "source_chunk": chunk["chunk_id"],
        })
    if item["paraphrase"]:
        records.append({
            "question": item["paraphrase"],
            "expected_doc": chunk["doc_id"],
            "type": "换说法",
            "source_chunk": chunk["chunk_id"],
        })

print("生成了{}道题，跳过了{}块".format(len(records),count))
save_data(records, save_path)