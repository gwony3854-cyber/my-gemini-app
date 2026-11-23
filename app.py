import json
import streamlit as st
import streamlit.components.v1 as components
import requests

st.set_page_config(page_title="𝐍𝐘𝐗", page_icon="🌙", layout="centered")

st.markdown("""
<style>
    html, body, [class*="css"] {background-color: #090b10 !important; color: #f1f5f9 !important;}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stBottom"] {background-color: #090b10 !important;}
    [data-testid="stSidebar"], header, footer, #MainMenu {display: none !important;}
    .block-container {max-width: 740px; padding-top: 1rem; padding-bottom: 1.5rem;}
    .nyx-welcome {text-align: center; margin-top: 8vh; margin-bottom: 1.8rem;}
    .nyx-moon {font-size: 2.3rem; margin-bottom: 6px;}
    .nyx-title {background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.1rem; font-weight: 700;}
    .nyx-desc {color: #94a3b8; font-size: 0.95rem; margin-top: 6px;}
    .drawer-box {background-color: #111520; border: 1px solid #263147; border-radius: 16px; padding: 14px; margin-bottom: 16px;}
    .u-wrap {display: flex; justify-content: flex-end; margin: 14px 0; scroll-margin-top: 24px;}
    .u-msg {background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; padding: 11px 17px; border-radius: 18px 18px 4px 18px; max-width: 76%; font-size: 0.96rem; line-height: 1.5; word-break: break-word;}
    .a-head {display: flex; align-items: center; gap: 8px; color: #38bdf8; font-weight: 600; font-size: 0.9rem; margin-top: 16px; margin-bottom: 6px;}
    div.stButton > button {background-color: #141926 !important; color: #e2e8f0 !important; border: 1px solid #263147 !important; border-radius: 12px !important; padding: 8px 12px !important; font-size: 0.9rem !important; text-align: left !important;}
    div.stButton > button:hover {border-color: #38bdf8 !important; color: #ffffff !important;}
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
            res = requests.post(url, params={"key": API_KEY}, json={"systemInstruction": {"parts": [{"text": "너의 이름은 𝐍𝐘𝐗(NYX)다. 텍스트, 이미지, 파일을 정확히 이해하고 한국어로 친절하게 답변하는 AI 어시스턴트다."}]}, "contents": contents}, timeout=30).json()
            cands = res.get("candidates")
            if isinstance(cands, list) and len(cands) > 0:
                p_list = next(iter(cands)).get("content", {}).get("parts", list())
                txt = "".join(p.get("text", "") for p in p_list).strip()
                if txt:
                    return txt
        except Exception:
            continue
    return "잠시 연결이 원활하지 않습니다. 다시 시도해 주세요."

for k, v in (("messages", list()), ("drawer_open", False), ("jump_id", ""), ("last_nonce", "")):
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
    st.markdown('<div class="drawer-box"><b>🕒 내가 말한 대화 기록 (누르면 해당 위치로 이동)</b></div>', unsafe_allow_html=True)
    if st.button("＋ 새 채팅 시작하기", use_container_width=True):
        st.session_state.messages = list()
        st.session_state.drawer_open = False
        st.session_state.jump_id = ""
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
    st.markdown('<div class="nyx-welcome"><div class="nyx-moon">🌙</div><div class="nyx-title">𝐍𝐘𝐗와 대화 시작하기</div><div class="nyx-desc">무엇이든 물어보거나 하단 ＋, 🎙️ 버튼으로 질문해 보세요.</div></div>', unsafe_allow_html=True)

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

bar_html = """
<div style="font-family:sans-serif;color:#f1f5f9;position:relative;padding-top:155px;">
  <div id="toast" style="display:none;position:absolute;top:92px;left:8px;right:8px;background:#1e293b;color:#38bdf8;padding:9px 14px;border-radius:12px;font-size:13px;border:1px solid #334155;text-align:center;"></div>
  <div id="menu" style="display:none;position:absolute;bottom:68px;left:8px;background:#141926;border:1px solid #2a354d;border-radius:16px;padding:6px;width:190px;box-shadow:0 8px 24px rgba(0,0,0,0.6);z-index:99;">
    <div onclick="pickFile('img')" style="padding:10px 12px;border-radius:10px;cursor:pointer;font-size:14px;">🖼️ 이미지 추가</div>
    <div onclick="openCam()" style="padding:10px 12px;border-radius:10px;cursor:pointer;font-size:14px;">📷 카메라 촬영</div>
    <div onclick="pickFile('doc')" style="padding:10px 12px;border-radius:10px;cursor:pointer;font-size:14px;">📎 파일 추가</div>
  </div>
  <div id="chip" style="display:none;margin:0 8px 8px 8px;background:#141926;border:1px solid #2a354d;padding:6px 12px;border-radius:12px;font-size:13px;color:#38bdf8;justify-content:space-between;align-items:center;">
    <span id="chipName"></span><span onclick="clearFile()" style="cursor:pointer;color:#94a3b8;font-weight:bold;">✕</span>
  </div>
  <div style="display:flex;align-items:center;background:#121621;border:1px solid #252e42;border-radius:28px;padding:6px 8px;gap:6px;">
    <button onclick="toggleMenu()" style="width:36px;height:36px;border-radius:50%;border:none;background:#1b2232;color:#e2e8f0;font-size:20px;cursor:pointer;">＋</button>
    <input id="txt" type="text" placeholder="𝐍𝐘𝐗에게 메시지 보내기..." onkeydown="if(event.key==='Enter')sendMsg()" style="flex:1;background:transparent;border:none;outline:none;color:#f8fafc;font-size:15px;padding:6px;">
    <button id="micBtn" onclick="startVoice()" style="width:36px;height:36px;border-radius:50%;border:none;background:transparent;color:#cbd5e1;font-size:18px;cursor:pointer;">🎙️</button>
    <button onclick="sendMsg()" style="width:36px;height:36px;border-radius:50%;border:none;background:#2563eb;color:#ffffff;font-size:16px;font-weight:bold;cursor:pointer;">↑</button>
  </div>
  <input id="inImg" type="file" accept="image/*" style="display:none" onchange="onFile(this)">
  <input id="inCam" type="file" accept="image/*" capture="environment" style="display:none" onchange="onFile(this)">
  <input id="inDoc" type="file" accept=".pdf,.txt,.csv,.py,.md" style="display:none" onchange="onFile(this)">
</div>
<script>
let fileB64 = "", fileMime = "", fileName = "";
function showToast(m) { const t=document.getElementById('toast'); t.innerText=m; t.style.display='block'; setTimeout(()=>t.style.display='none', 4000); }
function toggleMenu() { const m=document.getElementById('menu'); m.style.display = (m.style.display==='block') ? 'none' : 'block'; }
function pickFile(type) {
  document.getElementById('menu').style.display='none';
  if(type==='img') document.getElementById('inImg').click();
  if(type==='doc') document.getElementById('inDoc').click();
}
async function openCam() {
  document.getElementById('menu').style.display='none';
  try {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const s = await navigator.mediaDevices.getUserMedia({video: true});
      s.getTracks().forEach(t => t.stop());
    }
    document.getElementById('inCam').click();
  } catch (e) {
    showToast("🔒 카메라 권한이 꺼져 있습니다. 브라우저 설정에서 카메라 권한을 허용해 주세요.");
  }
}
function onFile(el) {
  const f = el.files; if(!f) return;
  fileName = f.name; fileMime = f.type || "image/jpeg";
  const r = new FileReader();
  r.onload = () => { fileB64 = r.result.split(','); document.getElementById('chipName').innerText = "📎 " + fileName; document.getElementById('chip').style.display='flex'; };
  r.readAsDataURL(f);
}
function clearFile() { fileB64=""; fileMime=""; fileName=""; document.getElementById('chip').style.display='none'; }
async function startVoice() {
  try {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const s = await navigator.mediaDevices.getUserMedia({audio: true});
      s.getTracks().forEach(t => t.stop());
    }
  } catch (e) {
    showToast("🔒 마이크(음성) 권한이 꺼져 있습니다. 브라우저 설정에서 마이크 권한을 허용해 주세요.");
    return;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR) { showToast("이 브라우저에서는 음성 인식을 지원하지 않습니다."); return; }
  const rec = new SR(); rec.lang = 'ko-KR';
  document.getElementById('micBtn').style.color = '#ef4444';
  rec.onresult = (e) => { document.getElementById('txt').value = e.results.transcript; document.getElementById('micBtn').style.color = '#cbd5e1'; };
  rec.onerror = () => { document.getElementById('micBtn').style.color = '#cbd5e1'; showToast("🔒 음성 인식 권한을 확인해 주세요."); };
  rec.start();
}
function sendMsg() {
  const val = document.getElementById('txt').value.trim();
  if(!val && !fileB64) return;
  const payload = JSON.stringify({text: val || (fileName + " 분석해줘"), b64: fileB64, mime: fileMime, name: fileName, nonce: Date.now()});
  const pDoc = window.parent.document;
  const box = pDoc.querySelector('textarea[aria-label="nyx_bridge"]');
  if(box) {
    const setter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, "value").set;
    setter.call(box, payload);
    box.dispatchEvent(new Event('input', {bubbles: true}));
    setTimeout(() => {
      box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}));
    }, 80);
  }
  document.getElementById('txt').value = ""; clearFile();
}
</script>
"""
components.html(bar_html, height=230)

st.markdown('<style>div[data-testid="stTextArea"]{position:fixed;left:-9999px;opacity:0;}</style>', unsafe_allow_html=True)
bridge = st.text_area("nyx_bridge", label_visibility="collapsed")
if bridge:
    try:
        data = json.loads(bridge)
        nonce = str(data.get("nonce", ""))
        if nonce and nonce != st.session_state.last_nonce:
            st.session_state.last_nonce = nonce
            u_text = data.get("text", "")
            if data.get("name"):
                u_text = f"📎 [{data.get('name')}] {u_text}"
            media_part = {"inline_data": {"mime_type": data["mime"], "data": data["b64"]}} if data.get("b64") else None
            st.session_state.messages.append({"role": "user", "content": u_text})
            with st.spinner("🌙 𝐍𝐘𝐗가 답변하고 있습니다..."):
                reply = ask_nyx(st.session_state.messages, media_part=media_part)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
    except Exception:
        pass

