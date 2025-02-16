import firebase_admin
from firebase_admin import credentials, auth, firestore
import uuid
import requests

# Initialize Firebase only once
cred = credentials.Certificate("C:/Users/iskan/OneDrive/Desktop/API KEYS/dr-kokua-firebase-adminsdk-fbsvc-b63dcc4b93.json")

# Check if Firebase is already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.get_app()  # Use the already initialized app if it exists

# Initialize Firestore client
db = firestore.client()
FIREBASE_WEB_API_KEY = "AIzaSyDk3xnBChVjyUgKAaVf74LB6twVyrwdcbs"

class UserLogin:
    def register_user(email, password, phone_number):
        """Registers a new user in Firebase Authentication and Firestore."""
        try:
            user_record = auth.create_user(email=email, password=password, phone_number=phone_number)
            uid = user_record.uid  # Firebase UID

            # Generate a unique family token
            family_token = str(uuid.uuid4())

            # Store user details in Firestore
            user_data = {
                "uid": uid,
                "email": email,
                "phone_number": phone_number,
                "family_token": family_token,
                "linked_users": []
            }
            db.collection("users").document(uid).set(user_data)

            return {
                "message": "User registered successfully!",
                "user_id": uid,
                "family_link": f"http://yourapp.com/join/{family_token}"
            }

        except Exception as e:
            return {"error": str(e)}

    def login_user(email, password):
        """Authenticates user via Firebase Authentication REST API"""
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            data = response.json()

            if "error" in data:
                return {"error": data["error"]["message"]}

            return {
                "message": "Login successful",
                "user_id": data["localId"],
                "id_token": data["idToken"]
            }

        except Exception as e:
            return {"error": str(e)}

    def join_family(family_token, new_user_uid):
        """Allows a user to join a family using the provided family token."""
        try:
            # Find the user with the given family token
            users_ref = db.collection("users")
            query = users_ref.where("family_token", "==", family_token).limit(1)
            results = query.stream()

            family_owner = None
            for doc in results:
                family_owner = doc
                break

            if not family_owner:
                return {"error": "Invalid family token"}

            # Update the linked users list
            owner_uid = family_owner.id
            owner_data = family_owner.to_dict()

            linked_users = owner_data.get("linked_users", [])
            if new_user_uid in linked_users:
                return {"error": "User is already in this family"}

            linked_users.append(new_user_uid)

            # Update Firestore with the new linked users
            users_ref.document(owner_uid).update({"linked_users": linked_users})

            return {"message": "User successfully joined the family"}

        except Exception as e:
            return {"error": str(e)}
pass
