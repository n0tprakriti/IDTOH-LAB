
# single_file_app.py
import streamlit as st
import requests

# ---- Configuration ----
GEMINI_API_KEY = "AIzaSyC-sioEi2Dyx54pPSx9BLxomJmdXHYbWiM"
GEMINI_TEXT_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GEMINI_IMAGE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent"
IMAGE_SAVE_PATH = "generated_posters"

PROMPT_TEMPLATES = {
    "Instagram": "Write a cool post for Instagram about: {topic}, include captions",
    "LinkedIn": "Write a professional LinkedIn post on: {topic}",
    "Twitter": "Write a concise and impactful tweet with hashtags on: {topic}",
}

# ---- LLM Functions ----
def query_gemini_text(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(f"{GEMINI_TEXT_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)
    if response.status_code == 200:
        candidates = response.json().get("candidates", [])
        return candidates[0]["content"]["parts"][0]["text"] if candidates else "No response"
    return f"Error: {response.text}"

# ---- Streamlit UI ----
st.set_page_config(page_title="Smart Content Generator", layout="centered")
st.title("\U0001F4DD Social Media Content Generator")

with st.form("content_form"):
    topic = st.text_input("What do you want to post about?")
    platform = st.selectbox("Choose a platform", list(PROMPT_TEMPLATES.keys()))
    post_type = st.selectbox("Post type", ["Text"])
    tone = st.selectbox("Tone", ["Professional", "Casual", "Funny", "Emotional"])
    submit = st.form_submit_button("Generate")

if submit:
    if not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating content..."):
            prompt = PROMPT_TEMPLATES[platform].format(topic=topic)
            full_prompt = f"Use a {tone.lower()} tone. {prompt}"
            output = query_gemini_text(full_prompt)
            st.subheader("\U0001F4AC Generated Content")
            st.write(output)

st.markdown("---")
st.caption("\U0001F4DD Feedback")
feedback = st.text_input("Tell us what to improve")
if feedback:
    st.success("Thanks for your feedback!")