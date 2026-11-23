# Project Overview
Analyse customers, products and orders in Snowflake and produce insights.

Tables (database.schema: COCO_ANALYST.MY_TABLE):
- DIM_CUSTOMERS: one row per customer
- DIM_PRODUCTS: one row per product
- FCT_ORDER_LINES: one row per order line (raw fact table)
- V_VALID_ORDER_LINES: view over FCT_ORDER_LINES, COMPLETED orders only.
  Use this by default for all analysis.

# Rules
- Read-only: only SELECT / DESCRIBE / SHOW. Never run INSERT, UPDATE,
  DELETE, DROP, TRUNCATE, CREATE, ALTER or GRANT.
- Use warehouse SNOWFLAKE_LEARNING_WH; always add LIMIT when exploring.
- Never output raw PII. Columns listed as PII in the Data Dictionary must
  not appear in query results shown to the user or in reports. Aggregate,
  or identify customers by CUSTOMER_ID only.
- Never sum or average money across different currencies. Group by
  CURRENCY, or ask the user for a conversion rate.
- Save every query you run to sql/<skill>_<short_description>.sql.
- Write findings to reports/<topic>.md with the SQL used, assumptions
  and caveats.
- If a definition (churn, active, segment) is not in this file, state
  your assumption in the report instead of guessing silently.

# Custom Skills
- profile-table: first step for any new table
- customer-segmentation: RFM / value segments
- churn-analysis: retention and churn drivers

# Data Dictionary
## DIM_CUSTOMERS (one row per customer)
- Key: CUSTOMER_ID (VARCHAR). INDEX is a row number, not a key.
- PII, never output raw: FIRST_NAME, LAST_NAME, COMPANY, PHONE_1,
  PHONE_2, EMAIL, WEBSITE
- Safe to aggregate: CITY, COUNTRY, SUBSCRIPTION_DATE

## DIM_PRODUCTS (one row per product)
- Key: PRODUCT_ID
- PRICE is in CURRENCY; never sum or average across currencies.
- EAN is an identifier (text); never aggregate it.
- INTERNAL_ID and PRODUCT_DESCRIPTION: do not output.
- Groupable attributes: BRAND, CATEGORY, COLOR, SIZE, AVAILABILITY

## FCT_ORDER_LINES (one row per order line)
- Key: ORDER_LINE_ID. An order (ORDER_ID) has 1 to 4 lines.
- Joins: CUSTOMER_ID -> DIM_CUSTOMERS, PRODUCT_ID -> DIM_PRODUCTS
- Columns: ORDER_DATE, ORDER_STATUS (COMPLETED / CANCELLED / REFUNDED),
  QUANTITY, UNIT_PRICE, DISCOUNT_AMOUNT, LINE_AMOUNT, CURRENCY
- Amount: LINE_AMOUNT = QUANTITY * UNIT_PRICE - DISCOUNT_AMOUNT, in CURRENCY.
- Always analyse V_VALID_ORDER_LINES (COMPLETED only) unless the user
  asks about cancelled or refunded orders.
- Frequency = COUNT(DISTINCT ORDER_ID), not row count.
- Data is synthetic; do not present patterns as real business findings.

## Shared definitions
- Reference date: CURRENT_DATE()
- Customers with no valid orders: report as "No orders", do not drop them.
- New customer: first valid order within the last 30 days.
- Churn: no valid order in the last 90 days (customers with at least
  one valid order before that window).