# Project Overview
Analyse the customer table in Snowflake and produce insights.
Table: COCO_ANALYST.MY_TABLE.DIM_CUSTOMERS

# Rules
- Read-only: only SELECT / DESCRIBE / SHOW. Never run INSERT, UPDATE, DELETE, DROP, TRUNCATE.
- Use warehouse SNOWFLAKE_LEARNING_WH; always add LIMIT when exploring.
- Never output raw PII (email, phone, name). Aggregate or mask.
- Save every query you run to sql/ with a descriptive filename.
- Write findings to reports/<topic>.md with the SQL used and caveats.

# Custom Skills
- profile-table: first step for any new table
- customer-segmentation: RFM / value segments
- churn-analysis: retention and churn drivers