CREATE OR REPLACE CORTEX SEARCH SERVICE RESOLVED_TICKETS_SEARCH
ON BODY_ANSWER
ATTRIBUTES
    SUBJECT,
    TYPE,
    QUEUE,
    PRIORITY,
    LANGUAGE,
    VERSION,
    BODY_ANSWER
WAREHOUSE = COMPUTE_WH
TARGET_LAG = '1 hour'
EMBEDDING_MODEL = 'snowflake-arctic-embed-m-v1.5'
REFRESH_MODE = INCREMENTAL
AS
SELECT
    SUBJECT,
    TYPE,
    QUEUE,
    PRIORITY,
    LANGUAGE,
    VERSION,

    /* Structured semantic field */
    CONCAT(
        'Customer issue: ', BODY, '. ',
        'Resolution provided: ', ANSWER, '. ',
        'Tags: ',
        CONCAT_WS(', ',
            TAG_1, TAG_2, TAG_3, TAG_4,
            TAG_5, TAG_6, TAG_7, TAG_8
        )
    ) AS BODY_ANSWER

FROM RESOLVED_TICKETS;