# Light and Love House | Retail Performance & Customer Analytics

**One cohesive, end-to-end Data Analytics portfolio project** using a fully **synthetic** Nigerian home décor and gifting retail dataset. It explores profitability, revenue trends, customer segments, acquisition channels and 90-day repeat purchasing.

> **Data disclosure:** Light and Love House is a fictional demonstration retailer. All 1,450 cleaned transactions are generated with a fixed random seed. No revenue, customer or operational numbers in this repository describe an actual business.

![Executive dashboard](dashboard/01-executive-dashboard.png)

![Customer and retention dashboard](dashboard/02-customer-retention-dashboard.png)

## Business questions

1. How much realized revenue and merchandise gross profit does the illustrative retailer generate?
2. Which product categories, regions and acquisition channels account for the largest sales shares?
3. How do new, returning and loyal customers contribute differently to revenue?
4. What proportion of eligible customers make another purchase within 90 days of their first?
5. How does January–September performance compare between 2025 and 2026?

## Executive summary (simulated results)

| Indicator | Result | Definition |
| --- | ---: | --- |
| Clean order records | 1,450 | Unique orders after removing 17 duplicate rows |
| Completed orders | 1,201 | Used for realized sales and costs |
| Realized revenue | ₦35,553,820 | Discounted sales from completed orders |
| Gross profit | ₦15,227,020 | Realized revenue minus merchandise COGS |
| Gross margin | 42.83% | Gross profit / realized revenue |
| Average order value | ₦29,604 | Revenue / completed orders |
| Repeat buyer rate | 65.94% | Buyers with 2+ completed orders / all buyers |
| Eligible 90-day repurchase rate | 26.55% | Second purchase within 1–90 days / eligible first-time customers |
| Jan–Sep sales change (2026 vs. 2025) | +23.61% | Compares matching nine-month windows |

### Supported findings

- **Gift Sets** is the leading category by realized revenue (₦8,070,825).
- **Website** is the leading recorded acquisition channel (₦8,002,415). These tags describe transactions and do not prove channel incrementality.
- **Lagos** records the largest share of realized revenue among the synthetic regions.
- Customer segments contribute different shares: New 11.4%, Returning 35.6%, Loyal 53.0% of realized revenue.
- Exactly 388 customers had sufficient follow-up for the 90-day metric; 103 repeated within that window.

See [Executive report](docs/EXECUTIVE_REPORT.md) for interpretation, recommendations and limitations.

## Dashboards and workbook

The Excel workbook, **[Light-and-Love-House-Analytics.xlsx](Light-and-Love-House-Analytics.xlsx)**, contains:

| Worksheet | Purpose |
| --- | --- |
| Start Here | Scope, methodology, definitions and interpretation notes |
| Executive Dashboard | Formula-driven KPIs and native Excel charts |
| Monthly Trends | Revenue, orders, cost, profit, margin and AOV by month |
| Category Performance | Merchandise performance by product family |
| Customer Segments | One-order, 2–3-order and 4+-order customer segments |
| Acquisition Channels | Revenue, completed orders and margins by channel |
| 90D Repurchase | Eligible first-purchase cohorts and 90-day repeat rates |
| Region Performance | Summary of the synthetic geographic sales mix |
| Data Quality | Records removed, blank fields and capitalization fixes |
| Order Records | 1,450 clean orders and live revenue/COGS/profit formulas |
| Data Dictionary | Complete descriptions for every data column |
| Chart Sources | Formula references used by native Excel chart series |

## File layout

```text
Light-and-Love-House-Analytics.xlsx  # Excel workbook
README.md
.gitignore
requirements.txt
├── data/
│   ├── orders_raw.csv              # Raw synthetic orders with intentional quality issues
│   ├── orders_clean.csv            # Deduplicated, standardized data
│   └── quality_summary.json
├── dashboard/
│   ├── 01-executive-dashboard.png
│   └── 02-customer-retention-dashboard.png
├── outputs/
│   ├── metrics.json
│   ├── monthly_summary.csv
│   ├── category_summary.csv
│   ├── customer_segments.csv
│   ├── customer_level.csv
│   ├── channel_summary.csv
│   ├── region_summary.csv
│   ├── cohort_90d.csv
│   └── validation.json
├── scripts/
│   ├── build_data.py
│   ├── analyze.py
│   ├── make_visuals.py
│   └── build_workbook_artifact.py
├── sql/
│   └── analysis_queries.sql
├── docs/
│   ├── EXECUTIVE_REPORT.md
│   ├── DATA_DICTIONARY.md
│   └── PROJECT_WALKTHROUGH.md
└── tests/
    └── test_analysis.py
```

## Reproduce the analysis

Requires **Python 3.10+**. The generator, analyses, metrics and validation tests use only Python's standard library.

```bash
python scripts/build_data.py
python scripts/analyze.py
python -m unittest discover -s tests -v
```

To regenerate PNG dashboard images, install the optional plotting dependency and run:

```bash
python -m pip install -r requirements.txt
python scripts/make_visuals.py
```

The Excel workbook is **included already**. Its builder (`scripts/build_workbook_artifact.py`) additionally uses the `artifact_tool` spreadsheet environment. No extra package is necessary to open the supplied `.xlsx` in Excel or another compatible spreadsheet application.

For independent verification, run the SQLite queries in [`sql/analysis_queries.sql`](sql/analysis_queries.sql) after importing `data/orders_clean.csv` into a SQLite table named `orders_clean`.

## Data preparation

The dataset generator adds known, controlled data-quality issues. The cleaner removes exactly **17** duplicate order IDs, replaces 19 missing regions and 14 missing acquisition channel labels with **Not Provided**, normalizes inconsistent capitalization, and leaves 611 missing ratings empty rather than treating them as zero.

**Financial rule:** An order contributes realized revenue and merchandise COGS only when its status is `Completed`. Returned or cancelled orders contribute zero to both. This convention is explicitly documented and excludes overhead, shipping and refund handling costs.

## Limitations and interpretation

The dataset is synthetic, not a sample of actual customers. The generated channel mix, growth rates, segments and buying behaviours are **illustrative**, not evidence that a real business behaves similarly. Repeat-buyer rate is not the same metric as 90-day cohort repurchase. There are no inferential or causal conclusions, no tested marketing experiments, and no forecast of a real company's revenue.

## Project context

Prepared as a practical Data Analytics learning and portfolio project for the **BoyCode Africa Data Analysis programme**. Repository maintained by [Obari-EmmanuelS](https://github.com/Obari-EmmanuelS). All datasets and analysis scripts in this project were newly generated for this example; no files from other GitHub repositories were incorporated.
