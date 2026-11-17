#读 data/test_answers.json
#写
#预期 文档级 Hit@5：28/36
#块级 Hit@5：28/36
#拒答：8/36，其中误拒 3
#引用文档命中率：80%
#无答案题拒答：10/10

from ingest import load_data
import re
data = load_data("data/test_answers.json")

def calc(records):
    # 在这里：初始化 6 个计数器（文档命中、块命中、拒答、误拒、引用数、引用命中）
    file_right=0
    block_count = 0
    refused = 0
    error_refused = 0
    ok_refused = 0
    answered=0
    ns_count = 0
    all_count = 0
    cite_hit = 0
    for item in records:
        if any(r["doc_id"]==item["expected_doc"]for r in item["sources"] ):
            file_right+=1
        if any(r["chunk_id"]==item["source_chunk"] for r in item["sources"]):
            block_count+=1
        if "文档中没有找到相关内容" in item["answer"]:
            refused+=1
            found=False
            if any(r["doc_id"]==item["expected_doc"]for r in item["sources"] ):
                found=True
            if found:
                error_refused+=1
            else:
                ok_refused+=1
            continue
        answered += 1
        nums = set()
        for x in re.findall(r"\[(\d+)\]", item["answer"]):
            nums.add(int(x))
        if len(nums) == 0:
            ns_count += 1

            continue
        for n in nums:
            if n in range(1, 6):  # 越界：n 不在 1 到 5 之间
                all_count += 1
                if item["sources"][n - 1]["doc_id"] == item["expected_doc"]:  # 命中：第 n 块的 doc_id 等于这道题的 expected_doc
                    cite_hit += 1
    return {"题数": len(records),
            "文档命中": file_right,
            "块命中": block_count,
            "拒答":refused,
            "误拒：":error_refused,
            "正确拒绝":ok_refused,
            "引用文档命中率":cite_hit/all_count,
            "cite_hit":cite_hit,
            "all_count":all_count,
            }

answerable = [r for r in data if r["answerable"]]
or_answerable = [r for r in answerable if r["type"] == "原词"]
change_answerable = [r for r in answerable if r["type"] == "换说法"]
print(calc(answerable))
print(calc(or_answerable))
print(calc(change_answerable))
unanswerable = [r for r in data if not r["answerable"]]
count=0
for r in unanswerable:
    if "文档中没有找到相关内容" in r["answer"]:
        count+=1
print("无答案题拒答",count,"/",len(unanswerable))