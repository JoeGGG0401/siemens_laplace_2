import streamlit as st
import task_details
import data_acquisition
import device_management
import hr_management
import supply_chain_management
import material_data_management
import smart_production_plan
import dingtalk_notification_1
import dingtalk_notification_2
import create_work_order
import work_order_dispatch


def show_task_execution():
    # 创建多个步骤的标签页
    tabs = st.tabs([
        "任务详情",
        "数据获取",
        "智能生产计划",
        "工单创建",
        "工单下发"
    ])

    # 任务详情标签页
    with tabs[0]:
        task_details.show_task_details()

    # 数据获取标签页
    with tabs[1]:
        sub_tabs = st.tabs(["恒基DMP订单", "蘑菇云智控设备组管理", "恒基DMP人力资源", "恒基DMP供应链管理", "黑湖MES物料主数据"])
        with sub_tabs[0]:
            data_acquisition.show_data_acquisition()
        with sub_tabs[1]:
            device_management.show_device_management()
        with sub_tabs[2]:
            hr_management.show_hr_management()
        with sub_tabs[3]:
            supply_chain_management.show_supply_chain_management()
        with sub_tabs[4]:
            material_data_management.show_material_data_management()

    # 智能生产计划标签页
    with tabs[2]:
        smart_production_plan.show_smart_production_plan()

    # 工单创建标签页
    with tabs[3]:
        sub_tabs = st.tabs(["钉钉工作通知", "黑湖MES生产工单创建"])
        with sub_tabs[0]:
            dingtalk_notification_1.show_dingtalk_notification()
        with sub_tabs[1]:
            create_work_order.show_create_work_order()

    # 工单下发标签页
    with tabs[4]:
        sub_tabs = st.tabs(["钉钉工作通知", "黑湖MES生产工单下发"])
        with sub_tabs[0]:
            dingtalk_notification_2.show_dingtalk_notification()
        with sub_tabs[1]:
            work_order_dispatch.show_work_order_dispatch()