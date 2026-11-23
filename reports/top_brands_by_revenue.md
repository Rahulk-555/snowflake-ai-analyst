# Top 10 brands by revenue, per currency

Only one currency exists in the data: USD (all statuses). Total completed revenue: 19,451,703.10 USD across 8,046 brands.

| Rank | Brand | Revenue (USD) | Orders | Units |
|---|---|---|---|---|
| 1 | Petersen Group | 18,962.40 | 9 | 23 |
| 2 | Hull, Shields and Walsh | 18,334.80 | 7 | 20 |
| 3 | Weeks Inc | 17,857.10 | 11 | 25 |
| 4 | Kline Group | 16,602.60 | 12 | 26 |
| 5 | Proctor Ltd | 16,554.00 | 7 | 18 |
| 6 | Lloyd Ltd | 16,051.30 | 9 | 21 |
| 7 | Brady PLC | 15,758.60 | 10 | 21 |
| 8 | Villanueva Ltd | 15,676.60 | 10 | 19 |
| 9 | Wood and Sons | 15,449.00 | 8 | 16 |
| 10 | Kennedy PLC | 15,196.90 | 11 | 23 |

## SQL
See sql/explore_top_brands_by_revenue.sql

## Assumptions and caveats
- Revenue = SUM(LINE_AMOUNT) (net of discounts) from V_VALID_ORDER_LINES (COMPLETED only).
- Grouped by order-line CURRENCY; product currency matches order currency on all lines.
- All order lines joined to a product (no unmatched lines).
- Revenue is extremely fragmented: 8,046 brands, top brand = ~0.1% of revenue. Ranking differences are tiny and driven by a handful of orders.
- Brand names look like generated company names; data is synthetic, not real business findings.
