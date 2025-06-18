# Airflow Setup Guide

This guide walks through setting up Apache Airflow locally to establish the data pipeline for the Campaign Donor Trends Analytics project.

## 1. Install Airflow

Activate your project’s virtual environment:

```bash
source .venv/bin/activate
```

Install Airflow with BigQuery support:

```bash
pip install "apache-airflow[google]" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.11.txt"
```

> Make sure the Python version is 3.11 for compatibility.

## 2. Initialize the Airflow Database

```bash
airflow db migrate
```

This will create the Airflow metadata database (`airflow.db`) locally under `~/airflow`.

## 3. Start Airflow Webserver & Scheduler

In separate terminal windows:

```bash
# Terminal 1
airflow webserver --port 8080

# Terminal 2
airflow scheduler
```

Visit `http://localhost:8080` to access the Airflow UI.

> Default credentials:
> - Username: `airflow`
> - Password: `airflow`

## 4. Copy DAG to Airflow DAGs Folder

Ensure your DAG file (`donor_pipeline_dag.py`) is placed in the correct directory:

```bash
cp dags/donor_pipeline_dag.py ~/airflow/dags/
```

You should see your DAG appear in the Airflow UI after refreshing.

## 5. Trigger & Monitor DAG

Once visible, you can trigger your DAG manually and monitor its run in the Airflow UI. Logs and status for each task will be available in the web interface.

## Final Notes

- Ensure the `dbt run` commands and seed data are complete before triggering the DAG.
- You can use BashOperators or PythonOperators to invoke dbt CLI commands from within the DAG.
