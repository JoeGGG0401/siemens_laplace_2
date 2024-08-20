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
            "根据订单需求、生产能力、物料供应情况、设备状态等信息生成智能工单并写入MES系统中，通过钉钉推送给相关人员，确保资源合理分配和生产计划准确执行。")

    with col2:
        st.image('data/workflow_1.png', caption='任务流程图')

    # 展示关联的订单信息
    if 'current_task_id' in st.session_state:
        task = tasks[tasks['任务编号'] == st.session_state['current_task_id']].iloc[0]
        if pd.notna(task.get('当前订单号')):
            st.success(f"当前关联的订单编号: {task['当前订单号']}")
        else:
            st.warning("尚未选择订单")
    else:
        st.warning("请选择一个任务以查看更多信息。")