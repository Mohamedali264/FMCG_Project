# db_connection.py
import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONFIG

def fetch_data(query):
    # مسار الشهادة
    ssl_ca_path = DB_CONFIG["ssl_ca"]

    # بناء URL الاتصال مع دعم الـ SSL
    url = (
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}?ssl_ca={ssl_ca_path}"
    )

    engine = create_engine(url)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    return df

# Dictionary of tables and their queries
TABLE_QUERIES = {
    1: ("Outlets", "SELECT * FROM outlets;"),
    2: ("Sales", "SELECT * FROM sales;"),
    3: ("Return_products", "SELECT * FROM return_products;"),
    4: ("Visits", "SELECT * FROM visits;"),
    5: ("Warehouse", "SELECT * FROM warehouse;"),
    6: ("Rep_list", "SELECT * FROM rep_list;"),
    7: ("Target", "SELECT * FROM target;"),
    8: ("Products", "SELECT * FROM products;"),
}
