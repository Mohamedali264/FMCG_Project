# visualizations/layout.py

from dash import html, dcc
from visualizations.charts import QUERIES

def visualizations_layout():
    return html.Div([
        html.H2("📊 Data Visualizations", style={
            "textAlign": "center",
            "fontWeight": "bold",
            "color": "var(--text-color)",
            "marginBottom": "30px"
        }),
        
        html.Div([
            dcc.Dropdown(
                id='chart-selector',
                options=[{"label": v["title"], "value": i} for i, v in QUERIES.items()],
                value=1,
                clearable=False,
                placeholder="Select a chart...",
                style={
                    "width": "60%",
                    "margin": "auto",
                    "marginBottom": "20px",
                    "backgroundColor": "var(--input-background)",
                    "color": "var(--text-color)",
                    "border": "1px solid var(--border-color)",
                    "borderRadius": "10px",
                    "padding": "10px"
                }
            ),
            
            html.Div([
                dcc.Loading(
                    id="loading-graph",
                    type="circle",
                    color="var(--primary-color)",
                    children=[
                        html.Div(
                            dcc.Graph(id="chart-display"),
                            className="graph-container"
                        )
                    ]
                )
            ], style={"padding": "20px"})
            
        ], style={
            "backgroundColor": "var(--card-background)",
            "padding": "30px",
            "borderRadius": "15px",
            "boxShadow": "0px 4px 10px rgba(0,0,0,0.1)",
            "maxWidth": "1200px",
            "margin": "auto"
        })
    ], style={"padding": "50px 20px"})
