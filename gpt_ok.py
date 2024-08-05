from openai import OpenAI
import streamlit as st

st.title("聊天机器人")
st.button("如果模型做的不好，请给我们反馈")

key = 'sk-SFXiex2MCespk9H83d766aE49cCd4cFd8a5b4dEbAb728507'
client = OpenAI(api_key=key, base_url="https://free.gpt.ge/v1/", default_headers={"x-foo": "true"})

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("请问我问题"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
