import pandas as pd
import plotly.express as px
import streamlit as st

def load_data():
    return pd.read_excel("data/工单数据.xlsx")

def preprocess_data(data):
    data['接收时间'] = pd.to_datetime(data['接收时间'], errors='coerce')
    data['处理完成'] = pd.to_datetime(data['处理完成'], errors='coerce')
    return data

def calculate_metrics(data):
    total_orders = len(data)
    average_process_time = (data['处理完成'] - data['接收时间']).dt.total_seconds().mean() / 3600
    return total_orders, round(average_process_time, 2)

def plot_total_vs_actual_hours(data):
    fig = px.bar(data, x='设备名称', y='紧急程度', title="设备紧急程度对比")
    return fig

def plot_histogram_actual_hours(data):
    fig = px.histogram(data, x='处理完成', title="工单处理完成时间分布")
    return fig

def show_dashboards():
    data = load_data()
    data = preprocess_data(data)
    total_orders, average_process_time = calculate_metrics(data)

    col1, col2 = st.columns(2)
    col1.metric("总工单数", total_orders)
    col2.metric("平均处理时间 (小时)", average_process_time)

    col3, col4 = st.columns(2)
    col3.plotly_chart(plot_total_vs_actual_hours(data), use_container_width=True)
    col4.plotly_chart(plot_histogram_actual_hours(data), use_container_width=True)

    # 直接展示数据表
    st.markdown("**工单详情**：")
    st.dataframe(data)  # 使用 st.dataframe 直接展示数据表
