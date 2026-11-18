#读 data/eval_ambiguous.json  data/chunks/json
#写
#预期  所有文档都在

from ingest import load_data


data = load_data("data/eval_ambiguous.json")
chunks = load_data("data/chunks.json")

docs=set()
for chunk in chunks:
    docs.add(chunk["doc_id"])
count=0
for d in data:
    missing=False
    for item in d["expected_docs"]:
        if item not in docs:
            print(item)
            missing=True
    if not missing:
        count+=1

assert count==8
assert len(data) == 8
print("ok")