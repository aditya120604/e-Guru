import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Secure API key access
api_key = st.secrets["GEMINI_API_KEY"]

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0.7
)

# Language greetings
greetings = {
    "english": "Hello! I am your AI Tutor.",
    "hindi": "नमस्ते! मैं आपका एआई ट्यूटर हूँ।",
    "gujarati": "હેલો! હું તમારો એઆઇ ટ્યુટર છું.",
    "marathi": "नमस्कार! मी तुमचा AI शिक्षक आहे.",
    "tamil": "வணக்கம்! நான் உங்கள் AI டுடார்.",
    "telugu": "హలో! నేను మీ AI ట్యూటర్‌ని.",
    "bengali": "হ্যালো! আমি তোমার AI শিক্ষক।",
    "kannada": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ AI ಟ್ಯೂಟರ್.",
    "malayalam": "ഹലോ! ഞാൻ നിങ്ങളുടെ AI ട്യൂട്ടറാണ്.",
    "odia": "ନମସ୍କାର! ମୁଁ ତୁମର AI ଶିକ୍ଷକ ଅଛି।"
}

# Page config
st.set_page_config(page_title="e-Guru", page_icon="🧠")
st.markdown("""
# 🧠 e-Guru  
#### *Your Digital Guide to Smarter Learning*
""")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "selected_q" not in st.session_state:
    st.session_state.selected_q = None

# Sidebar: History and Clear Button
with st.sidebar:
    st.header("📚 Conversation History")

    if st.session_state.history:
        for i, qa in enumerate(st.session_state.history):
            if st.button(f"Q{i+1}: {qa['question'][:30]}...", key=f"q{i}"):
                st.session_state.selected_q = i
        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.session_state.selected_q = None
    else:
        st.markdown("_No questions asked yet._")

# Language selection
language = st.selectbox("Select your language:", list(greetings.keys()), format_func=str.capitalize)

# Greeting
st.markdown(f"### {greetings[language]}")

# User inputs
name = st.text_input("Enter your name:")
grade = st.text_input("Which grade are you studying in?")
question = st.text_area("Ask your academic doubt here:")

# Ask button
if st.button("Ask"):
    if not all([name, grade, question]):
        st.warning("Please fill all the fields.")
    else:
        system_prompt = (
            f"You are an AI tutor helping a grade {grade} student named {name}. "
            f"Explain clearly and respond in {language.capitalize()} language."
        )
        full_prompt = f"{system_prompt}\n\nStudent's Question: {question}"
        response = llm.invoke(full_prompt)
        answer = response.content

        # Store response in history and show
        st.session_state.history.append({"question": question, "answer": answer})
        st.session_state.selected_q = len(st.session_state.history) - 1

# Show selected Q&A
if st.session_state.selected_q is not None:
    selected = st.session_state.history[st.session_state.selected_q]
    st.markdown("## 📖 Selected Q&A")
    st.markdown(f"**Question:** {selected['question']}")
    st.markdown(f"**Answer:** {selected['answer']}")

