CREATE TABLE ZEN_MESSAGES (
    message_id STRING,
    ticket_id STRING,
    sender_role STRING,   -- USER / AGENT_AI / AGENT_HUMAN
    content STRING,
    created_at TIMESTAMP
);