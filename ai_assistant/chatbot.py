# chatbot.py
import os
import pandasai as pai
from pandasai import DataFrame as PaiDF
from data.db_connection import fetch_data, TABLE_QUERIES

# 🔐 ضع API Key الخاص بك هنا
pai.api_key.set("PAI-c692f014-a1b6-4596-9b5e-d0f7fcd907eb")  # <-- غيّره بـ المفتاح الحقيقي

def run_chatbot(question: str, selected_tables: list):
    # 🧹 حذف أي صور قديمة من charts
    charts_dir = os.path.join("exports", "charts")
    if os.path.exists(charts_dir):
        for file in os.listdir(charts_dir):
            if file.endswith(".png"):
                os.remove(os.path.join(charts_dir, file))

    dfs = []
    for _, (table_name, query) in TABLE_QUERIES.items():
        if table_name not in selected_tables:
            continue
        try:
            df = fetch_data(query)
            if df is not None and not df.empty:
                dfs.append(PaiDF(df))
        except Exception as e:
            print(f"[❌] Error loading {table_name}: {e}")

    if not dfs:
        return {"type": "text", "content": "⚠️ No valid data was selected."}

    try:
        result = pai.chat(question, *dfs)

        # 🖼️ بعد السؤال، لو فيه صورة جديدة اتولدت، نعرضها
        if os.path.exists(charts_dir):
            charts = [f for f in os.listdir(charts_dir) if f.endswith(".png")]
            if charts:
                latest_chart = sorted(
                    [os.path.join(charts_dir, f) for f in charts],
                    key=os.path.getmtime,
                    reverse=True
                )[0]
                return {"type": "image", "path": latest_chart}

        # لو مفيش شارت جديد - يبقى نص عادي
        return {"type": "text", "content": str(result)}

    except Exception as e:
        return {"type": "text", "content": f"❌ Error: {str(e)}"}