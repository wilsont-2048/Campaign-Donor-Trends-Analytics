# Campaign Donor Trends Analytics

A complete data pipeline project that uses data engineering, transformation, and visualization using **Apache Airflow**, **dbt**, **BigQuery**, and **Streamlit**. The pipeline uses Federal Election Commission (FEC) individual contribution data, transforms it for analysis, and visualizes key insights through an interactive dashboard.

## Tech Stack

| Layer          | Tool                  |
| -------------- | --------------------- |
| Ingestion      | Apache Airflow        |
| Transformation | dbt (Data Build Tool) |
| Storage        | BigQuery              |
| Dashboard      | Streamlit             |

## Project Structure

```bash
Campaign-Donor-Trends-Analytics/
├── dags/                             # Airflow DAGs
│   └── donor_pipeline_dag.py
├── data/                             # Data obtained from FEC site
│   ├── indiv_header_file.csv         # Header file provided by FEC
│   └── itcont.txt                    # Data on individual contributions
├── dbt/                              # dbt models and seeds
│   ├── models/
│   │   ├── staging/stg_donations.sql
│   │   └── marts/fct_donor_summary.sql
│   ├── seeds/donations_sample.csv
│   └── dbt_project.yml
├── helper_scripts/
│   ├── process_fec_contributions.py  # Helper script to downsize itcont.txt
├── streamlit_app/                    # Streamlit UI
│   └── donor_dashboard.py
├── airflow_setup.md                  # Local Airflow setup guide
├── requirements.txt                  # Streamlit + BigQuery dependencies
├── .gitignore
└── README.md
```

## Features

- **Airflow DAG** to orchestrate data loads
- **dbt models** for staging and donor fact table creation
- **Streamlit dashboard** for exploring donor contributions:
  - Filter by donation amount
  - Filter by occupation
  - View top donors, contribution count, and last donation dates
- **BigQuery** stores raw and transformed datasets

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/wilsont-2048/Campaign-Donor-Trends-Analytics.git
cd Campaign-Donor-Trends-Analytics
```

### 2. Set Up Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Upload Seed Data to BigQuery

Before running `dbt seed`, upload the seed CSV (`dbt/seeds/donations_sample.csv`) to your BigQuery project manually:

1. Go to [Google Cloud Console → BigQuery](https://console.cloud.google.com/bigquery).
2. Select your project and click `+ Create Dataset`. Name it `campaign_dbt`.
3. Click `Create Table`:
   - **Source**: Upload `donations_sample.csv`
   - **File format**: CSV
   - **Table name**: `donations_sample`
   - **Schema**: Use the following structure:

```json
[
  {"name": "donor_name", "type": "STRING"},
  {"name": "city", "type": "STRING"},
  {"name": "state", "type": "STRING"},
  {"name": "zip_code", "type": "STRING"},
  {"name": "occupation", "type": "STRING"},
  {"name": "employer", "type": "STRING"},
  {"name": "donation_date", "type": "STRING"},
  {"name": "amount", "type": "FLOAT"},
  {"name": "candidate_id", "type": "STRING"}
]
```

4. Under **Advanced options**, set `Skip header rows` to `1`.
5. **Location**: Must match the region in your `dbt` profile (e.g. `northamerica-northeast2`)

This ensures the data is accessible to your `stg_donations` model in dbt.

### 4. Set Up dbt

- Install `dbt-bigquery`
- Configure `~/.dbt/profiles.yml` for your BigQuery project
- Run transformations:

```bash
cd dbt
dbt seed
dbt run
```

### 5. Run Streamlit Dashboard

```bash
cd streamlit_app
streamlit run donor_dashboard.py
```

### 6. Airflow (Optional)

Follow steps in `airflow_setup.md` to orchestrate DAG locally

## Dashboard Preview

<img src="assets/images/Donor Summary.jpg" width="600"/>

## Data Source

- Federal Election Commission (FEC), Individual Contribution Data [[https://www.fec.gov/data/](https://www.fec.gov/data/browse-data/?tab=bulk-data)]
