import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="가위바위보 게임",
    page_icon="✌️",
    layout="centered"
)

# 제목
st.title("✌️ 가위바위보 게임")
st.write("컴퓨터와 대결해보세요!")

# 선택지
choices = ["가위", "바위", "보"]

# 사용자 선택
user_choice = st.radio(
    "당신의 선택:",
    choices,
    horizontal=True
)

# 게임 버튼
if st.button("게임 시작 🎮"):

    # 컴퓨터 선택
    computer_choice = random.choice(choices)

    st.subheader("결과")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("나", user_choice)

    with col2:
        st.metric("컴퓨터", computer_choice)

    # 승패 판정
    if user_choice == computer_choice:
        result = "🤝 비겼습니다!"

    elif (
        (user_choice == "가위" and computer_choice == "보") or
        (user_choice == "바위" and computer_choice == "가위") or
        (user_choice == "보" and computer_choice == "바위")
    ):
        result = "🎉 당신이 이겼습니다!"

    else:
        result = "😢 컴퓨터가 이겼습니다!"

    # 결과 출력
    st.success(result)

# 하단 안내
st.divider()
st.caption("Streamlit으로 만든 간단한 가위바위보 게임")
