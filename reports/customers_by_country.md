# Customers by Country

Source: `COCO_ANALYST.MY_TABLE.DIM_CUSTOMERS`

## Findings
- 243 distinct countries. Every country has a customer count between 26 and 84.
- Top 5: Korea (84), Congo (81), Vanuatu (58), Sierra Leone (56), then a five-way tie at 54 (Cote d'Ivoire, Montenegro, US Virgin Islands, Mauritius, Andorra).
- Bottom: Palestinian Territory, Antarctica, Mayotte and New Caledonia (26 each).
- Most countries have 30 to 50 customers. That fairly even spread suggests the data is synthetic.

## SQL
See `sql/customers_by_country.sql`.

## Caveats
- The row count equals the distinct CUSTOMER_ID count in every country, so there are no duplicate customers per country.
- Country values are not normalised. "Korea" and "Congo" are ambiguous, since each can refer to two countries, which may explain why they have the highest counts.
