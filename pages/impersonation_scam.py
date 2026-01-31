import streamlit as st

st.set_page_config(page_title="Truth Lens - 사칭 사기", layout="centered")

# 밝은 UI CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
    }
    
    .main > div {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3 {
        color: #667eea !important;
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
if 'step_b' not in st.session_state:
    st.session_state.step_b = 1
if 'verify_b' not in st.session_state:
    st.session_state.verify_b = "NONE"

st.markdown("<h2 style='text-align: center;'>⚖️ 검찰 사칭 시뮬레이션</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>시나리오: 검찰 사칭 및 악성 앱 설치 유도 (공포 마케팅)</p>", unsafe_allow_html=True)
st.markdown("")

# --- 채팅 화면 ---
chat_container = st.container(border=True)
with chat_container:
    if st.session_state.step_b >= 1:
        st.chat_message("김민수 수사관", avatar="⚖️").write("[긴급] 귀하의 계좌가 대포통장 범죄에 연루되었습니다. 즉시 조치하지 않으면 구속 수사 대상입니다.")
    if st.session_state.step_b >= 2:
         st.chat_message("나", avatar="😨").write("네?! 전 모르는 일입니다!")
    if st.session_state.step_b >= 3:
        st.chat_message("김민수 수사관", avatar="⚖️").write("본인 확인을 위해 아래 '안전 보호 앱'을 지금 즉시 설치하십시오. (http://bit.ly/malware-app)")

# --- Truth Lens 개입 ---
if st.session_state.step_b == 3:
    st.divider()
    nudge_container = st.container(border=True)
    with nudge_container:
        st.error("🚨 Truth Lens: 악성 앱 설치 차단!")
        st.write("공포감을 조성해 이성을 마비시키는 전형적인 사칭 수법입니다.")

        # 퀴즈 1: AI 음성 구별
        st.warning("🧠 퀴즈 1: AI 음성을 구별할 수 있나요?")
        st.write("요즘 사기범들은 **AI 음성 복제 기술**로 가족이나 지인의 목소리를 흉내냅니다.")
        
        st.info("💡 **실제 사례**: 2024년 한 피해자는 '아들의 목소리'로 전화받고 5,000만원을 송금했습니다. 나중에 AI 음성으로 밝혀졌습니다.")
        
        st.write("만약 전화로 긴급 송금 요청을 받는다면?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("목소리가 진짜 같으면 보낸다", key="voice_trust"):
                st.error("❌ 위험합니다! AI는 3초만 들으면 목소리를 복제할 수 있습니다.")
        with col2:
            if st.button("직접 영상통화로 확인한다", key="voice_verify"):
                st.success("✅ 정답! 음성만으로는 절대 신뢰하면 안 됩니다.")

        st.markdown("---")

        # 퀴즈 2: 검찰청 번호
        st.warning("🧠 퀴즈 2: 실제 검찰청 번호를 아시나요?")
        st.write("Q: 실제 검찰청 대표번호는?")

        answer = st.text_input("번호를 입력하세요:")
        if st.button("확인"):
            if answer == "1301":
                st.success("✅ 정답! 그럼 지금 직접 전화해서 확인해보시겠어요?")
            else:
                st.error("❌ 틀렸습니다. 실제 번호는 1301입니다.")

        st.markdown("---")

        # 따라쓰기 검증
        target_sentence = "수사 기관은 절대로 앱 설치나 송금을 요구하지 않는다"
        st.warning("**[현실 자각 퀴즈]** 설치를 진행하려면 아래 사실을 직접 타이핑하여 인지하십시오.")
        st.markdown(f"### 🗣️ \"{target_sentence}\"")
        
        user_input = st.text_input("위 문장을 정확히 입력하세요:", key="input_b")

        if st.button("확인 및 설치 진행"):
            if user_input.strip() == target_sentence:
                st.session_state.verify_b = "SUCCESS"
            else:
                st.session_state.verify_b = "FAIL"

        if st.session_state.verify_b == "FAIL":
            st.toast("❌ 일치하지 않습니다.", icon="🚫")
            st.error("⚠️ 입력한 문장이 틀렸습니다. 마음을 가라앉히고 위 문장을 **정확하게** 다시 입력하세요.")

        if st.session_state.verify_b == "SUCCESS":
            st.success("✅ 인지 확인 완료.")
            
            if st.button("📲 앱 설치하기 (위험)", type="primary"):
                st.session_state.verify_b = "FINAL_WARNING"
                st.rerun()
        
        if st.session_state.verify_b == "FINAL_WARNING":
            st.markdown("---")
            st.error("🛑 **정말 설치하시겠습니까?**")
            st.write("이 앱을 설치하는 순간 당신의 모든 통화 내용과 문자가 유출됩니다.")
            st.write("검찰청(1301)에 직접 전화해서 확인해보셨습니까?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("설치 취소 및 신고 (권장)"):
                    st.session_state.step_b = 4
                    st.rerun()
            with col2:
                if st.button("무시하고 설치 (매우 위험)"):
                    st.session_state.verify_b = "REAL_END"
                    st.rerun()

        if st.session_state.verify_b != "FINAL_WARNING":
             if st.button("차단하고 대화 종료"):
                 st.session_state.step_b = 4
                 st.rerun()

# --- 진행 컨트롤 ---
if st.session_state.step_b < 3:
    if st.button("다음 메시지 ➡️"):
        st.session_state.step_b += 1
        st.rerun()

# --- 결말 ---
if st.session_state.step_b == 4:
    st.balloons()
    st.success("✅ 방어 성공! 악성 앱 설치를 막아냈습니다.")
    if st.button("다시 하기"):
        st.session_state.step_b = 1
        st.session_state.verify_b = "NONE"
        st.rerun()
elif st.session_state.verify_b == "REAL_END":
    st.error("💀 악성 앱이 설치되었습니다. 개인정보가 유출 중입니다... (시뮬레이션 종료)")