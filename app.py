from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
import pickle
import json
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
from PIL import Image
import io
import os

# Initialize FastAPI app
app = FastAPI(title="Herb Identification API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the models and class names
print("Loading models...")
feature_extractor = tf.keras.models.load_model('feature_extractor.keras')
with open('pca.pkl', 'rb') as f:
    pca = pickle.load(f)
with open('svm_model.pkl', 'rb') as f:
    svm_model = pickle.load(f)
with open('class_names.json', 'r') as f:
    class_names = json.load(f)
print("Models loaded successfully!")

IMG_SIZE = (300, 300)

def classify_image(img_bytes):
    """
    Classify an image using the loaded models
    """
    try:
        # Load and preprocess image
        img = Image.open(io.BytesIO(img_bytes))
        img = img.convert('RGB')
        img = img.resize(IMG_SIZE)
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Extract features
        features = feature_extractor.predict(img_array, verbose=0)
        
        # Apply PCA
        flat_pca = pca.transform(features)
        
        # Predict
        pred = svm_model.predict(flat_pca)[0]
        
        # Get prediction probabilities (if available)
        try:
            probabilities = svm_model.decision_function(flat_pca)[0]
            # Normalize to get confidence scores
            confidence = float(np.max(probabilities))
        except:
            confidence = 1.0
        
        return {
            "prediction": class_names[pred],
            "class_index": int(pred),
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the main HTML page
    """
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict the herb/plant species from an uploaded image
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read image bytes
    img_bytes = await file.read()
    
    # Classify image
    result = classify_image(img_bytes)
    
    return JSONResponse(content=result)

@app.get("/classes")
async def get_classes():
    """
    Get list of all available classes
    """
    return JSONResponse(content={"classes": class_names, "total": len(class_names)})

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "models_loaded": True}

# Mount static files
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
