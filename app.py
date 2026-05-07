import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Sales Forecast Dashboard",
    page_icon="✨",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

weekly_sales = pd.read_csv("weekly_sales.csv")
forecast = pd.read_csv("forecast.csv")

weekly_sales['Date'] = pd.to_datetime(weekly_sales['Date'])
forecast['ds'] = pd.to_datetime(forecast['ds'])

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: 700;
    background: linear-gradient(to right, #ff00cc, #3333ff, #00f5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #d1d5db;
    margin-bottom: 35px;
}

/* CONTROL BOX */

.control-box {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(16px);
    padding: 20px;
    border-radius: 22px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(31,38,135,0.37);
}

/* KPI CARDS */

.card {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(16px);
    padding: 25px;
    border-radius: 24px;
    text-align: center;
    transition: 0.3s ease-in-out;
    box-shadow: 0 8px 32px rgba(31,38,135,0.37);
}

.card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 10px 40px rgba(255,0,204,0.35);
}

.card h3 {
    color: #cbd5e1;
    font-size: 18px;
}

.card h1 {
    color: white;
    font-size: 36px;
    font-weight: 700;
}

/* INSIGHT BOX */

.insight-box {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(16px);
    padding: 28px;
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(31,38,135,0.37);
    font-size: 18px;
    line-height: 1.9;
}

/* HEADINGS */

h2 {
    color: white !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.markdown("""
<div class="main-title">
✨ Sales Forecasting Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
Machine Learning + Forecast Analytics + Business Intelligence
</div>
""", unsafe_allow_html=True)

# ---------------- CONTROL CENTER ----------------

st.markdown("""
<div class="control-box">
<h2>🎛 Control Center</h2>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    start_date = st.date_input(
        "📅 Start Date",
        weekly_sales['Date'].min()
    )

with c2:
    end_date = st.date_input(
        "📅 End Date",
        weekly_sales['Date'].max()
    )

with c3:
    chart_theme = st.selectbox(
        "🎨 Chart Theme",
        [
            "plotly_dark",
            "ggplot2",
            "seaborn",
            "simple_white"
        ]
    )

with c4:
    show_raw = st.toggle("🗂 Show Dataset")

# ---------------- FILTER DATA ----------------

filtered_data = weekly_sales[
    (weekly_sales['Date'] >= pd.to_datetime(start_date)) &
    (weekly_sales['Date'] <= pd.to_datetime(end_date))
]

forecast_filtered = forecast[
    (forecast['ds'] >= pd.to_datetime(start_date)) &
    (forecast['ds'] <= pd.to_datetime(end_date))
]

filtered_data = filtered_data.copy()

filtered_data['Month'] = filtered_data['Date'].dt.strftime('%b')

# ---------------- RAW DATA ----------------

if show_raw:
    st.markdown("## 🧾 Dataset Preview")
    st.dataframe(filtered_data.head(20))

# ---------------- KPI SECTION ----------------

st.markdown("## 📈 Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card">
        <h3>Total Sales</h3>
        <h1>{filtered_data['Sales'].sum():,.0f}</h1>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <h3>Average Sales</h3>
        <h1>{filtered_data['Sales'].mean():,.0f}</h1>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <h3>Maximum Sales</h3>
        <h1>{filtered_data['Sales'].max():,.0f}</h1>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="card">
        <h3>Total Weeks</h3>
        <h1>{len(filtered_data)}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- SALES TREND ----------------

st.markdown("## 📊 Weekly Sales Trend")

fig1 = px.line(
    filtered_data,
    x='Date',
    y='Sales',
    markers=True,
    template=str(chart_theme)
)

fig1.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=450
)

st.plotly_chart(
    fig1,
    use_container_width=True,
    key="chart1"
)

# ---------------- FORECAST ----------------

st.markdown("## 🔮 Future Sales Forecast")

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=forecast_filtered['ds'],
        y=forecast_filtered['yhat'],
        mode='lines+markers',
        name='Forecast'
    )
)

fig2.update_layout(
    template=str(chart_theme),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=450,
    hovermode='x unified'
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    key="chart2"
)

# ---------------- MONTHLY ANALYSIS ----------------

st.markdown("## 📅 Monthly Sales Analysis")

monthly_sales = filtered_data.groupby('Month')['Sales'].mean().reset_index()

fig3 = px.bar(
    monthly_sales,
    x='Month',
    y='Sales',
    template=str(chart_theme),
    text_auto=True
)

fig3.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=450
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    key="chart3"
)

# ---------------- PIE CHART ----------------

st.markdown("## 🥧 Sales Distribution")

pie_chart = px.pie(
    monthly_sales,
    names='Month',
    values='Sales',
    hole=0.5,
    template=str(chart_theme)
)

pie_chart.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)

st.plotly_chart(
    pie_chart,
    use_container_width=True,
    key="chart4"
)

# ---------------- INSIGHTS ----------------

st.markdown("## 💡 Business Insights")

st.markdown("""
<div class="insight-box">

✅ Sales increase significantly during festive seasons.<br><br>

✅ Promotions positively impact customer purchases.<br><br>

✅ Strong seasonal demand patterns are visible.<br><br>

✅ Forecast predicts stable future business growth.<br><br>

✅ Inventory planning should focus on high-demand periods.

</div>
""", unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<center>
<h4 style="color:white;">
Created by Anany Kanjolia ✨
</h4>
</center>
""", unsafe_allow_html=True)