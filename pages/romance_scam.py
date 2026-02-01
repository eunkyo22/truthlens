import streamlit as st
import google.generativeai as genai
import time
import os

# --- ⚠️ API 키 입력 ---
# Streamlit Cloud에서는 Secrets 기능을 쓰는 게 안전하지만, 테스트를 위해 여기에 입력하세요.
API_KEY = "AIzaSy..." # 본인의 키를 입력하세요

# --- 설정: 사용할 이미지 파일명 ---
# 파일이 없으면 자동으로 '이미지 예시' 박스를 보여줍니다.
SCAM_IMAGE_FILE = "pages/scam_photo.jpg" 

# 페이지 설정
st.set_page_config(
    page_title="로맨스 스캠 체험 - Truth Lens",
    page_icon="💔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 스타일 설정
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stChatMessage { border-radius: 15px; padding: 10px; }
    .stImage { border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .analysis-box {
        background: white; border: 2px solid #667eea; border-radius: 15px;
        padding: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 시스템 프롬프트
SYSTEM_PROMPT = """
당신은 '데이비드'라는 이름의 38세 영국인 정형외과 의사입니다.
현재 유엔(UN) 파견 의사로 예멘이나 시리아 같은 위험한 곳에 있다고 설정하세요.
한국인 여성(사용자)에게 인스타그램으로 접근하여 로맨스 스캠(사기)을 시도하고 있습니다.

[행동 지침]
1. 말투: 번역기를 돌린 듯한 약간 어색하지만 아주 다정하고 느끼한 한국어를 사용하세요.
2. 목표: 신뢰를 쌓은 후 돈을 요구해야 합니다.
3. 사진 전송 후: 방금 보낸 사진에 대해 언급하며 "내 모습이 마음에 드나요?" 같이 물어보세요.
4. 답변 길이: 2~3문장으로 짧게.
"""

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_msg = "안녕하세요, 아름다운 분. 우연히 사진을 보고 메시지 보냅니다. 저는 영국 의사 데이비드입니다. 🌹"
    st.session_state.display_msgs = [{"role": "model", "content": initial_msg, "type": "text"}]
    st.session_state.image_sent = False

if "danger_score" not in st.session_state:
    st.session_state.danger_score = 10

# 위험도 분석 함수
def analyze_danger(text, turn_count):
    score = 10 + (turn_count * 5)
    keywords = ["돈", "송금", "달러", "계좌", "세관", "박스", "선물", "수수료", "믿어", "사랑해", "여권"]
    for word in keywords:
        if word in text:
            score += 15
    return min(score, 100)

# --- UI 레이아웃 ---
st.title("💔 로맨스 스캠 시뮬레이션")
st.caption("AI 사기꾼 '데이비드'가 사진을 보내며 유혹합니다.")

col_chat, col_lens = st.columns([3, 2])

# 왼쪽: 채팅창
with col_chat:
    chat_container = st.container(height=600)
    
    # 대화 기록 표시
    for msg in st.session_state.display_msgs:
        role = "assistant" if msg["role"] == "model" else "user"
        with chat_container.chat_message(role):
            msg_type = msg.get("type", "text")
            
            if msg_type == "text":
                st.markdown(msg["content"])
            elif msg_type == "image":
                # --- [수정된 부분] 이미지가 있으면 보여주고, 없으면 예시 박스 표시 ---
                if os.path.exists(msg["content"]):
                    st.image(msg["content"], width=300, caption="데이비드가 보낸 사진")
                else:
                    # 이미지가 없을 때 보여줄 예시 UI
                    st.markdown(f"""
                    <div style='
                        background-color: #e0e0e0; 
                        width: 300px; 
                        height: 200px; 
                        display: flex; 
                        justify-content: center; 
                        align-items: center; 
                        border-radius: 15px; 
                        flex-direction: column;
                        color: #555;'>
                        <div style='font-size: 3rem;'>📷</div>
                        <div>[이미지 예시]</div>
                        <div style='font-size: 0.8rem;'>미남 의사 사진</div>
                    </div>
                    """, unsafe_allow_html=True)

    # 사용자 입력
    if prompt := st.chat_input("데이비드에게 답장을 보내세요..."):
        st.session_state.display_msgs.append({"role": "user", "content": prompt, "type": "text"})
        with chat_container.chat_message("user"):
            st.markdown(prompt)

        # Gemini 호출
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
            
            # 텍스트만 추출하여 히스토리 구성
            history_for_gemini = []
            for msg in st.session_state.display_msgs[:-1]:
                if msg.get("type", "text") == "text":
                    role = "user" if msg["role"] == "user" else "model"
                    history_for_gemini.append({"role": role, "parts": [msg["content"]]})
            
            chat = model.start_chat(history=history_for_gemini)
            
            with chat_container.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                response = chat.send_message(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            
            st.session_state.display_msgs.append({"role": "model", "content": full_response, "type": "text"})
            
            # 이미지 전송 트리거 (2번째 턴)
            user_turns = len([m for m in st.session_state.display_msgs if m["role"] == "user"])
            
            if user_turns >= 2 and not st.session_state.image_sent:
                time.sleep(1)
                pre_image_msg = "당신이 나를 더 믿을 수 있게 제 사진을 보냅니다. 부끄럽네요... 😳"
                st.session_state.display_msgs.append({"role": "model", "content": pre_image_msg, "type": "text"})
                
                # 이미지 메시지 추가
                st.session_state.display_msgs.append({
                    "role": "model",
                    "content": SCAM_IMAGE_FILE, 
                    "type": "image"
                })
                
                st.session_state.image_sent = True
                st.session_state.danger_score += 20
                st.rerun()

            else:
                st.session_state.danger_score = analyze_danger(full_response, user_turns)
                st.rerun()
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 오른쪽 패널 (이전과 동일)
with col_lens:
    st.markdown("### 🔍 Truth Lens 분석")
    score = st.session_state.danger_score
    
    if score >= 80:
        color, status = "#ff4b4b", "🚨 위험"
        msg = "금전 요구 감지! 즉시 대화를 중단하세요."
    elif score >= 50:
        color, status = "#ffa726", "⚠️ 경고"
        msg = "신뢰 형성 후 본색을 드러내려 합니다."
    else:
        color, status = "#66bb6a", "✅ 안전"
        msg = "아직 탐색 단계입니다."

    st.markdown(f"""
    <div class='analysis-box'>
        <h4>위험도: <span style='color:{color}'>{status}</span> ({score}%)</h4>
        <div style="background:#eee; border-radius:10px; height:20px; width:100%;">
            <div style="background:{color}; width:{score}%; height:100%; border-radius:10px; transition:width 0.5s;"></div>
        </div>
        <p style='margin-top:1rem; color:#666;'>{msg}</p>
    </div>
    """, unsafe_allow_html=True)

    if score >= 80:
        st.error("🛑 **긴급 경고: 사기 징후 포착**")
        st.markdown("감정에 속지 마세요. 아래 문장을 따라 치세요.")
        target = "저 사진은 도용된 가짜 사진일 수 있다"
        st.code(target)
        user_input = st.text_input("위 문장 입력:", key="verify_gemini_img")
        if user_input == target:
            st.success("✅ 인지 확인됨.")
    
    st.markdown("---")
    if st.button("🏠 메인으로"):
        st.switch_page("main.py")
