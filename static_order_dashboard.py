import streamlit as st
import pandas as pd
import plotly.express as px

# 数据加载函数
def load_data():
    df = pd.read_excel('data/静态订单【预测】.xlsx')
    print("列名：", df.columns)  # 打印列名来检查它们是否正确
    return df

# 数据分析和指标计算
def calculate_metrics(df):
    total_orders = df['订单数量'].sum()
    total_shipments = df['发货数量'].sum()
    # 由于没有提供转化率和订单比率的列，需要确认是否需要这些计算，或是否有其他列可以用来计算
    return total_orders, total_shipments

# 创建图表
def create_charts(df):
    order_chart = px.pie(df, names='客户全称', values='订单数量', title='客户订单总数', )
    shipment_chart = px.pie(df, names='客户全称', values='发货数量', title='客户发货量')
    return order_chart, shipment_chart

# Streamlit 仪表板展示
def show_dashboards():
    df = load_data()
    total_orders, total_shipments = calculate_metrics(df)
    order_chart, shipment_chart = create_charts(df)

    st.title('订单与发货预测仪表板')
    col1, col2 = st.columns(2)
    col1.metric("总订单数", total_orders)
    col2.metric("总发货量", total_shipments)

    col3, col4 = st.columns(2)
    col3.plotly_chart(order_chart, use_container_width=True)
    col4.plotly_chart(shipment_chart, use_container_width=True)

    st.write("详细订单数据:")
    st.dataframe(df)
