import streamlit as st
import qrcode
import cv2
from PIL import Image
import numpy as np

def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img

def read_qr_code_from_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    return data if data else None

# --- Streamlit UI ---
st.title("🔳 QR Code Generator & Reader")

tab1, tab2 = st.tabs(["📤 Generate QR", "📥 Read QR"])

with tab1:
    st.header("Generate QR Code")
    user_data = st.text_input("Enter data to encode:", key="qr_input_generate")

    if user_data:
        img = create_qr_code(user_data)
        st.image(img, caption="Generated QR Code")
        st.success("QR Code generated successfully!")

with tab2:
    st.header("Read QR Code")
    uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"], key="qr_upload_reader")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded QR Image")
        decoded_data = read_qr_code_from_image(uploaded_file)
        if decoded_data:
            st.success(f"Decoded Data: {decoded_data}")
        else:
            st.warning("No QR Code detected in the image.")
