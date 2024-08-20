import streamlit as st
import pandas as pd
import json

# Load tasks data
def load_tasks():
    return pd.read_csv('data/tasks.csv')

# Update task status
def update_task_status(tasks_df, task_id, step_name):
    tasks_df.loc[tasks_df['任务编号'] == task_id, step_name] = 'done'
    tasks_df.to_csv('data/tasks.csv', index=False)

def show_dingtalk_notification():
    """Display the DingTalk notification interface."""
    st.title("钉钉工作通知")

    # Load tasks
    tasks_df = load_tasks()

    # Load production plan and prepare report
    report = """
            **工单号**: P20210831-001  
            **产品名称**: 螺丝 | 钢板  
            **订单日期**: 2024/08/20  
            **计划完成**: 2024/09/30  
            **计划数量**: 1000个  
            **计划完成量**: 0个  
            **不良数量**: 100个  
            **实际时间**: 2024/08/30  
            """
    notification_text = report.replace('\n', ' ').replace('# ', '')  # Simplify markdown to plain text for notification

    if 'current_task_id' in st.session_state:
        current_task_id = st.session_state['current_task_id']
        current_task = tasks_df.loc[tasks_df['任务编号'] == current_task_id].iloc[0]
        # Text input for customizing notification content
        user_input = st.text_area("通知内容", notification_text, key="notification_content_2")

        # Check if the task step is completed
        if current_task.get('钉钉工作通知2', "") == 'done':
            col1, col2 = st.columns([1, 3])  # 划分列的比例，col1更窄，适合放置图片
            with col1:
                st.image('data/发送截图_2.png', caption='通知已发送截图')
            with col2:
                st.success("钉钉通知已发送，并完成此任务。")
        else:
            if st.button("发送通知", key="send_notification_2"):
                # Simulate sending the notification
                # Here you would integrate with an actual API to send the notification
                col1, col2 = st.columns([1, 3])  # 划分列的比例，col1更窄，适合放置图片
                with col1:
                    st.image('data/发送截图_2.png', caption='通知已发送截图')
                with col2:
                    st.success("钉钉通知已发送，并更新任务状态。")
                update_task_status(tasks_df, current_task_id, '钉钉工作通知2')
    else:
        st.error("未设置当前任务ID，请从任务详情页面选择任务。")