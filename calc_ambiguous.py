#读 data/ambiguous_answers.json
#写 无
#预期检索覆盖 23 / 23
#回答覆盖 15 / 23
#拒答 3 / 8
from ingest import load_data
import re
data = load_data("data/ambiguous_answers.json")
refused=0
RC_count=0
AC_count=0
for d in data:
    is_refused=False
    if "文档中没有找到相关内容" in d["answer"]:
        refused+=1
        is_refused=True

    sources_doc_id=set()
    expected_doc = set(d["expected_docs"])
    for x in d["sources"]:
        sources_doc_id.add(x["doc_id"])
    RC=sources_doc_id & expected_doc
    RC_count+=len(RC)
    nums=set()
    for x in re.findall(r"\[(\d+)\]", d["answer"]):
        nums.add(int(x))
    answer_doc=set()
    for n in nums:
        if n in range(1, 6):  # 越界：n 不在 1 到 5 之间
            answer_doc.add(d["sources"][n - 1]["doc_id"])
    AC=answer_doc & expected_doc
    AC_count+=len(AC)
    print("question", d["question"],
          "refused:", is_refused,
          "RC",len(RC)/len(expected_doc),
          "AC",len(AC)/len(expected_doc))

assert sum(len(r["expected_docs"]) for r in data)==23
print(RC_count,AC_count, refused)


