import os
import json
from google.cloud import vision
from google.oauth2 import service_account
from flask import Flask, jsonify, request

# Initialize Google Vision Client
class VisionAPI:
   
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

        for line in lines:
            line = line.strip().lower()

            # Detect patient name
            if "patient" in line or "name" in line:
                extracted_info["patient_name"] = line.split(":")[-1].strip()
            
            # Detect medicine name
            elif "mg" in line or "tablet" in line or "capsule" in line:
                extracted_info["medicine_name"] = line.strip()

            # Detect amount and frequency
            elif "ambil" in line and "biji" in line:
                words = line.split()
                extracted_info["amount"] = words[words.index("biji") - 1]  # Extract amount
                extracted_info["frequency"] = " ".join(words[words.index("biji") + 1:])  # Extract frequency

            # Detect description
            elif "sebelum" in line or "selepas" in line:
                extracted_info["description"] = line.strip()

        return extracted_info
pass


