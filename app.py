import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

@st.cache_resource
def get_session():
    return new_session("u2net")

# Load model session
session = get_session()


def remove_bg_cached(_image):
    return remove(_image, session=session)

st.title("Background Remover App")
st.write("Upload an image and remove its background instantly!")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption='Original Image', use_container_width=True)

    if st.button("Remove Background"):
        with st.spinner("Removing background..."):

            output_image = remove_bg_cached(input_image)
            buf = io.BytesIO()
            output_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.image(output_image, caption='Background Removed', use_container_width=True)
            st.download_button(label="Download Image", data=byte_im, file_name="output.png", mime="image/png")
