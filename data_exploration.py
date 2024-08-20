import streamlit as st
import supply_chain_dashboard
import raw_material_dashboard
import employee_hours_dashboard
import work_order_dashboard
import material_dispatch_dashboard
import monthly_performance_dashboard
import monitor_video
import orders_and_shipping_dashboard
import real_time_monitoring_dashboard
import static_order_dashboard


def show_data_exploration():
    # 标签页切换不同的数据看板
    tabs = st.tabs(["供应链看板", "原料库看板", "员工工时看板", "工单看板", "放料明细看板", "月度绩效看板", "监控视频",
                    "订单与发货预测", "实时设备监控", "静态订单"])

    with tabs[0]:
        supply_chain_dashboard.show_dashboards()
    with tabs[1]:
        raw_material_dashboard.show_dashboards()
    with tabs[2]:
        employee_hours_dashboard.show_dashboards()
    with tabs[3]:
        work_order_dashboard.show_dashboards()
    with tabs[4]:
        material_dispatch_dashboard.show_dashboards()
    with tabs[5]:
        monthly_performance_dashboard.show_dashboards()
    with tabs[6]:
        monitor_video.show_dashboards()
    with tabs[7]:
        orders_and_shipping_dashboard.show_dashboards()
    with tabs[8]:
        real_time_monitoring_dashboard.show_dashboards()
    with tabs[9]:
        static_order_dashboard.show_dashboards()

