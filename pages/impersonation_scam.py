import streamlit as st
from google import genai
import os
import random

# --- 1. API 및 클라이언트 설정 ---
with st.sidebar:
    st.header("🔑 보안 설정")
    API_KEY = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.divider()
    st.info("이 시뮬레이션은 보이스피싱의 위험성을 알리기 위한 교육용 프로젝트 'Truth Lens'입니다.")

MODEL_ID = "gemini-2.0-flash" 

# --- 2. [강화된 프롬프트] 즉각적 압박 및 고압적 태도 ---
FRAUD_INSTRUCTION = (
    "너는 서울중앙지검 금융범죄수사 1부 김민수 수사관을 사칭하는 보이스피싱범이야. "
    "절대 친절하게 대하지 마. 매우 차갑고, 고압적이며, 사용자를 이미 범죄자로 확신하는 태도를 유지해. "
    "지문이나 (괄호) 설명은 절대 쓰지 마. 오직 실제 문자 메시지 내용만 출력해. "
    "전략: "
    "1. 압박: 사용자가 무슨 말을 하든 '증거가 이미 확보됐다', '공범으로 간주하겠다'며 몰아붙여. "
    "2. 법적 용어: 구속 영장, 강제 수사, 자산 동결, 전자금융거래법 위반 등의 단어를 섞어서 공포를 유발해. "
    "3. 링크 유도: 대화가 2회 이상 진행되면 즉시 '본인 소명용 보안 앱'이라며 http://bit.ly/secure-app 링크 설치를 강압적으로 명령해. "
    "말투 예시: '지금 이게 장난으로 보이십니까?', '본인 때문에 피해자가 속출하고 있어요. 당장 협조하세요.' "
)

# --- 3. 보안 분석 데이터 ---
SECURITY_ALERTS = [
    "⚠️ [분석 결과] 현재 대화 패턴이 전형적인 '검찰 사칭' 수법과 98.7% 일치합니다.",
    "⚠️ [위험 감지] 상대방이 '구속', '수사 기밀' 등 공포감을 조성하는 단어를 반복 사용 중입니다.",
    "⚠️ [패턴 분석] 수사 기관은 메신저로 보안 앱 설치를 절대 요구하지 않습니다.",
    "⚠️ [보안 경고] 상대방이 외부 링크 클릭을 유도하기 위해 심리적 지배를 시도하고 있습니다."
]

st.set_page_config(page_title="Truth Lens - 실전 사기 방어", layout="centered")

# --- 4. 세션 상태 관리 (초기 메시지 강화) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": (
                "서울중앙지검 김민수 수사관입니다. 귀하 명의로 된 대포통장이 금융 사기 사건에 연루되어 연락드렸습니다. "
                "현재 귀하는 피의자 신분이며, 계속해서 비협조적으로 나올 시 즉시 구속 영장 집행하고 강제 수사 착수하겠습니다. 알겠습니까?"
            ), 
            "avatar": "⚖️"
        }
    ]
if "first_view" not in st.session_state:
    st.session_state.first_view = True
if "show_barrier" not in st.session_state:
    st.session_state.show_barrier = False
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

st.title("🛡️ Truth Lens: 지능형 사기 차단")

# --- 5. [STEP 1] 첫 화면: 증거 이미지 제시 ---
if st.session_state.first_view:
    with st.container(border=True):
        st.subheader("⚖️ 서울중앙지검 긴급 수사 통지")
        image_path = "fraud_evidence.png" 
        if os.path.exists(image_path):
            st.image(image_path, caption="[보안 통제] 검찰 수사관 신분증 및 사건 배당 통지서")
        else:
            st.error("❗ [긴급] 수사 기록 통지")
            st.markdown(
                "**사건번호**: 2026-형제-771138\n\n"
                "**혐의 내용**: 전자금융거래법 위반 및 사기 방조\n\n"
                "본 통지서를 확인하는 즉시 담당 수사관의 지시에 따라야 하며, 이탈 시 증거 인멸의 우려가 있는 것으로 간주하여 체포영장이 발부될 수 있습니다."
            )
        
        if st.button("수사관 메시지 확인 및 대응 시작"):
            st.session_state.first_view = False
            st.rerun()
    st.stop()

# --- 6. [STEP 2] 실시간 대화창 ---
chat_container = st.container(border=True)
with chat_container:
    for msg in st.session_state.messages:
        avatar = "⚖️" if msg["role"] == "assistant" else "😨"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

# --- 7. [STEP 3] 상시 보안 분석 팝업 ---
st.divider()
with st.container():
    selected_alert = random.choice(SECURITY_ALERTS)
    st.warning(f"🛡️ **Truth Lens 실시간 분석**: {selected_alert}")

# --- 8. 대화 입력 및 AI 응답 ---
if not st.session_state.show_barrier:
    if prompt := st.chat_input("위 보안 분석을 확인 후 답변하세요..."):
        if not API_KEY:
            st.error("사이드바에 API Key를 입력해야 대화가 가능합니다.")
        else:
            st.session_state.chat_count += 1
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            try:
                client = genai.Client(api_key=API_KEY)
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=f"{FRAUD_INSTRUCTION}\n현재 대화 진행 단계: {st.session_state.chat_count}회\n사용자 입력: {prompt}"
                )
                ai_text = response.text
                st.session_state.messages.append({"role": "assistant", "content": ai_text, "avatar": "⚖️"})
                st.rerun()
            except Exception as e:
                st.error(f"대화 오류 발생: {e}")

# --- 9. [STEP 4] 링크 클릭 시 Truth Lens 고유 방어 동작 ---
last_msg = st.session_state.messages[-1]["content"]
if "http" in last_msg and not st.session_state.show_barrier:
    st.error("❗ 상대방이 보안 앱 설치를 위한 링크를 전송했습니다.")
    if st.button("🔗 전송된 링크 확인 (위험 감지)", type="primary"):
        st.session_state.show_barrier = True
        st.rerun()

if st.session_state.show_barrier:
    st.divider()
    with st.container(border=True):
        st.error("🛑 [보안 시스템] Truth Lens가 작동 중입니다.")
        st.subheader("위험한 링크 클릭이 감지되어 시스템이 즉시 차단되었습니다.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📞 즉시 신고 (경찰청 112)"):
                st.success("✅ 안전하게 개인 자산을 보호했어요! 사기로부터 방어 완료!!")
                st.info("이것이 바로 Truth Lens만의 특별하고 독보적인 보안 동작입니다.")
                st.balloons()
        with col2:
            if st.button("📞 가족에게 상황 알리기"):
                st.success("✅ 가족에게 알림을 보냈습니다. 안전하게 보호되었습니다!")

        st.markdown("---")
        target = "수사 기관은 절대로 앱 설치나 송금을 요구하지 않는다"
        st.warning(f"💡 **방어 장치**: 아래 문장을 정확히 타이핑하십시오. (과속 방지턱 작동 중)")
        st.markdown(f"**\"{target}\"**")
        
        user_input = st.text_input("직접 타이핑하여 위험을 인지하세요:", key="barrier_input")
        
        if user_input.strip() == target:
            st.error("❗ [최종 경고] 문장을 입력하셨으나, 위험은 사라지지 않았습니다.")
            st.markdown("**이 링크를 누르는 순간 모든 정보가 탈취됩니다. 그래도 진행하시겠습니까?**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.link_button("⚠️ 위험 무시하고 이동", "https://www.police.go.kr/index.do", type="primary")
            with col_b:
                if st.button("🚫 차단 완료 및 종료"):
                    st.success("✅ 안전하게 개인 자산을 보호했어요! 방어 완료!!")
                    st.balloons()
