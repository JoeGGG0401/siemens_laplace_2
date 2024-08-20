import streamlit as st
import pandas as pd


# Load tasks from CSV file
def load_tasks():
    try:
        return pd.read_csv('data/tasks.csv')
    except FileNotFoundError:
        st.error("Task data file not found.")
        return pd.DataFrame()


# Save tasks to CSV file
def save_tasks(tasks_df):
    tasks_df.to_csv('data/tasks.csv', index=False)

def count_completed_steps(row):
    return sum([1 for x in row if x == 'done'])


# Display the dashboard with tasks and metrics
def show_dashboard():
    tasks_df = load_tasks()
    if not tasks_df.empty:
        # Display task metrics
        # Calculate the number of completed tasks based on the definition of 8 'done' states
        tasks_df['Completed Steps'] = tasks_df.apply(count_completed_steps, axis=1)
        completed_tasks = tasks_df[tasks_df['Completed Steps'] >= 8].shape[0]
        ongoing_tasks = tasks_df.shape[0] - completed_tasks

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tasks", tasks_df.shape[0])
        col2.metric("Completed Tasks", completed_tasks)
        col3.metric("Ongoing Tasks", ongoing_tasks)

        # Display tasks table
        st.subheader("任务详情")
        st.dataframe(tasks_df)

        # Add new task button and form
        with st.form("new_task_form"):
            task_id = st.text_input("任务编号")
            task_name = st.text_input("任务名")
            task_start_date = st.date_input("任务开始时间")
            task_progress = st.text_input("任务进度", "0%")
            executor = st.text_input("执行人")
            priority = st.selectbox("任务优先级", ["高", "中", "低"])
            order_id = st.text_input("当前订单号")

            submit_button = st.form_submit_button("创建任务")
            if submit_button:
                # Add new task to DataFrame
                new_data = {
                    '任务编号': [task_id],
                    '任务名': [task_name],
                    '任务开始时间': [task_start_date],
                    '任务进度': [task_progress],
                    '执行人': [executor],
                    '任务优先级': [priority],
                    '当前订单号': [order_id],
                    '蘑菇云智控设备组管理': [''],
                    '恒基DMP人力资源': [''],
                    '恒基DMP供应链管理': [''],
                    '黑湖MES物料主数据': [''],
                    'AI分析': [''],
                    '钉钉工作通知': [''],
                    '钉钉工作通知2': [''],
                    '黑湖MES生产工单下发': ['']
                }
                new_task_df = pd.DataFrame(new_data)
                tasks_df = pd.concat([tasks_df, new_task_df], ignore_index=True)
                save_tasks(tasks_df)
                st.success("新任务已创建")
    else:
        st.warning("No task data available.")


