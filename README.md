# 💳 Financial Fraud Detection System

An intelligent Machine Learning-powered app to **detect fraudulent financial transactions** using real-time inputs and batch CSV predictions. Designed with an engaging UI, voice assistant, Lottie animations, and chatbot support for explanation and guidance.

---

## 🔍 Features

✅ ML Model with **96% AUC Score**  
✅ Real-time **manual transaction input**  
✅ **Batch prediction** from uploaded CSV  
✅ Fraud probability **bar chart visualization**  
✅ 🎥 Dynamic **animations** (safe/risk prediction)  
✅ 🎙️ **Voice output** (female assistant reads result aloud)  
✅ 🤖 **Chatbot** for user queries and explanation  
✅ Clean, colorful layout with sidebar assistant

---

## 🚀 Getting Started

### Download the Dataset From Kaggle [https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud]

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/financial-fraud-detection.git
cd financial-fraud-detection
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run streamlit_app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧠 How It Works

- Uses a trained **XGBoost model** with imbalanced-learn strategies
- Allows **manual input** for top features using Streamlit UI
- Allows **CSV file upload** for batch predictions
- Applies any preprocessing like **PCA** or **standardization**
- Displays a **fraud probability bar graph**
- Voice output with **sweet female voice** reads prediction aloud
- **Lottie animations** show fraud/safe result
- Includes a sidebar **chatbot** with preset user queries

---

## 📁 Project Structure

```
.
├── streamlit_app.py               # Main Streamlit application
├── models/
│   ├── fraud_model.pkl            # Trained machine learning model
├── src/
│   └── real_time_scoring.py       # Partial scoring logic
├── assets/
│   ├── fraud.json                 # Main UI animation
│   ├── danger.json                # Animation for risky prediction
│   └── safe.json                  # Animation for safe prediction
├── requirements.txt               # Python dependencies
└── README.md
```

---

## 🗂️ CSV Format for Upload

- Your CSV must contain **exactly 30 numeric features** with no headers.
- Example (single row):

```csv
0.021,0.112,0.513,0.009,... (total 30 features)
```

---

## 🤖 Chatbot Suggestions

You can ask the chatbot:

- 💬 *What is fraud detection?*  
- 💬 *How accurate is this model?*  
- 💬 *Which features are most important?*  
- 💬 *How is fraud risk calculated?*

---

## 🧑‍💻 Author

**Developed by:** *[Johnson Obhalloju]*  
**Role:** AI/ML Engineer & Aspiring Data Scientist  
**Email:** [obhallojujohnson@gmail.com]
---

## 📌 Future Enhancements

- 🌐 Deploy to **Render or Vercel**
- 🔒 Add **user authentication**
- 📈 Add **dashboard with fraud insights**
- 📱 Make layout **mobile-responsive**

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and build upon it!

---
```
