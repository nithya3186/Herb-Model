# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup
```bash
./setup.sh
```

### Step 2: Run
```bash
./run.sh
```

### Step 3: Use
Open your browser to: **http://localhost:8000**

---

## 📝 What You'll See

1. A beautiful web interface with a purple gradient background
2. An upload area where you can drag and drop or click to upload images
3. After uploading, click "Identify Herb" to get predictions
4. Results will show:
   - The identified herb/plant name
   - Confidence score
   - Preview of your uploaded image

---

## 🌿 Supported Plants

The system can identify **92 different herb and plant species** including:
- Tulsi (Holy Basil)
- Neem
- Aloe Vera
- Turmeric
- Ginger
- Mint
- Basil
- Coriander
- And 85 more!

---

## 🔧 Troubleshooting

### If setup.sh fails:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### If run.sh fails:
```bash
source venv/bin/activate
python app.py
```

### Port already in use:
Edit `app.py` and change the port number in the last line:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000 to 8001
```

---

## 📊 Model Performance

- **Accuracy**: 95.92%
- **Model**: EfficientNetV2B3 + PCA + SVM
- **Input Size**: 300x300 pixels
- **Supported Formats**: JPG, PNG, JPEG

---

## 🎯 Tips for Best Results

1. Use clear, well-lit images
2. Focus on the leaves or distinctive parts of the plant
3. Avoid blurry or dark images
4. Single plant per image works best
5. Image size should be reasonable (under 10MB)

---

## 📞 Need Help?

Check the full README.md for detailed documentation and API endpoints.
