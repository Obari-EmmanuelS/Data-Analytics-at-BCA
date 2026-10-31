# Project Walkthrough — Light and Love House

Use these notes to understand the work well enough to explain the project accurately. Don't claim to have performed any analysis you cannot demonstrate.

## What was built

A synthetic end-to-end retail data exercise: a deterministic source generator, cleaning logic, reusable aggregation script, an Excel workbook, executive dashboard screenshots, SQL validation queries and automated tests.

## Rebuild in six steps

1. Read `scripts/build_data.py` to see how the fictional orders and controlled anomalies are generated.
2. Compare `data/orders_raw.csv` with `data/orders_clean.csv` for duplicates and missing categories.
3. Read `scripts/analyze.py` for completed-order rules and margin calculations.
4. Open `Light-and-Love-House-Analytics.xlsx`, beginning at **Start Here** and **Executive Dashboard**.
5. Review Customer Segments and 90D Repurchase, noting these are different measures.
6. Run `python -m unittest discover -s tests -v` and confirm all checks succeed.

## Explain three important decisions

**Why remove duplicate Order IDs?** Because leaving duplicated transaction IDs inflates reported sales and transaction counts.

**Why not replace missing customer ratings with zero?** Because no response is not the same as a poor rating. Filling with zero distorts averages and distributions.

**Why exclude returns and cancellations from realized revenue?** Because the retail exercise defines realized revenue as the net value of completed sales; returns/cancellations are not fulfilled revenue.

## Demonstrate an insight

Use category revenue to state which product family is largest in the simulated dataset. Do not claim to know *why* without additional evidence. Recommend a small controlled business test and explain what metric would show whether it succeeded.

## What to say about the data

This is an educational case study with simulated customer/order data created for practice. It is not a company dataset and the numerical findings are illustrative.

## How to customize without copying

Change the underlying business question and generate new synthetic transactions, then rerun scripts and validate the workbook. Do not merely rename another person's workbook, dashboard screenshots or README text.
