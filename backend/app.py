
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from bson import ObjectId
# auth functions
from auth import register_user, login_user

# mongodb collection
from database import analysis_collection

# gradio api client
from gradio_client import Client, handle_file


# -------------------------------
# CONFIG
# -------------------------------

# IMPORTANT: your current colab gradio link
GRADIO_URL = "https://538d5678e4a248946a.gradio.live"

# connect gradio api
client = Client(GRADIO_URL)


# flask setup
app = Flask(__name__)
CORS(app)


# -------------------------------
# HOME ROUTE
# -------------------------------

@app.route("/")
def home():
    return "Chest X Reasoner Backend Running"


# -------------------------------
# REGISTER ROUTE
# -------------------------------

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    result = register_user(
        data["name"],
        data["email"],
        data["password"]
    )

    return jsonify(result)


# -------------------------------
# LOGIN ROUTE
# -------------------------------

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    user_id = login_user(
        data["email"],
        data["password"]
    )

    if user_id:
        return jsonify({
            "message": "Login success",
            "user_id": user_id
        })

    return jsonify({
        "error": "Invalid credentials"
    }), 401

# -------------------------------
# HISTORY ROUTE
# -------------------------------

@app.route("/history/<user_id>", methods=["GET"])
def history(user_id):

    records = analysis_collection.find(
        {"user_id": user_id}
    ).sort("_id", -1)

    output = []

    for r in records:
        created_at = r.get("created_at")

        if created_at:
            created_str = created_at.strftime("%Y-%m-%d %H:%M")
        else:
            created_str = "Unknown date"

        output.append({
            "id": str(r["_id"]),
            "question": r.get("question", ""),
            "result": r.get("result", ""),
            "created_at": created_str
        })

    return jsonify(output)
# -------------------------------
# ANALYZE ROUTE
# -------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    print("ANALYZE ROUTE HIT")

    # check image
    if "image" not in request.files:
        return jsonify({
            "error": "No image uploaded"
        }), 400

    image = request.files["image"]

    question = request.form.get("question")
    user_id = request.form.get("user_id")

    if not question:
        return jsonify({
            "error": "Question missing"
        }), 400

    # temp image save
    temp_path = "temp_upload.png"
    image.save(temp_path)

    try:

        # send to colab gradio api
        result = client.predict(
            image=handle_file(temp_path),
            question=question,
            api_name="/predict"
        )

        # delete temp image
        os.remove(temp_path)

        # save in mongodb
        analysis_collection.insert_one({

            "user_id": user_id,
            "question": question,
            "result": result,
            "created_at": datetime.utcnow()

        })

        return jsonify({

            "message": "Analysis complete",
            "result": result

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# -------------------------------
# RUN APP
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)

