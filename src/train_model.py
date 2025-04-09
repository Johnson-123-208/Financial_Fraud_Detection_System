import joblib
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
from imblearn.over_sampling import SMOTE
from src.data_preprocessing import preprocess_data

def train():
    X_train, X_test, y_train, y_test = preprocess_data("data/transactions.csv")

    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_train, y_train)

    clf1 = LogisticRegression(max_iter=1000)
    clf2 = XGBClassifier(use_label_encoder=False, eval_metric='logloss')

    ensemble = VotingClassifier(estimators=[
        ('lr', clf1),
        ('xgb', clf2)
    ], voting='soft')

    ensemble.fit(X_res, y_res)
    preds = ensemble.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, preds)

    print(f"AUC Score: {auc_score:.4f}")

    joblib.dump(ensemble, "models/model.pkl")

if __name__ == "__main__":
    train()
