# Customers with no orders

## Findings
- Total customers: 10,000
- No valid (COMPLETED) orders: 4,719 (47.2%) -> reported as "No orders"
- No orders of any status: 4,385 (43.9%)
- 334 customers placed orders, but all of them were CANCELLED or REFUNDED

## SQL
See sql/explore_customers_no_orders.sql

## Assumptions and caveats
- "Not placed any orders" = no rows in V_VALID_ORDER_LINES (COMPLETED only), per AGENTS.md. Any-status count shown for comparison.
- Customers identified by CUSTOMER_ID only; no PII output.
- Data is synthetic; not a real business finding.
