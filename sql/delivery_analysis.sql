-- ====================================================================
-- Project: Bhopal Quick-Commerce Logistics Analysis
-- Engine: DuckDB / Standard ANSI SQL
-- ====================================================================

-- Query 1: Locality Bottleneck & Average TAT
SELECT
    locality,
    COUNT(*) AS total_orders,
    ROUND(AVG(delivery_time), 2) AS avg_tat_mins
FROM bhopal_orders_dataset
GROUP BY locality
ORDER BY avg_tat_mins DESC
LIMIT 5;

-- Query 2: SLA Breach Rate (% Orders > 30 mins)
SELECT
    locality,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_time > 30 THEN 1 ELSE 0 END) AS sla_breaches,
    ROUND(SUM(CASE WHEN delivery_time > 30 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS sla_breach_pct
FROM bhopal_orders_dataset
GROUP BY locality
HAVING COUNT(*) >= 100
ORDER BY sla_breach_pct DESC
LIMIT 5;

-- Query 3: Peak Hour Delay Analysis
SELECT
    EXTRACT(HOUR FROM CAST(timestamp AS TIMESTAMP)) AS order_hour,
    COUNT(*) AS order_volume,
    ROUND(AVG(delivery_time), 2) AS avg_tat_mins,
    ROUND(AVG(order_value), 2) AS avg_order_value
FROM bhopal_orders_dataset
GROUP BY order_hour
ORDER BY avg_tat_mins DESC
LIMIT 5;

-- Query 4: Platform Performance (Window Function - Zomato vs Swiggy)
WITH PlatformStats AS (
    SELECT
        platform,
        locality,
        COUNT(*) AS order_count,
        ROUND(AVG(delivery_time), 2) AS avg_tat,
        DENSE_RANK() OVER (PARTITION BY platform ORDER BY AVG(delivery_time) DESC) AS tat_rank
    FROM bhopal_orders_dataset
    GROUP BY platform, locality
)
SELECT platform, locality, order_count, avg_tat
FROM PlatformStats
WHERE tat_rank <= 3
ORDER BY platform, tat_rank;
