# Power BI Data Export Summary

## 📊 Available CSV Files for Power BI Dashboard

### **Primary Data Tables**

#### 1. `bank_transactions_daily.csv` - Main Dashboard Data
- **Records**: 230 daily aggregates
- **Columns**: `txn_date`, `bank_id`, `total_volume`, `total_value`, `avg_value`, `median_value`, `created_at`
- **Purpose**: Primary data for daily transaction volume charts and trends
- **Date Range**: 2025-07-26 to 2025-09-09 (46 days)

#### 2. `transactions_raw.csv` - Detailed Transaction Data  
- **Records**: 27,490 individual transactions
- **Columns**: `transaction_id`, `bank_id`, `customer_id`, `amount`, `timestamp`, `txn_date`, `txn_year`, `txn_month`, `txn_day`, `txn_hour`
- **Purpose**: Granular analysis, customer segmentation, hourly patterns
- **Size**: ~2.2MB

### **Analytics Tables**

#### 3. `top_banks_7day.csv` - Bank Performance Rankings
- **Records**: 5 banks
- **Columns**: `bank_id`, `volume_7d`, `value_7d`, `avg_value_7d`, `trading_days_7d`
- **Purpose**: Top 5 banks by volume widget

#### 4. `monthly_trends.csv` - Monthly Comparison Data
- **Records**: 15 month-bank combinations  
- **Columns**: `year`, `month`, `bank_id`, `monthly_volume`, `monthly_value`, `avg_transaction_value`, `trading_days`, `month_start`, `month_end`
- **Purpose**: Monthly trend comparison charts

#### 5. `anomaly_detection.csv` - Anomalous Volume Detection
- **Records**: 230 daily records with anomaly flags
- **Columns**: `txn_date`, `bank_id`, `total_volume`, `total_value`, `avg_value`, `median_value`, `anomaly_flag`
- **Anomaly Types**: `HIGH_VOLUME`, `HIGH_AVG_VALUE`, `HIGH_TOTAL_VALUE`, `LOW_VOLUME`, `NORMAL`
- **Purpose**: Outlier detection and alerts

#### 6. `customer_analytics.csv` - Customer Insights
- **Records**: 1,000 customer-bank relationships
- **Columns**: `customer_id`, `bank_id`, `transaction_count`, `avg_transaction_value`, `total_spent`, `min_transaction`, `max_transaction`, `first_transaction`, `last_transaction`
- **Purpose**: Customer segmentation and behavior analysis

## 🎯 Power BI Dashboard Implementation Guide

### **Required Visualizations**

1. **Daily Total Transaction Volume**
   - Data Source: `bank_transactions_daily.csv`
   - Chart Type: Line chart or Area chart
   - X-axis: `txn_date`, Y-axis: `total_volume`
   - Group by: `bank_id`

2. **Top 5 Banks by Volume** 
   - Data Source: `top_banks_7day.csv`
   - Chart Type: Bar chart or Column chart
   - X-axis: `bank_id`, Y-axis: `volume_7d`

3. **Monthly Trend Comparison**
   - Data Source: `monthly_trends.csv` 
   - Chart Type: Line chart with multiple series
   - X-axis: `month`, Y-axis: `monthly_volume`
   - Legend: `bank_id`

4. **Anomalous Volume Detection**
   - Data Source: `anomaly_detection.csv`
   - Chart Type: Scatter plot or Table with conditional formatting
   - Color by: `anomaly_flag`
   - Filters: Exclude 'NORMAL' for alerts view

### **Key Measures to Create in Power BI**

```dax
Total Volume = SUM(bank_transactions_daily[total_volume])
Total Value = SUM(bank_transactions_daily[total_value]) 
Average Transaction = AVERAGE(bank_transactions_daily[avg_value])
Anomaly Count = COUNTROWS(FILTER(anomaly_detection, anomaly_detection[anomaly_flag] <> "NORMAL"))
```

### **Connection Information**
- **File Location**: `powerbi_exports/` folder
- **Import Method**: Get Data → Text/CSV → Browse to select files
- **Refresh**: Manual refresh from CSV files or connect directly to MySQL database

## 📈 Data Quality Summary

- ✅ **Complete Date Coverage**: 46 consecutive trading days
- ✅ **All Banks Represented**: 5 banks (BANK_1 through BANK_5)  
- ✅ **Anomalies Detected**: Multiple high-value days identified
- ✅ **Customer Diversity**: 200 unique customers across all banks
- ✅ **Data Integrity**: All values validated and cleaned