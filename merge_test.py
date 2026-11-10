from ingest import save_data,load_data
import os
import sys
candidates = load_data("data/test_candidates.json")
#questions = load_data("data/eval_questions.json")
save_path="data/test_questions.json"
if os.path.exists(save_path):
    print(f"{save_path} 已存在，不覆盖。要重新生成请先手动删除或改名。")
    sys.exit()
used_id = set()
for path in ["data/eval_questions.json", "data/eval_candidates.json", "data/eval_candidates2.json"]:
    for q in load_data(path):
        used_id.add(q["expected_doc"])
questions =  []
keep_ids = {3,4, 9,10 ,13,14 , 17,18 , 19,20 , 23,24,  25,26 , 29,30  ,33,34,
37,38 , 45,46,  47,48 , 51,52 , 53,54,  55,56  ,57,58,  59,60 , 65,66}
added=0
for i,x in enumerate(candidates,start=1):
    if i not in keep_ids:
        continue
    if x["expected_doc"] in used_id:
        print("警告：与开发集重叠", i, x["expected_doc"])
    new_data={
        "question":x["question"],
        "expected_doc":x["expected_doc"],
        "type":x["type"],
    }
    questions.append(new_data)
    added += 1
save_data(questions, save_path)
print("新加了", added, "题，现在共",len(questions), "题")

