import pandas as pd
import plotly.express as px
from db_config import get_connection
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load Gemini key from .env

# ------------------ Basic Utilities ------------------

def get_states():
    conn = get_connection()
    query = "SELECT DISTINCT state FROM aggregated_transaction ORDER BY state;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['state'].tolist()

def get_years():
    conn = get_connection()
    query = "SELECT DISTINCT year FROM aggregated_transaction ORDER BY year;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['year'].tolist()

# ------------------ Visualizations ------------------

def get_transaction_insights(state, year):
    conn = get_connection()
    query = """
    SELECT transaction_type, SUM(amount) as total_amount
    FROM aggregated_transaction
    WHERE state = %s AND year = %s
    GROUP BY transaction_type
    ORDER BY total_amount DESC;
    """
    df = pd.read_sql(query, conn, params=(state, year))
    conn.close()
    fig = px.bar(df, x='transaction_type', y='total_amount',
                 title=f'{state} - Transaction Types ({year})')
    return fig

def plot_total_transaction_by_state():
    conn = get_connection()
    query = "SELECT state, SUM(amount) AS total FROM aggregated_transaction GROUP BY state;"
    df = pd.read_sql(query, conn)
    conn.close()
    fig = px.bar(df, x='state', y='total', title="Total Transaction Amount by State", color='total')
    return fig

def plot_total_users_by_state():
    conn = get_connection()
    query = "SELECT state, SUM(registered_users) AS total FROM map_user GROUP BY state;"
    df = pd.read_sql(query, conn)
    conn.close()
    fig = px.bar(df, x='state', y='total', title="Total Registered Users by State", color='total')
    return fig

def plot_district_transactions(state):
    conn = get_connection()
    query = "SELECT district, SUM(amount) AS total FROM map_transaction WHERE state = %s GROUP BY district;"
    df = pd.read_sql(query, conn, params=(state,))
    conn.close()
    fig = px.bar(df, x='district', y='total', title=f"{state} - Transactions by District")
    return fig

def plot_district_users(state):
    conn = get_connection()
    query = "SELECT district, SUM(registered_users) AS total FROM map_user WHERE state = %s GROUP BY district;"
    df = pd.read_sql(query, conn, params=(state,))
    conn.close()
    fig = px.bar(df, x='district', y='total', title=f"{state} - Registered Users by District")
    return fig

def plot_quarterly_transactions(state, year):
    conn = get_connection()
    query = """
    SELECT quarter, SUM(amount) AS total
    FROM aggregated_transaction
    WHERE state = %s AND year = %s
    GROUP BY quarter ORDER BY quarter;
    """
    df = pd.read_sql(query, conn, params=(state, year))
    conn.close()
    fig = px.line(df, x='quarter', y='total', markers=True,
                  title=f"{state} - Quarterly Transaction Amount ({year})")
    return fig

def plot_quarterly_app_opens(state, year):
    conn = get_connection()
    query = """
    SELECT quarter, SUM(app_opens) AS total
    FROM map_user
    WHERE state = %s AND year = %s
    GROUP BY quarter ORDER BY quarter;
    """
    df = pd.read_sql(query, conn, params=(state, year))
    conn.close()
    fig = px.line(df, x='quarter', y='total', markers=True,
                  title=f"{state} - Quarterly App Opens ({year})")
    return fig

# ------------------ Geo Visualization ------------------

def plot_geo_transaction(year, quarter):
    geojson_path = os.path.join(os.path.dirname(__file__), 'states_india.geojson')
    with open(geojson_path, 'r', encoding='utf-8') as f:
        india_geojson = json.load(f)

    for feature in india_geojson["features"]:
        feature["properties"]["st_nm"] = feature["properties"]["st_nm"].title().strip()

    conn = get_connection()
    query = """
    SELECT state, SUM(amount) AS total
    FROM aggregated_transaction
    WHERE year = %s AND quarter = %s
    GROUP BY state;
    """
    df = pd.read_sql(query, conn, params=(year, quarter))
    conn.close()
    df['state'] = df['state'].str.title().str.strip()

    fig = px.choropleth_mapbox(
        df,
        geojson=india_geojson,
        locations='state',
        featureidkey="properties.st_nm",
        color='total',
        color_continuous_scale="YlOrBr",
        mapbox_style="carto-positron",
        zoom=3.5,
        center={"lat": 23.5937, "lon": 80.9629},
        opacity=0.8,
        title=f"🗺️ India State-wise Transactions in Q{quarter} {year}",
        height=650
    )
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    return fig

# ------------------ Gemini AI Summary ------------------

def generate_gemini_insight(state, year, quarter):
    conn = get_connection()
    query = """
    SELECT transaction_type, SUM(amount) as total_amount
    FROM aggregated_transaction
    WHERE state = %s AND year = %s AND quarter = %s
    GROUP BY transaction_type
    ORDER BY total_amount DESC;
    """
    df = pd.read_sql(query, conn, params=(state, year, quarter))
    conn.close()

    if df.empty:
        return "❌ No data found for this selection."

    prompt = f"""
    Analyze PhonePe transaction data for:
    - State: {state}
    - Year: {year}
    - Quarter: Q{quarter}

    Summary Table:
    {df.to_string(index=False)}

    Provide:
    - Key insights in bullet points
    - Trends, growth patterns or declines
    - Business suggestions (brief)
    """

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": os.getenv("GEMINI_API_KEY")
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"❌ Gemini API Error: {response.text}"
