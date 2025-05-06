import streamlit as st
import os
import base64
from openai import OpenAI
import logging
from logging.handlers import RotatingFileHandler

# Logger Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = RotatingFileHandler('app.log', maxBytes=5*1024*1024, backupCount=3)
logger.addHandler(file_handler)

# Setup OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
client = OpenAI()

# URL for top-center logo
logo_url = "https://cdn.brandfetch.io/idR3duQxYl/theme/light/symbol.svg?c=1dxbfHSJFAPEGdCLU4o5B"  # Replace with your logo URL

# Custom CSS for styling
st.markdown(
    f"""
    <style>
    .main {{
        background-color: #f0f2f6;
        color: #202123;
        font-family: 'Helvetica Neue', sans-serif;
        padding: 2rem;
    }}
    .stButton>button {{
        background-color: #10a37f;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1rem;
    }}
    .stFileUploader>div, .stTextArea>div {{
        background-color: white;
        border: 1px solid #e1e3e6;
        border-radius: 8px;
        padding: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Header with centered logo
st.markdown(
    f"<div style='text-align:center; margin-bottom: 1rem;'><img src='{logo_url}' width='120'/></div>",
    unsafe_allow_html=True
)
st.header("🖼️ GPT-Image-1 Testing Interface")
st.write("Upload an image, enter a prompt, and click **Submit** to edit the image.")

# File upload and prompt input
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"], help="Choose an image to edit.")
prompt = st.text_area("Prompt", placeholder="Describe what you want to do with the image...", height=100)

# Submit button
if st.button("Submit"):
    if uploaded_file and prompt.strip():
        try:
            # Show spinner while generating
            with st.spinner("Generating image, please wait..."):
                # Save uploaded image
                temp_path = "uploaded_image.jpg"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Call OpenAI image edit API
                with open(temp_path, "rb") as img_file:
                    result = client.images.edit(
                        model="gpt-image-1",
                        image=[img_file],
                        prompt=prompt,
                    )

                # Decode result
                b64 = result.data[0].b64_json
                img_data = base64.b64decode(b64)

            # Display generated image
            st.image(img_data, caption="Edited Image", use_container_width=True)

            # Download button
            st.download_button(
                label="Download Image",
                data=img_data,
                file_name="edited_output.png",
                mime="image/png"
            )

            # Save locally and log
            with open("edited_output.png", "wb") as out:
                out.write(img_data)
            logger.info("Image generated and saved locally.")
            st.success("✅ Image generated successfully.")

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload an image and enter a prompt before submitting.")
