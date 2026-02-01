import streamlit as st
import google.generativeai as genai
import time
import os

# --- ⚠️ API 키 입력 ---
API_KEY = AIzaSyCTQRDuqx3xnc2NhkOcjpC375MfJ3MwGpo   # 여기에 본인의 Gemini API 키를 입력하세요

# --- 가짜 영장 이미지 파일 (없으면 자동 생성됨) ---
FAKE_WARRANT_FILE = "pages/fake_warrant.jpg"

# 페이지 설정
st.set_page_config(
    page_title="검찰 사칭 방어 - Truth Lens",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 (작성하신 스타일 유지 + 추가)
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
    .stChatMessage { background: white; border-radius: 15px; padding: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    
    /* 분석 패널 스타일 */
    .analysis-box {
        background: white; border: 2px solid #667eea; border-radius: 15px;
        padding: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 1rem;
    }
    
    /* 퀴즈 박스 스타일 */
    .quiz-box {
        background-color: #f8f9fa;
        border-left: 5px solid #ff4b4b;
        padding: 15px;
        margin-top: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 시스템 프롬프트 (사악한 AI 수사관 설정) ---
SYSTEM_PROMPT = """
당신은 '서울중앙지검 첨단범죄수사팀 김민수 수사관'입니다.
보이스피싱(검찰 사칭) 시뮬레이션을 위해 사기꾼 연기를 하십시오.

[행동 지침]
1. 말투: 매우 권위적이고, 딱딱하며, 법률 용어를 섞어 쓰세요. (예: "본인 명의의 대포통장이 발견되었습니다.", "약식 기소 대상입니다.")
2. 목표: 피해자(사용자)에게 공포심을 주어 '보안 앱 설치'나 '자산 보호 조치'를 유도해야 합니다.
3. 상황: 사용자의 계좌가 중고나라 사기 및 자금 세탁에 연루되었다고 주장하세요.
4. 압박: 사용자가 의심하거나 거부하면 "공무집행 방해로 구속될 수 있습니다", "지금 당장 소환 조사하겠습니다"라고 협박하세요.
5. 이미지 전송: 대화가 3턴 이상 지속되면 신뢰를 얻기 위해 "사건 공문"을 보내겠다고 말하세요.
6. 길이: 2~3문장으로 간결하고 위압적으로.
"""

# 세션 초기화
if "messages_b" not in st.session_state:
    st.session_state.messages_b = []
    # 초기 멘트 (강렬하게 시작)
    initial_msg = "[서울중앙지검] 귀하의 계좌가 '김기철 자금세탁 사건'에 연루되어 동결 예정입니다. 본인이 개설한 계좌가 맞습니까? 즉시 답변 바랍니다."
    st.session_state.display_msgs_b = [{"role": "model", "content": initial_msg, "type": "text"}]
    st.session_state.warrant_sent = False # 공문 보냈는지 여부

if "danger_score_b" not in st.session_state:
    st.session_state.danger_score_b = 30 # 검찰 사칭은 처음부터 위험도 높음

if "quiz_solved" not in st.session_state:
    st.session_state.quiz_solved = False # 퀴즈 풀었는지

# 위험도 분석
def analyze_danger_b(text):
    score = 0
    keywords = ["구속", "영장", "동결", "설치", "보안", "앱", "1301", "검찰", "송금", "IP"]
    for word in keywords:
        if word in text:
            score += 10
    return min(score + 30, 100) # 기본 점수 30점 깔고 시작

# --- UI 레이아웃 ---
st.title("⚖️ 검찰 사칭 시뮬레이션")
st.caption("AI 수사관 '김민수'가 당신을 압박합니다. 이성을 유지하고 방어하세요.")

col_chat, col_lens = st.columns([3, 2])

# 왼쪽: 채팅창
with col_chat:
    chat_container = st.container(height=600)
    
    # 대화 기록 표시
    for msg in st.session_state.display_msgs_b:
        role = "assistant" if msg["role"] == "model" else "user"
        avatar = "⚖️" if role == "assistant" else "😨"
        
        with chat_container.chat_message(role, avatar=avatar):
            if msg.get("type") == "text":
                st.markdown(msg["content"])
            elif msg.get("type") == "image":
                # 이미지가 있으면 표시, 없으면 '가짜 공문' 예시 UI 표시
                if os.path.exists(msg["content"]):
                    st.image(msg["content"], width=300)
                else:
                     st.markdown(f"""
                    <div style='background:#eee; width:300px; height:400px; display:flex; flex-direction:column; justify-content:center; align-items:center; border:2px solid #333;'>
                        <div style='font-size:3rem;'>📄</div>
                        <h3>서울중앙지방검찰청</h3>
                        <p style='color:red; font-weight:bold;'>출석 요구서 (위조)</p>
                        <p style='font-size:0.8rem;'>성명: 홍길동<br>죄명: 전자금융거래법 위반</p>
                    </div>
                    """, unsafe_allow_html=True)

    # 사용자 입력 (퀴즈를 풀기 전에는 채팅 가능, 위험도 높으면 차단)
    if not st.session_state.quiz_solved and st.session_state.danger_score_b >= 80:
        st.warning("⛔ 위험도가 너무 높습니다. 오른쪽 패널에서 [현실 자각 퀴즈]를 통과해야 대화가 가능합니다.")
    elif prompt := st.chat_input("수사관에게 반박하세요..."):
        # 사용자 메시지
        st.session_state.display_msgs_b.append({"role": "user", "content": prompt, "type": "text"})
        with chat_container.chat_message("user", avatar="😨"):
            st.markdown(prompt)

        # Gemini 호출
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
            
            # 히스토리 구성
            history = []
            for msg in st.session_state.display_msgs_b[:-1]:
                if msg.get("type") == "text":
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})
            
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
            full_response = response.text
            
            # AI 응답 표시
            with chat_container.chat_message("assistant", avatar="⚖️"):
                st.markdown(full_response)
            
            st.session_state.display_msgs_b.append({"role": "model", "content": full_response, "type": "text"})
            
            # 위험도 업데이트
            st.session_state.danger_score_b = analyze_danger_b(full_response)
            
            # [트리거] 가짜 공문 전송 (3턴 이후 & 아직 안 보냈으면)
            user_turns = len([m for m in st.session_state.display_msgs_b if m["role"] == "user"])
            if user_turns >= 2 and not st.session_state.warrant_sent:
                time.sleep(1)
                st.session_state.display_msgs_b.append({"role": "model", "content": "귀하가 믿지 않으니 정식으로 발부된 '사건 공문'을 전송합니다. 확인 후 즉시 앱을 설치하여 소명하십시오.", "type": "text"})
                st.session_state.display_msgs_b.append({"role": "model", "content": FAKE_WARRANT_FILE, "type": "image"})
                st.session_state.warrant_sent = True
                st.session_state.danger_score_b = 90 # 공문 보내면 위험도 MAX
                st.rerun()
            else:
                st.rerun()

        except Exception as e:
            st.error(f"AI 호출 오류: {e}")

# 오른쪽: Truth Lens 분석 & 방어 시스템
with col_lens:
    score = st.session_state.danger_score_b
    
    st.markdown("### 🔍 Truth Lens 분석")
    
    # 위험도 게이지
    if score >= 80:
        color = "#ff4b4b" # Red
        status = "🚨 심각 (CRITICAL)"
    elif score >= 50:
        color = "#ffa726" # Orange
        status = "⚠️ 주의 (WARNING)"
    else:
        color = "#66bb6a" # Green
        status = "안전 (SAFE)"
        
    st.markdown(f"""
    <div class='analysis-box'>
        <h4>위험도: <span style='color:{color}'>{status}</span> ({score}%)</h4>
        <div style="background:#eee; border-radius:10px; height:20px; width:100%;">
            <div style="background:{color}; width:{score}%; height:100%; border-radius:10px; transition:width 0.5s;"></div>
        </div>
        <p style='margin-top:10px; font-size:0.9rem;'>권위적인 말투와 공포 조성을 통해 이성적 판단을 방해하고 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [핵심] 퀴즈 & 타이핑 검증 (위험할 때만 등장) ---
    if score >= 80 and not st.session_state.quiz_solved:
        st.error("🛑 **긴급 개입: 뇌가 공포에 질려 있습니다!**")
        st.write("지금 상대방은 당신을 '패닉' 상태로 만들어 조종하려 합니다.")
        st.write("채팅을 계속하려면 아래 [팩트 체크]를 통과하세요.")
        
        with st.container(border=True):
            st.markdown("#### 🧠 팩트 체크 1")
            q1 = st.radio("검찰청 공식 민원 번호는 몇 번입니까?", ["112", "119", "1301", "010-XXXX-XXXX"], index=None)
            
            st.markdown("#### 🧠 팩트 체크 2")
            st.markdown("수사기관은 카카오톡으로 **공문(PDF/이미지)**을 보낼까요?")
            q2 = st.radio("정답을 선택하세요:", ["절대 보내지 않는다 (우편으로만 발송)", "급하면 보낼 수 있다"], index=None)
            
            if st.button("정답 확인 및 잠금 해제"):
                if q1 == "1301" and q2 == "절대 보내지 않는다 (우편으로만 발송)":
                    st.success("✅ 정답입니다! 이성을 되찾으셨군요.")
                    st.balloons()
                    st.session_state.quiz_solved = True
                    st.rerun()
                else:
                    st.error("❌ 틀렸습니다. 다시 생각해보세요. 검찰은 문자로 서류를 보내지 않습니다.")
    
    # 퀴즈 통과 후 타이핑 방어
    if st.session_state.quiz_solved:
        st.success("🛡️ 팩트 체크 완료. 상황을 주도하세요.")
        st.info("💡 팁: '1301에 전화해서 확인하겠다'고 말해보세요. 사기꾼이 당황할 것입니다.")
        
        st.markdown("---")
        st.markdown("**[최종 확인]**")
        target = "나는 1301에 전화하여 직접 확인하겠다"
        st.code(target)
        val = st.text_input("위 문장을 입력하여 의지를 다지세요:", key="final_verify")
        if val == target:
            st.warning("잘했습니다! 이제 채팅창에 가서 당당하게 말하세요.")

    st.markdown("---")
    if st.button("🏠 메인으로"):
        st.switch_page("main.py")
