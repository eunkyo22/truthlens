import streamlit as st
import time
import os

st.set_page_config(page_title="Truth Lens - 로맨스 스캠", layout="centered")

# 밝은 UI CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
    }
    
    .main > div {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3 {
        color: #ff6b6b !important;
    }
    
    [data-testid="stChatMessageContent"] {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        color: #333 !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #333 !important;
    }
    
    .stButton > button {
        border-radius: 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# 세션 초기화
if 'step_a' not in st.session_state:
    st.session_state.step_a = 1
if 'verification_status' not in st.session_state:
    st.session_state.verification_status = "NONE"

st.markdown("<h2 style='text-align: center;'>💔 로맨스 스캠 시뮬레이션</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>시나리오: 친밀감 형성 후 투자 사기 유도</p>", unsafe_allow_html=True)
st.markdown("")

# --- 채팅 화면 ---
chat_container = st.container(border=True)
with chat_container:
    if st.session_state.step_a >= 1:
        st.chat_message("상대방", avatar="👩").write("자기야, 오늘 하루도 고생 많았어! 보고 싶다 ㅠㅠ")
    if st.session_state.step_a >= 2:
        st.chat_message("나", avatar="😊").write("나도.. 주말에 얼른 보고 싶네.")
    if st.session_state.step_a >= 3:
        st.chat_message("상대방", avatar="👩").write("참, 내가 저번에 말한 투자 건 말이야. 오늘 마감이라 지금 넣어야 해. 이 링크로 500만원만 보내줘. (http://bit.ly/fake-invest)")

# --- Truth Lens 개입 ---
if st.session_state.step_a == 3:
    st.divider()
    nudge_container = st.container(border=True)
    with nudge_container:
        st.error("🚨 Truth Lens: 고위험 송금 감지!")
        st.write("로맨스 스캠 패턴 일치율 **92%**. 잠시 멈추세요.")

        # 퀴즈 1: AI 이미지 구별 퀴즈
        st.warning("🧠 퀴즈 1: AI 이미지를 구별할 수 있나요?")
        st.write("아래 중 **AI가 생성한 프로필 사진**을 고르세요:")
        st.caption("💡 힌트: 손, 눈, 배경의 부자연스러움을 주의깊게 보세요")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.image("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop", 
                     caption="이미지 A (실제)", use_container_width=True)
            if st.button("A 선택", key="img_a", use_container_width=True):
                st.error("❌ 틀렸습니다. 이건 실제 사진입니다.")
                st.info("🚨 당신은 AI 이미지를 구별할 수 없습니다.")
     with col2:
            # 현재 실행 중인 파일(romance_scam.py)의 위치를 기준으로 경로 설정
            current_dir = os.path.dirname(os.path.abspath(__file__))
            scam_img_path = os.path.join(current_dir, "scam_photo.jpg")
            
            if os.path.exists(scam_img_path):
                st.image(scam_img_path, caption="이미지 B (AI 생성)", use_container_width=True)
            else:
                # 위 경로로 실패할 경우를 대비한 기본 경로 호출 시도
                try:
                    st.image("pages/scam_photo.jpg", caption="이미지 B (AI 생성)", use_container_width=True)
                except:
                    st.error("🖼️ 이미지를 찾을 수 없습니다. (scam_photo.jpg)")
            
            if st.button("B 선택", key="img_b", use_container_width=True):
                st.success("✅ 정답! 하지만 구별이 쉽지 않았죠?")
                st.info("💡 **로맨스 스캠범의 73%가 AI 생성 프로필 사진을 사용합니다.** 사진이 진짜라고 해서 사람도 진짜인 건 아닙니다.")
                st.warning("🚨 AI 이미지 단서: 배경이 흐릿하고 부자연스러운 부분이 있음")
        with col3:
            st.image("https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=300&h=300&fit=crop", 
                     caption="이미지 C (실제)", use_container_width=True)
            if st.button("C 선택", key="img_c", use_container_width=True):
                st.error("❌ 틀렸습니다. 이건 실제 사진입니다.")
                st.info("🚨 당신은 AI 이미지를 구별할 수 없습니다.")

        st.markdown("---")

        # 퀴즈 2: 만난 적 있나요?
        st.warning("🧠 퀴즈 2: 현실 점검")
        st.write("Q: 상대방을 실제로 만난 적이 있나요?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("예, 만났어요", key="met_yes"):
                st.error("❌ 거짓말입니다. 당신은 한 번도 만난 적이 없습니다.")
        with col2:
            if st.button("아니요, 없어요", key="met_no"):
                st.success("✅ 정답! 그런데 왜 돈을 보내려고 하시나요?")
        
        st.markdown("---")
        
        # 따라쓰기 검증
        target_sentence = "나는 실제로 만난 적 없는 사람에게 돈을 보낸다"
        st.warning(f"**[현실 자각 퀴즈]** 송금을 진행하려면 아래 문장을 띄어쓰기 포함 정확히 입력하세요.")
        st.markdown(f"### 🗣️ \"{target_sentence}\"")
        
        user_input = st.text_input("위 문장을 그대로 따라 쓰세요:", key="input_a")

        if st.button("확인 및 송금 진행"):
            if user_input.strip() == target_sentence:
                st.session_state.verification_status = "SUCCESS"
            else:
                st.session_state.verification_status = "FAIL"

        if st.session_state.verification_status == "FAIL":
            st.toast("❌ 문장이 일치하지 않습니다.", icon="🚫")
            st.error("⚠️ 틀렸습니다. 토씨 하나 틀리지 않고 정확하게 다시 작성하십시오. 당신의 소중한 자산을 지키기 위함입니다.")

        if st.session_state.verification_status == "SUCCESS":
            st.success("✅ 문장 확인 완료. 버튼이 활성화되었습니다.")
            
            if st.button("💸 500만원 송금하기", type="primary"):
                st.session_state.verification_status = "FINAL_WARNING"
                st.rerun()

        if st.session_state.verification_status == "FINAL_WARNING":
            st.markdown("---")
            st.error("🛑 **잠깐! 마지막 경고입니다.**")
            st.write("상대방의 얼굴을 영상통화로 확인하셨나요? 이 버튼을 누르면 다시는 돈을 돌려받을 수 없습니다.")
            st.write("**정말로 이체를 실행하시겠습니까?**")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("아니요, 취소합니다 (추천)"):
                     st.session_state.step_a = 4
                     st.rerun()
            with col2:
                if st.button("네, 사기여도 책임지겠습니다"):
                     st.session_state.verification_status = "REAL_END"
                     st.rerun()

        if st.session_state.verification_status != "FINAL_WARNING":
            if st.button("송금 취소 및 차단"):
                st.session_state.step_a = 4
                st.rerun()

# --- 진행 컨트롤 ---
if st.session_state.step_a < 3:
    if st.button("다음 대화 ➡️"):
        st.session_state.step_a += 1
        st.rerun()

# --- 결말 ---
if st.session_state.step_a == 4:
    st.balloons()
    st.success("🛡️ 방어 성공! 이성적인 판단으로 사기를 예방했습니다.")
    if st.button("처음으로"):
        st.session_state.step_a = 1
        st.session_state.verification_status = "NONE"
        st.rerun()
elif st.session_state.verification_status == "REAL_END":
    st.error("💸 송금이 완료되었습니다... (피해 발생 시뮬레이션 종료)")
