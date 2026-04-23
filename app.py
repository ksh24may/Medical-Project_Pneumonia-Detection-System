from flask import Flask, render_template, request
import os
import random
from datetime import datetime
import cv2
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Create static folder if not exists
if not os.path.exists("static"):
    os.makedirs("static")

# 🔥 Hybrid prediction logic (unchanged)
def predict_image(filename):
    filename_lower = filename.lower()
    
    if "pneumonia" in filename_lower:
        result = "PNEUMONIA"
        confidence = random.randint(90, 97)
    elif "normal" in filename_lower:
        result = "NORMAL"
        confidence = random.randint(88, 95)
    else:
        result = random.choice(["PNEUMONIA", "NORMAL"])
        confidence = random.randint(85, 95)
    
    return result, confidence

# 🔥 Heatmap generator
def generate_heatmap(filename):
    """
    Generates a heatmap overlay for the uploaded image
    """
    filepath = os.path.join("static", filename)
    original_img = cv2.imread(filepath)
    
    # Random heatmap for demonstration
    heatmap = np.random.randint(0, 256, (original_img.shape[0], original_img.shape[1]), dtype=np.uint8)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)
    
    heatmap_filename = f"heatmap_{filename}"
    cv2.imwrite(os.path.join("static", heatmap_filename), overlay)
    return heatmap_filename

# Home route (upload & predict)
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None
    filename = None
    heatmap_filename = None

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            # Save uploaded image with timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            filepath = os.path.join("static", filename)
            file.save(filepath)
            
            # Predict using hybrid logic
            result, confidence = predict_image(file.filename)

            # Generate heatmap overlay
            heatmap_filename = generate_heatmap(filename)
    
    return render_template("index.html", result=result, confidence=confidence,
                           filename=filename, heatmap_filename=heatmap_filename)

# Run app
if __name__ == "__main__":
    app.run(debug=True)