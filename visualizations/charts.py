# charts.py

import plotly.express as px
import plotly.graph_objs as go
from data.db_connection import fetch_data

# Queries Dictionary
QUERIES = {
    1: {
        "title": "Top 10 Warehouses by Sales",
        "query": """
            SELECT w.warehouse_name, SUM(s.total_sales) AS warehouse_sales
            FROM warehouse AS w
            LEFT JOIN sales AS s
            USING (warehouse_name)
            GROUP BY w.warehouse_name
            ORDER BY warehouse_sales DESC
            LIMIT 10;
        """,
        "plot_function": "plot_warehouses_per_sales"
    },
    2: {
        "title": "Top 10 Products by Total Sales",
        "query": """
            SELECT p.product_name, SUM(s.total_sales) AS sum_product_sales
            FROM products p
            INNER JOIN sales s ON p.product_code = s.product_code
            GROUP BY p.product_name
            ORDER BY sum_product_sales DESC
            LIMIT 10;
        """,
        "plot_function": "plot_top_10_products_sales"
    },
    3: {
        "title": "Sales by Region",
        "query": """
            SELECT r.region, SUM(s.total_sales) AS sum_sales
            FROM rep_list AS r
            LEFT JOIN sales AS s USING (employee_name)
            GROUP BY r.region
            ORDER BY sum_sales DESC;
        """,
        "plot_function": "plot_sales_by_region"
    },
    4: {
        "title": "Monthly Growth Rate (2020-2021)",
        "query": """
            SELECT 
                YEAR(date) AS year, 
                MONTH(date) AS month, 
                SUM(total_sales) AS total_sales, 
                LAG(SUM(total_sales)) OVER (ORDER BY YEAR(date), MONTH(date)) AS prev_month_sales,
                (SUM(total_sales) - LAG(SUM(total_sales)) OVER (ORDER BY YEAR(date), MONTH(date))) / 
                NULLIF(LAG(SUM(total_sales)) OVER (ORDER BY YEAR(date), MONTH(date)), 0) * 100 AS growth_rate
            FROM sales
            GROUP BY year, month
            ORDER BY year, month;
        """,
        "plot_function": "plot_monthly_growth_rate"
    },
    5: {
        "title": "Quarterly Growth Rate (2020-2021)",
        "query": """
            SELECT 
                YEAR(date) AS year,
                QUARTER(date) AS quarter,
                SUM(total_sales) AS total_sales, 
                LAG(SUM(total_sales)) OVER (ORDER BY YEAR(date), QUARTER(date)) AS prev_quarter_sales,
                (SUM(total_sales) - LAG(SUM(total_sales)) OVER (ORDER BY YEAR(date), QUARTER(date))) / 
                NULLIF(LAG(SUM(total_sales)) OVER (ORDER BY YEAR(date), QUARTER(date)), 0) * 100 AS growth_rate
            FROM sales
            GROUP BY YEAR(date), QUARTER(date)
            ORDER BY year, quarter;
        """,
        "plot_function": "plot_quarterly_growth_rate"
    },
    6: {
        "title": "Product Sales Timeline",
        "query": """
            SELECT 
                s.Product_Name, 
                s.Date, 
                s.Warehouse_Name, 
                s.Quantity, 
                s.Total_Sales
            FROM sales s
            ORDER BY s.Product_Name, s.Date;
        """,
        "plot_function": "plot_product_sales_timeline"
    },
    7: {
        "title": "Top 10 Outlets by Sales (Overall)",
        "query": """
            SELECT o.outlet_name, o.outlet_class, SUM(s.total_sales) AS the_total_of_sales
            FROM outlets AS o
            INNER JOIN sales AS s ON o.outlet_id = s.outlet_id 
            GROUP BY o.outlet_name, o.outlet_class 
            ORDER BY the_total_of_sales DESC
            LIMIT 10;
        """,
        "plot_function": "plot_outlets_by_sales"
    },
    8: {
        "title": "Employee Target Achievement Status",
        "query": """
            SELECT 	
                employee_code, 
                employee_name,
                CASE 
                    WHEN AC >= 100 THEN 'Achieve the target'
                    WHEN AC < 100 THEN 'Target not achieved'
                END AS 'Target achievement'
            FROM target;
        """,
        "plot_function": "plot_employee_target"
    },
    9: {
        "title": "Product Ranking by Price Within Category",
        "query": """
            SELECT DISTINCT category, price,
                DENSE_RANK() OVER (ORDER BY price) AS rank_category
            FROM products
            ORDER BY rank_category DESC;
        """,
        "plot_function": "plot_product_ranking"
    },
    10: {
        "title": "Most Returned Products",
        "query": """
            SELECT p.product_name, SUM(r.quantity) AS quantity_product
            FROM products AS p
            LEFT JOIN return_products AS r
            USING (product_code)
            GROUP BY p.product_name
            ORDER BY quantity_product DESC
            LIMIT 10;
        """,
        "plot_function": "plot_most_return_products"
    }
}



# Helpers
def apply_theme(fig, theme):
    if theme == "dark":
        fig.update_layout(
            paper_bgcolor="#003566",
            plot_bgcolor="#003566",
            font_color="#f0f0f0",
            xaxis=dict(color="#f0f0f0"),
            yaxis=dict(color="#f0f0f0"),
        )
    else:
        fig.update_layout(
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font_color="#001845",
            xaxis=dict(color="#001845"),
            yaxis=dict(color="#001845"),
        )
    return fig

# 1- Warehouses by Sales
def plot_warehouses_per_sales(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.bar(df, x="warehouse_sales", y="warehouse_name", orientation='h',
                title="Top 10 Warehouses by Sales",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 2- Top 10 Products Sales
def plot_top_10_products_sales(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.bar(df, x="sum_product_sales", y="product_name", orientation='h',
                title="Top 10 Products by Total Sales",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 3- Sales by Region
def plot_sales_by_region(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.pie(df, names="region", values="sum_sales",
                title="Sales by Region",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 4- Monthly Growth Rate
def plot_monthly_growth_rate(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.line(df, x=["month"], y="growth_rate", markers=True,
                title="Monthly Growth Rate (2020-2021)",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 5- Quarterly Growth Rate
def plot_quarterly_growth_rate(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.line(df, x=["quarter"], y="growth_rate", markers=True,
                title="Quarterly Growth Rate (2020-2021)",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 6- Product Sales Timeline
def plot_product_sales_timeline(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.line(df, x="Date", y="Total_Sales", color="Product_Name",
                title="Product Sales Timeline",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 7- Outlets by Sales
def plot_outlets_by_sales(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.bar(df, x="the_total_of_sales", y="outlet_name", orientation='h',
                title="Top 10 Outlets by Sales (Overall)",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 8- Employee Target Achievement
def plot_employee_target(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.pie(df, names="Target achievement", title="Employee Target Achievement Status",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 9- Product Ranking by Price
def plot_product_ranking(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.bar(df, x="rank_category", y="price",
                title="Product Ranking by Price Within Category",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# 10- Most Returned Products
def plot_most_return_products(df, theme="light"):
    color = "#4EA8DE" if theme == "dark" else "#0466C8"
    fig = px.bar(df, x="quantity_product", y="product_name", orientation='h',
                title="Most Returned Products",
                color_discrete_sequence=[color])
    return apply_theme(fig, theme)

# داخل visualizations/charts.py

def get_chart(chart_id, theme="light"):
    if chart_id not in QUERIES:
        return go.Figure()

    query_info = QUERIES.get(chart_id)
    query = query_info.get("query")
    plot_function_name = query_info.get("plot_function")

    if not query or not plot_function_name:
        return go.Figure()

    try:
        df = fetch_data(query)
        print(f"[DEBUG] DataFrame for chart {chart_id}:\n", df.head())
        print("[DEBUG] Columns:", df.columns)
        print("[DEBUG] Number of Rows:", len(df))
    except Exception as e:
        print(f"[Error] Failed fetching data: {e}")
        return go.Figure()

    if plot_function_name in globals():
        plot_function = globals()[plot_function_name]
        return plot_function(df, theme)
    else:
        return go.Figure()
