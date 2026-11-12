---
name: profile-table
description: Profile a Snowflake table: schema, nulls, duplicates, distributions. Use before any analysis.
---

# Steps
1. DESCRIBE TABLE and report columns/types.
2. Row count, distinct count of the primary key, duplicate check.
3. Null % per column.
4. For numeric columns: min, max, avg, median, p95.
5. For categorical columns: top 10 values with counts.
6. Flag data quality issues (outliers, inconsistent casing, future dates).
7. Save SQL to sql/profile_<table>.sql and a summary to reports/profile_<table>.md.