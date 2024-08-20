import pandas as pd
import plotly.express as px
import streamlit as st

# 数据加载与预处理
def load_employee_hours_data():
    data = pd.read_excel("data/员工工时统计_前30名_完整版.xlsx")
    return preprocess_data(data)

def preprocess_data(data):
    # 将关键的工时列转换为数值类型
    data['总工时'] = pd.to_numeric(data['总工时'], errors='coerce')
    data['实际工时'] = pd.to_numeric(data['实际工时'], errors='coerce')

    # 计算关键指标
    total_hours = data['总工时'].sum()
    actual_hours = data['实际工时'].sum()
    average_total_hours = data['总工时'].mean()
    average_actual_hours = data['实际工时'].mean()

    # 计算实际工时与总工时的差异百分比
    percentage_difference = ((actual_hours - total_hours) / total_hours) * 100 if total_hours else 0

    metrics = {
        'total_hours': int(total_hours),
        'actual_hours': int(actual_hours),
        'average_total_hours': int(average_total_hours),
        'average_actual_hours': int(average_actual_hours),
        'percentage_difference': percentage_difference
    }
    return data, metrics

# 生成图表
def plot_total_vs_actual_hours(data):
    # 创建一个对比柱状图，其中“总工时”和“实际工时”为并列柱状图
    fig = px.bar(data, x='姓名', y=['总工时', '实际工时'],
                 barmode='group',  # 设置柱状图为分组模式
                 title="员工总工时与实际工时对比",
                 labels={'value': '工时', 'variable': '类别'},  # 自定义图例标签
                 color_discrete_map={'总工时': 'blue', '实际工时': 'lightblue'})  # 自定义颜色
    fig.update_layout(xaxis_title="姓名", yaxis_title="工时",
                      legend_title="工时类别")
    return fig


def plot_histogram_actual_hours(data):
    # 创建一个带有核密度估计的直方图，展示实际工时的分布
    fig = px.histogram(data, x='实际工时',
                       marginal='violin',  # 使用小提琴图作为边缘图
                       title="实际工时分布",
                       labels={'实际工时': '工时'},
                       color_discrete_sequence=['#636EFA'])  # 指定颜色
    fig.update_layout(xaxis_title="实际工时",
                      yaxis_title="频数",
                      bargap=0.2)  # 设置直方图柱间距
    return fig


# 展示看板
def show_dashboards():
    data, metrics = load_employee_hours_data()
    # 使用st.metric展示关键指标，并加入百分比差异
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总工时", f"{metrics['total_hours']:,}")
    col2.metric("实际工时", f"{metrics['actual_hours']:,}", f"{metrics['percentage_difference']:.2f}%")
    col3.metric("平均总工时", f"{metrics['average_total_hours']:,}")
    col4.metric("平均实际工时", f"{metrics['average_actual_hours']:,}", f"{metrics['percentage_difference']:.2f}%")

    # 展示图表
    col5, col6 = st.columns(2)
    col5.plotly_chart(plot_total_vs_actual_hours(data), use_container_width=True)
    col6.plotly_chart(plot_histogram_actual_hours(data), use_container_width=True)

    # 直接展示数据表
    st.markdown("**员工工时统计**：")
    st.dataframe(data)  # 使用 st.dataframe 直接展示数据表
