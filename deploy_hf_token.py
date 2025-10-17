"""
Deploy to Hugging Face Spaces using token
"""

import os
import subprocess
import sys

def deploy_with_token():
    """Deploy using Hugging Face token"""
    
    print("🚀 Deploying to Hugging Face Spaces")
    print("=" * 40)
    
    # Get token from environment or user
    token = os.getenv('HF_TOKEN')
    if not token:
        print("Please set your Hugging Face token:")
        print("export HF_TOKEN='your_token_here'")
        print("\nGet your token from: https://huggingface.co/settings/tokens")
        return False
    
    # Get username
    username = input("Enter your Hugging Face username: ").strip()
    if not username:
        print("❌ Username is required")
        return False
    
    space_name = f"{username}/synthetic-data-generator"
    
    try:
        from huggingface_hub import HfApi, create_repo
        
        # Set token
        api = HfApi(token=token)
        
        print(f"📦 Creating space: {space_name}")
        
        # Create the space
        create_repo(
            repo_id=space_name,
            repo_type="space",
            space_sdk="gradio",
            exist_ok=True
        )
        
        print(f"✅ Space created: https://huggingface.co/spaces/{space_name}")
        
        # Add remote
        subprocess.run([
            "git", "remote", "add", "hf", 
            f"https://huggingface.co/spaces/{space_name}"
        ], check=True)
        
        print("✅ Remote added")
        
        # Push to space
        print("📤 Pushing files to Hugging Face...")
        subprocess.run(["git", "push", "hf", "master"], check=True)
        
        print(f"🎉 Successfully deployed!")
        print(f"Your app is live at: https://huggingface.co/spaces/{space_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    deploy_with_token()
