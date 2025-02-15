# HealthGPS
import geocoder
import googlemaps
import webbrowser
from HealthGPS import HealthNavi

# MedNoti
import time
from datetime import datetime
from plyer import notification
from playsound import playsound
from MedNoti import NotiMed

# UserAuth
import firebase_admin
from firebase_admin import credentials, auth, firestore
import uuid
import requests
from UserAuth import UserLogin

# Vision
import os
import json
from google.cloud import vision
from google.oauth2 import service_account
from Vision import VisionAPI


# Flask
from flask import Flask, jsonify, request

# Firebase Initialize
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/iskan/OneDrive/Desktop/API KEYS/dr-kokua-firebase-adminsdk-fbsvc-b63dcc4b93.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize Flask app
app = Flask(__name__)

# Set Firebase API Key (Ensure this is securely stored in env variables)
FIREBASE_WEB_API_KEY = "AIzaSyDk3xnBChVjyUgKAaVf74LB6twVyrwdcbs"

# Initialize Vision API
vision_api = VisionAPI()

# -------------------------- HealthGPS --------------------------

@app.route("/get-location", methods=["GET"])
def get_location():
    health_navi = HealthNavi()
    lat, lng = health_navi.get_location()

    if lat is None or lng is None:
        return jsonify({"error": "Unable to retrieve location"}), 400

    return jsonify({"latitude": lat, "longitude": lng})

@app.route("/find-healthcare", methods=["GET"])
def find_healthcare():
    health_navi = HealthNavi()
    lat, lng, healthcare_list = health_navi.find_nearest_healthcare()

    if not healthcare_list:
        return jsonify({"error": "No healthcare providers found nearby"}), 404

    healthcare_data = [
        {"name": place[0], "address": place[1], "latitude": place[2], "longitude": place[3]}
        for place in healthcare_list
    ]

    return jsonify({
        "user_location": {"latitude": lat, "longitude": lng},
        "healthcare_providers": healthcare_data
    })

@app.route("/navigate-to-healthcare", methods=["POST"])
def navigate_to_healthcare():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    user_lat = data.get("user_lat")
    user_lng = data.get("user_lng")
    dest_lat = data.get("dest_lat")
    dest_lng = data.get("dest_lng")

    if not all([user_lat, user_lng, dest_lat, dest_lng]):
        return jsonify({"error": "Missing required fields"}), 400

    health_navi = HealthNavi()
    health_navi.launch_navigation(user_lat, user_lng, dest_lat, dest_lng)

    return jsonify({"message": "Navigating to healthcare provider..."})

# -------------------------- MedNoti --------------------------

def get_alarm_times(frequency):
    return ["08:00", "14:00", "20:00"]  # Example times

def save_alarms_to_db(user_uid, medicine_name, amount, description, alarm_times):
    db.collection("users").document(user_uid).collection("alarms").add({
        "medicine_name": medicine_name,
        "amount": amount,
        "description": description,
        "alarm_times": alarm_times,
        "status": "active"
    })

def check_time(alarm_time, medicine_name, amount, description):
    print(f"Alarm set for {alarm_time} - {medicine_name} ({amount}) {description}")

@app.route('/set-alarm', methods=['POST'])
def set_alarm():
    data = request.get_json()
    user_uid = data.get("user_uid")
    medicine_name = data.get("medicine_name")
    amount = data.get("amount")
    description = data.get("description")
    frequency = data.get("frequency")

    if not all([user_uid, medicine_name, amount, description, frequency]):
        return jsonify({"error": "Missing required fields"}), 400

    alarm_times = get_alarm_times(frequency)

    for time_str in alarm_times:
        alarm_time = datetime.strptime(time_str, "%H:%M").replace(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
        )
        save_alarms_to_db(user_uid, medicine_name, amount, description, alarm_times)
        check_time(alarm_time, medicine_name, amount, description)

    return jsonify({"message": "Alarms set successfully."})

# -------------------------- UserAuth --------------------------

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    phone_number = data.get("phone_number")

    if not all([email, password, phone_number]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        user_record = auth.create_user(email=email, password=password, phone_number=phone_number)
        uid = user_record.uid
        family_token = str(uuid.uuid4())

        db.collection("users").document(uid).set({
            "uid": uid,
            "email": email,
            "phone_number": phone_number,
            "family_token": family_token,
            "linked_users": []
        })

        return jsonify({
            "message": "User registered successfully!",
            "user_id": uid,
            "family_link": f"http://yourapp.com/join/{family_token}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        response = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
        data = response.json()

        if "error" in data:
            return jsonify({"error": data["error"]["message"]}), 400

        return jsonify({"message": "Login successful", "user_id": data["localId"], "id_token": data["idToken"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------------- Vision --------------------------

@app.route("/detect-text", methods=["POST"])
def detect_text():
    data = request.get_json()
    user_uid = data.get("user_uid")
    image_path = data.get("image_path")

    if not all([user_uid, image_path]) or not os.path.exists(image_path):
        return jsonify({"error": "Invalid user UID or image path"}), 400

    try:
        detected_texts = vision_api.detect_text(image_path)
        patient_name, medicine_name, amount, frequency, description = vision_api.extract_info(detected_texts)

        db.collection("users").document(user_uid).collection("medication_records").add({
            "patient_name": patient_name,
            "medicine_name": medicine_name,
            "amount": amount,
            "frequency": frequency,
            "description": description,
            "image_path": image_path
        })

        return jsonify({"message": "Text detected and data stored successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
