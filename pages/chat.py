import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
import ollama
from langchain_ollama.llms import OllamaLLM

# 템플릿 설정
template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

# 모델 설정
model = OllamaLLM(model="llama3.1")

# 체인 생성
chain = prompt | model

# Streamlit UI 설정
st.title("💬 Local LLMBot")

# 메시지 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "어떻게 도와드릴까요?"}]

# 이전 메시지 출력
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

# 응답 생성 함수
def generate_response():
    response = ollama.chat(model='llama3.1', stream=True, messages=st.session_state.messages)
    full_message = ""
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        full_message += token
        st.session_state["full_message"] += token
        yield token
    return full_message

# 사용자 입력 처리
if prompt := st.chat_input():
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)

    # 응답 생성 및 출력
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)

    # 생성된 응답 메시지 추가
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})