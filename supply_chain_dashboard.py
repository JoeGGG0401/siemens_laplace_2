import pandas as pd
import plotly.express as px
import streamlit as st


# 载入数据
def load_data():
    return pd.read_excel("data/供应链数据.xlsx")


# 数据清洗
def preprocess(data):
    data.dropna(subset=['供应商全称', '日期'], inplace=True)
    return data


# 供应商交易总览
def supplier_transactions(data):
    supplier_summary = data.groupby('供应商全称').agg({'数量': 'sum', '待勾稽金额': 'sum'}).reset_index()
    fig = px.bar(supplier_summary, x='供应商全称', y='待勾稽金额', title="各供应商交易金额")
    return fig


# 物料分类分析
def material_classification(data):
    material_summary = data.groupby('物料分类').agg({'数量': 'sum', '待勾稽金额': 'sum'}).reset_index()
    fig = px.pie(material_summary, values='待勾稽金额', names='物料分类', title="物料分类交易金额")
    return fig


# 时间序列分析图
def time_series_analysis(data):
    data['月份'] = data['日期'].dt.to_period('M').astype(str)  # 将Period转换为字符串
    time_summary = data.groupby('月份').agg({'待勾稽金额': 'sum', '数量': 'sum'}).reset_index()
    fig = px.line(time_summary, x='月份', y='待勾稽金额', title="时间序列分析：采购金额")
    fig.update_xaxes(type='category')  # 确保x轴为分类轴
    return fig

# 供应商交易频次图
def supplier_frequency(data):
    freq_summary = data['供应商全称'].value_counts().reset_index()
    freq_summary.columns = ['供应商全称', '交易次数']
    fig = px.bar(freq_summary, x='供应商全称', y='交易次数', title="供应商交易频次")
    return fig


# 集成所有Dashboard
def show_dashboards():
    data = load_data()
    data = preprocess(data)

    # 显示关键指标
    total_transactions = data['待勾稽金额'].sum()
    total_items = data['数量'].sum()
    unique_suppliers = data['供应商全称'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("交易总金额", f"¥{total_transactions:,.2f}")
    col2.metric("总物料数量", f"{total_items:,.2f}")
    col3.metric("供应商数量", unique_suppliers)

    # 显示图表
    col4, col5 = st.columns(2)
    with col4:
        st.plotly_chart(supplier_transactions(data), use_container_width=True)
    with col5:
        st.plotly_chart(material_classification(data), use_container_width=True)

    col6, col7 = st.columns(2)
    with col6:
        st.plotly_chart(time_series_analysis(data), use_container_width=True)
    with col7:
        st.plotly_chart(supplier_frequency(data), use_container_width=True)

    st.markdown("**供应链数据**：")
    st.dataframe(data)  # 使用 st.dataframe 直接展示数据表
