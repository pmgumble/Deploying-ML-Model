from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)
cv = pickle.load(open("models/cv.pkl","rb"))
clf = pickle.load(open("models/clf.pkl","rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        email = request.form.get('content')
    tokenized_email = cv.transform([email]) # X 
    prediction = clf.predict(tokenized_email)
    prediction = 1 if prediction == 1 else -1
    return render_template("index.html", prediction=prediction, email=email)


@app.route('/api/predict', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)  # Get data posted as a json
    email = data['content']
    tokenized_email = cv.transform([email]) # X 
    prediction = clf.predict(tokenized_email)
    # If the email is spam prediction should be 1
    prediction = 1 if prediction == 1 else -1
    return jsonify({'prediction': prediction, 'email': email})  # Return prediction



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)