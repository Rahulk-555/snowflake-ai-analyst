# Loyal Customers – Tenure-Based Segmentation

Table: `COCO_ANALYST.MY_TABLE.DIM_CUSTOMERS` (10,000 customers)
SQL: `sql/segmentation.sql`

## Method
No transaction data exists, so RFM was not possible. Loyalty is proxied by tenure:
customers are split into 5 equal groups (NTILE) by `SUBSCRIPTION_DATE`; the oldest 20% are "Loyal".

## Segments
| Score | Segment | Customers | % | Subscribed between | Avg tenure (days) |
|---|---|---|---|---|---|
| 5 | Loyal (longest tenure) | 2,000 | 20% | 2020-01-01 – 2020-06-27 | 2,417 |
| 4 | Established | 2,000 | 20% | 2020-06-27 – 2020-12-14 | 2,243 |
| 3 | Mid | 2,000 | 20% | 2020-12-15 – 2021-06-11 | 2,070 |
| 2 | Recent | 2,000 | 20% | 2021-06-12 – 2021-12-04 | 1,890 |
| 1 | New | 2,000 | 20% | 2021-12-04 – 2022-05-29 | 1,717 |

## Loyal segment – top countries
Congo 20, Mauritius 19, Andorra 18, Cayman Islands / Burkina Faso / Netherlands / French Guiana / Bouvet Island 14 each, Korea / Jordan 13 each.
Spread is very even (no country >1% of the segment).

## Longest-tenured customers (subscribed 2020-01-01, IDs only)
0b8CfA0897d2C01, 11D5aeDE5C4Cb7C, 28D7BcC82d076F2, 4BED16854D39FaB, 4d41c0F3D0f7Ea0,
60C9aDD9699DFa2, 7d3FA7522B4fc29, 81EcdBEd03Bda27, 94cceEcfd1Bdde8, C0C4e62eD1C8Aa2

## Caveats
- Tenure ≠ loyalty: there is no purchase, activity or churn/cancellation data, so a long-tenured customer may be inactive.
- No revenue column, so revenue / % of revenue per segment (skill step 5) cannot be reported.
- Subscription dates are evenly spread from 2020-01 to 2022-05 and countries look uniformly distributed, which suggests synthetic data.
- Quintile boundaries break ties arbitrarily (e.g. 2020-06-27 falls in two segments).
- No PII is included; names, emails and phones were excluded.
