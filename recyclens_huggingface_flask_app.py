from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
from ultralytics import YOLO
import requests
import io
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()
HF_API_KEY = os.getenv("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")

app = Flask(__name__)
CORS(app)

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Prompt templates for Hugging Face
PROMPT_TEMPLATES = {
    "bottle": "An eco-friendly reusable water bottle made of bamboo or glass",
    "bag": "A recycled cloth shopping bag placed on a white surface",
    "cup": "A biodegradable coffee cup made from recycled paper",
    "default": "An eco-friendly product made from sustainable materials"
}

SUGGESTION_DATA = {
    "bottle": [
        {
            "type": "eco_alternative",
            "text": "Switch to stainless steel bottles",
            "link": "https://www.ecobottles.in/products/stainless-steel-bottle"
        },
        {
            "type": "DIY",
            "text": "DIY Vertical Garden with old plastic bottles",
            "link": "https://www.youtube.com/watch?v=K2V0uwHkqFw"
        }
    ]
}

# Hugging Face image generation
def generate_image_huggingface(prompt, model="CompVis/stable-diffusion-v1-4"):
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    data = { "inputs": prompt }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # Encode to base64 so frontend can render it directly
            image_base64 = base64.b64encode(response.content).decode("utf-8")
            return f"data:image/png;base64,{image_base64}"
        else:
            print("Hugging Face error:", response.text)
    except Exception as e:
        print("Hugging Face exception:", e)
    return ""

def generate_prompt(prediction):
    return PROMPT_TEMPLATES.get(prediction, PROMPT_TEMPLATES["default"])

@app.route("/generate-image", methods=["POST"])
def generate_image_from_text():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt missing"}), 400

    image_data = generate_image_huggingface(prompt)
    return jsonify({"image": image_data})

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))
    results = model(image)

    labels = results[0].names
    classes = results[0].boxes.cls.tolist()
    prediction = labels[int(classes[0])] if classes else "Unknown"

    base_suggestions = SUGGESTION_DATA.get(prediction, [])
    enhanced_suggestions = []

    for suggestion in base_suggestions:
        suggestion["image"] = ""  # You can extend with SerpAPI fallback here
        enhanced_suggestions.append(suggestion)

    # Hugging Face image suggestion
    if prediction != "Unknown":
        prompt = generate_prompt(prediction)
        generated_image = generate_image_huggingface(prompt)
        ai_suggestion = {
            "type": "ai_generated",
            "text": prompt,
            "link": "",
            "image": generated_image
        }
        enhanced_suggestions.append(ai_suggestion)

    return jsonify({
        "prediction": prediction,
        "suggestions": enhanced_suggestions
    })

if __name__ == "__main__":
    app.run(port=5001)

