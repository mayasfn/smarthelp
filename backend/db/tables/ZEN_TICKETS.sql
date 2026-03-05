CREATE TABLE ZEN_TICKETS IF NOT EXISTS (
    ticket_id STRING,
    user STRING,
    subject STRING,
    priority STRING,
    type STRING,
    queue STRING,
    status STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);