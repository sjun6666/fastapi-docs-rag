import sqlite3
from history import init_db,save_record
SOURCES = [{"chunk_id": f"a.md#{i}", "doc_id": "a.md"} for i in range(5)]
def test_normal():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    qa_id = save_record(conn,"什么是依赖注入","ok",0,200,None,SOURCES)
    row = conn.execute("SELECT question,answer, refused, status, error FROM qa_history WHERE id = ?",(qa_id,)).fetchone()
    assert row ==("什么是依赖注入","ok",0,200,None,)
    ranks = conn.execute(
        "SELECT rank FROM qa_sources WHERE qa_id = ? ORDER BY rank",(qa_id,)).fetchall()

    assert ranks ==[(1,),(2,),(3,),(4,),(5,)]
def test_refused():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    qa_id1 = save_record(conn,"在 FastAPI 中使用 mamba","文档中没有找到相关内容",1,200,None, SOURCES)
    row1 = conn.execute("SELECT question,answer,refused,status,error FROM qa_history WHERE id = ?",(qa_id1,)).fetchone()
    assert row1 ==("在 FastAPI 中使用 mamba","文档中没有找到相关内容",1,200,None)
    ranks1 = conn.execute(
        "SELECT rank FROM qa_sources WHERE qa_id = ? ORDER BY rank",(qa_id1,)).fetchall()

    assert ranks1 ==[(1,),(2,),(3,),(4,),(5,)]
def test_error():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    qa_id2 = save_record(conn,"什么是依赖注入",None,0,502,"上游调用失败",[])
    row2 = conn.execute("SELECT question,answer,refused,status,error FROM qa_history WHERE id = ?",(qa_id2,)).fetchone()
    assert row2 == ("什么是依赖注入", None, 0, 502, "上游调用失败")
    ranks2 = conn.execute("SELECT COUNT(*) FROM qa_sources WHERE qa_id = ?",(qa_id2,)).fetchone()[0]
    assert ranks2==0