CREATE TABLE object_urls AS (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    bucket     VARCHAR(1024) NOT NULL,
    object     VARCHAR(1024) NOT NULL,
    url        VARCHAR(2048) NOT NULL,
    created_at TEXT
);