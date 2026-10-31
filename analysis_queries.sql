-- Light and Love House | SQLite-compatible verification queries.
-- Import data/orders_clean.csv as orders_clean using your SQLite tool.
-- Dates are ISO YYYY-MM-DD strings; numeric fields should be imported as numbers.
-- These are independent checks, not needed for the Excel dashboard to work.

-- 1. KPI totals from completed orders only; returns and cancellations are excluded.
SELECT COUNT(*) AS completed_orders,
 ROUND(SUM(units * unit_price_ngn * (1-discount_pct)), 2) AS realized_revenue_ngn,
 ROUND(SUM(units * unit_cost_ngn), 2) AS cogs_ngn,
 ROUND(SUM(units * (unit_price_ngn * (1-discount_pct) - unit_cost_ngn)), 2) AS gross_profit_ngn
FROM orders_clean WHERE order_status = 'Completed';

-- 2. Category ranking.
SELECT category, COUNT(*) AS completed_orders,
 ROUND(SUM(units * unit_price_ngn * (1-discount_pct)), 2) AS revenue_ngn
FROM orders_clean WHERE order_status = 'Completed'
GROUP BY category ORDER BY revenue_ngn DESC;

-- 3. Month-by-month sales.
SELECT SUBSTR(order_date, 1, 7) AS month,
 COUNT(*) AS completed_orders,
 ROUND(SUM(units * unit_price_ngn * (1-discount_pct)), 2) AS revenue_ngn
FROM orders_clean WHERE order_status = 'Completed'
GROUP BY month ORDER BY month;

-- 4. Customer segments, based on lifetime completed orders within the observed period.
WITH customer_orders AS (
 SELECT customer_id, COUNT(*) AS completed_orders,
 SUM(units * unit_price_ngn * (1-discount_pct)) AS revenue
 FROM orders_clean WHERE order_status = 'Completed'
 GROUP BY customer_id
), segments AS (
 SELECT CASE WHEN completed_orders = 1 THEN 'New'
             WHEN completed_orders BETWEEN 2 AND 3 THEN 'Returning'
             ELSE 'Loyal' END AS segment, revenue
 FROM customer_orders
)
SELECT segment, COUNT(*) AS customers, ROUND(SUM(revenue),2) AS revenue_ngn
FROM segments GROUP BY segment ORDER BY revenue_ngn DESC;
