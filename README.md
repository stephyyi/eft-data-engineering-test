# EFT Data Engineering Test

This repository contains the solution to the EFT Corporation Data Engineering Pre-Test Assignment. It implements a complete daily ETL pipeline for ingesting, transforming, and aggregating banking transaction data, with outputs designed for both reporting (MySQL) and dashboarding (Power BI).

## Features

- **Apache Airflow DAG**: Orchestrates a daily pipeline to ingest raw transactions (CSV/S3), transform them in Python, and load results into MySQL
- **Python Transformation Module**: Cleans nulls, validates schema, and aggregates transaction totals per bank per day
- **MySQL Integration**: Stores daily aggregates with idempotent upserts keyed by (txn_date, bank_id)
- **SQL Analytics**: Queries for top banks by transaction volume and average transaction value per customer
- **Mock Data**: 46 days of realistic transactional data with anomalies for testing
- **Power BI Dashboard**: Visualizes daily totals, top 5 banks, monthly trends, and anomalies

## Repository Structure

```
airflow/dags/transactions_pipeline_dag.py  # Airflow DAG definition
src/transform.py                           # Python transformation logic
sql/queries.sql                           # SQL queries for analytics
data/sample_transactions.csv              # Mock transaction dataset
powerbi_exports/                          # screenshots of Powerbi visualization
requirements.txt                          # Python dependencies
setup.sh                                  # Setup script
test_setup.py                            # Installation verification
```

## Technology Stack

- **Apache Airflow** - workflow orchestration
- **Python** (pandas, numpy, sqlalchemy) - data cleaning and transformation
- **MySQL** - storage and reporting
- **Power BI** - visualization and anomaly detection

## Setup Instructions

### Prerequisites
- Python 3.11+
- MySQL 8.x or compatible
- Apache Airflow 2.7+

### Installation
```bash
# Run automated setup
chmod +x setup.sh
./setup.sh

# Or manual installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Setup
```bash
# Create MySQL database
mysql -u root -e "CREATE DATABASE IF NOT EXISTS analytics;"

# Verify installation
python test_setup.py
```

## Usage

### Running the ETL Pipeline
```bash
# Activate environment
source venv/bin/activate

# Transform data directly
python src/transform.py --in data/sample_transactions.csv --out output.csv

# Run complete pipeline simulation
python -c "
from airflow.dags.transactions_pipeline_dag import extract_and_transform, load_to_mysql
# Pipeline execution logic here
"
```

### SQL Analytics
```sql
-- Top 5 banks by volume (last 7 days)
SELECT bank_id, SUM(total_volume) AS volume_7d
FROM bank_transactions_daily
WHERE txn_date >= CURDATE() - INTERVAL 7 DAY
GROUP BY bank_id
ORDER BY volume_7d DESC
LIMIT 5;
```


#### Power BI Dashboard Screenshots
- For the powerbi dashboard I couldn't download the file itself as I was using the free PowerBi service on my Mac which doen't have that functionality.
However, see below the screenshots form my work.

Link to dashboard : https://app.powerbi.com/groups/me/dashboards/9d165387-7089-4902-97a3-8428b4916366?ctid=5e4540c5-6c3d-470b-87c8-e7e62f1d3086&pbi_source=linkShare

**Daily Transaction Volume Overview. && Top 5 Banks Performance**

![Top Banks Performance](powerbi_exports/Screenshot%202025-09-09%20at%2013.18.59.png)

**Monthly Trends Analysis**

![Monthly Trends](powerbi_exports/Screenshot%202025-09-09%20at%2013.19.12.png)

**Anomaly Detection Dashboard**

![Anomaly Detection](powerbi_exports/Screenshot%202025-09-09%20at%2013.19.23.png)

## Data Schema

### Input Data (sample_transactions.csv)
- `transaction_id` - Unique transaction identifier
- `bank_id` - Bank identifier (BANK_1 to BANK_5)
- `customer_id` - Customer identifier
- `amount` - Transaction amount
- `timestamp` - Transaction timestamp

### Output Data (bank_transactions_daily)
- `txn_date` - Transaction date
- `bank_id` - Bank identifier
- `total_volume` - Number of transactions
- `total_value` - Sum of transaction amounts
- `avg_value` - Average transaction amount
- `median_value` - Median transaction amount

## Architecture

1. **Extract**: Read CSV transaction data
2. **Transform**: Clean, validate, and aggregate by bank and date
3. **Load**: Store aggregated data in MySQL
4. **Analyze**: Run SQL queries for insights
5. **Visualize**: Create Power BI dashboards

## Testing

Run the test suite to verify installation and functionality:
```bash
python test_setup.py
```
