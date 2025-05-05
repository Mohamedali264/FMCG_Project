import pandas as pd
from data.db_connection import fetch_data
import pygwalker as pyg
import os

JOIN_QUERY = """
SELECT
    s.date,
    o.outlet_id,
    o.outlet_name,
    p.product_id,
    p.product_name,
    r.employee_code,
    r.employee_name,
    w.warehouse_name,
    t.ac,
    s.total_sales
FROM sales s
LEFT JOIN outlets o ON s.outlet_id = o.outlet_id
LEFT JOIN products p ON s.product_code = p.product_code
LEFT JOIN rep_list r ON s.employee_name = r.employee_name
LEFT JOIN warehouse w ON s.warehouse_name = w.warehouse_name
LEFT JOIN target t ON s.employee_name = t.employee_name;
"""

def generate_pyg_report():
    df = fetch_data(JOIN_QUERY)
    html_str = pyg.to_html(df)

    file_path = os.path.join("assets", "pyg_report.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_str)
    
    return file_path
