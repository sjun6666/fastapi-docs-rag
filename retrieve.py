import json


def load_json(filename):
    with open(filename, encoding="utf-8") as json_file:
        return json.load(json_file)

def retrieve_documents(query, documents):
    worry = []
    for document in documents:
        for keyword in document["keywords"]:
            if keyword.lower() in query.lower():
                worry.append(document)
                break
    return worry

documents = load_json("data/documents.json")
print(retrieve_documents("params和timeout分别做什么？", documents))
print(retrieve_documents("北京今天的天气如何？", documents))
print(retrieve_documents("params怎么传查询参数？", documents))