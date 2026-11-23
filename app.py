import base64
import streamlit as st
import requests

st.set_page_config(page_title="𝐍𝐘𝐗", page_icon="🌙", layout="centered")

st.markdown("""
<style>
    html, body, [class*="css"] {background-color: #090b10 !important; color: #f1f5f9 !important;}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stBottom"], [data-testid="stBottom"] > div {
        background-color: #090b10 !important;
    }
    [data-testid="stSidebar"], header, footer, #MainMenu {display: none !important;}
    .block-container {max-width: 740px; padding-top: 1.5rem; padding-bottom: 6.5rem;}
    .nyx-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a2030; padding-bottom: 12px; margin-bottom: 16px;}
    .nyx-brand {font-size: 1.3rem; font-weight: 700; color: #f8fafc; letter-spacing: 1px;}
    .nyx-tag {font-size: 0.72rem; background: #141926; color: #38bdf8; border: 1px solid #263147; padding: 2px 9px; border-radius: 999px; margin-left: 8px;}
    .nyx-welcome {text-align: center; margin-top: 7vh; margin-bottom: 2rem;}
    .nyx-moon {font-size: 2.4rem; margin-bottom: 8px;}
    .nyx-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2.3rem; font-weight: 700;
    }
    .nyx-desc {color: #94a3b8; font-size: 1.02rem; margin-top: 8px;}
    .perm-notice {background-color: #121621; border: 1px solid #252e42; color: #94a3b8; padding: 10px 14px; border-radius: 12px; font-size: 0.85rem; text-align: center; margin: 12px 0;}
    .settings-box {background-color: #111520; border: 1px solid #263147; border-radius: 16px; padding: 16px; margin-bottom: 16px;}
    .u-wrap {display: flex; justify-content: flex-end; margin: 16px 0;}
    .u-msg {background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; padding: 11px 17px; border-radius: 18px 18px 4px 18px; max-width: 76%; font-size: 0.96rem; line-height: 1.5; word-break: break-word;}
    .a-head {display: flex; align-items: center; gap: 8px; color: #38bdf8; font-weight: 600; font-size: 0.9rem; margin-top: 18px; margin-bottom: 6px;}
    div.stButton > button {background-color: #121621 !important; color: #cbd5e1 !important; border: 1px solid #222a3d !important; border-radius: 14px !important; padding: 8px 12px !important; font-size: 0.84rem !important;}
    div.stButton > button:hover {border-color: #38bdf8 !important; color: #ffffff !important;}
    [data-testid="stChatInput"], [data-testid="stChatInput"] > div, [data-testid="stChatInput"] form {background-color: #121621 !important; border-color: #252e42 !important; border-radius: 24px !important;}
    [data-testid="stChatInput"] textarea {background-color: transparent !important; color: #f8fafc !important; caret-color: #38bdf8 !important;}
    [data-testid="stChatInput"] textarea::placeholder {color: #64748b !important; opacity: 1 !important;}
    [data-testid="stChatInputSubmitButton"] {background-color: #1e293b !important; color: #38bdf8 !important; border-radius: 50% !important;}
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_nyx(history, media_part=None):
    host = "generativelanguage" + "." + "googleapis" + "." + "com"
    contents = []
    for idx, m in enumerate(history[-12:]):
        role = "user" if m["role"] == "user" else "model"
        parts = [{"text": m["content"]}]
        if idx == len(history[-12:]) - 1 and media_part is not None:
            parts.append(media_part)
        contents.append({"role": role, "parts": parts})
    for model in ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3-flash-preview"]:
        url = "https://" + host + "/v1beta/models/" + model + ":generateContent"
        try:
            res = requests.post(url, params={"key": API_KEY}, json={"systemInstruction": {"parts": [{"text": "너의 이름은 𝐍𝐘𝐗(NYX)다. 텍스트, 이미지, 음성을 정확히 이해하고 한국어로 친절하게 답변하는 AI 어시스턴트다."}]}, "contents": contents}, timeout=30).json()
            cands = res.get("candidates")
            if isinstance(cands, list) and len(cands) > 0:
                txt = "".join(p.get("text", "") for p in next(iter(cands)).get("content", {}).get("parts", [])).strip()
                if txt:
                    return txt
        except Exception:
            continue
    return "잠시 연결이 원활하지 않습니다. 다시 시도해 주세요."

for k, v in [("messages", []), ("cam_on", False), ("mic_on", False), ("show_settings", False), ("last_media_id", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

c1, c2, c3 = st.columns()
with c1:
    st.markdown('<div class="nyx-header"><div><span class="nyx-brand">🌙 𝐍𝐘𝐗</span><span class="nyx-tag">AI</span></div></div>', unsafe_allow_html=True)
with c2:
    if st.button("⚙️ 설정", use_container_width=True):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()
with c3:
    if st.button("초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_media_id = None
        st.rerun()

if st.session_state.show_settings:
    st.markdown('<div class="settings-box"><b>⚙️ 장치 권한 및 기능 설정</b><br><span style="color:#94a3b8;font-size:0.83rem;">사용할 기능을 켜면 아래 입력 영역에 카메라와 마이크가 활성화됩니다.</span></div>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.session_state.cam_on = st.toggle("📷 카메라 기능 켜기", value=st.session_state.cam_on)
    with s2:
        st.session_state.mic_on = st.toggle("🎙️ 음성(마이크) 기능 켜기", value=st.session_state.mic_on)

picked = None
if not st.session_state.messages:
    st.markdown('<div class="nyx-welcome"><div class="nyx-moon">🌙</div><div class="nyx-title">𝐍𝐘𝐗와 대화 시작하기</div><div class="nyx-desc">텍스트는 물론 카메라와 음성으로도 질문할 수 있습니다.</div></div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        if st.button("✨ 새로운 아이디어 추천해줘", use_container_width=True):
            picked = "기발하고 실용적인 프로젝트 아이디어 3가지를 추천해줘"
    with b2:
        if st.button("💻 파이썬 코드 도움받기", use_container_width=True):
            picked = "초보자도 이해하기 쉬운 파이썬 자동화 예제 코드를 작성해줘"

if not st.session_state.cam_on and not st.session_state.mic_on:
    st.markdown('<div class="perm-notice">🔒 <b>카메라 및 음성 기능 비활성화됨</b> — 사용하려면 오른쪽 위 <b>[⚙️ 설정]</b>에서 스위치를 켜주세요.</div>', unsafe_allow_html=True)
elif not st.session_state.cam_on:
    st.markdown('<div class="perm-notice">🔒 <b>카메라 꺼짐</b> — 카메라로 질문하려면 <b>[⚙️ 설정]</b>에서 카메라 기능을 켜주세요.</div>', unsafe_allow_html=True)
elif not st.session_state.mic_on:
    st.markdown('<div class="perm-notice">🔒 <b>음성(마이크) 꺼짐</b> — 목소리로 질문하려면 <b>[⚙️ 설정]</b>에서 음성 기능을 켜주세요.</div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="u-wrap"><div class="u-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="a-head">🌙 𝐍𝐘𝐗</div>', unsafe_allow_html=True)
        st.markdown(msg["content"])

cam_file, aud_file = None, None
if st.session_state.cam_on or st.session_state.mic_on:
    m_cols = st.columns(2 if (st.session_state.cam_on and st.session_state.mic_on) else 1)
    idx = 0
    if st.session_state.cam_on:
        with m_cols[idx]:
            cam_file = st.camera_input("📷 카메라 촬영 후 전송")
        idx += 1
    if st.session_state.mic_on:
        with m_cols[idx]:
            aud_file = st.audio_input("🎙️ 음성 녹음 후 전송")

media_part, auto_media_prompt = None, None
if cam_file is not None:
    mid = f"cam_{cam_file.name}_{cam_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        media_part = {"inline_data": {"mime_type": cam_file.type or "image/jpeg", "data": base64.b64encode(cam_file.getvalue()).decode("utf-8")}}
        auto_media_prompt = "📷 [카메라 사진 전송] 이 사진의 내용을 분석해서 알려줘."
elif aud_file is not None:
    mid = f"aud_{aud_file.name}_{aud_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        media_part = {"inline_data": {"mime_type": aud_file.type or "audio/wav", "data": base64.b64encode(aud_file.getvalue()).decode("utf-8")}}
        auto_media_prompt = "🎙️ [음성 메시지 전송] 방금 말한 음성 내용을 듣고 답변해줘."

prompt = st.chat_input("𝐍𝐘𝐗에게 메시지 보내기...") or picked or auto_media_prompt
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="u-wrap"><div class="u-msg">{prompt}</div></div>', unsafe_allow_html=True)
    with st.spinner("🌙 𝐍𝐘𝐗가 분석하고 있습니다..."):
        reply = ask_nyx(st.session_state.messages, media_part=media_part)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
