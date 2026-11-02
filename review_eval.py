from ingest import load_data
data = load_data("data/eval_candidates.json")
chunks = load_data("data/chunks.json")
table={}

for chunk in chunks:
    table[chunk["chunk_id"]] = chunk
for i,q in enumerate(data,start=1):
    if q["source_chunk"] in table:
        table[q["source_chunk"]]["text"][:300]
        pass_question={
            "序号":i,
            "类型":q["type"],
            "问题":q["question"]
        }
        print(pass_question)

