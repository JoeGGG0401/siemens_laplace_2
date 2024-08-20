import json

import streamlit as st
import requests
import homepage
import task_execution
import task_execution_2
import data_exploration

# 聊天机器人配置
API_URL = "https://dify.laplacelab.ai/v1/chat-messages"
API_KEY = "app-afCotUtfHbYZlLrFKHXRXD0A"  # 替换成你的API密钥

if 'current_task_id' not in st.session_state:
    st.session_state['current_task_id'] = None

def send_message(query):
    """发送消息到聊天机器人并获取响应."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": {},
        "query": query,
        "response_mode": "streaming",
        "conversation_id": "",
        "user": "1"
    }
    response = requests.post(API_URL, headers=headers, json=data, stream=True)
    return response

# 设置页面布局和网站名称
st.set_page_config(
    page_icon="🏭",
    page_title="拉普拉斯🚀西门子",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("Laplace AI Lab 管理系统")



# 根据页面状态进行渲染
page = st.sidebar.radio("选择页面", ("首页", "数据探索", "智能生产计划", "数据大屏"))

# Page Routing
if page == "首页":
    homepage.show_dashboard()
elif page == "数据探索":
    data_exploration.show_data_exploration()
elif page == "智能生产计划":
    task_execution.show_task_execution()
elif page == "数据大屏":
    task_execution_2.show_task_execution()



if "messages" not in st.session_state:
    st.session_state.messages = []


# 聊天机器人交互部分
with st.sidebar:
    messages = st.container(height=400)
    messages.chat_message("assistant").write(f"您好，欢迎使用拉普拉斯智能助手")
    for message in st.session_state.messages:
        messages.chat_message(message["role"]).write(message["content"])

    if prompt := st.chat_input("请输入您的问题", key="chat_input"):
        messages.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = send_message(prompt)

        with messages.chat_message("assistant"):
            display_area = st.empty()
            full_message = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        decoded_line = decoded_line[6:]
                    try:
                        message_data = json.loads(decoded_line)
                        if 'answer' in message_data:
                            full_message += message_data['answer']
                            display_area.markdown(full_message)
                        if 'event' in message_data and message_data['event'] == 'message_end':
                            break
                    except json.JSONDecodeError as e:
                        st.error("解析JSON时出错")
                        continue
            st.session_state.messages.append({"role": "assistant", "content": full_message})

