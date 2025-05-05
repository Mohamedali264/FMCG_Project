from dash import html, dcc

def upload_layout():
    return html.Div([
        html.H2("📤 Upload & Analyze Your Data", className="fw-bold", style={"color": "var(--text-color)"}),

        html.P("Upload your CSV or Excel file and explore it using AutoClean, YData Profiling, and Pygwalker.",
            className="text-muted", style={"fontSize": "1rem"}),

        html.Hr(),
        
        dcc.Store(id="upload-data-store"),

        # Upload Area
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.I(className="bi bi-cloud-arrow-up-fill me-2"),
                "Drag & Drop or ",
                html.A("Browse File", style={"color": "var(--primary-color)", "textDecoration": "underline"})
            ]),
            style={
                'width': '100%',
                'height': '120px',
                'lineHeight': '120px',
                'borderWidth': '2px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'backgroundColor': 'var(--card-background)',
                'color': 'var(--text-color)',
                'cursor': 'pointer',
                'marginBottom': '20px'
            },
            multiple=False
        ),

        html.Div(id="file-info", style={"marginBottom": "10px"}),

        # Table Preview
        html.Div(id='uploaded-preview'),

        # Buttons
        html.Div([
            html.Button("🧹 Clean with AutoClean", id="clean-autoclean-btn", n_clicks=0, className="btn btn-warning me-2"),
            html.Button("📋 YData Report", id="gen-ydata-btn", n_clicks=0, className="btn btn-outline-primary me-2"),
            html.Button("🧠 Pygwalker", id="open-pygwalker-btn", n_clicks=0, className="btn btn-outline-secondary me-2"),
            html.Button("🗑️ Clear", id="clear-upload-report", n_clicks=0, className="btn btn-outline-danger"),
            html.Button("🗑️ Delete Old Reports", id="clear-upload-old-reports", n_clicks=0, className="btn btn-danger"),
        ], id="upload-action-buttons", style={"display": "none", "marginTop": "20px"}),

        html.Hr(),

        html.Div(id="report-output")
    ], style={"padding": "30px"})
