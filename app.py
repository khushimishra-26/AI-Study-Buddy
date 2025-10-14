import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit page configuration
st.set_page_config(page_title="🎓 AI Study Buddy", page_icon="📘", layout="wide")

st.title("🎓 AI-Powered Study Buddy")
st.markdown("Your personal AI companion for learning — explain, summarize, and quiz yourself easily!")

# Sidebar options
st.sidebar.title("🧭 Choose a Function")
option = st.sidebar.radio("Select an action:", ["Explain Topic", "Summarize Notes", "Generate Quiz"])

# User input
user_input = st.text_area("✏️ Enter your topic, notes, or text here:", height=200)

# Generate button
if st.button("🚀 Generate"):
    if not user_input.strip():
        st.warning("Please enter some text or topic first.")
    else:
        with st.spinner("AI is thinking... 💡"):
            if option == "Explain Topic":
                prompt = f"Explain the following topic in simple terms suitable for a student:\n\n{user_input}\n\nExplanation:"
            elif option == "Summarize Notes":
                prompt = f"Summarize the following notes clearly and concisely:\n\n{user_input}\n\nSummary:"
            else:
                prompt = f"Generate 5 multiple-choice quiz questions (with answers) from the following content:\n\n{user_input}\n\nQuiz:"

            response = client.chat.completions.create(
                model="gpt-4o-mini",  # You can use "gpt-4-turbo" if available
                messages=[
                    {"role": "system", "content": "You are an AI study assistant that helps students learn efficiently."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )

            output = response.choices[0].message.content.strip()
            st.success("✅ Done!")
            st.markdown("### 📘 Output:")
            st.write(output)

# Footer
st.markdown("---")
st.markdown("Built on macOS using Streamlit and OpenAI")
