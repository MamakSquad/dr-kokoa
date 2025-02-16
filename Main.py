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
import sys
sound_file = r"C:\Users\iskan\OneDrive\Desktop\API KEYS\WhatsApp Audio 2025-02-15 at 00.03.08_c019a86b.mp3"

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
Vision_API_KEY = "AIzaSyC2KPlLyT24z1HObpzeL69_NCSIwC1aU5U"
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
        alarm_times = []

        # If the frequency mentions "pagi", set alarm at 9 AM
        if 'pagi' in frequency:
            alarm_times.append("09:00")
        
        # If the frequency mentions "tengah hari", set alarm at 12 PM
        if 'tengah hari' in frequency or '1 kali' in frequency:
            alarm_times.append("12:00")
        
        # If the frequency mentions "petang", set alarm at 4 PM
        if 'petang' in frequency or '3 kali' in frequency:
            alarm_times.append("16:00")
        
        # If the frequency mentions "malam", set alarm at 9 PM
        if 'malam' in frequency or '2 kali' in frequency or '4 kali' in frequency:
            alarm_times.append("21:00")
        
        return alarm_times

def save_alarms_to_db(user_uid, medicine_name, amount, description, alarm_times):
        # Save alarm information to Firestore
        doc_ref = db.collection("users").document(user_uid).collection("alarms").document()
        doc_ref.set({
            "medicine_name": medicine_name,
            "amount": amount,
            "description": description,
            "alarm_times": alarm_times,
            "status": "active"  # Track the alarm status (active or inactive)
        })
def check_time(target_datetime, medicine_name, amount, description):
        """Waits until the target time and then sends a notification + plays sound."""
        print(f"Waiting for {target_datetime}...")

        while True:
            current_time = datetime.now()
            print(f"Current time: {current_time}", end="\r")  

            if current_time >= target_datetime:
                print(f"\nAlert! It's time: {current_time}")
                
                # Show desktop notification
                try:
                    notification.notify(
                        title=f"Time for {medicine_name}",
                        message=f"Take {amount} of {medicine_name} ({description}) at {current_time.strftime('%Y-%m-%d %H:%M')}",
                        timeout=10
                    )
                    print("Notification sent!")
                except Exception as e:
                    print(f"Error sending notification: {e}")

                # Play sound
                if os.path.exists(sound_file):
                    try:
                        playsound(sound_file)
                        print("Sound played successfully!")
                    except Exception as e:
                        print(f"Error playing sound: {e}")
                        if sys.platform.startswith("win"):
                            import winsound
                            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
                            print("Played sound using winsound (Windows only).")
                else:
                    print(f"Sound file not found: {sound_file}")

                break  

            time.sleep(1) 

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

@app.route('/view-alarms', methods=['GET'])
def view_alarms():
    user_uid = request.args.get("user_uid")

    if not user_uid:
        return jsonify({"error": "Missing user UID"}), 400

    active_alarms = NotiMed.get_active_alarms(user_uid)

    if not active_alarms:
        return jsonify({"message": "No active alarms found."})

    return jsonify({"active_alarms": active_alarms})

@app.route('/check-alarm', methods=['POST'])
def check_alarm():
    data = request.get_json()
    user_uid = data.get("user_uid")
    medicine_name = data.get("medicine_name")
    target_time = data.get("target_time")  # Expected format: "HH:MM"

    if not all([user_uid, medicine_name, target_time]):
        return jsonify({"error": "Missing required fields"}), 400

    alarm_time = datetime.strptime(target_time, "%H:%M").replace(
        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
    )

    NotiMed.check_time(alarm_time, medicine_name, "1 dose", "Take with water")

    return jsonify({"message": f"Checked alarm for {medicine_name} at {target_time}."})

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
pass

if __name__ == "__main__":
    app.run(host="0.0.0.0")
