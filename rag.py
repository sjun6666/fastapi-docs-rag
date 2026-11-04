from ingest import load_data
from bm25_search import build_index, search
from llm import ask_llm

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
def answer(question, bm25,chunks):

    results = search(question,bm25, chunks)
    prompt = build_prompt(question, results)
    reply = ask_llm(prompt)
    sources = []
    for r in results:
        sources.append(r["chunk_id"])
    return {"answer": reply, "sources": sources}
if __name__ == "__main__":
    chunks = load_data("data/chunks.json")
    bm25 = build_index(chunks)
    for q in ["怎么声明路径参数","前端调用接口被浏览器拦截了怎么办","Django 怎么配置数据库"]:
        print(answer(q, bm25, chunks))






