import streamlit as st
import pandas as pd


def load_orders():
    """载入订单数据"""
    try:
        return pd.read_csv('data/orders.csv')
    except FileNotFoundError:
        st.error("订单数据文件未找到，请确保文件路径正确！")
        return pd.DataFrame()


def load_tasks():
    """载入任务数据"""
    try:
        return pd.read_csv('data/tasks.csv')
    except FileNotFoundError:
        st.error("任务数据文件未找到，请确保文件路径正确！")
        return pd.DataFrame()


def save_tasks(tasks_df):
    """保存更新后的任务数据到CSV"""
    tasks_df.to_csv('data/tasks.csv', index=False)


def show_data_acquisition():
    st.title("恒基DMP订单")

    # 载入订单数据和任务数据
    orders_df = load_orders()
    tasks_df = load_tasks()

    if tasks_df.empty or orders_df.empty:
        return  # 如果数据不存在，则停止执行后续代码

    # 确保已从任务详情页选择了任务
    if 'current_task_id' not in st.session_state:
        st.error("请先从任务详情页选择一个任务。")
        return

    task_details = tasks_df[tasks_df['任务编号'] == st.session_state['current_task_id']].iloc[0]
    if pd.notna(task_details['当前订单号']):
        st.success(f"当前任务已关联订单编号: {task_details['当前订单号']}")
        linked_order_details = orders_df[orders_df['订单编号'] == task_details['当前订单号']]
        st.write("当前关联的订单详情：", linked_order_details)

    # 订单选择和详情更新
    order_options = orders_df['订单编号'].tolist()
    selected_order_id = st.selectbox("选择订单编号", order_options)

    if st.button("获取并关联订单"):
        selected_order_details = orders_df[orders_df['订单编号'] == selected_order_id]
        if not selected_order_details.empty:
            st.write("选中的订单详情：", selected_order_details)

            # 更新任务CSV文件中的当前订单号
            tasks_df.loc[tasks_df['任务编号'] == st.session_state['current_task_id'], '当前订单号'] = selected_order_id
            save_tasks(tasks_df)

            # 更新session state，以便在需要时引用订单信息
            st.session_state['selected_order_id'] = selected_order_id
        else:
            st.error("选择的订单编号不存在，请检查订单数据。")