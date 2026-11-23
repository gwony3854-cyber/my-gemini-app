import streamlit as st
import requests

st.set_page_config(page_title="𝐍𝐘𝐗", page_icon="🌙", layout="centered")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] {font-family: 'Noto Sans KR', sans-serif; background-color: #0f1219; color: #f1f5f9;}
    .stApp {background-color: #0f1219;}
    [data-testid="stSidebar"], header, footer, #MainMenu {display: none !important;}
    .block-container {max-width: 740px; padding-top: 1.5rem; padding-bottom: 6rem;}

    /* 상단 NYX 오리지널 헤더 */
    .nyx-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e2536; padding-bottom: 12px; margin-bottom: 20px;}
    .nyx-brand {font-size: 1.3rem; font-weight: 700; color: #f8fafc; letter-spacing: 1px;}
    .nyx-tag {font-size: 0.72rem; background: #1e293b; color: #38bdf8; border: 1px solid #334155; padding: 2px 9px; border-radius: 999px; margin-left: 8px;}

    /* 중앙 히어로 영역 */
    .nyx-welcome {text-align: center; margin-top: 9vh; margin-bottom: 2.2rem;}
    .nyx-moon {font-size: 2.4rem; margin-bottom: 8px;}
    .nyx-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem;
        font-weight: 700;
    }
    .nyx-desc {color: #94a3b8; font-size: 1.05rem; margin-top: 8px;}

    /* 대화 말풍선 */
    .u-wrap {display: flex; justify-content: flex-end; margin: 16px 0;}
    .u-msg {
        background: linear-gradient(135deg, #2563eb, #4f46e5);
        color: #ffffff;
        padding: 11px 17px;
        border-radius: 18px 18px 4px 18px;
        max-width: 76%;
        font-size: 0.96rem;
        line-height: 1.5;
        word-break: break-word;
    }
    .a-head {display: flex; align-items: center; gap: 8px; color: #38bdf8; font-weight: 600; font-size: 0.9rem; margin-top: 18px; margin-bottom: 6px;}

    /* 버튼 & 하단 입력 바 */
    div.stButton > button {
        background-color: #161b26 !important;
        color: #cbd5e1 !important;
        border: 1px solid #263045 !important;
        border-radius: 14px !important;
        padding: 10px 14px !important;
        font-size: 0.86rem !important;
    }
    div.stButton > button:hover {border-color: #38bdf8 !important; color: #ffffff !important;}
    [data-testid="stChatInput"] {background-color: #0f1219 !important;}
    [data-testid="stChatInput"] > div {background-color: #161b26 !important; border: 1px solid #2a354d !important; border-radius: 24px !important;}
    [data-testid="stChatInput"] textarea {color: #f1f5f9 !important;}
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_nyx(history):
    host = "generativelanguage" + "." + "googleapis" + "." + "com"
    for model in ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3-flash-preview"]:
        url = "https://" + host + "/v1beta/models/" + model + ":generateContent"
        payload = {
            "systemInstruction": {"parts": [{"text": "너의 이름은 𝐍𝐘𝐗(NYX)다. 사용자의 질문과 지시에 명료하고 정확하며 친절하게 한국어로 답변하는 AI 어시스턴트다."}]},
            "contents": [
                {"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
                for m in history[-12:]
            ]
        }
        try:
            res = requests.post(url, params={"key": API_KEY}, json=payload, timeout=25).json()
            cands = res.get("candidates")
            if isinstance(cands, list) and len(cands) > 0:
                parts = next(iter(cands)).get("content", {}).get("parts", [])
                txt = "".join(p.get("text", "") for p in parts).strip()
                if txt:
                    return txt
        except Exception:
            continue
    return "잠시 연결이 원활하지 않습니다. 다시 질문해 주세요."

if "messages" not in st.session_state:
    st.session_state.messages = []

c_left, c_right = st.columns([4, 1])
with c_left:
    st.markdown('<div class="nyx-header"><div><span class="nyx-brand">🌙 𝐍𝐘𝐗</span><span class="nyx-tag">AI</span></div></div>', unsafe_allow_html=True)
with c_right:
    if st.button("초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

picked = None
if not st.session_state.messages:
    st.markdown("""
    <div class="nyx-welcome">
        <div class="nyx-moon">🌙</div>
        <div class="nyx-title">𝐍𝐘𝐗와 대화 시작하기</div>
        <div class="nyx-desc">아이디어 기획부터 코딩, 일상 질문까지 무엇이든 물어보세요.</div>
    </div>
    """, unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        if st.button("✨ 새로운 아이디어 추천해줘", use_container_width=True):
            picked = "기발하고 실용적인 프로젝트 아이디어 3가지를 추천해줘"
    with b2:
        if st.button("💻 파이썬 코드 도움받기", use_container_width=True):
            picked = "초보자도 이해하기 쉬운 파이썬 자동화 예제 코드를 작성해줘"

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="u-wrap"><div class="u-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="a-head">🌙 𝐍𝐘𝐗</div>', unsafe_allow_html=True)
        st.markdown(msg["content"])

prompt = st.chat_input("𝐍𝐘𝐗에게 메시지 보내기...") or picked
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="u-wrap"><div class="u-msg">{prompt}</div></div>', unsafe_allow_html=True)
    with st.spinner("🌙 𝐍𝐘𝐗가 답변을 작성하고 있습니다..."):
        reply = ask_nyx(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
