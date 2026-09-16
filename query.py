import pandas as pd
import duckdb

# 1. Load Dataset
file_path = '/Users/parasbadhran/Downloads/bhopal_orders_dataset.xlsx'
df = pd.read_excel(file_path, sheet_name='bhopal_orders_dataset')

# Preprocess timestamp safely in Pandas (fixes the DOUBLE -> TIMESTAMP casting error)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df['order_hour'] = df['timestamp'].dt.hour

print("==================================================")
print("BHOPAL DELIVERY TURNAROUND TIME (TAT) SQL ANALYSIS")
print("==================================================\n")

# --------------------------------------------------
# Query 1: Locality Bottleneck & Average TAT
# --------------------------------------------------
q1 = duckdb.sql("""
    SELECT
        locality,
        COUNT(*) AS total_orders,
        ROUND(AVG(delivery_time), 2) AS avg_tat_mins
    FROM df
    GROUP BY locality
    ORDER BY avg_tat_mins DESC
    LIMIT 5
""").df()

print("--- 1. TOP 5 WORST LOCALITIES BY AVERAGE TAT ---")
print(q1.to_string(index=False))
print("\n")

# --------------------------------------------------
# Query 2: SLA Breach Rate (% Orders > 30 mins)
# --------------------------------------------------
q2 = duckdb.sql("""
    SELECT
        locality,
        COUNT(*) AS total_orders,
        SUM(
            CASE
                WHEN delivery_time > 30 THEN 1
                ELSE 0
            END
        ) AS sla_breaches,
        ROUND(
            SUM(
                CASE
                    WHEN delivery_time > 30 THEN 1
                    ELSE 0
                END
            ) * 100.0 / COUNT(*),
            2
        ) AS sla_breach_pct
    FROM df
    GROUP BY locality
    HAVING COUNT(*) >= 100
    ORDER BY sla_breach_pct DESC
    LIMIT 5
""").df()

print("--- 2. TOP 5 LOCALITIES WITH HIGHEST SLA BREACH RATE (>30 MINS) ---")
print(q2.to_string(index=False))
print("\n")

# --------------------------------------------------
# Query 3: Peak Hour Delay Analysis
# --------------------------------------------------
q3 = duckdb.sql("""
    SELECT
        order_hour,
        COUNT(*) AS order_volume,
        ROUND(AVG(delivery_time), 2) AS avg_tat_mins,
        ROUND(AVG(order_value), 2) AS avg_order_value
    FROM df
    WHERE order_hour IS NOT NULL
    GROUP BY order_hour
    ORDER BY avg_tat_mins DESC
    LIMIT 5
""").df()

print("--- 3. PEAK HOURS WITH LONGEST DELIVERY DELAYS ---")
print(q3.to_string(index=False))
print("\n")

# --------------------------------------------------
# Query 4: Platform Performance (Window Function)
# --------------------------------------------------
q4 = duckdb.sql("""
    WITH PlatformStats AS (
        SELECT
            platform,
            locality,
            COUNT(*) AS order_count,
            ROUND(AVG(delivery_time), 2) AS avg_tat,
            DENSE_RANK() OVER (
                PARTITION BY platform
                ORDER BY AVG(delivery_time) DESC
            ) AS tat_rank
        FROM df
        GROUP BY platform, locality
    )
    SELECT
        platform,
        locality,
        order_count,
        avg_tat
    FROM PlatformStats
    WHERE tat_rank <= 3
    ORDER BY platform, tat_rank
""").df()

print("--- 4. TOP 3 SLOWEST LOCALITIES PER PLATFORM (WINDOW FUNCTION) ---")
print(q4.to_string(index=False))