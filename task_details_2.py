import streamlit as st
import pandas as pd


# 载入任务数据
def load_tasks():
    try:
        return pd.read_csv('data/tasks.csv')
    except FileNotFoundError:
        st.error("任务数据文件未找到，请确保文件路径正确！")
        return pd.DataFrame()


# 显示任务详情页面
def show_task_details():
    tasks = load_tasks()
    if tasks.empty:
        st.warning("当前没有可用的任务数据。")
        return

    col1, col2 = st.columns(2)
    with col1:
        # 选择任务并保存到session state
        task_options = tasks.apply(lambda x: f"{x['任务编号']} - {x['任务名']}", axis=1)
        selected_task = st.selectbox("选择任务", task_options, key='selected_task_index')
        task_id = selected_task.split(' - ')[0]

        # 如果切换了任务，更新session state
        if 'current_task_id' not in st.session_state or st.session_state['current_task_id'] != task_id:
            st.session_state['current_task_id'] = task_id

        task_details = tasks[tasks['任务编号'] == task_id].iloc[0]

        # 显示任务基本信息
        st.subheader("任务基本信息")
        st.text(f"任务名: {task_details['任务名']}")
        st.text(f"任务编号: {task_details['任务编号']}")
        st.text(f"任务开始时间: {task_details['任务开始时间']}")
        st.text(f"任务进度: {task_details['任务进度']}")
        st.text(f"执行人: {task_details['执行人']}")
        st.text(f"任务优先级: {task_details['任务优先级']}")

        # 任务描述
        st.subheader("任务描述")
        st.write(
            "通过收集不同来源的数据，并进行整合，最终实现了数据可视化和智能检索助手，解决了企业端多平台数据可视化以及智能分析数据的问题。")

    with col2:
        st.image('data/workflow_2.png', caption='任务流程图')
