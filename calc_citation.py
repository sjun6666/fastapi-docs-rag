from ingest import load_data
import re
data = load_data("data/dev_answers.json")
chunks=load_data("data/chunks.json")
table={}
for chunk in chunks:
    table[chunk["chunk_id"]]=chunk

refuse_count = 0
out_count = 0
all_count=0
cite_hit = 0
ns_count = 0
answered =0
error_count=0
wrong_refuse=0
for record in data:
    text = record["answer"]
    if "文档中没有找到相关内容" in text:
        refuse_count += 1
        found = False
        for item in record["sources"]:

            if item["doc_id"]==record["expected_doc"]:
                print(item["chunk_id"])
                print(table[item["chunk_id"]]["text"])
                found=True

        if found:
            error_count+=1
            print("误拒",record["question"])
        else:
            wrong_refuse+=1
        continue
    answered += 1
    nums = set()
    for x in re.findall(r"\[(\d+)\]", text):
        nums.add(int(x))
    if len(nums) == 0:
        ns_count += 1


        continue
    for n in nums:
        if n not in range(1,6):                 # 越界：n 不在 1 到 5 之间
            out_count += 1
        else:
            all_count += 1
            if record["sources"][n - 1]["doc_id"]==record["expected_doc"]:             # 命中：第 n 块的 doc_id 等于这道题的 expected_doc
                cite_hit += 1

print("拒答题数：",refuse_count)
print("作答题数",answered)
print("无引用作答题",ns_count)
print("越界引用数字",out_count)
if all_count > 0:
    print("引用文档命中率",cite_hit/all_count)
    print(all_count)
    print(cite_hit)
print("误拒",error_count)#8
print("合理拒答",wrong_refuse)#7