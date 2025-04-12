# app.py 示例
import streamlit as st

st.title("Hello, Streamlit!")
name = st.text_input("你的名字")
if name:
    st.write(f"你好，{name}！欢迎使用这个小工具！")
