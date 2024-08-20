import pandas as pd
import streamlit as st

def show_work_order_dispatch():
    st.title("黑湖MES生产工单下发")

    # 载入任务数据
    tasks_df = load_tasks()

    # 获取当前任务ID
    if 'current_task_id' in st.session_state:
        current_task_id = st.session_state['current_task_id']
        current_task = tasks_df.loc[tasks_df['任务编号'] == current_task_id].iloc[0]

        with st.container(border=True):
            st.markdown("""
            **工单号**: P20210831-001  
            **产品名称**: 螺丝 | 钢板  
            **订单日期**: 2024/08/20  
            **计划完成**: 2024/09/30  
            **计划数量**: 1000个  
            **计划完成量**: 0个  
            **不良数量**: 100个  
            **实际时间**: 2024/08/30  
            """)

        # 检查任务是否已完成工单下发
        if current_task.get('黑湖MES生产工单下发', "") == 'done':
            st.image('data/工单下发成功截图.png', caption='工单下发成功截图')
            st.success("工单已成功下发并完成此任务。")
        else:
            if st.button("下发工单"):
                # 模拟发送工单
                # 在实际应用中，这里会调用后端API来完成工单的下发
                update_task_status(tasks_df, current_task_id, '黑湖MES生产工单下发')
                st.image('data/工单下发成功截图.png', caption='工单下发成功截图')
                st.success("工单已成功下发并更新任务状态。")
    else:
        st.error("未设置当前任务ID，请从任务详情页面选择任务。")

def load_tasks():
    return pd.read_csv('data/tasks.csv')

def update_task_status(tasks_df, task_id, step_name):
    tasks_df.loc[tasks_df['任务编号'] == task_id, step_name] = 'done'
    tasks_df.to_csv('data/tasks.csv', index=False)