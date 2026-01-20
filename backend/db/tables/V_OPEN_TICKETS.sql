CREATE VIEW V_OPEN_TICKETS AS
SELECT
    t.ticket_id,
    t.subject,
    t.priority,
    t.status,
    COUNT(m.message_id) AS nb_messages,
    MAX(m.created_at) AS last_activity
FROM ZEN_TICKETS t
LEFT JOIN ZEN_MESSAGES m USING(ticket_id)
WHERE t.status != 'RESOLVED'
GROUP BY 1,2,3,4;