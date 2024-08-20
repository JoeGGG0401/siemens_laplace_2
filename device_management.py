import streamlit as st
import pandas as pd


# 载入设备组数据
def load_device_data():
    try:
        return pd.read_csv('data/设备组管理数据.csv')
    except FileNotFoundError:
        st.error("设备组数据文件未找到，请确保文件路径正确！")
        return pd.DataFrame()


# 载入任务数据
def load_tasks():
    return pd.read_csv('data/tasks.csv')


# 更新任务状态
def update_task_status(tasks_df, task_id):
    tasks_df.loc[tasks_df['任务编号'] == task_id, '蘑菇云智控设备组管理'] = 'done'
    tasks_df.to_csv('data/tasks.csv', index=False)


# 显示设备管理界面
def show_device_management():
    st.title("蘑菇云智控设备组管理")

    # 载入任务数据
    tasks_df = load_tasks()

    # 获取当前任务ID
    if 'current_task_id' in st.session_state:
        current_task_id = st.session_state['current_task_id']
        current_task = tasks_df[tasks_df['任务编号'] == current_task_id].iloc[0]

        # 检查任务是否已完成
        if current_task.get('蘑菇云智控设备组管理', "") and current_task['蘑菇云智控设备组管理'] == 'done':
            device_data = load_device_data()
            if not device_data.empty:
                st.dataframe(device_data)
                st.success("设备数据已获取，任务已完成。")
            else:
                st.error("没有设备数据可显示。")
        else:
            if st.button("获取设备数据"):
                device_data = load_device_data()
                if not device_data.empty:
                    st.dataframe(device_data)
                    update_task_status(tasks_df, current_task_id)
                    st.success("设备数据已获取，任务状态已更新。")
                else:
                    st.error("没有设备数据可显示。")
    else:
        st.error("未设置当前任务ID，请从任务详情页面选择任务。")
