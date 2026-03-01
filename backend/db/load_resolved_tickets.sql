-- Script to load RESOLVED_TICKETS data from CSV
-- 
-- Prerequisites:
-- 1. The RESOLVED_TICKETS table must exist
-- 2. The CSV file must be uploaded to a Snowflake stage
--
-- Usage:
-- Option 1: If CSV is already in a stage:
--   Replace @your_stage_name with your actual stage name
--
-- Option 2: Upload CSV file first using SnowSQL or Snowflake UI:
--   PUT file:///path/to/aa_dataset-tickets-multi-lang-5-2-50-version.csv @~/staged;

-- Create a file format for CSV with headers
CREATE OR REPLACE FILE FORMAT csv_format
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
ESCAPE_UNENCLOSED_FIELD = NONE
ENCODING = 'UTF8'
NULL_IF = ('', 'NULL');

-- Option 1: Load from user stage (after using PUT command)
-- COPY INTO RESOLVED_TICKETS
-- FROM @~/staged/aa_dataset-tickets-multi-lang-5-2-50-version.csv
-- FILE_FORMAT = csv_format
-- ON_ERROR = 'CONTINUE'
-- PURGE = FALSE;

-- Option 2: Load from internal named stage
-- First create a stage if it doesn't exist:
-- CREATE STAGE IF NOT EXISTS data_stage;
-- 
-- Then upload the file using SnowSQL:
-- PUT file:///path/to/aa_dataset-tickets-multi-lang-5-2-50-version.csv @data_stage;
--
-- Then load:
-- COPY INTO RESOLVED_TICKETS
-- FROM @data_stage/aa_dataset-tickets-multi-lang-5-2-50-version.csv
-- FILE_FORMAT = csv_format
-- ON_ERROR = 'CONTINUE';

-- Option 3: Load from external stage (S3, Azure, GCS)
-- COPY INTO RESOLVED_TICKETS
-- FROM 's3://your-bucket/path/to/aa_dataset-tickets-multi-lang-5-2-50-version.csv'
-- CREDENTIALS = (AWS_KEY_ID='your_key' AWS_SECRET_KEY='your_secret')
-- FILE_FORMAT = csv_format
-- ON_ERROR = 'CONTINUE';

-- Verify the data was loaded
-- SELECT COUNT(*) as total_records FROM RESOLVED_TICKETS;
-- SELECT * FROM RESOLVED_TICKETS LIMIT 5;
