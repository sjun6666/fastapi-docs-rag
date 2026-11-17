#读 test_candidates.json，test_questions.json
#写
#预期：36 道全部查到

from ingest import load_data


test_c = load_data("data/test_candidates.json")
table={}
for q in test_c:
    table[q["question"]]=q["source_chunk"]
count=0
u_count=0
test_q=load_data("data/test_questions.json")
for q in test_q:
    if q["question"] in table:
        count+=1
        print(table[q["question"]])
    else:
        u_count+=1

assert count==36
print("ok")