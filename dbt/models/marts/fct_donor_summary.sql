-- models/marts/fct_donor_summary.sql

with donations as (

    select * from {{ ref('stg_donations') }}

),

aggregated as (

    select
        donor_name,
        city,
        state,
        zip_code,
        occupation,
        employer,
        count(*) as donation_count,
        sum(amount) as total_contributed,
        max(donation_date) as last_donation_date

    from donations
    group by
        donor_name, city, state, zip_code, occupation, employer

)

select * from aggregated
