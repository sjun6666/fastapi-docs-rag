#读"data/dev_answers.json"
#写：无
#预期 count=4


from ingest import load_data



data = load_data("data/dev_answers.json")

phrases = ["资料中没有", "没有给出", "未提及", "没有提到","没有明确","未说明","并未"]
count = 0
for record in data:
    if "文档中没有找到相关内容" in record["answer"]:
        continue
    result=False
    for phrase in phrases:
        if phrase in record["answer"]:
            result=True
    if result:
        count += 1
        print(record["question"])
print(count)# 实际：1

