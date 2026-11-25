import sqlite3
from history import init_db,save_record,list_records
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
def make_db():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    save_record(conn,"问题1","回答1",0,200,None,SOURCES)
    save_record(conn,"问题2","回答2",0,200,None,SOURCES)
    save_record(conn,"问题3","文档中没有找到相关内容",1,200,None,SOURCES)
    return conn
def test_list_order():
    conn = make_db()
    row = list_records(conn)
    assert len(row) == 3
    assert row[0]["question"] == "问题3"
def test_list_refused():
    conn = make_db()
    row = list_records(conn,refused=1)
    assert len(row) == 1
    assert row[0]["question"]=="问题3"
    row = list_records(conn,refused=0)
    assert len(row) == 2
    assert row[0]["question"]=="问题2"
    assert row[1]["question"]=="问题1"
def test_list_limit():
    conn = make_db()
    rows = list_records(conn,limit=2)
    assert len(rows) == 2
    assert rows[0]["question"]=="问题3"
    assert rows[1]["question"]=="问题2"
