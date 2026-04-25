import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# ── SETUP ────────────────────────────────────────────
fake = Faker()
random.seed(42)
Faker.seed(42)

NUM_CUSTOMERS = 1000
NUM_PRODUCTS  = 100
NUM_ORDERS    = 10000
OUTPUT_DIR    = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── CUSTOMERS ────────────────────────────────────────
print("Generating customers...")

REGIONS   = ["North", "South", "East", "West", "Central"]
SEGMENTS  = ["Consumer", "Corporate", "Home Office"]

customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id"  : f"CUST-{i:04d}",
        "first_name"   : fake.first_name(),
        "last_name"    : fake.last_name(),
        "email"        : fake.unique.email(),
        "phone"        : fake.phone_number(),
        "city"         : fake.city(),
        "state"        : fake.state(),
        "region"       : random.choice(REGIONS),
        "segment"      : random.choice(SEGMENTS),
        "created_date" : fake.date_between(
                            start_date="-3y",
                            end_date="today"
                         ).strftime("%Y-%m-%d"),
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)
print(f"  customers.csv -- {len(customers_df)} rows")

# ── PRODUCTS ─────────────────────────────────────────
print("Generating products...")

CATEGORIES = ["Electronics","Clothing","Food",
              "Books","Home","Sports","Beauty"]
SUB_CATEGORIES = {
    "Electronics" : ["Phones","Laptops","Tablets","Cameras"],
    "Clothing"    : ["Men","Women","Kids","Sports"],
    "Food"        : ["Snacks","Beverages","Dairy","Bakery"],
    "Books"       : ["Fiction","Non-Fiction","Education","Comics"],
    "Home"        : ["Furniture","Kitchen","Decor","Garden"],
    "Sports"      : ["Fitness","Outdoor","Team Sports","Water"],
    "Beauty"      : ["Skincare","Haircare","Makeup","Fragrance"],
}

products = []
for i in range(1, NUM_PRODUCTS + 1):
    cat = random.choice(CATEGORIES)
    products.append({
        "product_id"   : f"PROD-{i:04d}",
        "product_name" : fake.catch_phrase(),
        "category"     : cat,
        "sub_category" : random.choice(SUB_CATEGORIES[cat]),
        "unit_price"   : round(random.uniform(5.0, 999.99), 2),
        "cost_price"   : round(random.uniform(2.0, 500.00), 2),
        "supplier"     : fake.company(),
        "is_active"    : random.choice([True, True, True, False]),
        "launch_date"  : fake.date_between(
                            start_date="-5y",
                            end_date="today"
                         ).strftime("%Y-%m-%d"),
    })

products_df = pd.DataFrame(products)
products_df.to_csv(f"{OUTPUT_DIR}/products.csv", index=False)
print(f"  products.csv -- {len(products_df)} rows")

# ── ORDERS ───────────────────────────────────────────
print("Generating orders...")

STATUS_LIST  = ["Completed","Completed","Completed",
                "Pending","Cancelled","Returned"]
PAYMENT_LIST = ["Credit Card","Debit Card",
                "UPI","Net Banking","Cash on Delivery"]
SHIP_LIST    = ["Standard","Express","Same Day","Economy"]

orders      = []
start_date  = datetime.now() - timedelta(days=365 * 2)

for i in range(1, NUM_ORDERS + 1):
    cust       = random.choice(customers)
    prod       = random.choice(products)
    qty        = random.randint(1, 10)
    price      = prod["unit_price"]
    discount   = round(random.uniform(0, 0.30), 2)
    amount     = round(qty * price * (1 - discount), 2)
    order_date = start_date + timedelta(
                    days=random.randint(0, 730))

    orders.append({
        "order_id"        : f"ORD-{i:06d}",
        "customer_id"     : cust["customer_id"],
        "product_id"      : prod["product_id"],
        "order_date"      : order_date.strftime("%Y-%m-%d"),
        "ship_date"       : (order_date + timedelta(
                                days=random.randint(1, 7))
                            ).strftime("%Y-%m-%d"),
        "quantity"        : qty,
        "unit_price"      : price,
        "discount"        : discount,
        "total_amount"    : amount,
        "status"          : random.choice(STATUS_LIST),
        "payment_method"  : random.choice(PAYMENT_LIST),
        "shipping_method" : random.choice(SHIP_LIST),
        "region"          : cust["region"],
    })

orders_df = pd.DataFrame(orders)
orders_df.to_csv(f"{OUTPUT_DIR}/orders.csv", index=False)
print(f"  orders.csv -- {len(orders_df)} rows")

# ── SUMMARY ──────────────────────────────────────────
print("\n" + "="*45)
print("  DATA GENERATION COMPLETE!")
print("="*45)
print(f"  Customers : {len(customers_df):,}")
print(f"  Products  : {len(products_df):,}")
print(f"  Orders    : {len(orders_df):,}")
print(f"  Total rows: {len(customers_df)+len(products_df)+len(orders_df):,}")
print(f"\n  Files saved to: {OUTPUT_DIR}/")
print("  Ready for Snowflake loading!")
print("="*45)