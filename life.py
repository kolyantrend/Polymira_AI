import time
import subprocess
import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
INTERVAL_MINUTES = 300  # 5 hours
INTERVAL = INTERVAL_MINUTES * 60
BASE_DIR = "/var/www/Polymira_AI"
REPO_NAME = os.path.basename(BASE_DIR)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# Указываем полный путь к git, который мы нашли через 'which git'
GIT_PATH = "/usr/bin/git"

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] 🤖 {message}", flush=True)

def ensure_github_repo():
    """Checks if the repository exists on GitHub and creates it if missing"""
    if not GITHUB_TOKEN:
        log("⚠️ GITHUB_TOKEN missing in .env. GitHub sync disabled.")
        return False

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    try:
        user_res = requests.get("https://api.github.com/user", headers=headers)
        if user_res.status_code != 200:
            log("❌ GitHub Token Invalid. Check your .env file.")
            return False

        username = user_res.json()['login']
        authenticated_url = f"https://{GITHUB_TOKEN}@github.com/{username}/{REPO_NAME}.git"
        
        remote_check = subprocess.run([GIT_PATH, "remote", "get-url", "origin"], 
                                    capture_output=True, text=True, cwd=BASE_DIR)
        
        if authenticated_url not in remote_check.stdout:
            subprocess.run([GIT_PATH, "remote", "remove", "origin"], stderr=subprocess.DEVNULL, cwd=BASE_DIR)
            subprocess.run([GIT_PATH, "remote", "add", "origin", authenticated_url], check=True, cwd=BASE_DIR)
            
        return True
    except Exception as e:
        log(f"⚠️ GitHub check failed: {e}")
        return False

def run_script(script_name):
    """Executes auxiliary scripts (scanner, brain)"""
    script_path = os.path.join(BASE_DIR, script_name)
    if not os.path.exists(script_path):
        log(f"❌ Error: {script_name} not found!")
        return

    log(f"Starting {script_name}...")
    try:
        subprocess.run([sys.executable, script_path], check=True, cwd=BASE_DIR)
        log(f"✅ {script_name} finished successfully.")
    except Exception as e:
        log(f"⚠️ Error in {script_name}: {e}")

def git_save_and_upload():
    """Saves progress and pushes updates to GitHub"""
    log("💾 Starting GitHub Sync...")

    try:
        if not ensure_github_repo(): return

        branch_res = subprocess.run([GIT_PATH, "rev-parse", "--abbrev-ref", "HEAD"], 
                                   capture_output=True, text=True, check=True, cwd=BASE_DIR)
        branch = branch_res.stdout.strip()

        subprocess.run([GIT_PATH, "config", "user.name", "kolyantrend"], cwd=BASE_DIR)
        subprocess.run([GIT_PATH, "config", "user.email", "kolyantrend@users.noreply.github.com"], cwd=BASE_DIR)

        log(f"📥 Pulling latest changes from {branch}...")
        subprocess.run([GIT_PATH, "pull", "origin", branch, "--rebase"], cwd=BASE_DIR)

        subprocess.run([GIT_PATH, "add", "."], check=True, cwd=BASE_DIR)

        status = subprocess.run([GIT_PATH, "status", "--porcelain"], capture_output=True, text=True, cwd=BASE_DIR)
        if not status.stdout.strip():
            log("ℹ️ No changes to commit.")
            return

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        subprocess.run([GIT_PATH, "commit", "-m", f"Auto-update: {timestamp}"], check=True, cwd=BASE_DIR)
        
        log(f"📤 Pushing to {branch}...")
        result = subprocess.run([GIT_PATH, "push", "origin", branch], capture_output=True, text=True, cwd=BASE_DIR)

        if result.returncode == 0:
            log(f"🚀 SUCCESS: GitHub updated at {timestamp}")
        else:
            log(f"❌ Git Push Error: {result.stderr}")

    except Exception as e:
        log(f"❌ Git Automation Error: {e}")

def main():
    if not os.getenv("GEMINI_API_KEY"):
        log("❌ CRITICAL ERROR: GEMINI_API_KEY missing!")
        return

    log("🚀 Polymira Lifecycle Started (5h interval)")

    while True:
        load_dotenv() 
        run_script("scanner.py")
        run_script("brain.py")
        git_save_and_upload()
        log(f"💤 Next update in {INTERVAL_MINUTES} minutes...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
