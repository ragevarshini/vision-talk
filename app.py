import streamlit as st

from image_analyzer import analyze_image
from prompt_builder import build_prompt
from speech_to_text import speech_to_text
from text_to_speech import text_to_speech


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VisionTalk",
    page_icon="👁️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("👁️ VisionTalk")

st.write(
    "Conversational Image Recognition Chatbot "
    "for Visually Impaired Users"
)


# ============================================================
# SESSION STATE
# ============================================================

if "image_data" not in st.session_state:
    st.session_state.image_data = None

if "image_name" not in st.session_state:
    st.session_state.image_name = None

if "image_type" not in st.session_state:
    st.session_state.image_type = None

if "image_processed" not in st.session_state:
    st.session_state.image_processed = False

if "image_description" not in st.session_state:
    st.session_state.image_description = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🖼️ Upload Image")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    analyze_button = st.button(
        "🔍 Analyze Image",
        use_container_width=True
    )

    st.divider()

    st.info(
        """
        VisionTalk allows users to:

        • Upload an image
        • Understand image content
        • Ask questions about the image
        • Continue a conversation
        • Use speech input
        • Listen to AI answers
        """
    )

    if st.session_state.image_processed:

        st.success(
            f"Image: {st.session_state.image_name}"
        )

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.rerun()


# ============================================================
# IMAGE ANALYSIS
# ============================================================

if analyze_button:

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload an image first."
        )

    else:

        try:

            with st.spinner(
                "🧠 Analyzing image..."
            ):

                # --------------------------------------------
                # Read image
                # --------------------------------------------

                image_bytes = uploaded_file.getvalue()

                # --------------------------------------------
                # Save image information
                # --------------------------------------------

                st.session_state.image_data = image_bytes

                st.session_state.image_name = (
                    uploaded_file.name
                )

                st.session_state.image_type = (
                    uploaded_file.type
                )

                # --------------------------------------------
                # Analyze image
                # --------------------------------------------

                description = analyze_image(
                    image_bytes,
                    uploaded_file.type
                )

                # --------------------------------------------
                # Save description
                # --------------------------------------------

                st.session_state.image_description = (
                    description
                )

                st.session_state.image_processed = True

                # --------------------------------------------
                # Clear previous conversation
                # --------------------------------------------

                st.session_state.chat_history = []

            st.success(
                "✅ Image analyzed successfully!"
            )

        except Exception as e:

            st.error(
                f"❌ Error analyzing image: {str(e)}"
            )


# ============================================================
# IMAGE DISPLAY
# ============================================================

if st.session_state.image_data is not None:

    st.divider()

    st.header("🖼️ Uploaded Image")

    col1, col2 = st.columns([1, 1])

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    with col1:

        st.image(
            st.session_state.image_data,
            caption=st.session_state.image_name,
            use_container_width=True
        )

    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    with col2:

        st.subheader("🔎 Image Description")

        if st.session_state.image_description:

            st.write(
                st.session_state.image_description
            )

        else:

            st.info(
                "Click 'Analyze Image' to understand "
                "the image."
            )


# ============================================================
# CHAT SECTION
# ============================================================

st.divider()

st.header("💬 Talk to VisionTalk")


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.chat_history:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ============================================================
# QUESTION INPUT
# ============================================================

st.subheader("🎤 Ask VisionTalk")

col1, col2 = st.columns([3, 1])


# ============================================================
# TEXT INPUT
# ============================================================

with col1:

    typed_question = st.chat_input(
        "Type your question about the image..."
    )


# ============================================================
# VOICE INPUT
# ============================================================

with col2:

    audio_input = st.audio_input(
        "🎤 Speak",
        sample_rate=16000
    )


# ============================================================
# INITIAL QUESTION
# ============================================================

question = typed_question


# ============================================================
# SPEECH TO TEXT
# ============================================================

if audio_input is not None:

    if not st.session_state.image_processed:

        st.warning(
            "⚠️ Please upload and analyze an image first."
        )

    else:

        with st.spinner(
            "🎤 Converting speech to text..."
        ):

            try:

                voice_question = speech_to_text(
                    audio_input,
                    language="en-IN"
                )

                if voice_question:

                    question = voice_question

                    st.success(
                        f"🗣️ You said: {voice_question}"
                    )

                else:

                    st.warning(
                        "⚠️ I couldn't understand your speech. "
                        "Please try again."
                    )

            except Exception as e:

                st.error(
                    f"❌ Speech recognition error: {e}"
                )


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # Check image
    # --------------------------------------------------------

    if not st.session_state.image_processed:

        st.warning(
            "⚠️ Please upload and analyze an image first."
        )

    else:

        # ----------------------------------------------------
        # Save user question
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        # ----------------------------------------------------
        # Display user question
        # ----------------------------------------------------

        with st.chat_message("user"):

            st.write(question)


        # ----------------------------------------------------
        # Generate AI answer
        # ----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "👁️ Understanding the image..."
            ):

                # Build prompt
                prompt = build_prompt(
                    question,
                    st.session_state.chat_history,
                    st.session_state.image_description
                )

                # Analyze image and generate answer
                answer = analyze_image(
                    st.session_state.image_data,
                    st.session_state.image_type,
                    prompt
                )

            # ------------------------------------------------
            # Display answer
            # ------------------------------------------------

            st.write(answer)


            # =================================================
            # TEXT TO SPEECH
            # =================================================

            try:

                with st.spinner(
                    "🔊 Generating voice..."
                ):

                    audio_file = text_to_speech(
                        answer
                    )

                st.audio(
                    audio_file,
                    format="audio/wav"
                )

            except Exception as e:

                st.warning(
                    f"🔊 Could not generate voice: {e}"
                )


        # ----------------------------------------------------
        # Save assistant answer
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )