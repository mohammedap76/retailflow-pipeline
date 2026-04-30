WITH source AS (
    -- Read raw orders from RAW schema
    SELECT * FROM {{ source('raw', 'RAW_ORDERS') }}
),

cleaned AS (
    SELECT
        order_id,
        customer_id,
        product_id,
        TRY_TO_DATE(order_date, 'YYYY-MM-DD')   AS order_date,
        TRY_TO_DATE(ship_date,  'YYYY-MM-DD')   AS ship_date,
        quantity::INT                            AS quantity,
        unit_price::FLOAT                        AS unit_price,
        discount::FLOAT                          AS discount,
        total_amount::FLOAT                      AS total_amount,
        UPPER(TRIM(status))                      AS status,
        TRIM(payment_method)                     AS payment_method,
        TRIM(shipping_method)                    AS shipping_method,
        UPPER(region)                            AS region,

        -- Derived columns
        DATEDIFF(
            'day',
            TRY_TO_DATE(order_date, 'YYYY-MM-DD'),
            TRY_TO_DATE(ship_date,  'YYYY-MM-DD')
        )                                        AS days_to_ship,

        CASE
            WHEN UPPER(status) = 'COMPLETED'
            THEN 1 ELSE 0
        END                                      AS is_completed,

        DATE_TRUNC(
            'month',
            TRY_TO_DATE(order_date, 'YYYY-MM-DD')
        )                                        AS order_month,

        loaded_at

    FROM source
    WHERE order_id IS NOT NULL
)

SELECT * FROM cleaned