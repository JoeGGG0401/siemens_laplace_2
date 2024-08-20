import pandas as pd
import plotly.express as px
import streamlit as st

def load_data():
    data = pd.read_excel("data/放料明细.xlsx")
    return preprocess_data(data)

def preprocess_data(data):
    # 删除第二行（索引为1的行）
    data = data.drop(0)  # 注意这里使用的是行的索引
    data['放料日期'] = pd.to_datetime(data['放料日期'], errors='coerce')
    data['重量'] = pd.to_numeric(data['重量'], errors='coerce')
    data['剩余重量'] = pd.to_numeric(data['剩余重量'], errors='coerce')
    return data

def calculate_metrics(data):
    total_weight = data['重量'].sum()
    average_remaining = data['剩余重量'].mean()
    pass_rate = (data[data['检验状态'] == '合格'].shape[0] / data.shape[0]) * 100
    return total_weight, round(average_remaining, 2), round(pass_rate, 2)

def plot_weight_distribution(data):
    fig = px.histogram(data, x='重量', title="重量分布图")
    return fig


def plot_activities_by_operator(data):
    # 统计每个放料人员的放料次数
    activity_data = data['放料人员'].value_counts().reset_index()
    activity_data.columns = ['放料人员', '次数']

    # 使用饼图展示每个放料人员的活动分布
    fig = px.pie(activity_data, values='次数', names='放料人员', title="放料人员活动分布",
                 color_discrete_sequence=px.colors.sequential.RdBu)  # 使用颜色序列增强视觉效果

    # 配置图表的布局
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def show_dashboards():
    data = load_data()
    total_weight, average_remaining, pass_rate = calculate_metrics(data)
    col1, col2, col3 = st.columns(3)
    col1.metric("总放料重量", f"{total_weight:,}")
    col2.metric("平均剩余重量", f"{average_remaining}")
    col3.metric("合格率", f"{pass_rate}%")

    col4, col5 = st.columns(2)
    col4.plotly_chart(plot_weight_distribution(data), use_container_width=True)
    col5.plotly_chart(plot_activities_by_operator(data), use_container_width=True)

    st.markdown("**放料明细**：")
    st.dataframe(data)