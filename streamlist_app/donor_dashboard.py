import streamlit as st
from google.cloud import bigquery
import pandas as pd
import altair as alt

st.set_page_config(page_title="Donor Summary", layout="wide")

st.title("Campaign Donor Summary")
st.caption("Data from dbt model: `fct_donor_summary`")

client = bigquery.Client(project="dbt-campaign-demo")

query = """
    SELECT donor_name, state, occupation, total_contributed, donation_count, last_donation_date
    FROM `dbt-campaign-demo.campaign_dbt.fct_donor_summary`
    ORDER BY total_contributed DESC
    LIMIT 1000
"""
df = client.query(query).to_dataframe()

df["last_donation_date"] = pd.to_datetime(df["last_donation_date"], format="%m%d%Y", errors="coerce")

states = df['state'].dropna().unique()
occupations = df['occupation'].dropna().unique()

min_amt, max_amt = st.slider(
    "Filter by Total Contributions ($)",
    float(df["total_contributed"].min()),
    float(df["total_contributed"].max()),
    (float(df["total_contributed"].min()), float(df["total_contributed"].max())),
    step=50.0
)

selected_occs = st.multiselect("Filter by Occupation", sorted(occupations))

filtered_df = df[
    (df["total_contributed"] >= min_amt) &
    (df["total_contributed"] <= max_amt)
]

if selected_occs:
    filtered_df = filtered_df[filtered_df["occupation"].isin(selected_occs)]

chart_data = (
    filtered_df.groupby("occupation", as_index=False)["total_contributed"]
    .sum()
    .sort_values("total_contributed", ascending=False)
    .head(15)
)

chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X("total_contributed:Q", title="Total Contributions ($)", axis=alt.Axis(format="~s")),
    y=alt.Y("occupation:N", sort="-x", title="Occupation"),
    tooltip=["occupation", alt.Tooltip("total_contributed", format=",")]
).properties(
    width=700,
    height=400,
    title="Top 15 Occupations by Total Contributions"
)

st.altair_chart(chart, use_container_width=True)

st.dataframe(
    filtered_df.style.format({
        "total_contributed": "${:,.0f}",
        "donation_count": "{:,}",
        "last_donation_date": lambda d: d.strftime("%b %d, %Y") if pd.notnull(d) else ""
    }),
    use_container_width=True
)