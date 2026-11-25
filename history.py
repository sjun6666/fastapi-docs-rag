import sqlite3
from datetime import datetime
def init_db(conn):
    with open("docs/schema.sql",encoding="utf-8") as file:
        conn.executescript(file.read())

def save_record(conn, question, answer, refused, status, error, sources):
    created_at = datetime.now().isoformat(timespec="seconds")
    try:
        cursor = conn.execute("INSERT INTO qa_history (created_at, question, answer, refused, status, error) VALUES (?,?,?,?,?,?)",(created_at, question, answer, refused, status, error))

        qa_id = cursor.lastrowid

        for rank,source in enumerate(sources, start=1):
            conn.execute(
                "INSERT INTO qa_sources(chunk_id, doc_id,qa_id,rank) VALUES (?,?,?,?)",(source["chunk_id"], source["doc_id"], qa_id, rank)
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return qa_id

def list_records(conn, limit=10, refused=None):
    cols = ["id", "created_at", "question", "answer", "refused", "status", "error"]
    sql = "SELECT id, created_at, question, answer, refused, status, error FROM qa_history"
    params = []
    if refused is not None:
        sql += " WHERE refused=?"                 # 拼上 WHERE 条件
        params.append(refused)         # refused 为 True 放 1，为 False 放 0
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    records = []
    for row in rows:
        d = dict(zip(cols, row))
        d["refused"] = bool(d["refused"])  # 1 → True，0 → False
        records.append(d)
    return records  # 每一行都转成字典

