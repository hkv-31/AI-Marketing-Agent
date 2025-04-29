# app.py

import streamlit as st
from generateImage import generate_image
from webSearch import trend_search
from Instabot import upload_photo
import os

# Global testing flag
testing_mode = False  # Set False when you want real API

# Initialize session state variables
if "name" not in st.session_state:
    st.session_state.name = None
if "brand_info_done" not in st.session_state:
    st.session_state.brand_info_done = False
if "trend_summary" not in st.session_state:
    st.session_state.trend_summary = None
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

# App setup
st.set_page_config(page_title="AI Marketing Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI Marketing Agent")

# Step 1: User name
if not st.session_state.name:
    st.session_state.name = st.text_input("Enter your name:")

    if not st.session_state.name:
        st.stop()

# Step 2: Brand info
if not st.session_state.brand_info_done:
    st.subheader("Brand Details")
    brand_name = st.text_input("Brand Name")
    brand_niche = st.text_input("Brand Niche (e.g., Food, Fitness, Tech)")
    brand_identity = st.text_area("Brand Identity (Describe your tone, values, style)")
    website_url = st.text_input("Website URL (optional)")
    instagram_handle = st.text_input("Instagram Handle (optional)")

    if st.button("Analyze Brand"):
        with st.spinner('🔎 Scraping Trends...'):
            trend_summary = trend_search()
        st.success("✅ Trend Scraping Done!")
        st.session_state.trend_summary = trend_summary
        st.session_state.brand_info_done = True
        st.experimental_rerun()

# Step 3: Trend Scraping Done — Show Trend Summary
if st.session_state.brand_info_done and st.session_state.trend_summary:
    st.subheader("Trend Summary")
    st.info(st.session_state.trend_summary)

    st.subheader("Generate Post")

    # FIRST: Get upload and prompt **before** pressing button
    upload_image = st.file_uploader("Upload Brand Logo or Image (optional)", type=['jpg', 'jpeg', 'png'])

    custom_prompt = st.text_area("Custom Image Prompt (optional)", value=st.session_state.trend_summary)

    if st.button("Generate Post Image"):
        base_image_path = None

        if upload_image is not None:
            with open("temp_uploaded_image.jpg", "wb") as f:
                f.write(upload_image.read())
            base_image_path = "temp_uploaded_image.jpg"

        with st.spinner('🎨 Generating Image...'):
            image_bytes = generate_image(custom_prompt, base_image_path)

        st.success("✅ Post Image Generated!")

        if not testing_mode:
            st.image(image_bytes, caption="Generated Post", use_column_width=True)
        else:
            st.info("🧪 Testing Mode Active: Skipping actual image preview.")

        st.session_state.generated_image = "generated_output.jpeg"
        st.experimental_rerun()

# Step 5: Show Post and Instagram Posting
if st.session_state.generated_image:
    st.subheader("Post to Instagram")

    caption = st.text_area("Post Caption (Edit if you like)", value=f"🔥 {st.session_state.trend_summary}")

    username = st.text_input("Instagram Username")
    email = st.text_input("Instagram Email")  # Just for formality
    password = st.text_input("Instagram Password", type="password")

    if st.button("Post to Instagram"):
        with st.spinner('🚀 Posting...'):
            media_id = upload_photo(username, password, st.session_state.generated_image, caption)
        st.success(f"✅ Posted Successfully! Media ID: {media_id}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ for AI Foundry Project | Dummy Testing Mode: **{}**".format(testing_mode))
