import streamlit as st
import requests
from PIL import Image
import io

# ✅ Replace with your deployed Hugging Face API URL
API_URL = "https://rituja04-date-disease-prediction.hf.space/predict/"

# 🎨 Streamlit UI Configuration
st.set_page_config(page_title="Dates Disease Detector", page_icon="🌿", layout="centered")

# 🎨 Add Light Green Background and Navbar Color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d4f8c4; /* Light Green Background */
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green Button */
        color: white;
        border-radius: 8px;
        padding: 10px;
    }
    header {
        background-color: #66c267 !important; /* Green Navbar */
        height: 40px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎯 Title
st.title("🌿 Dates Disease Detection App")
st.write("Upload a dates leaf image to predict its disease.")

# 📤 File Upload
uploaded_file = st.file_uploader("📸 Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    try:
        # Open image using PIL
        image = Image.open(uploaded_file).convert("RGB")

        # Display uploaded image
        st.image(image, caption="📷 Uploaded Image", use_column_width=True)

        # Convert image to bytes for API request
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        files = {"file": image_bytes.getvalue()}

        # 🔍 Predict Button
        if st.button("🔍 Predict Disease"):
            with st.spinner("Processing... ⏳"):
                response = requests.post(API_URL, files=files)

                # Validate API Response
                if response.status_code == 200:
                    try:
                        result = response.json()

                        # Ensure required keys exist
                        if "disease" in result and "details" in result:
                            disease = result["disease"]
                            confidence = result.get("confidence", "N/A")
                            description = result["details"].get("description", "N/A")
                            cause = result["details"].get("cause", "N/A")
                            symptoms = result["details"].get("symptoms", "N/A")
                            solution = result["details"].get("solution", "N/A")

                            # ✅ Display Results
                            st.success(f"🌿 **Predicted Disease:** {disease}")
                            st.metric(label="📊 Confidence Score", value=f"{confidence}%")
                            st.write(f"💬 **Description:** {description}")
                            st.write(f"🦠 **Cause:** {cause}")
                            st.write(f"⚠️ **Symptoms:** {symptoms}")
                            st.write(f"💡 **Solution:** {solution}")

                        else:
                            st.error("❌ API response is missing required data.")
                    except Exception as e:
                        st.error(f"❌ Error parsing API response: {e}")
                else:
                    st.error(f"❌ API Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"❌ Error loading image: {e}")
