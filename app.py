import base64
import streamlit as st
import requests

st.set_page_config(page_title="𝐍𝐘𝐗", page_icon="🌙", layout="centered")

st.markdown("""
<style>
    html, body, [class*="css"] {background-color: #090b10 !important; color: #f1f5f9 !important;}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stBottom"], [data-testid="stBottom"] > div {background-color: #090b10 !important;}
    [data-testid="stSidebar"], header, footer, #MainMenu {display: none !important;}
    .block-container {max-width: 740px; padding-top: 1.2rem; padding-bottom: 7.5rem;}
    .nyx-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a2030; padding-bottom: 10px; margin-bottom: 14px;}
    .nyx-brand {font-size: 1.3rem; font-weight: 700; color: #f8fafc; letter-spacing: 1px;}
    .nyx-tag {font-size: 0.72rem; background: #141926; color: #38bdf8; border: 1px solid #263147; padding: 2px 9px; border-radius: 999px; margin-left: 8px;}
    .nyx-welcome {text-align: center; margin-top: 8vh; margin-bottom: 2rem;}
    .nyx-moon {font-size: 2.4rem; margin-bottom: 8px;}
    .nyx-title {background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.2rem; font-weight: 700;}
    .nyx-desc {color: #94a3b8; font-size: 0.98rem; margin-top: 8px;}
    .settings-box {background-color: #111520; border: 1px solid #263147; border-radius: 16px; padding: 16px; margin-bottom: 16px;}
    .warn-pill {background-color: #161b28; border: 1px solid #2c3752; color: #cbd5e1; padding: 10px 14px; border-radius: 12px; font-size: 0.85rem; margin: 8px 0;}
    .u-wrap {display: flex; justify-content: flex-end; margin: 14px 0;}
    .u-msg {background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; padding: 11px 17px; border-radius: 18px 18px 4px 18px; max-width: 76%; font-size: 0.96rem; line-height: 1.5; word-break: break-word;}
    .a-head {display: flex; align-items: center; gap: 8px; color: #38bdf8; font-weight: 600; font-size: 0.9rem; margin-top: 16px; margin-bottom: 6px;}
    div.stButton > button, [data-testid="stPopover"] > button {background-color: #141926 !important; color: #e2e8f0 !important; border: 1px solid #263147 !important; border-radius: 999px !important; padding: 8px 14px !important; font-size: 0.9rem !important;}
    [data-testid="stPopoverBody"] {background-color: #121621 !important; border: 1px solid #2a354d !important; border-radius: 16px !important;}
    [data-testid="stChatInput"], [data-testid="stChatInput"] > div, [data-testid="stChatInput"] form {background-color: #121621 !important; border-color: #252e42 !important; border-radius: 26px !important;}
    [data-testid="stChatInput"] textarea {background-color: transparent !important; color: #f8fafc !important;}
    [data-testid="stChatInputSubmitButton"] {background-color: #2563eb !important; color: #ffffff !important; border-radius: 50% !important;}
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def ask_nyx(history, media_part=None):
    host = "generativelanguage" + "." + "googleapis" + "." + "com"
    contents = list()
    recent = history[-12:]
    for idx, m in enumerate(recent):
        role = "user" if m.get("role") == "user" else "model"
        parts = list()
        parts.append({"text": m.get("content", "")})
        if idx == len(recent) - 1 and media_part is not None:
            parts.append(media_part)
        contents.append({"role": role, "parts": parts})
    for model in ("gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3-flash-preview"):
        url = "https://" + host + "/v1beta/models/" + model + ":generateContent"
        try:
            res = requests.post(url, params={"key": API_KEY}, json={"systemInstruction": {"parts": [{"text": "너의 이름은 𝐍𝐘𝐗(NYX)다. 텍스트, 이미지, 파일, 음성을 정확히 이해하고 한국어로 친절하게 답변하는 AI 어시스턴트다."}]}, "contents": contents}, timeout=30).json()
            cands = res.get("candidates")
            if isinstance(cands, list) and len(cands) > 0:
                p_list = next(iter(cands)).get("content", {}).get("parts", list())
                txt = "".join(p.get("text", "") for p in p_list).strip()
                if txt:
                    return txt
        except Exception:
            continue
    return "잠시 연결이 원활하지 않습니다. 다시 시도해 주세요."

for k, v in (("messages", list()), ("cam_on", False), ("mic_on", False), ("show_settings", False), ("last_media_id", None)):
    if k not in st.session_state:
        st.session_state[k] = v

h1, h2, h3 = st.columns((3, 1, 1))
with h1:
    st.markdown('<div class="nyx-header"><div><span class="nyx-brand">🌙 𝐍𝐘𝐗</span><span class="nyx-tag">AI</span></div></div>', unsafe_allow_html=True)
with h2:
    if st.button("⚙️ 설정", use_container_width=True):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()
with h3:
    if st.button("초기화", use_container_width=True):
        st.session_state.messages = list()
        st.session_state.last_media_id = None
        st.rerun()

if st.session_state.show_settings:
    st.markdown('<div class="settings-box"><b>⚙️ 장치 권한 설정</b><br><span style="color:#94a3b8;font-size:0.83rem;">스위치를 켜야 하단의 <b>[＋]</b> 이미지·카메라 메뉴와 <b>[🎙️]</b> 음성 인식을 사용할 수 있습니다.</span></div>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.session_state.cam_on = st.toggle("📷 사진 / 카메라 허용", value=st.session_state.cam_on)
    with s2:
        st.session_state.mic_on = st.toggle("🎙️ 음성 인식 허용", value=st.session_state.mic_on)

picked = None
if not st.session_state.messages:
    st.markdown('<div class="nyx-welcome"><div class="nyx-moon">🌙</div><div class="nyx-title">𝐍𝐘𝐗와 대화 시작하기</div><div class="nyx-desc">무엇이든 물어보거나 하단 ＋, 🎙️ 버튼으로 질문해 보세요.</div></div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        if st.button("✨ 새로운 아이디어 추천해줘", use_container_width=True):
            picked = "기발하고 실용적인 프로젝트 아이디어 3가지를 추천해줘"
    with b2:
        if st.button("💻 파이썬 코드 도움받기", use_container_width=True):
            picked = "초보자도 이해하기 쉬운 파이썬 자동화 예제 코드를 작성해줘"

for msg in st.session_state.messages:
    if msg.get("role") == "user":
        st.markdown(f'<div class="u-wrap"><div class="u-msg">{msg.get("content", "")}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="a-head">🌙 𝐍𝐘𝐗</div>', unsafe_allow_html=True)
        st.markdown(msg.get("content", ""))

img_file, cam_file, doc_file, aud_file = None, None, None, None
t_left, t_mid, t_right = st.columns((1, 4, 1))
with t_left:
    with st.popover("＋", use_container_width=True):
        if not st.session_state.cam_on:
            st.markdown('<div class="warn-pill">🔒 <b>사진/카메라 꺼짐</b><br>상단 <b>[⚙️ 설정]</b>에서 스위치를 켜주세요.</div>', unsafe_allow_html=True)
        else:
            img_file = st.file_uploader("🖼️ 이미지 추가 (앨범)", type=("png", "jpg", "jpeg", "webp"), key="up_img")
            cam_file = st.camera_input("📷 카메라 촬영", key="up_cam")
            doc_file = st.file_uploader("📎 파일 추가", type=("pdf", "txt", "csv", "py", "md"), key="up_doc")
with t_right:
    with st.popover("🎙️", use_container_width=True):
        if not st.session_state.mic_on:
            st.markdown('<div class="warn-pill">🔒 <b>음성 인식 꺼짐</b><br>상단 <b>[⚙️ 설정]</b>에서 스위치를 켜주세요.</div>', unsafe_allow_html=True)
        else:
            aud_file = st.audio_input("🎙️ 말하기 (녹음 후 전송)", key="up_aud")

text_in = st.chat_input("𝐍𝐘𝐗에게 메시지 보내기...")
media_part, media_label = None, None
if img_file is not None:
    mid = f"img_{img_file.name}_{img_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        media_part = {"inline_data": {"mime_type": img_file.type or "image/jpeg", "data": base64.b64encode(img_file.getvalue()).decode("utf-8")}}
        media_label = f"🖼️ [이미지 첨부: {img_file.name}] 이 이미지를 분석해줘."
elif cam_file is not None:
    mid = f"cam_{cam_file.name}_{cam_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        media_part = {"inline_data": {"mime_type": cam_file.type or "image/jpeg", "data": base64.b64encode(cam_file.getvalue()).decode("utf-8")}}
        media_label = "📷 [카메라 촬영] 이 사진의 내용을 알려줘."
elif doc_file is not None:
    mid = f"doc_{doc_file.name}_{doc_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        media_part = {"inline_data": {"mime_type": doc_file.type or "text/plain", "data": base64.b64encode(doc_file.getvalue()).decode("utf-8")}}
        media_label = f"📎 [파일 첨부: {doc_file.name}] 이 파일의 내용을 요약해줘."
elif aud_file is not None:
    mid = f"aud_{aud_file.name}_{aud_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        media_part = {"inline_data": {"mime_type": aud_file.type or "audio/wav", "data": base64.b64encode(aud_file.getvalue()).decode("utf-8")}}
        media_label = "🎙️ [음성 질문] 방금 말한 음성 내용을 인식해서 답변해줘."

prompt = text_in or picked or media_label
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="u-wrap"><div class="u-msg">{prompt}</div></div>', unsafe_allow_html=True)
    with st.spinner("🌙 𝐍𝐘𝐗가 답변하고 있습니다..."):
        reply = ask_nyx(st.session_state.messages, media_part=media_part)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

