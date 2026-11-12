# 读：data/dev_answers.json
# 写：无
# 预期：作答 36 道，抽 15 道
from ingest import load_data
import re
import random
random.seed(42)
s_data=[]
data = load_data("data/dev_answers.json")
chunks = load_data("data/chunks.json")
table={}
for chunk in chunks:
    table[chunk["chunk_id"]]=chunk["text"]
for d in data:
    if "文档中没有找到相关内容" in d["answer"]:
        continue
    s_data.append(d)
assert len(s_data) == 36
sample = random.sample(s_data, 15)

for item in sample:
    print(item["question"])
    print(item["answer"])
    nums = set()
    for x in re.findall(r"\[(\d+)\]", item["answer"]):
        nums.add(int(x))
    sorted_nums = sorted(nums)
    for n in sorted_nums:
        print(item["sources"][n - 1]["chunk_id"],n)
        print(table[item["sources"][n - 1]["chunk_id"]])

assert len(sample) == 15
