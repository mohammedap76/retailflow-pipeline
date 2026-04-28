-- Staging model for customers
-- Cleans and standardises raw customer data

WITH source AS (
    -- Step 1: Get raw data from source
    SELECT * FROM {{ source('raw', 'RAW_CUSTOMERS') }}
),

cleaned AS (
    -- Step 2: Clean and type cast columns
    SELECT
        customer_id,
        TRIM(first_name)                        AS first_name,
        TRIM(last_name)                         AS last_name,
        LOWER(TRIM(email))                      AS email,
        phone,
        INITCAP(city)                           AS city,
        INITCAP(state)                          AS state,
        UPPER(region)                           AS region,
        segment,
        TRY_TO_DATE(created_date, 'YYYY-MM-DD') AS created_date,
        loaded_at
    FROM source
    WHERE customer_id IS NOT NULL
      AND email IS NOT NULL
)

SELECT * FROM cleaned