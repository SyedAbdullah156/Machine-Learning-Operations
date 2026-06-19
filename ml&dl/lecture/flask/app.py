# app.py
from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# 1) Load model at startup (one-time). This avoids reloading from disk per-request.
# joblib.load returns the same Pipeline object we saved earlier.
MODEL = joblib.load("model.pkl")   # <-- joblib.load deserializes model.pkl

@app.route("/") 
def index():
    # render a simple HTML form (templates/index.html)
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # 2) Read form inputs (strings) and convert to floats for the model.
    # The Iris model expects 4 numeric features in the same order used during training.
    try:
        f1 = float(request.form["f1"])
        f2 = float(request.form["f2"])
        f3 = float(request.form["f3"])
        f4 = float(request.form["f4"])
    except Exception as e:
        return f"Invalid input: {e}", 400

    # 3) Prepare 2D array (n_samples, n_features) as sklearn expects
    X = np.array([[f1, f2, f3, f4]], dtype=float)

    # 4) Use loaded model to predict (model includes scaler so we can feed raw features)
    pred_class = int(MODEL.predict(X)[0])
    # Optionally get probabilities if classifier supports it
    proba = None
    if hasattr(MODEL, "predict_proba"):
        proba = MODEL.predict_proba(X)[0].tolist()

    # 5) Render result page with prediction
    return render_template("result.html", pred=pred_class, proba=proba)

if __name__ == "__main__":
    app.run(debug=True)
