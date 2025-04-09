import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

model = joblib.load("models/model.pkl")

def get_top_k_features(k=5):
    feature_importances = model.named_estimators_['xgb'].feature_importances_
    top_k_indices = np.argsort(feature_importances)[-k:][::-1]
    return top_k_indices

def score_partial_transaction(user_inputs, top_k_indices, default=0.0):
    full_input = [default] * 30  # Assuming 30 total features
    for idx, val in zip(top_k_indices, user_inputs):
        full_input[idx] = val

    # Dummy scaling (for demo only)
    dummy = np.random.rand(100, 30)
    scaler = StandardScaler().fit(dummy)
    scaled_input = scaler.transform([full_input])
    
    score = model.predict_proba(scaled_input)[0][1]
    return round(score, 4)
