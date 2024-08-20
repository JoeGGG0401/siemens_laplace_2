import json

import streamlit as st
import pandas as pd
import time


def load_production_plan():
    """加载生产计划的JSON数据"""
    with open('data/生产计划.json', 'r', encoding='utf-8') as file:
        return json.load(file)


# 载入所有相关数据
def load_all_data():
    orders = pd.read_csv('data/orders.csv')
    hr_data = pd.read_csv('data/人力资源数据.csv')
    device_data = pd.read_csv('data/设备组管理数据.csv')
    material_data = pd.read_csv('data/黑湖MES物料主数据.csv')
    supply_chain_data = pd.read_csv('data/supply_chain_data.csv')
    return orders, hr_data, device_data, material_data, supply_chain_data


# 载入任务数据
def load_tasks():
    return pd.read_csv('data/tasks.csv')


# 保存任务数据
def save_tasks(tasks_df):
    tasks_df.to_csv('data/tasks.csv', index=False)


# 显示收集的所有数据
def show_get_data():
    tasks_df = load_tasks()

    # 获取当前任务ID
    if 'current_task_id' in st.session_state:
        current_task_id = st.session_state['current_task_id']
        current_task = tasks_df[tasks_df['任务编号'] == current_task_id].iloc[0]

        # 根据任务的具体数据获取状态展示相应数据或提示
        orders, hr_data, device_data, material_data, supply_chain_data = load_all_data()

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        # 订单数据展示逻辑
        st.subheader("订单数据")
        if pd.notna(current_task['当前订单号']):
            order_data = orders[orders['订单编号'] == current_task['当前订单号']]
            if not order_data.empty:
                st.dataframe(order_data)
            else:
                st.warning("订单数据未找到，请检查订单编号是否正确。")
        else:
            st.warning("当前任务未关联订单，请先获取订单数据。")

        # 人力资源数据展示逻辑
        with col1:
            st.subheader("人力资源数据")
            if current_task.get('恒基DMP人力资源', None) == 'done':
                st.dataframe(hr_data)
            else:
                st.warning("人力资源数据未获取，请完成人力资源数据获取步骤。")

        with col2:
            # 设备数据展示逻辑
            st.subheader("设备数据")
            if current_task.get('蘑菇云智控设备组管理', None) == 'done':
                st.dataframe(device_data)
            else:
                st.warning("设备组数据未获取，请完成设备组数据获取步骤。")

        with col3:
            # 物料数据展示逻辑
            st.subheader("物料数据")
            if current_task.get('黑湖MES物料主数据', None) == 'done':
                st.dataframe(material_data)
            else:
                st.warning("物料数据未获取，请完成物料数据获取步骤。")

        with col4:
            # 供应链数据展示逻辑
            st.subheader("供应链数据")
            if current_task.get('恒基DMP供应链管理', None) == 'done':
                st.dataframe(supply_chain_data)
            else:
                st.warning("供应链数据未获取，请完成供应链数据获取步骤。")

    else:
        st.error("未设置当前任务ID，请从任务详情页面选择任务。")


# 模拟AI分析过程
def perform_ai_analysis(task_id):
    tasks = load_tasks()
    task_index = tasks[tasks['任务编号'] == task_id].index[0]
    time.sleep(5)  # 模拟分析耗时
    show_analyze()
    tasks.loc[task_index, 'AI分析'] = "done"
    save_tasks(tasks)

def show_analyze():
    production_plan = load_production_plan()

    # Display markdown report
    st.markdown(production_plan['report'])

    # Display order data
    st.subheader("订单详情")
    order_data = production_plan['order_data']
    order_info = order_data['订单信息']
    order_df = pd.DataFrame([order_info])
    st.table(order_df)

    # Display material requirements
    st.subheader("物料需求详情")
    material_requirements = pd.DataFrame(order_data['物料需求'])
    st.dataframe(material_requirements)

    # Display equipment arrangements
    st.subheader("设备安排详情")
    equipment_arrangements = pd.DataFrame(order_data['设备安排'])
    st.dataframe(equipment_arrangements)

    # Display human resource arrangements
    st.subheader("人力资源配置")
    hr_config = pd.DataFrame(order_data['人力资源配置'])
    st.dataframe(hr_config)

# 显示智能生产计划页面
def show_smart_production_plan():
    st.title("智能生产计划")
    tasks_df = load_tasks()

    # 获取当前任务ID
    if 'current_task_id' in st.session_state:
        current_task_id = st.session_state['current_task_id']
        current_task = tasks_df[tasks_df['任务编号'] == current_task_id].iloc[0]
        with st.expander("获取数据"):
            show_get_data()

        # 检查任务是否已完成AI分析
        if current_task.get('AI分析', "") == 'done':
            with st.expander("AI分析"):
                show_analyze()
                st.success(f"AI分析已完成")
            if st.button("重新生成"):
                with st.expander("AI分析"):
                    with st.spinner("正在执行AI分析..."):
                        perform_ai_analysis(current_task_id)
                        st.success(f"AI分析完成")
        else:
            if st.button("执行AI分析"):
                with st.expander("AI分析"):
                    with st.spinner("正在执行AI分析..."):
                        perform_ai_analysis(current_task_id)
                        st.success(f"AI分析完成")
    else:
        st.error("未设置当前任务ID，请从任务详情页面选择任务。")