import streamlit as st

st.set_page_config(
    page_title="VisionTalk Test",
    page_icon="👁️"
)

st.title("👁️ VisionTalk")
st.write("Streamlit is working!")

st.sidebar.header("🖼️ Upload Image")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:
    st.image(uploaded_file)

st.success("✅ VisionTalk interface is loading correctly!")