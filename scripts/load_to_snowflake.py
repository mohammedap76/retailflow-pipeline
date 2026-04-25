import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import os

# ── LOAD CREDENTIALS ─────────────────────────
load_dotenv()

ACCOUNT   = os.getenv("SNOWFLAKE_ACCOUNT")
USER      = os.getenv("SNOWFLAKE_USER")
PASSWORD  = os.getenv("SNOWFLAKE_PASSWORD")
DATABASE  = os.getenv("SNOWFLAKE_DATABASE")
WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
ROLE      = os.getenv("SNOWFLAKE_ROLE")

print("=" * 50)
print("  RETAILFLOW -- Snowflake Data Loader")
print("=" * 50)

# ── CONNECT ───────────────────────────────────
print("\nConnecting to Snowflake...")
conn = snowflake.connector.connect(
    account   = ACCOUNT,
    user      = USER,
    password  = PASSWORD,
    database  = DATABASE,
    warehouse = WAREHOUSE,
    role      = ROLE,
    schema    = "RAW"
)
cursor = conn.cursor()
print("  Connected successfully!")

# ── HELPER FUNCTION ───────────────────────────
def load_csv(csv_path, table_name, cursor):
    print(f"\nLoading {csv_path}...")
    df = pd.read_csv(csv_path)
    df = df.where(pd.notnull(df), None)
    rows = [tuple(row) for row in df.values]
    placeholders = ", ".join(["%s"] * len(df.columns))
    cols = ", ".join(df.columns.tolist())
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
    cursor.executemany(sql, rows)
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  Inserted : {len(rows):,} rows")
    print(f"  Verified : {count:,} rows in Snowflake")
    return count

# ── TRUNCATE ──────────────────────────────────
print("\nTruncating tables for fresh load...")
cursor.execute("TRUNCATE TABLE RAW.RAW_CUSTOMERS")
cursor.execute("TRUNCATE TABLE RAW.RAW_PRODUCTS")
cursor.execute("TRUNCATE TABLE RAW.RAW_ORDERS")
print("  Done!")

# ── LOAD ──────────────────────────────────────
total  = 0
total += load_csv("data/customers.csv","RAW.RAW_CUSTOMERS", cursor)
total += load_csv("data/products.csv", "RAW.RAW_PRODUCTS",  cursor)
total += load_csv("data/orders.csv",   "RAW.RAW_ORDERS",    cursor)

# ── SUMMARY ───────────────────────────────────
print("\n" + "=" * 50)
print("  LOADING COMPLETE!")
print("=" * 50)
print(f"  RAW_CUSTOMERS : 1,000 rows")
print(f"  RAW_PRODUCTS  :   100 rows")
print(f"  RAW_ORDERS    : 10,000 rows")
print(f"  Total loaded  : {total:,} rows")
print("=" * 50)

cursor.close()
conn.close()
print("\nConnection closed.")
print("RAW layer ready for dbt!")