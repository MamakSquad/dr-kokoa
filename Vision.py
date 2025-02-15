import os
import json
from google.cloud import vision
from google.oauth2 import service_account
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialize Google Vision Client
class VisionAPI:
    def __init__(self):
        # Load credentials from file
        credential_path = "./vision_key.json"
        with open(credential_path, "r") as cred_file:
            credentials_json = json.load(cred_file)

        # Authenticate using the loaded credentials
        credentials = service_account.Credentials.from_service_account_info(credentials_json)
        self.client = vision.ImageAnnotatorClient(credentials=credentials)

    def detect_text(self, image_path: str) -> str:
        """Detects and extracts text from an image using Google Cloud Vision API."""
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(f"Error: {response.error.message}")

        return response.text_annotations[0].description if response.text_annotations else ""

    def extract_info(self, text: str):
        """Extracts patient name, medicine name, amount, frequency, and description from text."""
        extracted_info = {
            "patient_name": None,
            "medicine_name": None,
            "amount": None,
            "frequency": None,
            "description": ""
        }

        lines = text.split("\n")

        for i, line in enumerate(lines):
            line = line.strip().lower()

            # Detect patient name (assumption: it starts with "Patient:" or similar keywords)
            if "patient" in line or "name" in line:
                extracted_info["patient_name"] = line.split(":")[-1].strip()
            
            # Detect medicine name (assumption: it contains 'mg', 'tablet', or 'capsule')
            elif "mg" in line or "tablet" in line or "capsule" in line:
                extracted_info["medicine_name"] = line.strip()

            # Detect amount and frequency (e.g., "Ambil 2 biji 3 kali sehari")
            elif "ambil" in line and "biji" in line:
                words = line.split()
                extracted_info["amount"] = words[words.index("biji") - 1]  # Extract amount
                extracted_info["frequency"] = " ".join(words[words.index("biji") + 1:])  # Extract frequency

            # Detect description: Combine relevant lines
            elif "sebelum" in line or "selepas" in line:
                extracted_info["description"] = line.strip()  # Set description

        return extracted_info["patient_name"], extracted_info["medicine_name"], extracted_info["amount"], extracted_info["frequency"], extracted_info["description"]

# Create VisionAPI instance
vision_api = VisionAPI()

@app.route('/detect', methods=['POST'])
def detect_text_endpoint():
    # Get the image file from the request
    image = request.files['image']  # Assuming the image is sent in a multipart form-data

    # Save the image temporarily to process
    image_path = 'temp_image.jpg'
    image.save(image_path)

    try:
        # Call the detect_text function
        text = vision_api.detect_text(image_path)
        patient_name, medicine_name, amount, frequency, description = vision_api.extract_info(text)

        # Return the extracted information as JSON
        return jsonify({
            "patient_name": patient_name,
            "medicine_name": medicine_name,
            "amount": amount,
            "frequency": frequency,
            "description": description
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0')
