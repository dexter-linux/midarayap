import base64
import datetime
import json
import os
import streamlit as st

# ==========================================
# 1. STREAMLIT CONFIG & WARM SUNSET THEME
# ==========================================
st.set_page_config(
    page_title="Whispers — Real-Time Chat Room",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

WARM_LIGHT_CSS = """
<style>
/* App background - Light Warm Linen & Sunset Glow */
.stApp {
    background: linear-gradient(135deg, #fdfbf7 0%, #fef5ed 50%, #f7ebe1 100%);
    color: #2c2523;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar styling - Warm Sand Glassmorphism */
[data-testid="stSidebar"] {
    background: rgba(253, 246, 238, 0.9);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(224, 130, 93, 0.2);
}

/* Main title styling */
.warm-header {
    background: linear-gradient(90deg, #e05638 0%, #d97736 50%, #c85a32 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}

.warm-subtitle {
    color: #7c5c4e;
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
    font-weight: 500;
}

/* Chat Input & Textarea Styling */
textarea, input, select {
    background-color: #ffffff !important;
    color: #2c2523 !important;
    border: 1px solid #e0825d !important;
    border-radius: 10px !important;
}

/* Custom Message Bubble */
.chat-bubble {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    border: 1px solid rgba(224, 130, 93, 0.25);
    box-shadow: 0 4px 15px rgba(184, 115, 84, 0.06);
    margin-bottom: 1rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #e05638 0%, #d97736 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(224, 86, 56, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(224, 86, 56, 0.5) !important;
}

/* Warm Line Divider */
.warm-line {
    height: 4px;
    background: linear-gradient(90deg, transparent, #e05638, #f0a273, transparent);
    border-radius: 2px;
    margin: 1.5rem 0;
}
</style>
"""

st.markdown(WARM_LIGHT_CSS, unsafe_allow_html=True)

# ==========================================
# 2. SHARED CHAT STORAGE SETUP
# ==========================================
CHAT_FILE = "chat_rooms.json"


def load_chat_data():
    """Load chat rooms from shared JSON storage."""
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"General": []}


def save_chat_data(data):
    """Save chat rooms to shared JSON storage."""
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# Load data into session memory
chat_data = load_chat_data()

# ==========================================
# 3. SIDEBAR — USER PROFILE & ROOMS
# ==========================================
with st.sidebar:
    st.markdown("## 💬 **Whispers Chatroom**")
    st.markdown("---")

    # Username Profile
    username = st.text_input("Your Name / Alias:", value="User_1")

    st.markdown("---")
    st.markdown("### 🚪 Select or Create Room")

    room_names = list(chat_data.keys())
    selected_room = st.selectbox("Choose Chat Room:", options=room_names)

    new_room = st.text_input("Create New Room:")
    if st.button("➕ Create Room"):
        if new_room.strip() and new_room.strip() not in chat_data:
            chat_data[new_room.strip()] = []
            save_chat_data(chat_data)
            st.success(f"Room '{new_room.strip()}' created!")
            st.rerun()

    st.markdown("---")
    if st.button("🔄 Refresh Messages"):
        st.rerun()

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
st.markdown(
    f'<div class="warm-header">💬 {selected_room}</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="warm-subtitle">Real-time messaging, audio voice notes, image sharing, and file transfers</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="warm-line"></div>', unsafe_allow_html=True)

# ==========================================
# 5. ATTACHMENT CONTROLS
# ==========================================
with st.expander("📎 Attach Media or Voice Note"):
    col1, col2, col3 = st.columns(3)

    uploaded_image = None
    uploaded_audio = None
    uploaded_video = None

    with col1:
        img_file = st.file_uploader(
            "Attach Image", type=["png", "jpg", "jpeg", "webp"]
        )
        if img_file:
            uploaded_image = img_file

    with col2:
        st.markdown("**Voice Note / Audio**")
        rec_audio = st.audio_input("Record Voice Note")
        aud_file = st.file_uploader(
            "Upload Audio", type=["wav", "mp3", "m4a", "ogg"]
        )
        if rec_audio:
            uploaded_audio = rec_audio
        elif aud_file:
            uploaded_audio = aud_file

    with col3:
        vid_file = st.file_uploader(
            "Attach Video File", type=["mp4", "mov", "avi"]
        )
        if vid_file:
            uploaded_video = vid_file

# ==========================================
# 6. RENDER CHAT MESSAGES
# ==========================================
room_messages = chat_data.get(selected_room, [])

if not room_messages:
    st.info("No messages in this room yet. Send a message below!")
else:
    for msg in room_messages:
        timestamp = msg.get("timestamp", "")
        sender = msg.get("sender", "Anonymous")
        text = msg.get("text", "")

        st.markdown(
            f"""
            <div class="chat-bubble">
                <span style="font-weight: 700; color: #e05638;">{sender}</span>
                <span style="font-size: 0.8rem; color: #7c5c4e; float: right;">{timestamp}</span>
                <p style="margin-top: 0.5rem; margin-bottom: 0.5rem; color: #2c2523;">{text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Render attachments if present
        if msg.get("image_data"):
            st.image(base64.b64decode(msg["image_data"]))
        if msg.get("audio_data"):
            st.audio(base64.b64decode(msg["audio_data"]))
        if msg.get("video_data"):
            st.video(base64.b64decode(msg["video_data"]))

st.markdown('<div class="warm-line"></div>', unsafe_allow_html=True)

# ==========================================
# 7. CHAT INPUT & SEND LOGIC
# ==========================================
user_message = st.chat_input("Type your message...")

if user_message or uploaded_image or uploaded_audio or uploaded_video:
    new_entry = {
        "sender": username,
        "text": user_message if user_message else "",
        "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
    }

    if uploaded_image:
        new_entry["image_data"] = base64.b64encode(
            uploaded_image.read()
        ).decode("utf-8")
    if uploaded_audio:
        new_entry["audio_data"] = base64.b64encode(
            uploaded_audio.read()
        ).decode("utf-8")
    if uploaded_video:
        new_entry["video_data"] = base64.b64encode(
            uploaded_video.read()
        ).decode("utf-8")

    chat_data[selected_room].append(new_entry)
    save_chat_data(chat_data)
    st.rerun()
