from ingest import save_data,load_data
candidates = load_data("data/eval_candidates.json")
questions = load_data("data/eval_questions.json")
existing = set()
for q in questions:
    existing.add(q["question"])


drop_ids={5,6,9,10,11,12,20,24,25,26,30,31,32,33,34,35,36}
added=0
for i,x in enumerate(candidates,start=1):
    if i in drop_ids:
        continue
    if x["question"] in existing:
        continue

    new_data={
        "question":x["question"],
        "expected_doc":x["expected_doc"],
        "type":x["type"],
    }
    questions.append(new_data)
    added += 1
save_data(questions, "data/eval_questions.json")
print("新加了", added, "题，现在共", len(questions), "题")

