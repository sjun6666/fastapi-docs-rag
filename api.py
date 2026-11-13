# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from ingest import load_data
from vector_search import get_vectors
from sentence_transformers import SentenceTransformer
from fastapi import HTTPException
from rag import answer
app = FastAPI()
model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
chunks = load_data("data/chunks.json")
vectors = get_vectors(chunks, model)
table = {}
for c in chunks:
    table[c["chunk_id"]] = c["doc_id"]
class AskRequest(BaseModel):     # 请求体长什么样
    question: str

@app.post("/ask")                # POST 方法，路径 /ask
def ask(req: AskRequest):        # FastAPI 自动把请求体解析成 AskRequest
    question = req.question.strip()
    if question == "":
        raise HTTPException(status_code=400, detail="请检查输入文本")
    try:
        result =  answer(question, model, vectors, chunks)
        refuse=False
        sources=[]
        if "文档中没有找到相关内容" in result["answer"]:
            refuse =True
        for cid in result["sources"]:
            sources.append({"chunk_id": cid, "doc_id": table[cid]})


    except RuntimeError as e:
        raise HTTPException(status_code=502, detail="模型服务调用失败")
    return {"question": question, "answer": result["answer"], "sources": sources, "refused": refuse}