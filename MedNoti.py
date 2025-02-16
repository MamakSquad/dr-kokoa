##MediNoti.py##
import time
from datetime import datetime
from plyer import notification
from playsound import playsound
import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from Main import db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:/Users/iskan/OneDrive/Desktop/API KEYS/dr-kokua-firebase-adminsdk-fbsvc-b63dcc4b93.json")  # Replace with your service account key path
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

sound_file = r"C:\Users\iskan\OneDrive\Desktop\API KEYS\WhatsApp Audio 2025-02-15 at 00.03.08_c019a86b.mp3"
class NotiMed:
    

    def get_user_time():
        """Prompts the user to input a target time and validates it."""
        while True:
            user_input = input("Enter the target time (YYYY-MM-DD HH:MM): ")
            try:
                target_datetime = datetime.strptime(user_input, "%Y-%m-%d %H:%M")
                return target_datetime
            except ValueError:
                print("Invalid format! Please enter the time in 'YYYY-MM-DD HH:MM' format.")

    # Helper function to convert frequency to alarm times
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

    # Function to store alarms in Firestore
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
        print("Alarms saved to Firebase Firestore.")

    # Function to retrieve and show the user's current active alarms
    def get_active_alarms(user_uid):
        alarms_ref = db.collection("users").document(user_uid).collection("alarms")
        active_alarms = alarms_ref.where("status", "==", "active").stream()
        
        alarms = []
        for alarm in active_alarms:
            alarm_data = alarm.to_dict()
            alarms.append(alarm_data)
        
        return alarms


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

    # When the user chooses number 1 (View Running Alarm):
    
