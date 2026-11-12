---
name: customer-segmentation
description: Segment customers by value and behaviour (RFM). Use when asked about customer segments, top customers or revenue concentration.
---

# Inputs
Ask the user for the table name and the columns for customer id, order/transaction date and amount if not in AGENTS.md.

# Steps
1. Confirm the columns exist with DESCRIBE TABLE.
2. Compute Recency, Frequency, Monetary per customer.
3. Score each 1-5 using NTILE(5).
4. Label segments: Champions, Loyal, At Risk, Lost, New.
5. Report customer count, revenue and % of total revenue per segment.
6. Save SQL to sql/segmentation.sql and findings to reports/segmentation.md.

# Rules
- SELECT only. Use LIMIT when previewing rows.
- Never output names, emails or phone numbers; use customer IDs only.
- State assumptions and data caveats at the end of the report.