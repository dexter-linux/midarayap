import os
import tempfile
import google.generativeai as genai
import streamlit as st

# ==========================================
# 1. STREAMLIT CONFIG & WARM SUNSET THEME
# ==========================================
st.set_page_config(
    page_title="Multimodal AI Chatbot",
    page_icon="🤖",
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
    margin-bottom: 2rem;
    font-weight: 500;
}

/* Chat Input & Selectbox Styling */
textarea, input, select {
    background-color: #ffffff !important;
    color: #2c2523 !important;
    border: 1px solid #e0825d !important;
    border-radius: 10px !important;
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
# 2. SIDEBAR & API KEY SETUP
# ==========================================
with st.sidebar:
    st.markdown("## 🤖 **Multimodal AI Assistant**")
    st.markdown("---")

    # Retrieve API key from Streamlit secrets or user input
    api_key = os.environ.get("GEMINI_API_KEY", "")

    if not api_key:
        api_key = st.text_input(
            "Enter Gemini API Key:",
            type="password",
            help="Get a free key at aistudio.google.com",
        )
        st.markdown("[Get a Free Gemini API Key](https://aistudio.google.com/)")
    else:
        st.success("🔑 API Key configured from secrets!")

    st.markdown("---")
    st.markdown(
        "**Supported Inputs:**\n"
        "• 💬 **Text Messages**\n"
        "• 🖼️ **Images** (PNG, JPG, WEBP)\n"
        "• 🎙️ **Audio Recording / Files** (WAV, MP3, M4A)\n"
        "• 🎥 **Video Files** (MP4, MOV, AVI)"
    )

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 3. INITIALIZE GEMINI CLIENT & STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown(
    '<div class="warm-header">🤖 Multimodal AI Assistant</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="warm-subtitle">Chat using text, audio recordings, images, and video powered by Gemini</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="warm-line"></div>', unsafe_allow_html=True)

if not api_key:
    st.warning(
        "Please provide a Gemini API Key in the sidebar to start chatting."
    )
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# ==========================================
# 4. MEDIA INPUT EXPANDER
# ==========================================
st.markdown("### 📎 Attach Media")

col1, col2, col3 = st.columns(3)

uploaded_image = None
uploaded_audio = None
uploaded_video = None

with col1:
    image_file = st.file_uploader(
        "Upload Image", type=["png", "jpg", "jpeg", "webp"], key="img_uploader"
    )
    if image_file:
        uploaded_image = image_file
        st.image(image_file, caption="Attached Image", use_container_width=True)

with col2:
    st.markdown("**Record or Upload Audio**")
    recorded_audio = st.audio_input("Record Voice", key="audio_recorder")
    audio_file = st.file_uploader(
        "Upload Audio", type=["wav", "mp3", "m4a", "ogg"], key="audio_uploader"
    )

    if recorded_audio:
        uploaded_audio = recorded_audio
    elif audio_file:
        uploaded_audio = audio_file

with col3:
    video_file = st.file_uploader(
        "Upload Video", type=["mp4", "mov", "avi"], key="vid_uploader"
    )
    if video_file:
        uploaded_video = video_file
        st.video(video_file)

st.markdown('<div class="warm-line"></div>', unsafe_allow_html=True)

# ==========================================
# 5. RENDER CHAT HISTORY
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "media_type" in msg:
            if msg["media_type"] == "image":
                st.image(msg["media_data"])
            elif msg["media_type"] == "audio":
                st.audio(msg["media_data"])
            elif msg["media_type"] == "video":
                st.video(msg["media_data"])

# ==========================================
# 6. HANDLE CHAT INPUT & MULTIMODAL INFERENCE
# ==========================================
user_prompt = st.chat_input("Ask a question or describe attached media...")

if user_prompt:
    contents = []
    temp_files_to_cleanup = []

    # Display user text in chat
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Process Image Attachment
    if uploaded_image:
        image_bytes = uploaded_image.read()
        contents.append({"mime_type": uploaded_image.type, "data": image_bytes})
        st.session_state.messages.append({
            "role": "user",
            "content": "[Attached Image]",
            "media_type": "image",
            "media_data": image_bytes,
        })

    # Process Audio Attachment
    if uploaded_audio:
        audio_bytes = uploaded_audio.read()
        mime_t = (
            uploaded_audio.type
            if hasattr(uploaded_audio, "type") and uploaded_audio.type
            else "audio/wav"
        )
        contents.append({"mime_type": mime_t, "data": audio_bytes})
        st.session_state.messages.append({
            "role": "user",
            "content": "[Attached Audio]",
            "media_type": "audio",
            "media_data": audio_bytes,
        })

    # Process Video Attachment
    if uploaded_video:
        suffix = f".{uploaded_video.name.split('.')[-1]}"
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix
        ) as tmp:
            tmp.write(uploaded_video.read())
            tmp_path = tmp.name
            temp_files_to_cleanup.append(tmp_path)

        st.info("Uploading video to Gemini for analysis...")
        video_gemini_file = genai.upload_file(tmp_path)
        contents.append(video_gemini_file)
        st.session_state.messages.append({
            "role": "user",
            "content": "[Attached Video]",
            "media_type": "video",
            "media_data": uploaded_video,
        })

    # Append Text Prompt
    contents.append(user_prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(contents)
                assistant_text = response.text
                st.markdown(assistant_text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_text}
                )
            except Exception as e:
                error_msg = f"Error generating response: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
            finally:
                for tmp_file in temp_files_to_cleanup:
                    if os.path.exists(tmp_file):
                        os.remove(tmp_file)
