from pathlib import Path
def load_markdown_files(folder):
    data = []
    for file in sorted(Path(folder).rglob("*.md")):
        text = file.read_text(encoding="utf-8")
        doc_id = file.relative_to(folder).as_posix()
        if doc_id.startswith("_"):
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

if __name__ == "__main__":
    data2 = load_markdown_files("data/raw/fastapi_zh")
    print(len(data2))
    print(data2[0]["doc_id"])



