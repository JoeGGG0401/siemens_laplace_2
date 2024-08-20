import pandas as pd
import plotly.express as px
import streamlit as st


# 载入数据
def load_data():
    # 这里加载数据
    return pd.read_excel("data/订单与发货预测.xlsx")


# 数据清洗
def preprocess(data):
    # 需要的数据清洗逻辑
    return data


# 计算关键指标
def calculate_metrics(data):
    total_initial_orders = data['期初订单'].sum()
    total_net_shipments = data['净发货'].sum()
    total_new_orders = data['新增订单'].sum()
    return total_initial_orders, total_net_shipments, total_new_orders


# 生成客户净发货量图表
def plot_net_shipments_by_customer(data):
    fig = px.bar(data, x='客户全称', y='净发货', title="各客户净发货量")
    return fig


# 生成产品新增订单量图表
def plot_new_orders_by_model(data):
    fig = px.bar(data, x='产品型号', y='新增订单', title="各产品型号新增订单量")
    return fig


# 集成所有Dashboard
def show_dashboards():
    data = load_data()
    data = preprocess(data)

    total_initial_orders, total_net_shipments, total_new_orders = calculate_metrics(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("总期初订单量", f"{total_initial_orders}")
    col2.metric("总净发货量", f"{total_net_shipments}")
    col3.metric("总新增订单量", f"{total_new_orders}")

    st.plotly_chart(plot_net_shipments_by_customer(data), use_container_width=True)
    st.plotly_chart(plot_new_orders_by_model(data), use_container_width=True)

    st.write("详细的订单与发货预测数据：")
    st.dataframe(data)

