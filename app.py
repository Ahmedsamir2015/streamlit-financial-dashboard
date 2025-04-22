import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="db4free.net",
        user="ahmedsamir2015",
        password=st.secrets["DB_PASSWORD"],
        database="ahmed2015"
    )

def get_sales():
    conn = get_connection()
    query = "SELECT * FROM sales ORDER BY Date DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("📊 لوحة تحليل الفواتير - Ahmed 2015 Database")

try:
    df = get_sales()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')

    st.subheader("📈 عدد الفواتير لكل عميل")
    invoice_counts = df['Customer'].value_counts().reset_index()
    invoice_counts.columns = ['Customer', 'InvoiceCount']
    fig1 = px.bar(invoice_counts, x='Customer', y='InvoiceCount')
    st.plotly_chart(fig1)

    st.subheader("💰 إجمالي الإنفاق حسب العميل")
    spending = df.groupby('Customer')['InvoiceAmount'].sum().reset_index()
    fig2 = px.bar(spending, x='Customer', y='InvoiceAmount')
    st.plotly_chart(fig2)

    st.subheader("📅 المبيعات حسب الشهر")
    monthly = df.groupby('Month')['InvoiceAmount'].sum().reset_index()
    monthly['Month'] = monthly['Month'].astype(str)
    fig3 = px.line(monthly, x='Month', y='InvoiceAmount')
    st.plotly_chart(fig3)

except Exception as e:
    st.error(f"حدث خطأ: {e}")
