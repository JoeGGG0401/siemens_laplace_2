import streamlit as st

def show_dashboards():
    # 视频文件路径
    video_path1 = "data/监控视频/成型车间.mp4"
    video_path2 = "data/监控视频/生产车间监控.mp4"

    # 展示视频
    st.header("成型车间监控")
    st.video(video_path1)

    st.header("生产车间监控")
    st.video(video_path2)