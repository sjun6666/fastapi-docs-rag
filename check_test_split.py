from ingest import load_data

count=0
c_num=0
records = []
used_id=set()
used_file= load_data("data/eval_questions.json")
chunks = load_data("data/chunks.json")
for f in used_file:
    used_id.add(f["expected_doc"])
used_file= load_data("data/eval_candidates.json")
for f in used_file:
    used_id.add(f["expected_doc"])
used_file= load_data("data/eval_candidates2.json")
for f in used_file:
    used_id.add(f["expected_doc"])
new_chunks = []
for chunk in chunks:
    if chunk["doc_id"]  not in used_id:
        new_chunks.append(chunk)

print("排除的文档数：", len(used_id))#30
print("全部块数：", len(chunks))#1093
print("剩下的块数：", len(new_chunks))#700