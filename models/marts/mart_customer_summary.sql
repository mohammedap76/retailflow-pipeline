WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

customer_orders AS (
    SELECT
        o.customer_id,
        COUNT(o.order_id)              AS total_orders,
        SUM(o.total_amount)            AS lifetime_value,
        AVG(o.total_amount)            AS avg_order_value,
        MIN(o.order_date)              AS first_order_date,
        MAX(o.order_date)              AS last_order_date,
        SUM(o.is_completed)            AS completed_orders,
        SUM(CASE WHEN o.status = 'CANCELLED'
            THEN 1 ELSE 0 END)         AS cancelled_orders,
        SUM(o.quantity)                AS total_units_bought,
        DATEDIFF('day',
            MIN(o.order_date),
            MAX(o.order_date))         AS customer_age_days
    FROM orders o
    GROUP BY o.customer_id
),

final AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.region,
        c.segment,
        c.created_date,
        co.total_orders,
        co.lifetime_value,
        co.avg_order_value,
        co.first_order_date,
        co.last_order_date,
        co.completed_orders,
        co.cancelled_orders,
        co.total_units_bought,
        co.customer_age_days,

        -- Customer segmentation
        CASE
            WHEN co.lifetime_value >= 10000 THEN 'Platinum'
            WHEN co.lifetime_value >= 5000  THEN 'Gold'
            WHEN co.lifetime_value >= 1000  THEN 'Silver'
            ELSE 'Bronze'
        END                            AS customer_tier

    FROM customers c
    LEFT JOIN customer_orders co
        ON c.customer_id = co.customer_id
)

SELECT * FROM final
ORDER BY lifetime_value DESC NULLS LAST