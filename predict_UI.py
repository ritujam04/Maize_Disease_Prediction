import streamlit as st
import requests
from PIL import Image
import io

# ✅ Replace with your deployed Hugging Face API URL
API_URL = "https://rituja04-maize-disease-api.hf.space/predict/"

# 🎨 Streamlit UI Configuration
st.set_page_config(page_title="Maize Disease Detector", page_icon="🌿", layout="centered")

# 🎨 Add Light Green Background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d4f8c4; /* Light Green */
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
            background-color: #66c267 !important; /* Dark Green Background */
            height: 40px; /* Adjust height if needed */
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# 🎯 Title
st.title("🌽 Maize Disease Detection App")
st.write("Upload a maize leaf image to predict its disease.")

# 📤 File Upload
uploaded_file = st.file_uploader("📸 Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to bytes for API request
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    files = {"file": image_bytes.getvalue()}

    # 🔍 Predict Button
    if st.button("🔍 Predict Disease"):
        with st.spinner("Processing... ⏳"):
           response = requests.post(API_URL, files=files)
           result = response.json()

           # Debugging: Print the response
           #st.write("API Response:", result)   
           if result is not None:
               status = result["status"]
               disease = result["Predicted Disease"]
               confidence = result.get("Confidence Score", "N/A")
               description = result.get("description", "N/A")
               cause = result["cause"]
               symptoms = result.get("symptoms", "N/A")
               solution = result.get("solution", "N/A")
               st.write(f"**Status**: {status}")   
               st.success(f"🌿 **Predicted Disease:** {disease}")
               st.metric(label="📊 Confidence Score", value=f"{confidence}%")
               st.write(f"💬 **Description:** {description}")
               st.write(f"🦠 **Cause**:{cause}")
               st.write(f"⚠️ **Symptoms:** {symptoms}")
               st.write(f"💡 **Solution:** {solution}")
           else:
               st.error("❌ Error: 'result' key not found in API response")


            
