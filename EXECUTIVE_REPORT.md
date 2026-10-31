# Light and Love House — Executive Analytics Report

**Reporting window:** 1 January 2025 to 30 September 2026  
**Scope:** Fictional home décor, lighting and gifting retailer in Nigeria  
**Nature of evidence:** Deterministic, simulated transaction data; **not real business performance**.

## Executive summary

From 1,450 cleaned unique orders (1,201 completed, 116 returned and 133 cancelled), the example produces realized revenue of **₦35,553,820**, merchandise COGS of **₦20,326,800**, and gross profit of **₦15,227,020**, for a **42.83%** gross margin. This excludes overhead and fulfillment costs.

## 1. Product performance

The largest revenue-generating product family is **Gift Sets**, with ₦8,070,825 in completed-order revenue. This is a descriptive concentration measure, not proof of superior demand elasticity or a causal driver of profit.

## 2. Channel and regional distribution

The highest recorded channel is **Website** with ₦8,002,415; **Lagos** leads the illustrative regional mix. Channel is a transaction attribute and cannot support claims about acquisition return on ad spend without marketing costs or experiments.

## 3. Customer behaviour

Of 411 customers with at least one completed purchase, **271** completed two or more orders during the observation window. This gives a **65.94%** period-wide repeat-buyer rate. Segment labels use completed-order count: New (1), Returning (2–3), Loyal (4+).

For 90-day repurchase, customers whose first completed order occurred after the eligibility cutoff are excluded. The eligible population is **388**, of whom **103** made another purchase within 1–90 days, yielding **26.55%**. These rates are different and must not be conflated.

## 4. Year-on-year comparability

Comparing **January–September 2025** (₦13,470,145) with **January–September 2026** (₦16,650,950) gives a **+23.61%** difference in revenue. Comparing full-year 2025 with only nine months of 2026 would not be meaningful.

## Proposed management experiments

1. **Test product bundles**, especially gift-set combinations. Measure margin per completed order, not just gross sales.
2. **Investigate customer segments** using basket size and repeat order timing. Test a modest retention offer with a control group rather than assuming rewards will increase purchases.
3. **Track channel acquisition costs** to understand whether the largest-revenue channel is also the most efficient.
4. **Monitor cancellation and return reasons** before changing operations or inventory policies; the current synthetic dataset does not record why orders failed.
5. **Review measurement quality**. Keep missing ratings missing, preserve a consistent financial-status policy and reconcile category totals to the headline revenue.

## Limitations

- Entirely synthetic observations; no external validity or statistically defensible inference about actual retail demand.
- Gross profit is not net profit. Shipping, taxes, salaries, advertising, warehousing and refund administration are excluded.
- Cohort metrics only use eligible customers. Customers acquired in late 2026 lack full follow-up.
- No experimental design; therefore channel/region associations do not establish causality.
- Dataset design intentionally varies order volumes, basket sizes and repeated purchases to make a realistic *exercise*, not an estimate of any real market.

## Source and reproducibility

All reported measures are computed by `scripts/analyze.py` from the included `data/orders_clean.csv`. The source data comes from `scripts/build_data.py` with fixed seed 268119. Checks appear in `outputs/validation.json` and `tests/test_analysis.py`.
