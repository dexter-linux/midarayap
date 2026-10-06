import base64
import datetime
import json
import os
import random
import time
import streamlit as st

# ==========================================
# 1. STREAMLIT CONFIG & CLIMATE THEMES (CSS)
# ==========================================
st.set_page_config(
    page_title="Whispers — Private Session Chat",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- THEME DEFINITIONS ---

# Option 1: 🌲 Pine Forest Theme
FOREST_THEME = """
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    color: #e8f5e9;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
[data-testid="stSidebar"] {
    background: rgba(15, 32, 39, 0.85);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(76, 175, 80, 0.2);
}
.theme-header {
    background: linear-gradient(90deg, #a8e063 0%, #56ab2f 50%, #2e7d32 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}
.theme-subtitle { color: #a3e635; font-size: 1.05rem; margin-bottom: 1.5rem; font-weight: 500; }
textarea, input, select { background-color: rgba(20, 40, 48, 0.85) !important; color: #f1f8e9 !important; border: 1px solid #4caf50 !important; border-radius: 10px !important; }
.chat-bubble { background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(12px); border-radius: 14px; padding: 1rem 1.2rem; border: 1px solid rgba(129, 199, 132, 0.2); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25); margin-bottom: 1rem; }
.stButton > button { background: linear-gradient(135deg, #56ab2f 0%, #2e7d32 100%) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.5rem 1.5rem !important; font-weight: 600 !important; box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4) !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(168, 224, 99, 0.5) !important; }
.theme-line { height: 4px; background: linear-gradient(90deg, transparent, #56ab2f, #a8e063, transparent); border-radius: 2px; margin: 1.5rem 0; }
</style>
"""

# Option 2: 🌊 Ocean Abyss Theme
OCEAN_THEME = """
<style>
.stApp {
    background: linear-gradient(135deg, #0b192c 0%, #1e3e62 50%, #001f3f 100%);
    color: #f0f8ff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
[data-testid="stSidebar"] {
    background: rgba(11, 25, 44, 0.85);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(0, 210, 255, 0.2);
}
.theme-header {
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 50%, #00f2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}
.theme-subtitle { color: #a8dadc; font-size: 1.05rem; margin-bottom: 1.5rem; font-weight: 500; }
textarea, input, select { background-color: rgba(15, 32, 67, 0.8) !important; color: #e0f7fa !important; border: 1px solid #00b4db !important; border-radius: 10px !important; }
.chat-bubble { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px); border-radius: 14px; padding: 1rem 1.2rem; border: 1px solid rgba(0, 212, 255, 0.25); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37); margin-bottom: 1rem; }
.stButton > button { background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.5rem 1.5rem !important; font-weight: 600 !important; box-shadow: 0 4px 15px rgba(0, 180, 219, 0.4) !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(0, 242, 254, 0.6) !important; }
.theme-line { height: 4px; background: linear-gradient(90deg, transparent, #00d2ff, #00f2fe, transparent); border-radius: 2px; margin: 1.5rem 0; }
</style>
"""

# Option 3: 🏜️ Warm Desert Sunset Theme
DESERT_THEME = """
<style>
.stApp {
    background: linear-gradient(135deg, #fdfbf7 0%, #fef5ed 50%, #f7ebe1 100%);
    color: #2c2523;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
[data-testid="stSidebar"] {
    background: rgba(253, 246, 238, 0.9);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(224, 130, 93, 0.2);
}
.theme-header {
    background: linear-gradient(90deg, #e05638 0%, #d97736 50%, #c85a32 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}
.theme-subtitle { color: #7c5c4e; font-size: 1.05rem; margin-bottom: 1.5rem; font-weight: 500; }
textarea, input, select { background-color: #ffffff !important; color: #2c2523 !important; border: 1px solid #e0825d !important; border-radius: 10px !important; }
.chat-bubble { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); border-radius: 14px; padding: 1rem 1.2rem; border: 1px solid rgba(224, 130, 93, 0.25); box-shadow: 0 4px 15px rgba(184, 115, 84, 0.06); margin-bottom: 1rem; }
.stButton > button { background: linear-gradient(135deg, #e05638 0%, #d97736 100%) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.5rem 1.5rem !important; font-weight: 600 !important; box-shadow: 0 4px 15px rgba(224, 86, 56, 0.3) !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(224, 86, 56, 0.5) !important; }
.theme-line { height: 4px; background: linear-gradient(90deg, transparent, #e05638, #f0a273, transparent); border-radius: 2px; margin: 1.5rem 0; }
</style>
"""

# Option 4: 🌿 Lush Botanical Garden Theme
PLANTS_THEME = """
<style>
.stApp {
    background: linear-gradient(135deg, #f4f9f4 0%, #e8f1e5 50%, #dbe7d6 100%);
    color: #1b3b22;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
[data-testid="stSidebar"] {
    background: rgba(244, 249, 244, 0.9);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(46, 125, 50, 0.2);
}
.theme-header {
    background: linear-gradient(90deg, #2e7d32 0%, #388e3c 50%, #1b5e20 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}
.theme-subtitle { color: #43a047; font-size: 1.05rem; margin-bottom: 1.5rem; font-weight: 500; }
textarea, input, select { background-color: #ffffff !important; color: #1b3b22 !important; border: 1px solid #4caf50 !important; border-radius: 10px !important; }
.chat-bubble { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-radius: 14px; padding: 1rem 1.2rem; border: 1px solid rgba(76, 175, 80, 0.25); box-shadow: 0 4px 15px rgba(46, 125, 50, 0.08); margin-bottom: 1rem; }
.stButton > button { background: linear-gradient(135deg, #388e3c 0%, #1b5e20 100%) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.5rem 1.5rem !important; font-weight: 600 !important; box-shadow: 0 4px 15px rgba(56, 142, 60, 0.3) !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(76, 175, 80, 0.5) !important; }
.theme-line { height: 4px; background: linear-gradient(90deg, transparent, #388e3c, #81c784, transparent); border-radius: 2px; margin: 1.5rem 0; }
</style>
"""

# CHANGE THIS LINE TO SWITCH THEMES: FOREST_THEME, OCEAN_THEME, DESERT_THEME, or PLANTS_THEME
SELECTED_THEME = FOREST_THEME

st.markdown(SELECTED_THEME, unsafe_allow_html=True)

# ==========================================
# 2. SHARED CHAT STORAGE SETUP
# ==========================================
CHAT_FILE = "chat_rooms.json"


def load_chat_data():
    """Load chat rooms and metadata safely from shared JSON storage."""
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    clean_data = {}
                    for room_name, room_val in data.items():
                        if isinstance(room_val, dict):
                            clean_data[room_name] = room_val
                        elif isinstance(room_val, list):
                            clean_data[room_name] = {
                                "host": "Legacy Host",
                                "pin": "",
                                "messages": room_val,
                                "active": True,
                            }
                    return clean_data
        except Exception:
            pass
    return {}


def save_chat_data(data):
    """Save chat rooms and metadata to shared JSON storage."""
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


chat_data = load_chat_data()

# ==========================================
# 3. SIDEBAR — USER IDENTITY & ROOM CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("## 🔒 **Whispers Private Chat**")
    st.markdown("---")

    username = st.text_input("Your Alias / Name:", value="Guest")
    st.markdown("---")

    action = st.radio("Choose Action:", ["Join Existing Room", "Host New Room"])

    if action == "Host New Room":
        st.markdown("### 🔑 Host Room Settings")
        new_room_id = st.text_input("New Room Name / ID:")

        auto_pin = st.checkbox("Auto-generate 6-digit PIN", value=True)

        if auto_pin:
            if "random_pin_val" not in st.session_state:
                st.session_state["random_pin_val"] = str(
                    random.randint(100000, 999999)
                )
            room_pin = st.session_state["random_pin_val"]
            st.info(f"🔑 Your Auto-Generated PIN: **{room_pin}**")
        else:
            room_pin = st.text_input("Set Custom Room PIN:", type="password")

        if st.button("🚀 Create & Host Room"):
            clean_room_id = new_room_id.strip()
            if not clean_room_id:
                st.error("Room Name cannot be empty.")
            elif clean_room_id in chat_data:
                st.error("A room with this name already exists!")
            else:
                chat_data[clean_room_id] = {
                    "host": username,
                    "pin": str(room_pin).strip(),
                    "messages": [],
                    "active": True,
                }
                save_chat_data(chat_data)
                st.session_state["current_room"] = clean_room_id
                st.session_state["is_host"] = True
                st.session_state["authenticated_room"] = clean_room_id
                if "random_pin_val" in st.session_state:
                    del st.session_state["random_pin_val"]
                st.success(f"Room '{clean_room_id}' created as Host!")
                st.rerun()

    else:
        st.markdown("### 🚪 Join Room")
        available_rooms = [
            r
            for r, data in chat_data.items()
            if isinstance(data, dict) and data.get("active", True)
        ]

        if not available_rooms:
            st.info("No active rooms available. Create one to get started!")
            selected_room = None
        else:
            selected_room = st.selectbox(
                "Select Room:", options=available_rooms
            )
            enter_pin = st.text_input(
                "Enter Security PIN (if set):", type="password"
            )

            if st.button("🔓 Enter Room"):
                room_info = chat_data.get(selected_room, {})
                if not isinstance(room_info, dict):
                    room_info = {
                        "host": "Unknown",
                        "pin": "",
                        "messages": [],
                        "active": True,
                    }

                expected_pin = str(room_info.get("pin", ""))

                if expected_pin and enter_pin.strip() != expected_pin:
                    st.error("Incorrect PIN!")
                else:
                    st.session_state["current_room"] = selected_room
                    st.session_state["is_host"] = (
                        username == room_info.get("host")
                    )
                    st.session_state["authenticated_room"] = selected_room
                    st.success("Joined room successfully!")
                    st.rerun()

    st.markdown("---")
    st.caption("ℹ️ Messages update automatically when refreshing or sending.")

# ==========================================
# 4. MAIN INTERFACE & ROOM LOGIC
# ==========================================
active_room = st.session_state.get("authenticated_room")

if not active_room or active_room not in chat_data:
    st.markdown(
        '<div class="theme-header">🌿 Whispers Chat</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="theme-subtitle">Host a private session or enter a PIN to join someone far away.</div>',
        unsafe_allow_html=True,
    )
    st.info("Select an option from the sidebar to start.")
    st.stop()

room_info = chat_data[active_room]

if not isinstance(room_info, dict):
    room_info = {"host": "Unknown", "pin": "", "messages": [], "active": True}

# Check if room was closed by the host
if not room_info.get("active", True):
    st.error(
        "🛑 This room session was closed and destroyed by the Host. All messages have been wiped."
    )
    if st.button("Return to Lobby"):
        del st.session_state["authenticated_room"]
        st.rerun()
    st.stop()

# Room Header & Host Controls
is_host = (username == room_info.get("host")) or st.session_state.get(
    "is_host", False
)

col_title, col_host_actions = st.columns([3, 1])

with col_title:
    st.markdown(
        f'<div class="theme-header">🔒 Room: {active_room}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="theme-subtitle">Host: <b>{room_info.get("host")}</b> | Joined as: <b>{username}</b></div>',
        unsafe_allow_html=True,
    )

with col_host_actions:
    if is_host:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔥 Close Room & Wipe All Data", type="primary"):
            if active_room in chat_data:
                del chat_data[active_room]
                save_chat_data(chat_data)
            if "authenticated_room" in st.session_state:
                del st.session_state["authenticated_room"]
            st.success("Session closed! All chat history wiped instantly.")
            time.sleep(1)
            st.rerun()

st.markdown('<div class="theme-line"></div>', unsafe_allow_html=True)

# ==========================================
# 5. ATTACHMENT CONTROLS
# ==========================================
with st.expander("📎 Attach Media / Voice Note"):
    col1, col2, col3 = st.columns(3)

    uploaded_image = None
    uploaded_audio = None
    uploaded_video = None

    with col1:
        img_file = st.file_uploader(
            "Attach Image", type=["png", "jpg", "jpeg", "webp"], key="room_img"
        )
        if img_file:
            uploaded_image = img_file

    with col2:
        rec_audio = st.audio_input("Record Voice Note", key="room_rec")
        aud_file = st.file_uploader(
            "Upload Audio", type=["wav", "mp3", "m4a", "ogg"], key="room_aud"
        )
        if rec_audio:
            uploaded_audio = rec_audio
        elif aud_file:
            uploaded_audio = aud_file

    with col3:
        vid_file = st.file_uploader(
            "Attach Video File", type=["mp4", "mov", "avi"], key="room_vid"
        )
        if vid_file:
            uploaded_video = vid_file

# ==========================================
# 6. RENDER CHAT MESSAGES
# ==========================================
messages = room_info.get("messages", []) if isinstance(room_info, dict) else []

if not messages:
    st.info("Room is active and secure. Send a message or media below!")
else:
    for msg in messages:
        if isinstance(msg, dict):
            sender = msg.get("sender", "Anonymous")
            timestamp = msg.get("timestamp", "")
            text = msg.get("text", "")

            st.markdown(
                f"""
                <div class="chat-bubble">
                    <span style="font-weight: 700;">{sender}</span>
                    <span style="font-size: 0.8rem; float: right;">{timestamp}</span>
                    <p style="margin-top: 0.5rem; margin-bottom: 0.5rem;">{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if msg.get("image_data"):
                st.image(base64.b64decode(msg["image_data"]))
            if msg.get("audio_data"):
                st.audio(base64.b64decode(msg["audio_data"]))
            if msg.get("video_data"):
                st.video(base64.b64decode(msg["video_data"]))

st.markdown('<div class="theme-line"></div>', unsafe_allow_html=True)

# ==========================================
# 7. CHAT INPUT & SEND LOGIC
# ==========================================
user_message = st.chat_input("Type your message...")

if user_message or uploaded_image or uploaded_audio or uploaded_video:
    new_msg = {
        "sender": username,
        "text": user_message if user_message else "",
        "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
    }

    if uploaded_image:
        new_msg["image_data"] = base64.b64encode(
            uploaded_image.read()
        ).decode("utf-8")
    if uploaded_audio:
        new_msg["audio_data"] = base64.b64encode(
            uploaded_audio.read()
        ).decode("utf-8")
    if uploaded_video:
        new_msg["video_data"] = base64.b64encode(
            uploaded_video.read()
        ).decode("utf-8")

    if isinstance(chat_data.get(active_room), dict):
        chat_data[active_room]["messages"].append(new_msg)
        save_chat_data(chat_data)
        st.rerun()
