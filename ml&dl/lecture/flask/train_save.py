# train_and_save.py
# Trains a tiny scikit-learn model and writes model.pkl using joblib.dump
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

# 1) prepare data
X, y = load_iris(return_X_y=True)
# 2) build pipeline (scaler + classifier). Pipeline ensures preprocessing is saved with model.
model = Pipeline([
    ("scaler", StandardScaler()),       # Standardize features (important for many models)
    ("clf", LogisticRegression(max_iter=200))
])

# 3) fit model (learn weights)
model.fit(X, y)

# 4) save to disk with joblib
# joblib.dump serializes Python objects efficiently (optimized for numpy arrays).
joblib.dump(model, "model.pkl")
print("model.pkl saved (joblib.dump)")
