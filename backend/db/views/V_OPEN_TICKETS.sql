CREATE OR REPLACE VIEW V_OPEN_TICKETS AS
SELECT
    t.ticket_id,
    t.subject,
    t.priority,
    t.type,
    t.queue,
    t.status,
    COUNT(m.message_id) AS nb_messages,
    MAX(m.created_at) AS last_activity
FROM ZEN_TICKETS t
LEFT JOIN ZEN_MESSAGES m USING(ticket_id)
WHERE t.status != 'RESOLVED'
GROUP BY 1,2,3,4,5,6
ORDER BY last_activity DESC;