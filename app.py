import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="진로 찾기 챗봇",
    page_icon="🎓",
)

st.title("🎓 진로 찾기 챗봇")
st.caption("관심사, 성격, 강점을 바탕으로 진로를 추천해드립니다.")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("API 키를 불러올 수 없습니다. Secrets 설정을 확인하세요.")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 😊\n\n"
                "관심 있는 분야, 좋아하는 과목, 성격 등을 알려주시면 "
                "적합한 진로와 직업을 추천해드릴게요."
            ),
        }
    ]

# 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("질문을 입력하세요"):

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini에 전달할 대화 구성
    history_text = ""

    for msg in st.session_state.messages:
        role = "사용자" if msg["role"] == "user" else "챗봇"
        history_text += f"{role}: {msg['content']}\n"

    system_prompt = """
당신은 진로 상담 전문가입니다.

규칙:
1. 학생의 관심사와 강점을 파악한다.
2. 적합한 직업과 진로를 3개 이상 제안한다.
3. 추천 이유를 설명한다.
4. 필요한 전공, 자격증, 학습 방법을 알려준다.
5. 친절하고 구체적으로 답변한다.
"""

    full_prompt = f"""
{system_prompt}

대화 기록:
{history_text}

답변:
"""

    try:
        with st.chat_message("assistant"):
            with st.spinner("생각 중..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=full_prompt,
                )

                answer = response.text

                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        error_msg = f"오류가 발생했습니다.\n\n{str(e)}"

        with st.chat_message("assistant"):
            st.error(error_msg)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_msg,
            }
        )
