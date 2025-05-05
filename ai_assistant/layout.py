from dash import html, dcc
from data.db_connection import TABLE_QUERIES

def ai_assistant_layout():
    return html.Div([
        html.H3("🤖 AI Assistant", style={"color": "#001845", "fontWeight": "bold"}),

        html.Div([
            dcc.Dropdown(
                id="ai-table-selector",
                options=[{"label": name, "value": name} for _, (name, _) in TABLE_QUERIES.items()],
                multi=True,
                placeholder="Select one or more tables to analyze",
                style={
                    "marginBottom": "15px",
                    "borderRadius": "8px",
                    "padding": "5px"
                }
            ),

            dcc.Textarea(
                id="user-question",
                placeholder="Ask your question here...",
                style={
                    "width": "100%",
                    "height": "120px",
                    "borderRadius": "8px",
                    "padding": "10px",
                    "fontSize": "16px",
                    "resize": "none"
                }
            ),

            html.Br(),

        html.Div([
            html.Button("Ask", id="ask-button", n_clicks=0, className="btn btn-primary", style={"marginRight": "10px"}),
            html.Button("🧹 Clear Chat", id="clear-chat", n_clicks=0, className="btn btn-secondary", style={"marginRight": "10px"}),
            html.Button("📥 Download PDF", id="download-pdf", n_clicks=0, className="btn btn-success")
        ], style={"textAlign": "right", "marginBottom": "20px"}),


            html.Br(),

            html.Div(id="error-msg", style={"color": "red", "marginBottom": "10px"}),  # 👈 لإظهار رسائل الخطأ

            dcc.Loading(
                id="loading-ai-response",
                type="circle",
                children=html.Div(id="chat-history")
            )
        ], style={
            "backgroundColor": "var(--card-background)",
            "padding": "30px",
            "borderRadius": "15px",
            "boxShadow": "0px 4px 12px rgba(0,0,0,0.1)"
        })

    ], style={"padding": "40px"})
