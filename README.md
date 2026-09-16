## Bhopal Quick-Commerce Logistics & SLA Performance Dashboard

An interactive logistics analytics dashboard and data pipeline built to audit dark store performance, delivery turnaround times (TAT), and SLA compliance across Bhopal localities.

---

## Summary
In the quick-commerce sector (e.g., Blinkit, Swiggy Instamart, Zomato), meeting a strict  30-minute delivery SLA  is paramount to customer retention and unit economics. This portfolio project analyzes 5,000+ delivery records across Bhopal to identify dark store bottlenecks, peak-hour congestion, platform disparities (Zomato vs. Swiggy), and localized SLA breaches.

---

## Tech Stack & Architecture
*  Frontend Visualization:  Excel 
*  Data Engineering & Pipeline:  Python (`pandas`, `openpyxl`) running natively on Apple Silicon.
*  SQL Query Engine:   DuckDB  for local database queries executed directly against `.xlsx` files.
*  Version Control:  Git & GitHub (`sql_delivery_analysis.py`, `delivery_queries.sql`).

---

##  Key Business Insights & Analytical Modules

The project is structured around core operational challenges faced by rapid-delivery networks:

1.  Locality Bottlenecks & Average TAT:  Pinpoints specific neighborhoods (e.g., Bairagarh, Berasia Road) suffering from inflated delivery times.
2.  SLA Breach Tracking (`> 30 mins`):  Isolates high-density areas exceeding acceptable delivery windows, tracking exact breach percentages per zone.
3.  Peak Hour Rush Analysis:  Evaluates order density and delivery delays during high-volume windows (such as the evening dinner rush).
4.  Platform Benchmarking (Window Functions):  Uses advanced SQL window functions (`DENSE_RANK()`) to rank and contrast performance metrics across platforms.

---

## Key Findings & Metrics

Locality Bottlenecks: Bairagarh records the highest average delivery time at 40.80 minutes.

SLA Breaches: Indrapuri suffers the worst breach rate, with 84.83% of orders exceeding the 30-minute window.

Peak Hours: Hour 10 experiences the longest system-wide delivery delays, averaging 41.77 minutes.

Platform Split: Swiggy's slowest zone is Bairagarh (41.74 mins), whereas Zomato's is Berasia Road (41.31 mins).

---
