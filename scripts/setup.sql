-- Setup script for the Hello Snowflake! application.
CREATE APPLICATION ROLE app_public;
CREATE SCHEMA IF NOT EXISTS core;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;

  
GRANT USAGE ON PROCEDURE core.hello() TO APPLICATION ROLE app_public;

CREATE OR ALTER VERSIONED SCHEMA code_schema;
GRANT USAGE ON SCHEMA code_schema TO APPLICATION ROLE app_public;

CREATE VIEW IF NOT EXISTS code_schema.fund_view
  AS SELECT *
  FROM fund_data.mutual_fund_details;
GRANT SELECT ON VIEW code_schema.fund_view TO APPLICATION ROLE app_public;

CREATE STREAMLIT code_schema.fund_streamlit
  FROM '/streamlit'
  MAIN_FILE = '/fund_analyzer.py'
;

GRANT USAGE ON STREAMLIT code_schema.fund_streamlit TO APPLICATION ROLE app_public;