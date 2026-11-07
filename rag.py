from ingest import load_data
import time
from llm import ask_llm
from vector_search import vector_search,get_vectors
from sentence_transformers import SentenceTransformer

def build_prompt(question, results):
    q_r_list=[]
    for i,result in enumerate(results,start=1):
        part = f"[{i}] 来源：{result['doc_id']}\n{result['text']}"
        q_r_list.append(part)
    context = "\n\n".join(q_r_list)
    prompt = f"""你是 FastAPI 文档问答助手。请只根据下面的资料回答问题。

    要求：
    1. 只使用资料里的信息，不要使用你自己的知识
    2. 每个说法后面用 [编号] 标出依据的资料，比如 [1]、[2]
    3. 如果资料里没有能回答问题的内容，只回答：文档中没有找到相关内容
    4. 用中文回答，简洁清楚

    资料：
    {context}

    问题：{question}
    """
    return prompt


def answer(question, model, vectors, chunks):
    results = vector_search(question, model, vectors, chunks)
    prompt = build_prompt(question, results)
    reply = ask_llm(prompt)
    sources = []
    for r in results:
        sources.append(r["chunk_id"])
    return {"answer": reply, "sources": sources}


if __name__ == "__main__":
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

    chunks = load_data("data/chunks.json")
    vectors = get_vectors(chunks, model)

    questions=["response_model_exclude_unset 有什么作用？","网址问号后面的参数怎么读取","Django 怎么配置数据库"]
    for q in questions:
        print(answer(q, model, vectors, chunks))






