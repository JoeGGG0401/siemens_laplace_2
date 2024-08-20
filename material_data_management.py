import streamlit as st
import pandas as pd

# 载入物料数据
def load_material_data():
    try:
        return pd.read_csv('data/黑湖MES物料主数据.csv')
    except FileNotFoundError:
        st.error("物料数据文件未找到，请确保文件路径正确！")
        return pd.DataFrame()

# 载入任务数据
def load_tasks():
    return pd.read_csv('data/tasks.csv')

# 更新任务状态
def update_task_status(tasks_df, task_id, step_name):
    tasks_df.loc[tasks_df['任务编号'] == task_id, step_name] = 'done'
    tasks_df.to_csv('data/tasks.csv', index=False)

# 显示物料数据管理界面
def show_material_data_management():
    st.title("黑湖MES物料主数据管理")

    # 载入任务数据
    tasks_df = load_tasks()

    # 获取当前任务ID
    if 'current_task_id' in st.session_state:
        current_task_id = st.session_state['current_task_id']
        current_task = tasks_df[tasks_df['任务编号'] == current_task_id].iloc[0]

        # 检查任务是否已完成
        if current_task.get('黑湖MES物料主数据', "") == 'done':
            material_data = load_material_data()
            if not material_data.empty:
                st.dataframe(material_data)
                st.success("物料数据已获取，任务已完成。")
            else:
                st.error("没有物料数据可显示。")
        else:
            if st.button("获取物料数据"):
                material_data = load_material_data()
                if not material_data.empty:
                    st.dataframe(material_data)
                    update_task_status(tasks_df, current_task_id, '黑湖MES物料主数据')
                    st.success("物料数据已获取，任务状态已更新。")
                else:
                    st.error("没有物料数据可显示。")
    else:
        st.error("未设置当前任务ID，请从任务详情页面选择任务。")