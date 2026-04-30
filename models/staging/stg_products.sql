WITH source AS (
    -- Read raw products from RAW schema
    SELECT * FROM {{ source('raw', 'RAW_PRODUCTS') }}
),

cleaned AS (
    -- Clean and enrich product data
    SELECT
        product_id,
        TRIM(product_name)                      AS product_name,
        INITCAP(category)                       AS category,
        INITCAP(sub_category)                   AS sub_category,
        unit_price::FLOAT                       AS unit_price,
        cost_price::FLOAT                       AS cost_price,

        -- Business logic: calculate margin
        ROUND(unit_price - cost_price, 2)       AS gross_margin,
        ROUND(
            (unit_price - cost_price)
            / NULLIF(unit_price, 0) * 100
        , 2)                                    AS margin_pct,

        TRIM(supplier)                          AS supplier,
        CASE
            WHEN UPPER(is_active) = 'TRUE'
            THEN TRUE ELSE FALSE
        END                                     AS is_active,
        TRY_TO_DATE(launch_date, 'YYYY-MM-DD')  AS launch_date,
        loaded_at

    FROM source
    WHERE product_id IS NOT NULL
)

SELECT * FROM cleaned