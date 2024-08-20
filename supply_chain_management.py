import streamlit as st
import pandas as pd

# 载入供应链数据
def load_supply_chain_data():
    try:
        return pd.read_csv('data/supply_chain_data.csv')
    except FileNotFoundError:
        st.error("供应链数据文件未找到，请确保文件路径正确！")
        return pd.DataFrame()

# 载入任务数据
def load_tasks():
    return pd.read_csv('data/tasks.csv')

# 更新任务状态
def update_task_status(tasks_df, task_id):
    tasks_df.loc[tasks_df['任务编号'] == task_id, '恒基DMP供应链管理'] = 'done'
    tasks_df.to_csv('data/tasks.csv', index=False)

# 显示供应链管理界面
def show_supply_chain_management():
    st.title("恒基DMP供应链管理")

    # 载入任务数据
    tasks_df = load_tasks()

    # 获取当前任务ID
    if 'current_task_id' in st.session_state:
        current_task_id = st.session_state['current_task_id']
        current_task = tasks_df[tasks_df['任务编号'] == current_task_id].iloc[0]

        # 检查任务是否已完成
        if current_task.get('恒基DMP供应链管理', "") == 'done':
            supply_chain_data = load_supply_chain_data()
            if not supply_chain_data.empty:
                st.dataframe(supply_chain_data)
                st.success("供应链数据已获取，任务已完成。")
            else:
                st.error("没有供应链数据可显示。")
        else:
            if st.button("获取供应链数据"):
                supply_chain_data = load_supply_chain_data()
                if not supply_chain_data.empty:
                    st.dataframe(supply_chain_data)
                    update_task_status(tasks_df, current_task_id)
                    st.success("供应链数据已获取，任务状态已更新。")
                else:
                    st.error("没有供应链数据可显示。")
    else:
        st.error("未设置当前任务ID，请从任务详情页面选择任务。")