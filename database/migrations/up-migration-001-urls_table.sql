CREATE TABLE urls (
    id                INTEGER PRIMARY KEY AUTO_INCREMENT,
    bucket            VARCHAR(1024) NOT NULL,
    object_key        VARCHAR(1024) NOT NULL,
    url               VARCHAR(2048) NOT NULL,
    created_at        DATETIME
);
