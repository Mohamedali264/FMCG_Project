# profiling/layout.py

from dash import html, dcc
from data.db_connection import TABLE_QUERIES

def profiling_layout():
    return html.Div([
        html.H3("📋 YData Profiling", style={"color": "#001845", "fontWeight": "bold"}),
        html.Br(),
        dcc.Dropdown(
            id="table-selector",
            options=[
                {"label": name, "value": table_id} 
                for table_id, (name, _) in TABLE_QUERIES.items()
            ],
            placeholder="Select a table...",
            style={"width": "50%"}
        ),
        html.Br(),
        html.Button("🗑️ Clear Old Reports", id="clear-old-ydata-btn", className="btn btn-outline-danger me-2"),
        html.Button("📊 Generate Report", id="generate-report-btn", className="btn btn-primary"),
        html.Br(), html.Br(),
        html.Div(id="report-container")
    ], style={"padding": "20px"})
