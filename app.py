# app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Cartoon Converter", layout="centered")

st.title("🎨 Image to Cartoon Converter")
st.write("Upload an image and convert it into a cartoon effect.")

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

def cartoonify_image(image):
    # Convert PIL image to OpenCV format
    img = np.array(image)

    # Convert RGB to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize image
    img = cv2.resize(img, (600, 600))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur the image
    gray_blur = cv2.medianBlur(gray, 5)

    # Detect edges
    edges = cv2.adaptiveThreshold(
        gray_blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        9
    )

    # Apply bilateral filter
    color = cv2.bilateralFilter(img, 9, 250, 250)

    # Combine edges with color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # Convert back to RGB
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)

    return cartoon

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("✨ Convert to Cartoon"):

        with st.spinner("Creating cartoon effect..."):

            cartoon_image = cartoonify_image(image)

            st.subheader("Cartoon Image")
            st.image(cartoon_image, use_container_width=True)

            # Convert image for download
            cartoon_pil = Image.fromarray(cartoon_image)

            buffer = BytesIO()
            cartoon_pil.save(buffer, format="PNG")

            st.download_button(
                label="⬇ Download Cartoon Image",
                data=buffer.getvalue(),
                file_name="cartoon_image.png",
                mime="image/png"
            )
