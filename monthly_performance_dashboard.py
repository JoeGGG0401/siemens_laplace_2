import streamlit as st
import os

def load_images(folder_path):
    # 获取文件夹内所有的图片文件
    images = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()  # 确保文件是有序的
    return images

def show_image_gallery(folder_path):
    # 加载图片文件名
    images = load_images(folder_path)
    if not images:
        st.error("未找到图片文件。请确保文件夹中有图片文件并重新加载页面。")
        return

    # 设置一个索引变量来跟踪当前显示的图片
    if 'index' not in st.session_state:
        st.session_state.index = 0

    # 创建按钮以及图片的显示逻辑
    col1, col2, col3 = st.columns([2, 30, 2])
    with col1:
        if st.button("◀️"):
            if st.session_state.index > 0:
                st.session_state.index -= 1
    with col3:
        if st.button("▶️"):
            if st.session_state.index < len(images) - 1:
                st.session_state.index += 1

    # 显示当前图片
    image_path = os.path.join(folder_path, images[st.session_state.index])
    st.image(image_path, use_column_width=True)

def show_dashboards():
    folder_path = "data/月度绩效"  # 指定包含图片的文件夹路径
    show_image_gallery(folder_path)
