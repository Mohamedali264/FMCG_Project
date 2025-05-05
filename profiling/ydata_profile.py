import os
import pandas as pd
from ydata_profiling import ProfileReport
from data.db_connection import fetch_data
from data.db_connection import TABLE_QUERIES
from utils.helpers import clean_old_reports  # ✨ استدعاء الدالة الجديدة

# نخلي التقرير يتولد في assets مباشرة
REPORTS_DIR = "assets"
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_profile_report(table_id: int) -> str:
    """
    Generates a ydata profiling report for the selected table.

    Args:
        table_id (int): ID of the table as defined in TABLE_QUERIES.

    Returns:
        str: Path to the generated HTML report.
    """
    if table_id not in TABLE_QUERIES:
        raise ValueError("Invalid table ID.")

    table_name, query = TABLE_QUERIES[table_id]
    df = fetch_data(query)

    # ✨ امسح أي تقرير قديم بنفس اسم الجدول
    clean_old_reports(prefix=f"{table_name.lower()}_profile_report", directory=REPORTS_DIR)

    report = ProfileReport(df, title=f"Profiling Report - {table_name}", explorative=True)

    output_path = os.path.join(REPORTS_DIR, f"{table_name.lower()}_profile_report.html")
    report.to_file(output_path)

    return output_path
