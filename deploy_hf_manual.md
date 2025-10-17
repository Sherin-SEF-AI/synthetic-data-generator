# 🚀 Manual Hugging Face Spaces Deployment

## Quick Deployment Steps

### Step 1: Create Space on Hugging Face
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in:
   - **Space name**: `synthetic-data-generator`
   - **License**: Apache 2.0
   - **SDK**: Gradio
   - **Hardware**: CPU Basic
   - **Visibility**: Public

### Step 2: Upload Files
Upload these files from your GitHub repository:

#### Required Files:
- `app.py` - Main application
- `requirements.txt` - Dependencies
- `README.md` - Documentation

#### Required Folders:
- `generators/` - All Python files
- `privacy/` - All Python files
- `templates/` - All Python files
- `utils/` - All Python files
- `assets/` - Example files

### Step 3: Configure Space
- Set app file to `app.py`
- The space will automatically build and deploy

### Step 4: Test Your App
- Wait for build to complete
- Test all features
- Your app will be live at: `https://huggingface.co/spaces/your-username/synthetic-data-generator`

## Alternative: Git Method (if you have HF token)

If you have a Hugging Face token:

```bash
# Get your token from: https://huggingface.co/settings/tokens
export HF_TOKEN="your_token_here"

# Create space using huggingface_hub
python -c "
from huggingface_hub import create_repo
create_repo(
    repo_id='your-username/synthetic-data-generator',
    repo_type='space',
    space_sdk='gradio',
    exist_ok=True
)
"

# Add remote and push
git remote add hf https://huggingface.co/spaces/your-username/synthetic-data-generator
git push hf master
```

## Your Repository is Ready!

All files are available at:
**https://github.com/Sherin-SEF-AI/synthetic-data-generator**

Just download and upload to your Hugging Face Space!
