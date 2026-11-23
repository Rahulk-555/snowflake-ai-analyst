# snowflake-ai-analyst

An AI-analyst project for testing the CoCo agent harness (context files and skills) against Snowflake data. The agent analyses customers, products and orders using the rules and definitions in `AGENTS.md` and the skills in `.cortex/skills/`.

> **Note:** All order data in this project is **synthetic**. Patterns in the results are test artefacts, not real business findings.

## Data model

Database/schema: `COCO_ANALYST.MY_TABLE`

| Object | Type | Grain / purpose |
|---|---|---|
| `DIM_CUSTOMERS` | Table | One row per customer (`CUSTOMER_ID`) |
| `DIM_PRODUCTS` | Table | One row per product (`PRODUCT_ID`) |
| `FCT_ORDER_LINES` | Table | One row per order line; joins to both dimensions |
| `V_VALID_ORDER_LINES` | View | `FCT_ORDER_LINES` filtered to `COMPLETED` orders; default source for analysis |

```
DIM_CUSTOMERS 1───* FCT_ORDER_LINES *───1 DIM_PRODUCTS
 (CUSTOMER_ID)        (ORDER_LINE_ID)       (PRODUCT_ID)
```

Full column notes, PII flags and shared definitions (valid orders, churn, "New" customers) are in the Data Dictionary section of `AGENTS.md`.

## Repo structure

```
.
├── AGENTS.md          # Project context, rules, data dictionary
├── README.md
├── .cortex/skills/    # Agent skills
├── setup/             # One-off SQL to create the fact table, view and synthetic data (run manually)
├── sql/               # Queries saved by the agent
└── reports/           # Findings written by the agent
```

## Skills

| Skill | Use it to |
|---|---|
| `profile-table` | Profile a new table (first step for any table) |
| `customer-segmentation` | RFM / value segments, top customers, revenue concentration |
| `churn-analysis` | Retention and churn drivers |

## Setup

1. **Snowflake objects.** Run the scripts in `setup/` in order, using a role that can create tables and views:
   1. create `FCT_ORDER_LINES`
   2. populate it with synthetic data
   3. create `V_VALID_ORDER_LINES`
2. **Check the data.** Confirm there are no orphan customer or product IDs and no orders dated before a customer's subscription date.
3. **Agent role.** Connect the agent with a role that has only `SELECT` on the four objects above and `USAGE` on the warehouse (`SNOWFLAKE_LEARNING_WH` by default). This is what actually enforces read-only access; the rule in `AGENTS.md` is a second layer.
4. **Connect.** Set up your Snowflake connection locally (for example in VS Code). Keep credentials out of the repo.
5. **Open the project** in your CoCo agent environment so it picks up `AGENTS.md` and `.cortex/skills/`.

## Usage

Example prompts:

- "Profile DIM_CUSTOMERS."
- "Segment our customers using RFM and show revenue share per segment."
- "Which customers are at risk of churning, by country?"

The agent saves each query to `sql/<skill>_<description>.sql` and writes findings to `reports/<topic>.md` with the SQL used, assumptions and caveats.

## Guardrails

- **Read-only:** SELECT / DESCRIBE / SHOW only.
- **No raw PII:** names, company, emails, phones and websites are never output. Customers are identified by `CUSTOMER_ID`.
- **No mixed currencies:** money is never summed or averaged across different currencies.
- **Stated assumptions:** anything not defined in `AGENTS.md` is called out in the report.

## Status

Work in progress. `product-analysis` is planned but not yet implemented.`
