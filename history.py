import sqlite3
from datetime import datetime
def init_db(conn):
    with open("docs/schema.sql",encoding="utf-8") as file:
        conn.executescript(file.read())

def save_record(conn, question, answer, refused, status, error, sources):
    created_at = datetime.now().isoformat()
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
