import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Load Data
def load_data():
    with open('data/设备实时状态数据.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Preprocess Data
def preprocess_data(data):
    machines = []
    for group in data['data']['groupObject']:
        for machine in group['groupList']:
            machine['groupName'] = group['groupName']
            machines.append(machine)
    return pd.DataFrame(machines)


# Visualizations
def plot_status_distribution(df_machines):
    fig = px.pie(df_machines, names='deviceState', title='设备状态分布',
                 labels={'deviceState': '设备状态'})
    return fig

def plot_group_status_distribution(df_machines):
    status_summary = df_machines.groupby(['groupName', 'deviceState']).size().reset_index(name='数量')
    fig = px.bar(status_summary, x='groupName', y='数量', color='deviceState',
                 title='各组设备状态',
                 labels={'groupName': '组名', 'deviceState': '设备状态', '数量': '数量'})
    return fig

# Display in Streamlit
def show_dashboards():
    data = load_data()
    df_machines = preprocess_data(data)

    # Metrics
    total_machines = len(df_machines)
    running_machines = df_machines[df_machines['deviceState'] == '1'].shape[0]
    idle_machines = df_machines[df_machines['deviceState'] == '0'].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("总设备数", total_machines)
    col2.metric("运行设备数", running_machines)
    col3.metric("空闲设备数", idle_machines)

    col4, col5 = st.columns(2)

    col4.plotly_chart(plot_status_distribution(df_machines), use_container_width=True)
    col5.plotly_chart(plot_group_status_distribution(df_machines), use_container_width=True)

    st.write("详细设备数据：")
    st.dataframe(df_machines)
