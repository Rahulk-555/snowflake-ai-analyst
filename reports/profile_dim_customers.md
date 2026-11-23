# Profile: DIM_CUSTOMERS

## Summary
10,000 rows, 12 columns. Structurally clean: no nulls/blanks, no duplicate keys, consistent formats.
Main issue: subscription dates stop at 2022-05-29 (~4.5 years before reference date 2026-11-23).

## Keys and duplicates
- CUSTOMER_ID: 10,000 distinct of 10,000 (also unique after trim/lower-case); fixed length 15, no whitespace.
- INDEX: 1..10,000, unique (row number, not a key).
- EMAIL: 10,000 distinct; no duplicate (first name, last name, company) combinations.
- No constraints declared (all columns nullable, no PK) - uniqueness holds today but is not enforced.

## Nulls
0% null or blank in every column.

## SUBSCRIPTION_DATE
- Range 2020-01-01 to 2022-05-29; no future dates, no pre-2000 dates.
- 2020: 4,212 (every day covered), 2021: 4,125 (every day), 2022: 1,663 (Jan 1 - May 29).
- ~11-12 signups/day, flat, incl. weekends (2,839 = 28.4% weekend, ~ calendar share).
- ODD: no signups after 2022-05-29. Either the table is a stale extract or acquisition stopped.
  Impact: "new customer" (first order in last 30 days) and churn logic use CURRENT_DATE(); tenure will look very long.
- Cross-check with orders: 0 customers ordered before subscribing; 0 orders reference unknown customers.

## Categorical
- COUNTRY: 243 distinct; top Korea 84, Congo 81, Vanuatu 58; no casing variants. Includes non-country "Antarctica (the territory South of 60 deg S)".
- CITY: 8,910 distinct, max 4 per city - near-unique, not useful for grouping. No casing variants.

## Format checks (aggregated; PII not shown)
- EMAIL: all match a basic email pattern.
- PHONE_1: 21 format patterns; 5,982 (59.8%) include an extension (xNNN). Not normalised.
- PHONE_2 never equals PHONE_1. WEBSITE always starts with http(s).

## Assumptions and caveats
- "Odd date" = future, pre-2000, null, or gaps/stops in the series.
- Blank = empty after TRIM.
- Data is synthetic (uniform distributions, invented cities); not real business findings.
