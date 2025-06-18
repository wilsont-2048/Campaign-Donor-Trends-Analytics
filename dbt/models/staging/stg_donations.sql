-- models/staging/stg_donations.sql

with source as (

    select * from {{ source('campaign_dbt', 'donations_raw') }}

),

renamed as (

    select
        donor_name,
        city,
        state,
        cast(zip_code as string) as zip_code,
        occupation,
        employer,
        donation_date,
        cast(amount as float64) as amount,
        candidate_id

    from source

)

select * from renamed
