# EFT Data Engineering Test  

This repository contains the solution to the EFT Corporation **Data Engineering Pre-Test Assignment**.  
It implements a complete **daily ETL pipeline** for ingesting, transforming, and aggregating banking transaction data, with outputs designed for both **reporting** (MySQL) and **dashboarding** (Power BI).  

---

## ✨ Features
- **Apache Airflow DAG**: Orchestrates a daily pipeline to ingest raw transactions (CSV / S3), transform them in Python, and load results into MySQL.  
- **Python Transformation Module**: Cleans nulls, validates schema, and aggregates transaction totals per bank per day.  
- **MySQL Integration**: Stores daily aggregates with idempotent upserts keyed by `(txn_date, bank_id)`.  
- **SQL Analytics**: Queries for top banks by transaction volume and average transaction value per customer.  
- **Mock Data**: 40+ days of realistic transactional data (with anomalies) for demo and testing.  
- **Power BI Dashboard**: Visualizes daily totals, top 5 banks, monthly trends, and anomalies with DAX measures.  

---

## 🗂️ Repository Structure
airflow/dags/transactions_pipeline_dag.py # Airflow DAG definition
src/transform.py # Python transformation logic
sql/queries.sql # SQL queries for analytics
data/sample_transactions.csv # Mock transaction dataset
powerbi/ # Power BI file / notes
README.md # Setup guide & documentation


---

## 🚀 Tech Stack
- **Apache Airflow** (workflow orchestration)  
- **Python (pandas, numpy, sqlalchemy)** (data cleaning & transformation)  
- **MySQL** (storage & reporting)  
- **Power BI** (visualization & anomaly detection)  

---

## ⚙️ Setup Instructions  

### 1. Prerequisites
- Python 3.9+  
- MySQL 8.x (or compatible)  
- Airflow 2.7+  
- Install dependencies:  
```bash
pip install pandas numpy sqlalchemy pymysql apache-airflow
