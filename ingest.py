from pathlib import Path
import json
def load_markdown_files(folder):
    data = []
    for file in sorted(Path(folder).rglob("*.md")):
        text = file.read_text(encoding="utf-8")
        doc_id = file.relative_to(folder).as_posix()
        if file.name.startswith("_"):
            continue
        elif len(text) < 100:
            continue
        else:
            doc = {
                "text": text,
                "doc_id": doc_id,
            }
            data.append(doc)
    return data
def split_into_chunks(doc, max_chars=500, overlap=100):
    start = 0
    text=doc["text"]
    doc_id = doc["doc_id"]
    chunks=[]
    while True:
        chunk={
            "chunk_id":f"{doc_id}#{len(chunks)}",
            "doc_id": doc_id,
            "text": text[start:start + max_chars],
        }
        chunks.append(chunk)
        if start+max_chars >= len(text):
            break
        start = start + max_chars - overlap
    return chunks
def save_data(data,path):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False, indent=2)
def load_data(path):
    with open(path,"r",encoding="utf-8") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    data2 = load_markdown_files("data/raw/fastapi_zh")
    path = "data/chunks.json"
    all_chunks = []
    counter = 0
    for doc in data2:
        chunks = split_into_chunks(doc)
        all_chunks.extend(chunks)
    for chunk in all_chunks:
        chunk_len = len(chunk["text"])
        counter += chunk_len
    save_data(all_chunks,path)
    data3 = load_data(path)
    print(len(data3))
    print(counter/len(all_chunks))
    print(len(data3)==len(all_chunks))



