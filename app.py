import base64
import streamlit as st
import streamlit.components.v1 as components
import requests

st.set_page_config(page_title="𝐍𝐘𝐗", page_icon="🌙", layout="centered")

st.markdown("""
<style>
    html, body, [class*="css"] {background-color: #090b10 !important; color: #f1f5f9 !important;}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stBottom"], [data-testid="stBottom"] > div {background-color: #090b10 !important;}
    [data-testid="stSidebar"], header, footer, #MainMenu {display: none !important;}
    .block-container {max-width: 740px; padding-top: 1rem; padding-bottom: 6.5rem;}
    .nyx-welcome {text-align: center; margin-top: 8vh; margin-bottom: 1.8rem;}
    .nyx-moon {font-size: 2.3rem; margin-bottom: 6px;}
    .nyx-title {background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.1rem; font-weight: 700;}
    .nyx-desc {color: #94a3b8; font-size: 0.95rem; margin-top: 6px;}
    .drawer-box {background-color: #111520; border: 1px solid #263147; border-radius: 16px; padding: 14px; margin-bottom: 16px;}
    .u-wrap {display: flex; justify-content: flex-end; margin: 14px 0; scroll-margin-top: 24px;}
    .u-msg {background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; padding: 11px 17px; border-radius: 18px 18px 4px 18px; max-width: 76%; font-size: 0.96rem; line-height: 1.5; word-break: break-word;}
    .a-head {display: flex; align-items: center; gap: 8px; color: #38bdf8; font-weight: 600; font-size: 0.9rem; margin-top: 16px; margin-bottom: 6px;}
    div.stButton > button {background-color: #141926 !important; color: #e2e8f0 !important; border: 1px solid #263147 !important; border-radius: 12px !important; padding: 8px 12px !important; font-size: 0.9rem !important;}
    div.stButton > button:hover {border-color: #38bdf8 !important; color: #ffffff !important;}

    /* 채팅 입력창 전체를 하나의 둥근 알약 바 형태로 통합 */
    [data-testid="stBottom"] > div {max-width: 740px; margin: 0 auto; position: relative;}
    [data-testid="stChatInput"], [data-testid="stChatInput"] > div, [data-testid="stChatInput"] form {
        background-color: #121621 !important; border-color: #252e42 !important; border-radius: 28px !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: transparent !important; color: #f8fafc !important; caret-color: #38bdf8 !important;
        padding-left: 46px !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {color: #64748b !important; opacity: 1 !important;}
    [data-testid="stChatInputSubmitButton"] {background-color: #2563eb !important; color: #ffffff !important; border-radius: 50% !important;}

    /* ＋ 버튼을 채팅 입력창 안쪽 왼쪽에 동그랗게 배치 */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 22px !important;
        left: max(22px, calc(50% - 348px)) !important;
        z-index: 1000 !important;
        width: 34px !important;
    }
    div[data-testid="stPopover"] > button {
        width: 34px !important; height: 34px !important; min-height: 34px !important;
        padding: 0 !important; border-radius: 50% !important;
        background-color: #1e2638 !important; color: #f8fafc !important;
        border: 1px solid #334155 !important; font-size: 19px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }
    div[data-testid="stPopover"] > button svg {display: none !important;}
    [data-testid="stPopoverBody"] {background-color: #121621 !important; border: 1px solid #2a354d !important; border-radius: 16px !important; width: 200px !important;}
    iframe {border: none !important;}
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

for k, v in (("messages", list()), ("drawer_open", False), ("jump_id", ""), ("tool_mode", ""), ("last_media_id", "")):
    if k not in st.session_state:
        st.session_state[k] = v

top_l, top_r = st.columns((1, 5))
with top_l:
    if st.button("☰", use_container_width=True):
        st.session_state.drawer_open = not st.session_state.drawer_open
        st.rerun()
with top_r:
    st.markdown('<div style="padding-top:6px;"><span style="font-size:1.3rem;font-weight:700;color:#f8fafc;">🌙 𝐍𝐘𝐗</span><span style="font-size:0.72rem;background:#141926;color:#38bdf8;border:1px solid #263147;padding:2px 9px;border-radius:999px;margin-left:8px;">AI</span></div>', unsafe_allow_html=True)

if st.session_state.drawer_open:
    st.markdown('<div class="drawer-box"><b>🕒 내가 말한 대화 기록 (클릭 시 이동)</b></div>', unsafe_allow_html=True)
    if st.button("＋ 새 채팅 시작하기", use_container_width=True):
        st.session_state.messages = list()
        st.session_state.drawer_open = False
        st.session_state.tool_mode = ""
        st.rerun()
    user_entries = [(i, m.get("content", "")) for i, m in enumerate(st.session_state.messages) if m.get("role") == "user"]
    if not user_entries:
        st.caption("아직 대화 기록이 없습니다.")
    else:
        for idx, text in reversed(user_entries):
            label = text if len(text) <= 32 else text[:32] + "..."
            if st.button(f"💬 {label}", key=f"hist_{idx}", use_container_width=True):
                st.session_state.jump_id = f"msg_{idx}"
                st.session_state.drawer_open = False
                st.rerun()

if not st.session_state.messages:
    st.markdown('<div class="nyx-welcome"><div class="nyx-moon">🌙</div><div class="nyx-title">𝐍𝐘𝐗와 대화 시작하기</div><div class="nyx-desc">입력창 안의 ＋ 버튼을 누르거나 질문을 입력해 보세요.</div></div>', unsafe_allow_html=True)

for idx, msg in enumerate(st.session_state.messages):
    if msg.get("role") == "user":
        st.markdown(f'<div id="msg_{idx}" class="u-wrap"><div class="u-msg">{msg.get("content", "")}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="a-head">🌙 𝐍𝐘𝐗</div>', unsafe_allow_html=True)
        st.markdown(msg.get("content", ""))

if st.session_state.jump_id:
    jid = st.session_state.jump_id
    st.session_state.jump_id = ""
    components.html(f"<script>const el=window.parent.document.getElementById('{jid}');if(el)el.scrollIntoView({{behavior:'smooth',block:'center'}});</script>", height=0)

img_file, cam_file, doc_file, aud_file = None, None, None, None
if st.session_state.tool_mode == "img":
    img_file = st.file_uploader("🖼️ 앨범에서 이미지 선택", type=("png", "jpg", "jpeg", "webp"))
elif st.session_state.tool_mode == "cam":
    st.caption("🔒 카메라 권한이 꺼져 있다면 브라우저 팝업에서 [허용]을 눌러주세요.")
    cam_file = st.camera_input("📷 사진 촬영")
elif st.session_state.tool_mode == "doc":
    doc_file = st.file_uploader("📎 문서/코드 파일 선택", type=("pdf", "txt", "csv", "py", "md"))
elif st.session_state.tool_mode == "mic":
    st.caption("🔒 마이크 권한이 꺼져 있다면 브라우저 팝업에서 [허용]을 눌러주세요.")
    aud_file = st.audio_input("🎙️ 음성으로 질문하기")

with st.popover("＋"):
    if st.button("🖼️ 이미지 추가", use_container_width=True):
        st.session_state.tool_mode = "img"
        st.rerun()
    if st.button("📷 카메라 촬영", use_container_width=True):
        st.session_state.tool_mode = "cam"
        st.rerun()
    if st.button("📎 파일 추가", use_container_width=True):
        st.session_state.tool_mode = "doc"
        st.rerun()
    if st.button("🎙️ 음성 인식", use_container_width=True):
        st.session_state.tool_mode = "mic"
        st.rerun()

text_in = st.chat_input("𝐍𝐘𝐗에게 메시지 보내기...")

media_part, media_label = None, None
if img_file is not None:
    mid = f"img_{img_file.name}_{img_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        st.session_state.tool_mode = ""
        media_part = {"inline_data": {"mime_type": img_file.type or "image/jpeg", "data": base64.b64encode(img_file.getvalue()).decode("utf-8")}}
        media_label = f"🖼️ [이미지: {img_file.name}] 이 이미지를 분석해줘."
elif cam_file is not None:
    mid = f"cam_{cam_file.name}_{cam_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        st.session_state.tool_mode = ""
        media_part = {"inline_data": {"mime_type": cam_file.type or "image/jpeg", "data": base64.b64encode(cam_file.getvalue()).decode("utf-8")}}
        media_label = "📷 [카메라 촬영] 이 사진의 내용을 알려줘."
elif doc_file is not None:
    mid = f"doc_{doc_file.name}_{doc_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        st.session_state.tool_mode = ""
        media_part = {"inline_data": {"mime_type": doc_file.type or "text/plain", "data": base64.b64encode(doc_file.getvalue()).decode("utf-8")}}
        media_label = f"📎 [파일: {doc_file.name}] 이 파일의 내용을 요약해줘."
elif aud_file is not None:
    mid = f"aud_{aud_file.name}_{aud_file.size}"
    if mid != st.session_state.last_media_id:
        st.session_state.last_media_id = mid
        st.session_state.tool_mode = ""
        media_part = {"inline_data": {"mime_type": aud_file.type or "audio/wav", "data": base64.b64encode(aud_file.getvalue()).decode("utf-8")}}
        media_label = "🎙️ [음성 질문] 방금 말한 음성 내용을 듣고 답변해줘."

prompt = text_in or media_label
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("🌙 𝐍𝐘𝐗가 답변하고 있습니다..."):
        reply = ask_nyx(st.session_state.messages, media_part=media_part)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

