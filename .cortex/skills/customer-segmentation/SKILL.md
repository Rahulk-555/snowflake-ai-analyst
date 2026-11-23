---
name: customer-segmentation
description: Segment customers by value and behaviour (RFM). Use when asked about customer segments, top customers or revenue concentration.
---

# Inputs
Use the Data Dictionary in AGENTS.md. Source for orders is
COCO_ANALYST.MY_TABLE.V_VALID_ORDER_LINES (customer id = CUSTOMER_ID,
date = ORDER_DATE, order id = ORDER_ID, amount = LINE_AMOUNT,
currency = CURRENCY). Customer list comes from DIM_CUSTOMERS.
Only ask the user if one of these objects is missing or has changed.

# Steps
1. Run DESCRIBE TABLE / DESCRIBE VIEW on V_VALID_ORDER_LINES and
   DIM_CUSTOMERS and confirm the columns above exist.
2. Check currencies: SELECT CURRENCY, SUM(LINE_AMOUNT), COUNT(*) GROUP BY
   CURRENCY. If more than one currency exists, ask the user which one to
   analyse or for a conversion rate. If no answer is available, use the
   currency with the highest revenue and state which lines were excluded.
   Never sum across currencies.
3. Per customer, compute from the valid order lines (in the chosen currency):
   - Recency = days from CURRENT_DATE() to the last ORDER_DATE
   - Frequency = COUNT(DISTINCT ORDER_ID)
   - Monetary = SUM(LINE_AMOUNT)
   - First order date = MIN(ORDER_DATE)
4. Score each metric 1-5 with NTILE(5). Order Recency so fewer days = 5;
   order Frequency and Monetary so higher = 5. Add CUSTOMER_ID to the
   ORDER BY to break ties deterministically.
5. Assign segments, first match wins:
   - New: first order within the last 30 days
   - Champions: R >= 4 and F >= 4
   - Loyal: R >= 3 and F >= 3
   - At Risk: R <= 2 and F >= 3
   - Lost: R <= 2 and F <= 2
   - Other: everyone else with orders
   Then LEFT JOIN DIM_CUSTOMERS and label customers with no valid
   orders as "No orders".
6. Report per segment: customer count, revenue, % of total revenue
   (denominator = revenue of all valid orders in scope), and optionally
   average Recency/Frequency/Monetary. Segment counts, including
   "No orders", must sum to the total customers in DIM_CUSTOMERS; flag
   it if they don't.
7. Optionally break segments down by COUNTRY (aggregate only).
8. Save SQL to sql/customer_segmentation_<short_description>.sql and
   findings to reports/customer_segmentation.md.

# Rules
- SELECT only. Use LIMIT when previewing rows.
- Never output PII columns listed in AGENTS.md (names, company, emails,
  phones, website). Identify customers by CUSTOMER_ID only.
- Never sum or average money across currencies.
- End the report with assumptions and caveats: chosen currency and any
  excluded lines, reference date, segment thresholds, tie handling,
  customers with no orders, and that the data is synthetic.