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
REPO_NAME = os.path.basename(os.getcwd())
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🤖 {message}")

def ensure_github_repo():
    """Checks if the repository exists on GitHub and creates it if missing"""
    if not GITHUB_TOKEN:
        log("⚠️ GITHUB_TOKEN missing. Skipping remote check.")
        return False

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    try:
        user_res = requests.get("https://api.github.com/user", headers=headers)
        if user_res.status_code != 200:
            log(f"❌ Could not verify GitHub user.")
            return False

        username = user_res.json()['login']
        repo_url = f"https://api.github.com/repos/{username}/{REPO_NAME}"
        check_res = requests.get(repo_url, headers=headers)

        if check_res.status_code == 404:
            log(f"🚀 Creating repository '{REPO_NAME}' on GitHub...")
            create_data = {"name": REPO_NAME, "private": False}
            requests.post("https://api.github.com/user/repos", headers=headers, json=create_data)
        
        authenticated_url = f"https://{GITHUB_TOKEN}@github.com/{username}/{REPO_NAME}.git"
        subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "add", "origin", authenticated_url], check=True)
        return True
    except Exception as e:
        log(f"⚠️ GitHub check failed: {e}")
        return False

def run_script(script_name):
    """Executes auxiliary scripts (scanner, brain)"""
    if not os.path.exists(script_name):
        log(f"❌ Error: {script_name} not found!")
        return

    log(f"Starting {script_name}...")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        log(f"✅ {script_name} finished successfully.")
    except Exception as e:
        log(f"⚠️ Error in {script_name}: {e}")

def git_save_and_upload():
    """Saves progress and pushes updates to GitHub"""
    log("💾 Syncing data with GitHub...")

    try:
        if not ensure_github_repo(): return

        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "branch", "-M", "master"], check=True)

        subprocess.run(["git", "config", "user.name", "kolyantrend"], check=True)
        subprocess.run(["git", "config", "user.email", "kolyantrend@users.noreply.github.com"], check=True)

        # Добавляем изменения
        subprocess.run(["git", "add", "."], check=True)
        
        # Проверяем, есть ли что коммитить, чтобы не плодить пустые ошибки
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status.stdout.strip():
            log("ℹ️ No changes to commit (everything is up to date).")
            return

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        subprocess.run(["git", "commit", "-m", f"Auto-update: {timestamp}"], check=True)
        
        result = subprocess.run(["git", "push", "-u", "origin", "master"], capture_output=True, text=True)

        if result.returncode == 0:
            log(f"🚀 SUCCESS: GitHub updated at {timestamp}")
        else:
            log(f"⚠️ Git Push Error: {result.stderr}")

    except Exception as e:
        log(f"❌ Git Automation Error: {e}")

def main():
    if not os.getenv("GEMINI_API_KEY"):
        log("❌ CRITICAL ERROR: GEMINI_API_KEY missing!")
        return

    log("🚀 Polymira Lifecycle Started")

    while True:
        run_script("scanner.py")
        run_script("brain.py")
        git_save_and_upload()
        log(f"💤 Next update in {INTERVAL_MINUTES} minutes...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
