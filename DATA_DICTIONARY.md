# Data Dictionary and Definitions

## Transaction columns

| Column | Format | Meaning |
| --- | --- | --- |
| `order_id` | Text | Synthetic order ID; unique in cleaned data |
| `order_date` | ISO date | Transaction date YYYY-MM-DD |
| `customer_id` | Text | Synthetic pseudonymous customer ID |
| `product_id` | Text | Synthetic product reference |
| `category` | Text | Lighting, Decor, Textiles, Aromas, Gift Sets or Tableware |
| `product` | Text | Retail product label |
| `region` | Text | Nigerian state/territory or Not Provided |
| `acquisition_channel` | Text | Recorded sales channel or Not Provided |
| `order_status` | Text | Completed, Returned or Cancelled |
| `units` | Integer | Product units in the order |
| `unit_price_ngn` | Numeric | Selling price per unit, before discount |
| `unit_cost_ngn` | Numeric | Merchandise cost per unit |
| `discount_pct` | Decimal | 0–0.15 discount proportion |
| `gift_order` | Yes/No | Whether order is categorized as gift-oriented |
| `customer_rating` | Integer or blank | Synthetic 2–5 rating, with nonresponse left blank |
| `occasion` | Text | Everyday, Birthday, Housewarming, Anniversary, Wedding or Holiday |

## Calculation conventions

**Completed orders only** contribute realized revenue, merchandise cost, gross profit and units sold. All values are NGN except rates and counts.

- `discounted order value = units × unit_price_ngn × (1 − discount_pct)`
- `realized revenue = discounted order value IF order_status == Completed ELSE 0`
- `COGS = units × unit_cost_ngn IF order_status == Completed ELSE 0`
- `gross profit = realized revenue − COGS`
- `gross margin (%) = 100 × gross profit / realized revenue`
- `AOV = realized revenue / completed order count`
- `repeat-buyer rate = buyers with 2+ completed orders / buyers with 1+ completed order`
- `90-day repurchase = eligible first-time buyers with a second completed order on days 1–90 / all eligible first-time buyers`

A customer is eligible for the 90-day measure only if their first completed purchase occurred at least 90 days before 30 Sep 2026. Same-day repeat orders do not count. Segments count completed orders only: New (1), Returning (2–3), Loyal (4+).

## Data handling

Raw data includes intentional duplicate IDs, blank categorical fields and non-standard capitalization. `scripts/build_data.py` makes those faults deterministically and then fixes them in the cleaned dataset. **Missing ratings remain missing**, avoiding false scores. CSV is generated, not scraped or collected from any real individuals.
