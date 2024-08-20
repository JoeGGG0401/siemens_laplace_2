import pandas as pd
import plotly.express as px
import streamlit as st

# 载入数据
def load_raw_material_data():
    data = pd.read_excel("data/原料库存明细.xlsx")
    return preprocess_raw_materials(data)

# 数据清洗
def preprocess_raw_materials(data):
    data = data.drop(0)  # 注意这里使用的是行的索引
    data.fillna({'安全库存': 0}, inplace=True)  # 假设缺少安全库存的用0填充
    return data

# 库存概览图表
def inventory_overview(data):
    fig = px.bar(data, x='原料名称', y=['期初数量', '入库数量', '领料数量', '退货数量', '期末数量'],
                 title="库存概览")
    return fig

# 安全库存状态图表
def safety_stock_status(data):
    data['库存风险'] = data.apply(lambda x: '低' if x['期末数量'] >= x['安全库存'] else '高', axis=1)
    fig = px.histogram(data, x='原料名称', color='库存风险', title="安全库存状态")
    return fig

# 供应商原料供应分析图表
def supplier_material_analysis(data):
    supplier_summary = data.groupby('供应商全称').agg({'期末数量': 'sum'}).reset_index()
    fig = px.pie(supplier_summary, values='期末数量', names='供应商全称', title="供应商原料供应分析")
    return fig

# 总结关键指标
def summarize_key_metrics(data):
    total_inventory = int(data['期末数量'].sum())
    total_received = int(data['入库数量'].sum())
    total_issues = int(data['领料数量'].sum())
    return total_inventory, total_received, total_issues

# 集成所有Dashboard，并在Streamlit中显示
def show_dashboards():
    data = load_raw_material_data()
    total_inventory, total_received, total_issues = summarize_key_metrics(data)

    # 显示关键指标
    col1, col2, col3 = st.columns(3)
    col1.metric("总库存数量", f"{total_inventory:,}")
    col2.metric("总入库数量", f"{total_received:,}")
    col3.metric("总领料数量", f"{total_issues:,}")

    # 显示图表
    col4, col5, col6= st.columns(3)
    with col4:
        st.plotly_chart(inventory_overview(data), use_container_width=True)
    with col5:
        st.plotly_chart(safety_stock_status(data), use_container_width=True)
    with col6:
        st.plotly_chart(supplier_material_analysis(data), use_container_width=True)

    # 直接展示数据表
    st.markdown("**原料库存明细**：")
    st.dataframe(data)  # 使用 st.dataframe 直接展示数据表
