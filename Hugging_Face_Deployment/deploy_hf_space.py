# 🚀 ERIA Hugging Face Spaces Deployment Assistant
# ==================================================
# This helper script automates the deployment of your Streamlit app onto Hugging Face Spaces!
#
# Steps it assists with:
# 1. Verification of all deployment-ready files.
# 2. Initializing git locally if not already done.
# 3. Committing files (app.py, utils.py, requirements.txt, Test_Data).
# 4. Adding your Hugging Face Space repository remote.
# 5. Pushing to Hugging Face to launch your live public app!

import os
import subprocess
import sys

def check_file_exists(file_path):
    if os.path.exists(file_path):
        print(f"  ✅ Found: {file_path}")
        return True
    else:
        print(f"  ❌ Missing: {file_path}")
        return False

def run_command(command, shell=True):
    try:
        result = subprocess.run(command, shell=shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    print("================================================================")
    print("🎓 Education Regulation Impact Analyzer (ERIA) - HF Deployer 🎓")
    print("================================================================\n")
    
    print("Step 1: Verifying required files inside project directory...")
    required_files = [
        "streamlit_app.py", "utils.py", "mock_data.py", "mock_data.json", 
        "requirements.txt", "README.md", "Test_Data/UGC_Reference_Links.md",
        "components/__init__.py"
    ]

    all_exist = True
    for f in required_files:
        if not check_file_exists(f):
            all_exist = False
            
    if not all_exist:
        print("\n❌ Error: Some required project files are missing. Please restore them before deploying.")
        sys.exit(1)

        
    print("\n✅ Verification Successful! All files are deployment-ready.")
    
    print("\nStep 2: Checking Git status...")
    git_installed, _ = run_command("git --version")
    if not git_installed:
        print("❌ Git is not installed or not in your system PATH. Please install Git to deploy to Hugging Face Spaces.")
        print("Alternative: You can manually upload 'app.py', 'utils.py', and 'requirements.txt' directly on Hugging Face's web interface!")
        sys.exit(1)
        
    # Check if git is initialized
    is_git_repo = os.path.exists(".git")
    if not is_git_repo:
        print("  💡 Git is not yet initialized in this directory. Initializing now...")
        run_command("git init")
        print("  ✅ Git repository initialized successfully.")
    else:
        print("  ✅ Existing Git repository detected.")
        
    # Configure main branch
    run_command("git checkout -b main")
    
    # Add files (including new modular components and mock dataset)
    run_command("git add streamlit_app.py utils.py mock_data.py mock_data.json requirements.txt README.md Test_Data/ components/")


    
    # Commit files
    committed, _ = run_command('git commit -m "Deploy ERIA Streamlit Dashboard to Hugging Face Spaces"')
    if committed:
        print("  ✅ Files committed successfully.")
    else:
        print("  ℹ️ No changes to commit (files are already up-to-date).")
        
    print("\nStep 4: Connect your Hugging Face Space repository")
    print("----------------------------------------------------------------")
    print("1. Go to https://huggingface.co/spaces and create a new Space.")
    print("2. Choose 'Streamlit' as the Space SDK.")
    print("3. Copy the Git URL under 'Clone this repository'.")
    print("   Example: https://huggingface.co/spaces/username/space-name")
    print("----------------------------------------------------------------\n")
    
    hf_remote_url = input("Enter your Hugging Face Space Git URL: ").strip()
    
    if not hf_remote_url:
        print("\n🛑 Deployment cancelled. No remote URL provided.")
        sys.exit(0)
        
    # Remove remote if it already exists
    run_command("git remote remove huggingface")
    
    # Add huggingface remote
    added, err = run_command(f"git remote add huggingface {hf_remote_url}")
    if added:
        print("  ✅ Hugging Face remote added successfully.")
    else:
        print(f"  ❌ Error adding remote: {err}")
        sys.exit(1)
        
    print("\nStep 5: Pushing codebase to Hugging Face Spaces...")
    print("  🚀 Pushing to 'main' branch on Hugging Face...")
    print("  (Note: You may be prompted to enter your Hugging Face credentials or access token.)\n")
    
    # Push to Hugging Face Space (force push to replace boilerplate)
    pushed, push_err = run_command("git push -u huggingface main --force")
    
    if pushed:
        print("\n🎉 SUCCESS! Your codebase has been pushed to Hugging Face Spaces!")
        print("Go to your Hugging Face Space link in your browser to watch the deployment build.")
        print("\n⚠️ IMPORTANT NEXT STEP:")
        print("1. In your Hugging Face Space, navigate to Settings -> Variables and secrets.")
        print("2. Under Secrets, add a new secret named 'GEMINI_API_KEY'.")
        print("3. Paste your Google AI Studio API key and save it.")
        print("This will run the analyzer securely for all users without exposing your key!")
    else:
        print(f"\n❌ Error pushing to Hugging Face: {push_err}")
        print("Troubleshooting: Ensure you have write access to the space and that your Hugging Face SSH/HTTPS keys are properly set up.")

if __name__ == "__main__":
    main()
