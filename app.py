import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OPENAI_API_KEY not found in your environment. Please set it in your .env file.")
    st.stop()

# -------------------------
# Initialize OpenAI client
# -------------------------
api_key = st.secrets["OPENAI_API_KEY"]
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
                    prompt = f"Explain the following topic in simple terms suitable for a student:\n\n{user_input}\n\nExplanation:"
                elif option == "Summarize Notes":
                    prompt = f"Summarize the following notes clearly and concisely:\n\n{user_input}\n\nSummary:"
                else:  # Generate Quiz
                    prompt = f"Generate 5 multiple-choice quiz questions (with answers) from the following content:\n\n{user_input}\n\nQuiz:"

                # -------------------------
                # Call OpenAI API
                # -------------------------
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an AI study assistant that helps students learn efficiently."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=600
                )

                output = response.choices[0].message.content.strip()

                # -------------------------
                # Display output
                # -------------------------
                st.success("✅ Done!")
                st.markdown("### 📘 Output:")
                st.markdown(output)

            except Exception as e:
                # Catch all exceptions, including quota errors
                if "insufficient_quota" in str(e) or "429" in str(e):
                    st.error(
                        "⚠️ Your OpenAI API quota has been exceeded. "
                        "Please check your usage or upgrade your plan to continue using the AI Study Buddy."
                    )
                else:
                    st.error(f"⚠️ Something went wrong: {e}")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.markdown("Built on macOS using Streamlit and OpenAI")




