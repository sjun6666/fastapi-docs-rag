# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from ingest import load_data
from vector_search import get_vectors
from sentence_transformers import SentenceTransformer
from fastapi import HTTPException
from rag import answer
import requests
import time
import logging, os
os.makedirs("logs", exist_ok=True)       # 目录不存在就建一个
logging.basicConfig(
    filename="logs/app.log", level=logging.WARNING, encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("api")
logger.setLevel(logging.INFO)

 # exc_info=True 会把 traceback 一起写进去
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
    docs = []
    if question == "":
        logger.warning(f"status=400 , reason=问题为空 q={question!r}")
        raise HTTPException(status_code=400,detail="请检查输入文本")
    try:
        start = time.perf_counter()
        result =  answer(question, model, vectors, chunks)
        ms = int((time.perf_counter() - start)*1000)
        refuse=False
        sources=[]
        if "文档中没有找到相关内容" in result["answer"]:
            refuse =True
        for cid in result["sources"]:
            docs.append(table[cid])
            sources.append({"chunk_id": cid, "doc_id": table[cid]})


    except (RuntimeError, requests.HTTPError) as e:
        logger.error(f"status=502,reason={e},q={question!r}",exc_info=True)
        raise HTTPException(status_code=502, detail="模型服务调用失败")
    logger.info(f"status=200 q={question!r},ms={ms},refuse={refuse},docs={docs}")
    return {"question": question, "answer": result["answer"], "sources": sources, "refused": refuse}