
CREATE TABLE qa_history (
    id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    refused INT NOT NULL,
    status INT NOT NULL,
    error TEXT
    );

CREATE TABLE qa_sources(
    qa_id INTEGER NOT NULL REFERENCES qa_history(id),
    rank INT NOT NULL,
    chunk_id TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    PRIMARY KEY (qa_id, rank)
    );
