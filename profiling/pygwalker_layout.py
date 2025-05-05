from dash import html

def pygwalker_layout():
    return html.Div([
        html.H3("🧠 Manage Pygwalker Reports", style={"color": "#001845", "fontWeight": "bold"}),
        html.Br(),
        html.Div([
            html.Button("🗑️ Clear Old Reports", id="clear-reports-btn", n_clicks=0, className="btn btn-danger me-2"),
            html.Button("⚙️ Generate Report", id="generate-report-btn", n_clicks=0, className="btn btn-primary me-2"),
            html.Button("📄 View Report", id="view-report-btn", n_clicks=0, className="btn btn-success", disabled=True),
        ]),
        html.Br(), html.Br(),
        html.Div(id="pygwalker-report-container")
    ], style={"padding": "20px"})
