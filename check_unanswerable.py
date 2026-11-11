from ingest import load_data
path='data/test_unanswerable.json'

questions=load_data(path)
count=0
null_count=0
result=set()
note_count=0
for item in questions:
    if item['expected_doc']is None:
        null_count+=1
    if item["type"] not in result:
        result.add(item["type"])
    if item["note"] !="":
        note_count+=1
    count+=1
print(result)#预期一个
print(null_count)#预期10
print(count)#预期10
print(note_count)#预期3

