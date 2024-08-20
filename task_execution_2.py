import string

import streamlit as st
import task_details
import data_acquisition
import real_time_monitoring_dashboard
import material_data_management
import task_details_2
import random


# 生成API Key
def generate_api_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


def show_task_execution():
    # 创建多个步骤的标签页
    tabs = st.tabs([
        "任务详情",
        "数据获取",
        "数据整合",
        "智能助手",
        "数据大屏"
    ])

    # 任务详情标签页
    with tabs[0]:
        task_details_2.show_task_details()

    # 数据获取标签页
    with tabs[1]:
        sub_tabs = st.tabs(["订单收集", "库存收集", "生产数据收集"])
        with sub_tabs[0]:
            data_acquisition.show_data_acquisition()
        with sub_tabs[1]:
            material_data_management.show_material_data_management()
        with sub_tabs[2]:
            real_time_monitoring_dashboard.show_dashboards()

    with tabs[2]:
        st.subheader("数据整合")
        real_time_monitoring_dashboard.show_dashboards()

    # 智能生产计划标签页
    with tabs[3]:
        st.subheader("智能助手配置")
        st.text_input("提示词")
        if st.button("生成API Key"):
            api_key = generate_api_key()
            st.success(f"生成的API Key: {api_key}")

    # 工单创建标签页
    with tabs[4]:
        st.subheader("数据可视化大屏")
        # 通过 iframe 嵌入外部的数据可视化大屏
        st.markdown(
            f'<iframe src="https://sales-operations.laplacelab.cn/" width="100%" height="600" frameborder="0"></iframe>',
            unsafe_allow_html=True)

