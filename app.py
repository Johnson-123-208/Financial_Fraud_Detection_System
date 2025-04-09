import streamlit as st
import pandas as pd
import numpy as np
from src.real_time_scoring import get_top_k_features, score_partial_transaction
import plotly.express as px
from streamlit_lottie import st_lottie
import json

# ---------------------------- CONFIG ----------------------------
st.set_page_config(page_title="🔍 Fraud Detection", layout="wide")

# ---------------------------- LOAD LOTTIE ----------------------------
def load_lottie(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------- INIT SESSION ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------- HEADER ----------------------------
st.title("💳 Real-Time Financial Fraud Detection System")
st.markdown("Upload transactions or manually enter features to predict fraud risk with live voice output and animation.")

# ---------------------------- SIDEBAR CHATBOT ----------------------------
with st.sidebar:
    st.markdown("### 🤖 Fraud Assistant Chatbot")
    user_input = st.text_input("Ask something", key="chat_input")

    st.markdown("💡 **Suggestions:**")
    suggestions = [
        "What is fraud detection?",
        "How accurate is the model?",
        "Which features are important?",
        "How is risk calculated?",
        "What is AUC score?"
    ]
    for q in suggestions:
        if st.button(q):
            user_input = q

    if user_input:
        def get_bot_response(msg):
            msg = msg.lower()
            if "fraud" in msg:
                return "Fraud detection identifies suspicious transactions using machine learning models."
            elif "accurate" in msg or "performance" in msg:
                return "This system achieved over 96% AUC score for high fraud prediction accuracy."
            elif "feature" in msg:
                return "Top features are derived from PCA, representing transaction behavior and patterns."
            elif "risk" in msg:
                return "Risk is based on model output, higher score means higher fraud probability."
            elif "auc" in msg:
                return "AUC stands for Area Under Curve, a performance metric — higher means better."
            else:
                return "I'm here to help! Ask about fraud, accuracy, features, or model."

        bot_reply = get_bot_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_reply))

    for speaker, msg in st.session_state.chat_history[::-1][:6]:
        st.markdown(f"**{speaker}:** {msg}")

# ---------------------------- MAIN LAYOUT ----------------------------
left_col, right_col = st.columns([2, 1])

# ---------------------------- LEFT COLUMN ----------------------------
with left_col:
    st.subheader("📁 Upload CSV or ✍️ Manual Input (Top 5 Features)")
    uploaded_file = st.file_uploader("Upload a CSV with 30 features", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        scores = []
        for i, row in df.iterrows():
            full_input = row.to_numpy()
            score = score_partial_transaction(full_input, np.arange(30))
            scores.append(score)

        df["Fraud Probability"] = scores

        st.subheader("📊 Top 10 Fraud Predictions")
        fig = px.bar(df.head(10), x=df.index[:10], y="Fraud Probability", color="Fraud Probability",
                     color_continuous_scale="reds", title="Fraud Probability Scores")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    #st.header("✍️ Manual Input (Top 5 Features)")

    top_k_indices = get_top_k_features(k=5)
    user_inputs = []
    input_cols = st.columns(3)

    for i, idx in enumerate(top_k_indices):
        with input_cols[i % 3]:
            val = st.number_input(f"Feature {idx + 1}", value=0.0, format="%.4f")
            user_inputs.append(val)

    if st.button("🚨 Predict Fraud"):
        score = score_partial_transaction(user_inputs, top_k_indices)
        percentage = score * 100

        st.markdown("### 🔎 Prediction Result")
        st.success(f"Fraud Probability: **{percentage:.2f}%**")
        st.progress(score)

        speech_text = f"Fraud probability is {percentage:.2f} percent."
        if score > 0.5:
            st.error("⚠️ High risk of fraud detected!")
            speech_text += " Warning! High risk of fraud detected!"
        else:
            st.info("✅ This transaction looks safe.")

        # Store speech in session state
        st.session_state["prediction_score"] = score
        st.session_state["speech_text"] = speech_text
        

        # Web browser voice (JavaScript)
        st.markdown(f"""
        <script>
        const speak = (text) => {{
            let msg = new SpeechSynthesisUtterance();
            msg.text = text;
            msg.pitch = 1.2;
            msg.rate = 1;
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(v => v.name.includes("Female") || v.name.includes("Google UK English Female"));
            msg.voice = preferredVoice || voices[0];
            window.speechSynthesis.speak(msg);
        }};
        speak("{speech_text}");
        </script>
        """, unsafe_allow_html=True)

        # Local voice output (pyttsx3)
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)

            voices = engine.getProperty('voices')
            for voice in voices:
                if "female" in voice.name.lower() or "zira" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break

            engine.say(speech_text)
            engine.runAndWait()
        except Exception as e:
            st.warning(f"Local voice engine error: {e}")

# 🔁 Repeat Voice Button (after prediction)
if "speech_text" in st.session_state and st.button("🔁 Repeat Voice"):
    speech_text = st.session_state["speech_text"]

    # Repeat browser voice
    st.markdown(f"""
    <script>
    const speak = (text) => {{
        let msg = new SpeechSynthesisUtterance();
        msg.text = text;
        msg.pitch = 1.2;
        msg.rate = 1;
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.name.includes("Female") || v.name.includes("Google UK English Female"));
        msg.voice = preferredVoice || voices[0];
        window.speechSynthesis.speak(msg);
    }};
    speak("{speech_text}");
    </script>
    """, unsafe_allow_html=True)

    # Repeat local pyttsx3 voice
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.say(speech_text)
        engine.runAndWait()
    except Exception as e:
        st.warning(f"Local voice engine error: {e}")

# ---------------------------- RIGHT COLUMN ----------------------------
with right_col:
    # Load main Lottie animation
    main_anim = load_lottie("assets/fraud.json")
    st_lottie(main_anim, speed=1.2, height=350)

    # Add floating animation for prediction result
    if "prediction_score" in st.session_state:
        verdict_animation = "assets/danger.json" if st.session_state["prediction_score"] > 0.5 else "assets/safe.json"

        # Add CSS to position the animation top-right
        st.markdown("""
        <style>
        .floating-verdict {
            position: absolute;
            top: 20px;
            right: 30px;
            width: 200px;
            z-index: 999;
        }
        </style>
        """, unsafe_allow_html=True)

        # Render floating verdict animation
        st.markdown('<div class="floating-verdict" id="verdict-lottie"></div>', unsafe_allow_html=True)
        st_lottie(load_lottie(verdict_animation), speed=1, height=350, key="verdict-lottie")
