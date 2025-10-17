"""
Deployment script for Hugging Face Spaces
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking deployment requirements...")
    
    # Check if git is installed
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install git first.")
        return False
    
    # Check if huggingface_hub is installed
    try:
        import huggingface_hub
        print("✅ huggingface_hub is installed")
    except ImportError:
        print("❌ huggingface_hub is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub"], check=True)
        print("✅ huggingface_hub installed")
    
    return True

def prepare_files():
    """Prepare files for deployment"""
    print("\n📁 Preparing files for deployment...")
    
    # Files to include in deployment
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "config.yaml",
        ".gitattributes",
        ".gitignore"
    ]
    
    # Directories to include
    required_dirs = [
        "generators/",
        "privacy/",
        "templates/",
        "utils/",
        "assets/"
    ]
    
    # Check if all required files exist
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    # Check if all required directories exist
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing required directories: {missing_dirs}")
        return False
    
    print("✅ All required files and directories present")
    return True

def create_git_repo():
    """Initialize git repository if not exists"""
    print("\n🔧 Setting up git repository...")
    
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already exists")
    
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

def deploy_to_huggingface():
    """Deploy to Hugging Face Spaces"""
    print("\n🚀 Deploying to Hugging Face Spaces...")
    
    # Get space name from user
    space_name = input("Enter your Hugging Face space name (e.g., 'username/synthetic-data-generator'): ").strip()
    
    if not space_name:
        print("❌ Space name is required")
        return False
    
    try:
        # Create space using huggingface_hub
        from huggingface_hub import HfApi, create_repo
        
        api = HfApi()
        
        # Create the space
        print(f"📦 Creating space: {space_name}")
        create_repo(
            repo_id=space_name,
            repo_type="space",
            space_sdk="gradio",
            exist_ok=True
        )
        
        # Push to the space
        print("📤 Pushing files to Hugging Face...")
        subprocess.run([
            "git", "remote", "add", "origin", 
            f"https://huggingface.co/spaces/{space_name}"
        ], check=True)
        
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        
        print(f"✅ Successfully deployed to: https://huggingface.co/spaces/{space_name}")
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🎲 Synthetic Data Generator - Hugging Face Deployment")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Prepare files
    if not prepare_files():
        return False
    
    # Setup git
    try:
        create_git_repo()
    except subprocess.CalledProcessError as e:
        print(f"❌ Git setup failed: {e}")
        return False
    
    # Deploy to Hugging Face
    if not deploy_to_huggingface():
        return False
    
    print("\n🎉 Deployment completed successfully!")
    print("Your Synthetic Data Generator is now live on Hugging Face Spaces!")
    
    return True

if __name__ == "__main__":
    main()
