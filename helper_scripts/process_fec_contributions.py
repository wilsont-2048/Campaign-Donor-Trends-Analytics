import pandas as pd

input_file = "./data/itcont.txt"
output_file = "./dbt/models/seeds/donations_sample.csv"
n_rows = 5000000

state_filter = "CA"

columns = [
    "CMTE_ID", "AMNDT_IND", "RPT_TP", "TRANSACTION_PGI", "IMAGE_NUM", "TRANSACTION_TP",
    "ENTITY_TP", "NAME", "CITY", "STATE", "ZIP_CODE", "EMPLOYER", "OCCUPATION",
    "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID", "CAND_ID", "TRAN_ID", "FILE_NUM",
    "MEMO_CD", "MEMO_TEXT", "SUB_ID"
]

print("Loading data...")
df = pd.read_csv(input_file, sep="|", header=None, names=columns, nrows=n_rows, low_memory=False)

df_clean = df[[
    "NAME", "CITY", "STATE", "ZIP_CODE", "OCCUPATION", "EMPLOYER",
    "TRANSACTION_DT", "TRANSACTION_AMT", "CAND_ID"
]].copy()

df_clean.columns = [
    "donor_name", "city", "state", "zip_code", "occupation", "employer",
    "donation_date", "amount", "candidate_id"
]

if state_filter:
    df_clean = df_clean[df_clean["state"] == state_filter]

df_clean = df_clean.dropna(subset=["candidate_id", "amount"])
df_clean.to_csv(output_file, index=False)

print(f"File saved as {output_file} with {len(df_clean)} rows.")
