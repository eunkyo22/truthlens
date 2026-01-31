import streamlit as st

st.set_page_config(
    page_title="Truth Lens - 사기 방어 시뮬레이터",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 밝고 깔끔한 커스텀 CSS
st.markdown("""
<style>
    /* 전체 배경 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* 메인 컨테이너 */
    .main > div {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    /* 제목 */
    h1 {
        color: #667eea !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    
    /* 부제목 */
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* 시나리오 카드 */
    .scenario-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .scenario-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
    }
    
    /* 버튼 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* 기능 박스 */
    .feature-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        text-align: center;
    }
    
    /* 통계 카드 */
    .stat-card {
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("<h1>🔍 Truth Lens</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI 기반 실시간 사기 방어 시뮬레이터</p>", unsafe_allow_html=True)

# 히어로 섹션
st.markdown("")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); border-radius: 15px; margin-bottom: 2rem;'>
        <h3 style='color: #333; margin-bottom: 1rem;'>감정을 마비시키는 순간, 이성을 깨우는 기술</h3>
        <p style='color: #555; font-size: 1.1rem;'>
            사기범의 심리 조작 기법을 실시간으로 감지하고<br>
            스스로 현실을 자각하도록 돕는 AI 넛지 시스템
        </p>
    </div>
    """, unsafe_allow_html=True)

# 핵심 기능
st.markdown("### ✨ 핵심 기능")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='feature-box'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🚨</div>
        <h4>실시간 탐지</h4>
        <p style='color: #666;'>사기 패턴 자동 인식</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-box'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🧠</div>
        <h4>인지 개입</h4>
        <p style='color: #666;'>이성적 사고 유도</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-box'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>✍️</div>
        <h4>타이핑 검증</h4>
        <p style='color: #666;'>현실 자각 문장 입력</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='feature-box'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🛡️</div>
        <h4>다단계 방어</h4>
        <p style='color: #666;'>여러 차례 경고</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("---")

# 시나리오 선택
st.markdown("### 🎮 체험해보기")
st.markdown("<p style='text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 2rem;'>실제 사기 상황을 시뮬레이션으로 체험하고, Truth Lens가 어떻게 당신을 보호하는지 확인하세요.</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
        <div class='scenario-card'>
            <div style='text-align: center; font-size: 4rem; margin-bottom: 1rem;'>💔</div>
            <h3 style='text-align: center; color: #667eea;'>로맨스 스캠</h3>
            <p style='text-align: center; color: #555; margin-bottom: 1rem;'>
                친밀감 형성 후 투자 유도<br><br>
                • 인스타그램/SNS DM<br>
                • 감정적 유대감 형성<br>
                • 급한 송금 요청
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎭 로맨스 스캠 시작하기", use_container_width=True, key="btn_romance"):
            st.switch_page("pages/romance_scam.py")
    
    with col_b:
        st.markdown("""
        <div class='scenario-card'>
            <div style='text-align: center; font-size: 4rem; margin-bottom: 1rem;'>⚖️</div>
            <h3 style='text-align: center; color: #667eea;'>검찰/경찰 사칭</h3>
            <p style='text-align: center; color: #555; margin-bottom: 1rem;'>
                공공기관 사칭<br><br>
                • 문자/카카오톡<br>
                • 긴급성/공포감 조성<br>
                • 악성 앱 설치 강요
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚔 검찰 사칭 시작하기", use_container_width=True, key="btn_impersonate"):
            st.switch_page("pages/impersonation_scam.py")

st.markdown("")
st.markdown("---")

# 통계 섹션
st.markdown("### 📊 왜 Truth Lens가 필요한가?")
st.markdown("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='stat-card' style='background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);'>
        <p style='font-size: 0.9rem; margin-bottom: 0.5rem;'>2023년 보이스피싱 피해액</p>
        <h2 style='font-size: 2.5rem; margin: 0;'>8,577억원</h2>
        <p style='font-size: 0.9rem; margin-top: 0.5rem;'>⬆️ +12.3% (전년 대비)</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='stat-card' style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);'>
        <p style='font-size: 0.9rem; margin-bottom: 0.5rem;'>로맨스 스캠 피해 건수</p>
        <h2 style='font-size: 2.5rem; margin: 0;'>1,247건</h2>
        <p style='font-size: 0.9rem; margin-top: 0.5rem;'>⬆️ +34% (증가 추세)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='stat-card' style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);'>
        <p style='font-size: 0.9rem; margin-bottom: 0.5rem;'>평균 피해 금액</p>
        <h2 style='font-size: 2.5rem; margin: 0;'>638만원</h2>
        <p style='font-size: 0.9rem; margin-top: 0.5rem;'>💰 1인당</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("---")

# 작동 원리
st.markdown("### 🔬 Truth Lens는 어떻게 작동하나요?")
st.markdown("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: #fff; border: 2px solid #667eea; border-radius: 15px; padding: 1.5rem;'>
        <div style='text-align: center; font-size: 3rem; margin-bottom: 1rem;'>🔍</div>
        <h4 style='color: #667eea; text-align: center;'>1단계: 패턴 인식</h4>
        <p style='color: #666; text-align: center;'>
            • AI가 실시간 분석<br>
            • 사기 패턴 감지<br>
            • 위험도 평가
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #fff; border: 2px solid #667eea; border-radius: 15px; padding: 1.5rem;'>
        <div style='text-align: center; font-size: 3rem; margin-bottom: 1rem;'>💡</div>
        <h4 style='color: #667eea; text-align: center;'>2단계: 현실 자각</h4>
        <p style='color: #666; text-align: center;'>
            • 타이핑 검증<br>
            • 감정 판단 중지<br>
            • 상황 재인식
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: #fff; border: 2px solid #667eea; border-radius: 15px; padding: 1.5rem;'>
        <div style='text-align: center; font-size: 3rem; margin-bottom: 1rem;'>🛡️</div>
        <h4 style='color: #667eea; text-align: center;'>3단계: 최종 경고</h4>
        <p style='color: #666; text-align: center;'>
            • 마지막 확인<br>
            • 명확한 선택지<br>
            • 취소/진행
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("---")

# 푸터
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px; margin-top: 2rem;'>
    <p style='color: #666; font-size: 1rem; margin-bottom: 0.5rem;'>
        ⚠️ 본 서비스는 교육 목적의 시뮬레이션입니다.
    </p>
    <p style='color: #666; font-size: 1rem; margin-bottom: 1rem;'>
        실제 사기 피해 시 <strong>112</strong> 또는 금융감독원 <strong>1332</strong>에 신고하세요.
    </p>
    <p style='color: #999; font-size: 0.9rem;'>
        © 2026 Truth Lens Project. 모두가 안전한 디지털 환경을 만듭니다.
    </p>
</div>
""", unsafe_allow_html=True)
