CREATE TABLE urls (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    bucket     VARCHAR(1024) NOT NULL,
    key        VARCHAR(1024) NOT NULL,
    url        VARCHAR(2048) NOT NULL,
    created_at DATETIME
);
