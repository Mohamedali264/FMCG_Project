from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([

    # Section 1 - Welcome
    dbc.Row([
        dbc.Col([
            html.H2("👋 Welcome to FMCG AI Dashboard", className="text-center fw-bold text-primary"),
            html.P("Your all-in-one solution for data analysis, visualization, and AI-powered insights.",
                className="text-center fs-5")
        ])
    ], className="my-4"),

    # Section 2 - Project Overview
    dbc.Row([
        dbc.Col([
            html.H4("📘 About the Project", className="text-centertext-primary fw-semibold"),
            html.P(
                "This dashboard integrates powerful tools for data analysis including AI Assistant, YData Profiling, and Pygwalker. "
                "It also includes insights via Excel Dashboards, Power BI, Tableau, and 30+ SQL queries to explore real-world FMCG data.",
                className="fs-6"
            )
        ])
    ], className="mb-5"),

    # Section 3 - Stats Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("📊 Total Tables", className="fw-bold text-center"),
            dbc.CardBody(html.H4("4", className="text-center"))
        ], className="shadow-sm rounded"), md=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("📁 Uploaded Files", className="fw-bold text-center"),
            dbc.CardBody(html.H4("1", className="text-center"))
        ], className="shadow-sm rounded"), md=4),

        dbc.Col(dbc.Card([
            dbc.CardHeader("🤖 AI Queries", className="fw-bold text-center"),
            dbc.CardBody(html.H4("12", className="text-center"))
        ], className="shadow-sm rounded"), md=4),
    ], className="mb-5 gy-3"),

    # Section 4 - Navigation Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("📊 Visualizations", className="card-title"),
                html.P("Explore dynamic charts and visuals."),
                dcc.Link("Go", href="/visualization", className="btn btn-primary")
            ])
        ], className="shadow-sm rounded"), md=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("📂 Upload CSV", className="card-title"),
                html.P("Upload your own datasets for analysis."),
                dcc.Link("Go", href="/upload", className="btn btn-primary")
            ])
        ], className="shadow-sm rounded"), md=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("🤖 AI Assistant", className="card-title"),
                html.P("Chat with AI to explore your data."),
                dcc.Link("Go", href="/chatbot", className="btn btn-primary")
            ])
        ], className="shadow-sm rounded"), md=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("📋 YData Profiling", className="card-title"),
                html.P("Generate automated data profiles."),
                dcc.Link("Go", href="/ydata-profile", className="btn btn-outline-secondary")
            ])
        ], className="shadow-sm rounded"), md=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("📈 Pygwalker", className="card-title"),
                html.P("Drag-and-drop data exploration."),
                dcc.Link("Go", href="/pygwalker", className="btn btn-outline-secondary")
            ])
        ], className="shadow-sm rounded"), md=4),
    ], className="gy-4 mb-5"),

    # Section 5 - About Me with Image
    dbc.Row([
        # Image
        dbc.Col([
            html.Img(src="/assets/IMG_0112.jpg", style={
                "width": "100%", "maxWidth": "300px",
                "borderRadius": "50%", "boxShadow": "0 4px 8px rgba(0,0,0,0.2)"
            })
        ], md=4, className="d-flex justify-content-center align-items-center"),

        # Text
        dbc.Col([
            html.H4("🙋 About Me", className="text-primary fw-semibold"),
            html.H5("Mohamed Ali", className="fw-bold mb-1"),
            html.P("Data Analyst", className="text-muted"),
            html.P(
                "Data Analyst with a strong foundation in Python and SQL, experienced in leading teams and delivering actionable insights "
                "through data analysis. Adept at leveraging advanced tools to streamline workflows, enhance decision-making, and achieve organizational goals.",
                className="fs-6"
            ),
            html.A("🔗 LinkedIn Profile", href="https://www.linkedin.com/in/mohamed-ali-hassan-a33b40320/", target="_blank")
        ], md=8)
    ], className="mb-5 gy-4")

], fluid=True, className="pt-4")
