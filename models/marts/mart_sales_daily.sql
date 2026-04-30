WITH orders AS (
    -- Pull from STAGING not RAW
    SELECT * FROM {{ ref('stg_orders') }}
),

daily_sales AS (
    SELECT
        order_date,
        region,
        COUNT(order_id)                    AS total_orders,
        SUM(total_amount)                  AS total_revenue,
        AVG(total_amount)                  AS avg_order_value,
        SUM(CASE WHEN is_completed = 1
            THEN total_amount ELSE 0
            END)                           AS completed_revenue,
        COUNT(CASE WHEN is_completed = 1
            THEN 1 END)                    AS completed_orders,
        SUM(CASE WHEN status = 'CANCELLED'
            THEN 1 ELSE 0
            END)                           AS cancelled_orders,
        SUM(quantity)                      AS total_units_sold
    FROM orders
    GROUP BY order_date, region
)

SELECT * FROM daily_sales
ORDER BY order_date DESC, total_revenue DESC