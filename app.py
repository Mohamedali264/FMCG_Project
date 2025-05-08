# app.py
import base64
import os
import uuid
import base64
import io
import dash
import pandas as pd
from dash import html, dcc, Input, Output, State, ctx, no_update, callback_context
import dash_bootstrap_components as dbc
from flask import send_from_directory
from flask import send_file
from ydata_profiling import ProfileReport
import pygwalker as pyg
from xhtml2pdf import pisa
from AutoClean.autoclean import AutoClean
import time

# Global cache
uploaded_df_upload_page = {}
    
# استيراد باقي السكربتات
from ydata_profiling import ProfileReport   
from pages.home import layout as home_layout
from pages.upload_layout import upload_layout
from visualizations.layout import visualizations_layout
from visualizations.charts import get_chart
from profiling.layout import profiling_layout
from profiling.ydata_profile import generate_profile_report
from profiling.pygwalker_layout import pygwalker_layout
from ai_assistant.layout import ai_assistant_layout
from ai_assistant.chatbot import run_chatbot
from profiling.pygwalker_view import generate_pyg_report

# إنشاء تطبيق Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "FMCG Dashboard"
server = app.server

# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dcc.Link("FMCG Dashboard", href="/",
                        style={"color": "white", "fontSize": "28px", "fontWeight": "bold", "textDecoration": "none"}),
                width="auto", className="me-auto"
            ),
            dbc.Col(
                dbc.Nav([
                    dbc.NavItem(dcc.Link("Visualizations", href="/visualizations", className="nav-link")),
                    dbc.NavItem(dcc.Link("YData Profiling", href="/profiling", className="nav-link")),
                    dbc.NavItem(dcc.Link("Pygwalker", href="/pygwalker", className="nav-link")),
                    dbc.NavItem(dcc.Link("AI Assistant", href="/ai", className="nav-link")),
                    dbc.NavItem(dcc.Link("Upload CSV", href="/upload", className="nav-link")),
                ], className="ms-auto", navbar=True),
                width="auto"
            )
        ], align="center", justify="between", className="w-100")
    ]),
    color="#001845", dark=True, className="mb-4"
)

# Layout التطبيق
app.layout = html.Div([
    html.Img(src="/assets/images/bg-sales.png", id="icon1", className="floating-icon"),
    html.Img(src="/assets/images/bg-dashboard.png", id="icon2", className="floating-icon"),
    html.Img(src="/assets/images/bg-analytics.png", id="icon3", className="floating-icon"),

    dcc.Location(id='url', refresh=False),
    navbar,
    dcc.Store(id='theme-store', data='dark'),
    dcc.Store(id='chat-store', data=[]),  # تخزين وضع الثيم
    html.Div(id='page-content'),

    html.Button("🌓", id="theme-toggle", className="theme-toggle"),
    
])

# التوجيه بين الصفحات
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/visualizations":
        return visualizations_layout()
    elif pathname == "/profiling":
        return profiling_layout()
    elif pathname == "/pygwalker":
        return pygwalker_layout()
    elif pathname == "/ai":
        return ai_assistant_layout()
    elif pathname == "/upload":
        return upload_layout()
    return html.H4("Page not found", style={"padding": "20px"})

# كولباك تغيير الثيم
@app.callback(
    Output('theme-store', 'data'),
    Input('theme-toggle', 'n_clicks'),
    State('theme-store', 'data'),
    prevent_initial_call=True
)
def toggle_theme(n_clicks, current_theme):
    return 'light' if current_theme == 'dark' else 'dark'

# كولباك ClientSide لتغيير الـ HTML attribute
app.clientside_callback(
    """
    function(theme) {
        if (theme) {
            document.documentElement.setAttribute('data-theme', theme);
        }
        return "";
    }
    """,
    Output('theme-toggle', 'title'),  # Dummy output عشان يشتغل الكولباك
    Input('theme-store', 'data')
)

# كولباك عرض الرسوم البيانية
@app.callback(
    Output("chart-display", "figure"),
    Input("chart-selector", "value"),
    Input('theme-store', 'data')
)
def update_chart(chart_id, theme):
    return get_chart(chart_id, theme)

# كولباك إنشاء تقارير ydata
@app.callback(
    Output("report-container", "children"),
    Input("generate-report-btn", "n_clicks"),
    State("table-selector", "value"),
    prevent_initial_call=True
)
def generate_report(n_clicks, table_id):
    if table_id is None:
        return html.Div("Please select a table.", style={"color": "red"})
    try:
        report_path = generate_profile_report(table_id)
        file_name = os.path.basename(report_path)

        return html.Iframe(
            src=f"/reports/{file_name}?v={int(time.time())}",  # 👈 إجبار المتصفح على تحميل جديد
            width="100%",
            height="900px",
            style={"border": "1px solid #ccc"}
        )

    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "red"})
    
@app.callback(
    Output("report-container", "children", allow_duplicate=True),
    Input("clear-old-ydata-btn", "n_clicks"),
    prevent_initial_call=True
)
def clear_old_ydata_reports(n_clicks):
    try:
        from utils.helpers import clean_old_reports
        clean_old_reports(prefix="_profile_report", directory="assets")
        return html.Div("🗑️ All old reports deleted.", style={"color": "green"})
    except Exception as e:
        return html.Div(f"❌ Failed to clear reports: {str(e)}", style={"color": "red"})

# ==========
# كولباك موحد: ارسال سؤال + Clear + مسح رسالة الخطأ
# ==========
@app.callback(
    Output("chat-store", "data"),
    Output("error-msg", "children"),
    Input("ask-button", "n_clicks"),
    Input("clear-chat", "n_clicks"),
    Input("user-question", "value"),
    Input("ai-table-selector", "value"),
    State("chat-store", "data"),
    prevent_initial_call=True
)
def update_chat(ask_clicks, clear_clicks, question, selected_tables, history):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "clear-chat":
        return [], ""

    if triggered_id in ["user-question", "ai-table-selector"]:
        raise dash.exceptions.PreventUpdate

    if triggered_id == "ask-button":
        if not question:
            return history, "⚠️ Please enter a question."
        if not selected_tables:
            return history, "⚠️ Please select at least one table."

        result = run_chatbot(question, selected_tables)

        entry = {"type": "text", "user": question}

        if isinstance(result, dict) and result.get("type") == "image":
            with open(result["path"], "rb") as f:
                encoded_image = base64.b64encode(f.read()).decode()
            entry["ai"] = {"type": "image", "src": f"data:image/png;base64,{encoded_image}"}
        else:
            ai_text = result.get("content")

            # لو الرد كان DataFrame بشكل نص، نحاول نجمّله
            if hasattr(ai_text, "to_string"):
                ai_text = ai_text.to_string(index=False)

            # أو نحاول نخليه أكثر وضوحًا إن كان منسق بشكل غريب
            elif isinstance(ai_text, str) and "\n" in ai_text and "  " in ai_text:
                lines = ai_text.splitlines()
                if len(lines) >= 2 and len(lines[0].split()) > 1:
                    # محاولة لاستخلاص الصف الأول فقط
                    headers = lines[0].split()
                    values = lines[1].split()
                    if len(headers) == len(values):
                        ai_text = f"The employee who made the most sales is {values[0]} with a total of {values[1]}."

            entry["ai"] = {"type": "text", "text": ai_text}

        return history + [entry], ""

    return history, ""

# ==========
# كولباك عرض المحادثة في الواجهة كفقاعات
# ==========
@app.callback(
    Output("chat-history", "children"),
    Input("chat-store", "data")
)
def update_chat_ui(history):
    ui = []
    for entry in history:
        user = entry.get("user", "")
        ai = entry.get("ai", {})
        ai_block = html.Div()

        if ai.get("type") == "text":
            ai_block = html.P(ai["text"], style={
                "backgroundColor": "#f1f1f1",
                "padding": "10px 15px",
                "borderRadius": "12px",
                "maxWidth": "80%",
                "color": "#001845"
            })
        elif ai.get("type") == "image":
            ai_block = html.Img(src=ai["src"], style={"maxWidth": "100%", "borderRadius": "10px"})

        ui.append(html.Div([
            html.P(f"🧑 You: {user}", className="chat-user-msg"),
            html.P("🤖 AI:", className="chat-ai-label"),
            ai_block
        ], style={"marginBottom": "25px"}))
    return ui

# ==========
# كولباك تحميل PDF
# ==========
@app.callback(
    Output("download-pdf", "n_clicks"),
    Input("download-pdf", "n_clicks"),
    State("chat-store", "data"),
    prevent_initial_call=True
)
def generate_pdf(n, chat_history):
    if not chat_history:
        return no_update

    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial; padding: 20px; }
            .bubble { padding: 10px 15px; border-radius: 12px; margin-bottom: 15px; max-width: 80%; }
            .user { background-color: #0466C8; color: white; margin-left: auto; }
            .ai { background-color: #f1f1f1; color: #001845; }
        </style>
    </head>
    <body>
        <h2>AI Chat History</h2>
    """

    for entry in chat_history:
        user = entry.get("user", "")
        ai = entry.get("ai", {})
        html_content += f'<div class="bubble user">🧑 You: {user}</div>'

        if ai.get("type") == "text":
            html_content += f'<div class="bubble ai">🤖 AI: {ai["text"]}</div>'

    html_content += "</body></html>"

    filename = f"chat_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join("exports", filename)

    with open(pdf_path, "wb") as f:
        pisa.CreatePDF(html_content, dest=f)

    with open("latest_pdf.txt", "w") as f:
        f.write(pdf_path)

    import webbrowser
    webbrowser.open_new_tab("http://127.0.0.1:8050/download_chat_pdf")

    return no_update

# Upload CSV 
@app.callback(
    Output("file-info", "children"),
    Output("uploaded-preview", "children"),
    Output("upload-action-buttons", "style"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def handle_upload(contents, filename):
    if not contents:
        return "No file uploaded.", "", {"display": "none"}

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    ext = os.path.splitext(filename)[-1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return f"❌ Unsupported file type: {ext}", "", {"display": "none"}

        uploaded_df_upload_page["data"] = df

        preview = html.Div([
            dcc.Loading(
                dcc.Graph(figure={
                    "data": [{
                        "type": "table",
                        "header": {"values": list(df.columns)},
                        "cells": {"values": [df[col] for col in df.columns]}
                    }],
                    "layout": {"height": 400}
                })
            )
        ])

        return html.Div(f"📁 File uploaded: {filename}"), preview, {"display": "block"}

    except Exception as e:
        return f"❌ Failed to read file: {str(e)}", "", {"display": "none"}
    
@app.callback(
    Output("report-output", "children"),
    Input("clean-autoclean-btn", "n_clicks"),
    Input("gen-ydata-btn", "n_clicks"),
    Input("open-pygwalker-btn", "n_clicks"),
    Input("clear-upload-report", "n_clicks"),
    prevent_initial_call=True
)
def handle_upload_buttons(clean_click, ydata_click, pygwalker_click, clear_click):
    triggered_id = ctx.triggered_id
    df = uploaded_df_upload_page.get("data")

    if not isinstance(df, pd.DataFrame):
        return html.Div("⚠️ Please upload a valid file first.", style={"color": "red"})

    # Clean
    if triggered_id == "clean-autoclean-btn":
        try:
            cleaner = AutoClean(df)
            cleaned = cleaner.output
            uploaded_df_upload_page["data"] = cleaned  # تحديث النسخة
            return html.Div("✅ Cleaned successfully.", style={"color": "green"})
        except Exception as e:
            return html.Div(f"❌ Cleaning failed: {str(e)}", style={"color": "red"})

    # Generate YData-style report
    elif triggered_id == "gen-ydata-btn":
        try:
            os.makedirs("assets/upload_reports", exist_ok=True)
            file_name = f"upload_report_{uuid.uuid4().hex[:6]}.html"
            file_path = os.path.join("assets/upload_reports", file_name)
            report = ProfileReport(df, title="Uploaded File Report", explorative=True)
            report.to_file(file_path)
            return html.Iframe(src=f"/upload-report/{file_name}", width="100%", height="900px", style={"border": "1px solid #ccc"})
        except Exception as e:
            return html.Div(f"❌ Report failed: {str(e)}", style={"color": "red"})

    # Generate Pygwalker-style HTML
    elif triggered_id == "open-pygwalker-btn":
        try:
            import pygwalker as pyg
            html_str = pyg.to_html(df)
            path = os.path.join("assets", "upload_pyg_report.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(html_str)
            return html.Iframe(src="/upload-pygwalker-report", width="100%", height="900px", style={"border": "1px solid #ccc"})
        except Exception as e:
            return html.Div(f"❌ Failed to generate Pygwalker view: {str(e)}", style={"color": "red"})

    # Clear
    elif triggered_id == "clear-upload-report":
        uploaded_df_upload_page.clear()
        return html.Div("🧹 Upload cleared.", style={"color": "green"})

    return ""

@app.callback(
    Output("report-output", "children", allow_duplicate=True),
    Input("clear-upload-old-reports", "n_clicks"),
    prevent_initial_call=True
)
def delete_old_upload_reports(n_clicks):
    try:
        deleted = []

        # 🧹 احذف ملف Pygwalker المؤقت (لو موجود)
        pyg_path = os.path.join("assets", "upload_pyg_report.html")
        if os.path.exists(pyg_path):
            os.remove(pyg_path)
            deleted.append("upload_pyg_report.html")

        # 🧹 احذف ملفات التقارير من upload_reports
        upload_reports_path = os.path.join("assets", "upload_reports")
        if os.path.exists(upload_reports_path):
            for f in os.listdir(upload_reports_path):
                if f.endswith(".html"):
                    os.remove(os.path.join(upload_reports_path, f))
                    deleted.append(f)

        if deleted:
            return html.Div(f"✅ Deleted {len(deleted)} old reports.", style={"color": "green"})
        else:
            return html.Div("ℹ️ No old reports found to delete.", style={"color": "gray"})

    except Exception as e:
        return html.Div(f"❌ Failed to delete reports: {str(e)}", style={"color": "red"})


# Manage Pygwalker buttons
@app.callback(
    Output("view-report-btn", "disabled"),
    Input("clear-reports-btn", "n_clicks"),
    Input("generate-report-btn", "n_clicks"),
    Input("url", "pathname"),
    prevent_initial_call=True
)
def manage_view_button(clear_clicks, generate_clicks, pathname):
    triggered_id = ctx.triggered_id
    file_path = os.path.join("assets", "pyg_report.html")

    if triggered_id == "clear-reports-btn":
        if os.path.exists(file_path):
            os.remove(file_path)
        return True

    elif triggered_id == "generate-report-btn":
        generate_pyg_report()
        return False

    elif triggered_id == "url":
        if os.path.exists(file_path):
            return False
        else:
            return True

    return True

# View generated Pygwalker report
@app.callback(
    Output("pygwalker-report-container", "children"),
    Input("view-report-btn", "n_clicks"),
    prevent_initial_call=True
)
def view_generated_report(n_clicks):
    file_path = os.path.join("assets", "pyg_report.html")
    if os.path.exists(file_path):
        return html.Iframe(
            src="/pygwalker-report",
            width="100%",
            height="900px",
            style={"border": "1px solid #ccc"}
        )
    else:
        return html.Div("\u26a0\ufe0f No report found. Please generate one.", style={"color": "red", "textAlign": "center"})

# Serve Reports
@app.server.route("/reports/<path:filename>")
def serve_report(filename):
    return send_from_directory("assets", filename)

@app.server.route("/pygwalker-report")
def serve_pyg_report():
    file_path = os.path.join("assets", "pyg_report.html")
    if os.path.exists(file_path):
        return open(file_path, "r", encoding="utf-8").read()
    else:
        return "⚠️ Report not found.", 404

@app.server.route("/download_chat_pdf")
def download_chat_pdf():
    try:
        with open("latest_pdf.txt", "r") as f:
            path = f.read()
        return send_file(path, as_attachment=True)
    except Exception:
        return "PDF not found", 404

@app.server.route("/upload-pygwalker-report")
def serve_upload_pyg():
    path = os.path.join("assets", "upload_pyg_report.html")
    if os.path.exists(path):
        return open(path, "r", encoding="utf-8").read()
    return "⚠️ No report found", 404

@app.server.route("/upload-report/<path:filename>")
def serve_upload_report(filename):
    return send_from_directory("assets/upload_reports", filename)

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
