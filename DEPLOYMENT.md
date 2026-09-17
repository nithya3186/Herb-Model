# Deployment Guide

This guide covers multiple deployment options for the Herb Identification System.

---

## 🚀 Quick Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Pros**: Free tier, easy setup, automatic deployments from GitHub  
**Cons**: Model files are large (may need to use external storage)

#### Steps:

1. **Create a `render.yaml` file** (already included in repo)

2. **Sign up at [Render.com](https://render.com)**

3. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select `Charan512/HerbIdentificationModel`
   - Configure:
     - **Name**: herb-identification
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free (or paid for better performance)

4. **Deploy!** Render will automatically deploy your app

**Note**: Due to large model files (100MB+), you may need to:
- Use Render's paid tier for more storage
- Or store models in cloud storage (S3, Google Cloud Storage)

---

### Option 2: Hugging Face Spaces (Recommended for ML Apps)

**Pros**: Free, designed for ML models, generous storage  
**Cons**: Requires converting to Gradio/Streamlit format

#### Steps:

1. **Create a Hugging Face account** at [huggingface.co](https://huggingface.co)

2. **Create a new Space**:
   - Go to Spaces → Create new Space
   - Choose "Gradio" or "Streamlit"
   - Name it "herb-identification"

3. **Convert the app** (I can help with this - see Option 2A below)

4. **Push your code** to the Space repository

---

### Option 3: Railway (Easy Deployment)

**Pros**: Easy setup, free tier, automatic deployments  
**Cons**: Free tier has limitations

#### Steps:

1. **Sign up at [Railway.app](https://railway.app)**

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Charan512/HerbIdentificationModel`

3. **Configure**:
   - Railway auto-detects Python
   - Add environment variables if needed
   - Deploy!

4. **Access your app** at the provided Railway URL

---

### Option 4: Google Cloud Run (Scalable)

**Pros**: Scales automatically, pay-per-use, generous free tier  
**Cons**: Requires Docker knowledge

#### Steps:

1. **Install Google Cloud SDK**:
   ```bash
   # Install gcloud CLI
   curl https://sdk.cloud.google.com | bash
   ```

2. **Create a Dockerfile** (already included)

3. **Build and deploy**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/herb-identification
   gcloud run deploy herb-identification --image gcr.io/YOUR_PROJECT_ID/herb-identification --platform managed
   ```

---

### Option 5: AWS EC2 (Full Control)

**Pros**: Full control, scalable  
**Cons**: More complex, requires server management

#### Steps:

1. **Launch EC2 Instance**:
   - Ubuntu 22.04 LTS
   - t2.medium or larger (for model loading)
   - Open port 8000

2. **SSH into instance and setup**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3-pip python3-venv -y
   
   # Clone repository
   git clone https://github.com/Charan512/HerbIdentificationModel.git
   cd HerbIdentificationModel
   
   # Run setup
   ./setup.sh
   
   # Install PM2 for process management
   sudo npm install -g pm2
   
   # Start app with PM2
   pm2 start "python3 app.py" --name herb-identification
   pm2 save
   pm2 startup
   ```

3. **Configure domain** (optional):
   - Point your domain to EC2 IP
   - Set up Nginx as reverse proxy
   - Add SSL with Let's Encrypt

---

### Option 6: Heroku (Classic Option)

**Pros**: Easy deployment, well-documented  
**Cons**: No free tier anymore, can be expensive

#### Steps:

1. **Install Heroku CLI**:
   ```bash
   brew install heroku/brew/heroku
   ```

2. **Create Heroku app**:
   ```bash
   heroku login
   heroku create herb-identification
   ```

3. **Add Procfile** (already included)

4. **Deploy**:
   ```bash
   git push heroku main
   ```

---

## 📦 Handling Large Model Files

Since your model files are large (100MB+), here are solutions:

### Option A: Git LFS (Large File Storage)

```bash
# Install Git LFS
brew install git-lfs
git lfs install

# Track large files
git lfs track "*.keras"
git lfs track "*.pkl"

# Add and commit
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

### Option B: Cloud Storage

Store models in S3/Google Cloud Storage and download on startup:

```python
# Add to app.py
import boto3
import os

def download_models():
    if not os.path.exists('feature_extractor.keras'):
        s3 = boto3.client('s3')
        s3.download_file('your-bucket', 'models/feature_extractor.keras', 'feature_extractor.keras')
        # Download other models...

download_models()
```

---

## 🔧 Production Optimizations

### 1. Use Gunicorn (Production WSGI Server)

Update `requirements.txt`:
```
gunicorn==21.2.0
```

Update start command:
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 2. Add Health Checks

Already included in `app.py`:
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": True}
```

### 3. Enable CORS (Already Done)

### 4. Add Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 5. Environment Variables

Create `.env` file:
```
PORT=8000
DEBUG=False
MODEL_PATH=./models
```

---

## 🎯 Recommended Deployment Path

**For Quick Demo**: Use **Render** or **Railway**  
**For ML-Specific**: Use **Hugging Face Spaces**  
**For Production**: Use **Google Cloud Run** or **AWS EC2**

---

## 📝 Next Steps After Deployment

1. **Test the deployed app** thoroughly
2. **Monitor performance** and errors
3. **Set up analytics** (optional)
4. **Configure custom domain** (optional)
5. **Add authentication** if needed (optional)

---

## 🆘 Need Help?

- Check deployment logs for errors
- Ensure all model files are accessible
- Verify environment variables are set
- Test locally first with `./run.sh`

---

## 📊 Cost Estimates

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Render | 750 hrs/month | $7/month |
| Railway | $5 credit/month | Pay-as-you-go |
| Hugging Face | Unlimited | Free for public |
| Google Cloud Run | 2M requests/month | Pay-per-use |
| AWS EC2 | 750 hrs/month (1 year) | ~$10-50/month |

---

Would you like me to help you with a specific deployment option?
