import streamlit as st
import json
import pandas as pd

def load_production_plan():
    with open('data/生产计划.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_production_plan(production_plan):
    with open('data/生产计划.json', 'w', encoding='utf-8') as file:
        json.dump(production_plan, file, indent=4)

def show_create_work_order():
    st.title("黑湖MES生产工单创建")
    production_plan = load_production_plan()

    # 使用列来分隔内容，每行显示两个部分
    col1, col2 = st.columns(2)

    # 订单信息
    with col1.container():
        st.subheader("订单信息")
        order_info = production_plan['order_data']['订单信息']
        for key in order_info.keys():
            order_info[key] = st.text_input(f"{key}", value=order_info[key])

    # 物料需求
    with col2.container():
        st.subheader("物料需求")
        for i, material in enumerate(production_plan['order_data']['物料需求']):
            with st.expander(f"物料 {i+1}"):
                for key, value in material.items():
                    material[key] = st.text_input(f"{key} {i+1}", value=value)

    col3, col4 = st.columns(2)

    # 设备安排
    with col3.container():
        st.subheader("设备安排")
        for i, device in enumerate(production_plan['order_data']['设备安排']):
            with st.expander(f"设备 {i+1}"):
                for key, value in device.items():
                    device[key] = st.text_input(f"{key} {i+1}", value=value)

    # 人力资源配置
    with col4.container():
        st.subheader("人力资源配置")
        for i, resource in enumerate(production_plan['order_data']['人力资源配置']):
            with st.expander(f"人员 {i+1}"):
                for key, value in resource.items():
                    resource[key] = st.text_input(f"{key} {i+1}", value=value)

    # 生产进度和质量控制
    with col1.container():
        st.subheader("生产进度和质量控制")
        quality_control = production_plan['order_data']['生产进度和质量控制']
        for key, value in quality_control.items():
            quality_control[key] = st.text_input(f"{key}", value=value)

    # 操作按钮
    if st.button("创建工单"):
        save_production_plan(production_plan)

        col1, col2 = st.columns([1, 3])  # 划分列的比例，col1更窄，适合放置图片
        with col1:
            st.image('data/创建工单成功截图.png', caption='工单创建成功截图')
        with col2:
            st.success("工单创建成功并数据已更新！")
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
