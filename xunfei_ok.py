import streamlit as st
import SparkApi
import json

from streamlit_chat import message

# 以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35
appid = "078f75e7"  # 填写控制台中获取的 APPID 信息
api_secret = "YjU3M2Y1MmY5YmUyZmZmZmZlYWYxOGU2"  # 填写控制台中获取的 APISecret 信息
api_key = "44a7caa1af474b8f4c0c2ba9db39e06f"  # 填写控制台中获取的 APIKey 信息

# domain = "generalv3.5"  # Max版本
# domain = "generalv3"       # Pro版本
domain = "general"  # Lite版本

# Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"  # Max服务地址
# Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址

text = []  # 用于存储对话内容的列表


def getText(role, content):
    """
    构造包含角色和内容的对话信息，并添加到对话列表中

    参数：
    role (str): 对话角色，可以是 "user"（用户）或 "assistant"（助手）
    content (str): 对话内容

    返回值：
    text (list): 更新后的对话列表
    """
    jsoncon = {"role": role, "content": content}
    text.append(jsoncon)
    return text


def getlength(text):
    """
    计算对话列表中所有对话内容的字符长度之和

    参数：
    text (list): 对话列表

    返回值：
    length (int): 对话内容的字符长度之和
    """
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    """
    检查对话列表中的对话内容字符长度是否超过限制（8000个字符）
    如果超过限制，删除最早的对话内容，直到满足字符长度限制

    参数：
    text (list): 对话列表

    返回值：
    text (list): 更新后满足字符长度限制的对话列表
    """
    while getlength(text) > 8000:
        del text[0]
    return text


def end_click():
    st.session_state['prompts'] = [
        {"role": "system", "content": "您是一个乐于助人的助手。尽量简洁明了地回答问题，并带有一点幽默表达。"}]
    st.session_state['past'] = []
    st.session_state['generated'] = []
    st.session_state['user'] = ""


if __name__ == '__main__':
    # 在 Streamlit 网页上显示欢迎文本
    st.markdown("#### 我是讯飞星火认知模型机器人，我可以回答您的任何问题！")

    # 初始化对话历史和生成的响应列表
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    # 获取用户输入的问题
    user_input = st.text_input("请输入您的问题:", key='input')

    if user_input:
        # 构造用户输入的对话信息
        question = checklen(getText("user", user_input))

        # 调用 SparkApi 中的函数进行问题回答
        SparkApi.answer = ""
        # print("星火:", end="")
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
        output = getText("assistant", SparkApi.answer)

        # 将用户输入和生成的响应添加到对话历史和生成的响应列表中
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(str(output[1]['content']))

    # with open('history.json', 'w', encoding='utf-8') as file:
    #     json.dump(st.session_state.to_dict(), file, ensure_ascii=False, indent=4)

    if st.session_state['generated']:
        # 在网页上显示对话历史和生成的响应
        # for i in range(len(st.session_state['generated']) - 1, -1, -1):
        for i in range(0, len(st.session_state['generated']), 1):
            # print('generate: ', st.session_state["generated"][i])
            # print('past: ', st.session_state['past'][i])

            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', allow_html=True)
            message(st.session_state["generated"][i], key=str(i), allow_html=True)
