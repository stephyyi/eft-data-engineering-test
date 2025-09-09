-- SQL Queries for EFT Analytics

-- 1. Top 5 banks by transaction volume in the last 7 days
SELECT bank_id, SUM(total_volume) AS volume_7d
FROM bank_transactions_daily
WHERE txn_date >= CURDATE() - INTERVAL 7 DAY
GROUP BY bank_id
ORDER BY volume_7d DESC
LIMIT 5;

-- 2. Average transaction value per customer for a given month
SELECT customer_id, AVG(amount) AS avg_txn_value_in_month
FROM transactions_raw
WHERE YEAR(timestamp) = @year
  AND MONTH(timestamp) = @month
GROUP BY customer_id;
