from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import os
import mlflow
from mlflow.sklearn import load_model

app = Flask(__name__)

# Use the Mongo URI from environment variable
mongo_uri = os.environ.get("MONGO_URI", "mongodb://172.22.160.1:27017/flaskdb")
client = MongoClient(mongo_uri)
db = client["flaskdb"]
collection = db["students"]

# Load the model using run_id
# mlflow.set_tracking_uri("http://localhost:5000")
# model_uri = f"runs:/d6b62a54ef8745f7a2de131497f53c66/logistic_model"
# lr_model = load_model(model_uri)

@app.route('/')
def index():
    students = list(collection.find({}, {"_id": 0}))
    return render_template('index.html', students=students)

@app.route('/predict', methods=['POST'])
def predict_pass():
    data = request.get_json()  # Get JSON body

    try:
        # validate and convert to python floats
        study_hours = float(data.get('study_hours'))
        sleep_hours = float(data.get('sleep_hours'))

        # model expects 2D array
        X = [[study_hours, sleep_hours]]

        # get prediction (numpy array) and probability
        pred_array = lr_model.predict(X)
        prob_array = lr_model.predict_proba(X)[:, 1]

        # Change data for storing
        pred = int(pred_array[0])                   # 0 or 1 as int
        prob = float(prob_array[0])                 # probability as float
        pred_label = ["Fail", "Pass"][pred]         # or use "passed" / "failed" string]

        print(pred, prob, pred_label)
        
        # build document to save on mongodb
        doc = {
            "study_hours": study_hours,
            "sleep_hours": sleep_hours,
            "prediction": pred_label,
            "prediction_int": pred,
            "probability": prob
        }
        # Making Prediction
        print(pred)
        collection.insert_one(doc)
        return jsonify({"message": f"Student prediction added successfully as {pred}!"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error: {e}"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
