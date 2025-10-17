"""
Direct deployment script for Hugging Face Spaces
"""

import os
import subprocess
import sys
from pathlib import Path

def setup_git():
    """Setup git repository"""
    print("🔧 Setting up git repository...")
    
    # Initialize git if not exists
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")
    
    # Set default branch to main
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    
    # Add all files
    subprocess.run(["git", "add", "."], check=True)
    print("✅ Files added to git")
    
    # Check if there are changes to commit
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip():
        subprocess.run(["git", "commit", "-m", "Initial commit: Synthetic Data Generator"], check=True)
        print("✅ Initial commit created")
    else:
        print("✅ No changes to commit")

def create_space_directly():
    """Create space using huggingface_hub directly"""
    print("🚀 Creating Hugging Face Space...")
    
    try:
        from huggingface_hub import HfApi, create_repo
        
        # You'll need to set your username here
        username = "your-username"  # Replace with your actual username
        space_name = f"{username}/synthetic-data-generator"
        
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
            "git", "remote", "add", "origin", 
            f"https://huggingface.co/spaces/{space_name}"
        ], check=True)
        
        print("✅ Remote added")
        
        return space_name
        
    except Exception as e:
        print(f"❌ Error creating space: {e}")
        return None

def push_to_space(space_name):
    """Push files to the space"""
    print(f"📤 Pushing files to {space_name}...")
    
    try:
        # Push to the space
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print(f"✅ Successfully deployed to: https://huggingface.co/spaces/{space_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Push failed: {e}")
        print("💡 You may need to authenticate with Hugging Face first:")
        print("   Run: huggingface-cli login")
        return False

def main():
    """Main deployment function"""
    print("🎲 Synthetic Data Generator - Direct Deployment")
    print("=" * 50)
    
    # Setup git
    try:
        setup_git()
    except subprocess.CalledProcessError as e:
        print(f"❌ Git setup failed: {e}")
        return False
    
    # Create space
    space_name = create_space_directly()
    if not space_name:
        return False
    
    # Push to space
    if not push_to_space(space_name):
        return False
    
    print("\n🎉 Deployment completed successfully!")
    print(f"Your Synthetic Data Generator is now live at:")
    print(f"https://huggingface.co/spaces/{space_name}")
    
    return True

if __name__ == "__main__":
    main()
