import streamlit as st
from openai import OpenAI
import os

st.set_page_config(
    page_title="LAWGURU",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    st.sidebar.title("MENU")
    api_key = ""
    st.sidebar.image("logo.jpeg", use_column_width=True)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    st.title("Your Friendly Neighbourhood Lawyer")

    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
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

if __name__ == "__main__":
    main()
