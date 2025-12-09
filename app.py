import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

# Try to get the key from Streamlit secrets first, then from .env
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

if not api_key:
    st.error("⚠️ OPENAI_API_KEY not found. Please set it in your .env or Streamlit secrets.")
    st.stop()

# -------------------------
# Initialize OpenAI client
# -------------------------
client = OpenAI(api_key=api_key)

# -------------------------
# Streamlit page setup
# -------------------------
st.set_page_config(page_title="🎓 AI Study Buddy", page_icon="📘", layout="wide")
st.title("🎓 AI-Powered Study Buddy")
st.markdown(
    "Your personal AI companion for learning — explain topics, summarize notes, and generate quizzes easily!"
)

# -------------------------
# Sidebar options
# -------------------------
st.sidebar.title("🧭 Choose a Function")
option = st.sidebar.radio("Select an action:", ["Explain Topic", "Summarize Notes", "Generate Quiz"])

# -------------------------
# User input
# -------------------------
user_input = st.text_area("✏️ Enter your topic, notes, or text here:", height=200)

# -------------------------
# Generate button
# -------------------------
if st.button("🚀 Generate"):
    if not user_input.strip():
        st.warning("Please enter some text or topic first.")
    else:
        with st.spinner("AI is thinking... 💡"):
            try:

                # -------------------------
                # Prepare prompt
                # -------------------------
                if option == "Explain Topic":
                    prompt = f"Explain the following topic in simple words for a student:\n\n{user_input}"
                elif option == "Summarize Notes":
                    prompt = f"Summarize these notes clearly and concisely:\n\n{user_input}"
                else:
                    prompt = (
                        "Generate 5 multiple-choice quiz questions with answers based on the following content:\n\n"
                        f"{user_input}"
                    )

                # -------------------------
                # Call OpenAI API (NEW METHOD)
                # -------------------------
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=[
                        {"role": "system", "content": "You are an AI study assistant helping students learn efficiently."},
                        {"role": "user", "content": prompt}
                    ],
                    max_output_tokens=600,
                    temperature=0.7,
                )

                output = response.output_text

                st.success("✅ Done!")
                st.markdown("### 📘 Output:")
                st.markdown(output)

            except Exception as e:
                if "insufficient_quota" in str(e) or "429" in str(e):
                    st.error(
                        "⚠️ Your OpenAI API quota has been exceeded. "
                        "Please check your usage or upgrade your plan."
                    )
                else:
                    st.error(f"⚠️ Something went wrong: {e}")

st.markdown("---")
st.markdown("Built on macOS using Streamlit and OpenAI")




