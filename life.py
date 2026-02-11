import time
import subprocess
import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv


# Load environment variables for keys and tokens
load_dotenv()


# Configuration (in minutes for clarity)
INTERVAL_MINUTES = 300  # 5 hours
INTERVAL = INTERVAL_MINUTES * 60  # Convert to seconds
REPO_NAME = os.path.basename(os.getcwd())  # Uses folder name as repo name
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🤖 {message}")


def ensure_github_repo():
    """Checks if the repository exists on GitHub and creates it if missing"""
    if not GITHUB_TOKEN:
        log("⚠️ GITHUB_TOKEN missing. Skipping remote check.")
        return False

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # 1. Get username
    user_res = requests.get("https://api.github.com/user", headers=headers)
    if user_res.status_code != 200:
        log(f"❌ Could not verify GitHub user: {user_res.json().get('message')}")
        return False

    username = user_res.json()['login']
    repo_url = f"https://api.github.com/repos/{username}/{REPO_NAME}"

    # 2. Check if repo exists
    check_res = requests.get(repo_url, headers=headers)

    if check_res.status_code == 404:
        log(f"🚀 Repository '{REPO_NAME}' not found. Creating it on GitHub (PUBLIC)...")
        create_data = {
            "name": REPO_NAME,
            "private": False,  # ✅ PUBLIC repository
            "description": "🔮 Polymira AI - Prediction Market Oracle",
            "homepage": "https://polymira.ai"
        }
        create_res = requests.post("https://api.github.com/user/repos", headers=headers, json=create_data)

        if create_res.status_code == 201:
            log(f"✅ Public repository created successfully: {create_res.json()['html_url']}")
        else:
            log(f"❌ Failed to create repo: {create_res.json().get('message')}")
            return False
    else:
        log(f"📦 Repository '{REPO_NAME}' already exists on GitHub.")

    # 3. Configure local Git remote
    authenticated_url = f"https://{GITHUB_TOKEN}@github.com/{username}/{REPO_NAME}.git"
    subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", authenticated_url], check=True)
    return True


def run_script(script_name):
    """Executes auxiliary scripts (scanner, brain) securely"""
    if not os.path.exists(script_name):
        log(f"❌ Error: File {script_name} not found!")
        return

    log(f"Starting {script_name}...")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        log(f"✅ {script_name} finished successfully.")
    except Exception as e:
        log(f"⚠️ Error in {script_name}: {e}")


def git_save_and_upload():
    """Saves progress and pushes updates to GitHub securely"""
    log("💾 Saving data and pushing to GitHub...")

    try:
        if not ensure_github_repo():
            return

        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "branch", "-M", "master"], check=True)

        # ✅ Configure Git user (prevents random author names)
        subprocess.run(["git", "config", "user.name", "kolyantrend"], check=True)
        subprocess.run(["git", "config", "user.email", "kolyantrend@users.noreply.github.com"], check=True)

        subprocess.run(["git", "add", "."], check=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        subprocess.run(["git", "commit", "-m", f"Auto-update: {timestamp}", "--allow-empty"], check=True)

        result = subprocess.run(["git", "push", "-u", "origin", "master"], capture_output=True, text=True)

        if result.returncode == 0:
            log(f"🚀 SUCCESS: Project uploaded/updated on GitHub ({timestamp})")
        else:
            log(f"⚠️ Git Push Error: {result.stderr}")

    except Exception as e:
        log(f"❌ Git Automation Error: {e}")


def main():
    if not os.getenv("GEMINI_API_KEY"):
        log("❌ CRITICAL ERROR: GEMINI_API_KEY not found in .env!")
        return

    print("=========================================")
    print("   POLYMIRA AI: AUTONOMOUS LIFECYCLE   ")
    print("=========================================")
    print(f"⏱ Update Interval: {INTERVAL_MINUTES} min ({INTERVAL_MINUTES/60:.1f} hours)")
    print("💻 System: Full Autonomy Mode (API-Driven)")
    print("=========================================\n")

    log("🚀 Initializing first cycle...")

    while True:
        run_script("scanner.py")
        run_script("brain.py")
        git_save_and_upload()
        log(f"💤 Sleeping for {INTERVAL_MINUTES} minutes ({INTERVAL_MINUTES/60:.1f} hours)...")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()

