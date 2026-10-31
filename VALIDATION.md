# Validation and Quality Assurance

**Dataset:** Fully synthetic Light and Love House retail orders  
**Period:** 2025-01-01 through 2026-09-30  
**Generator seed:** 268119

## Controls included

- Deduplicates orders using `order_id` and confirms that each clean order ID is unique.
- Maps blank region and sales-channel labels to `Not Provided`, preserving unknown values instead of inventing locations or channels.
- Normalizes inconsistent capitalization in source labels.
- Leaves customer ratings blank where no synthetic rating was generated.
- Realizes revenue and merchandise costs only for `Completed` orders.
- Confirms `gross profit = realized revenue − merchandise cost`.
- Confirms category totals, customer-segment totals and monthly totals reconcile to total realized revenue.
- Computes the 90-day repurchase rate only for customers who have a complete observation window.
- Compares January–September 2026 against January–September 2025 (not a partial period against a complete year).

## Run quality checks

From the project folder:

```bash
python scripts/build_data.py
python scripts/analyze.py
python -m unittest discover -s tests -v
```

The seven automated tests cover record uniqueness, zero revenue for returned/cancelled orders, financial arithmetic, metric reconciliation, cohort-rate bounds, cleaning counts and missing categorical values.

The analysis results are saved to `outputs/validation.json`, `outputs/metrics.json` and the reproducible summary CSVs. They can be inspected without Excel.

## What quality control does not prove

Reconciliation proves consistency within the synthetic dataset; it does not prove that the same numbers apply to an actual retail business. The dataset is an invented practice example, not independently sampled commercial evidence.
