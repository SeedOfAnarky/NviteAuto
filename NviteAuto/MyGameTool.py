import sys
import os
import webbrowser
import urllib.request
import urllib.error
import subprocess

print("=" * 60)
print("MyGameTool - Steam Version Tracker")
print("=" * 60)

RAW_BASE_URL = "https://raw.githubusercontent.com/SeedOfAnarky/NviteAuto/main/NviteAuto/Scripts"
REPO_FOLDER_URL = "https://github.com/SeedOfAnarky/NviteAuto/tree/main/NviteAuto/Scripts"

# Scripts folder lives next to MyGameTool.py
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(INSTALL_DIR, "Scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

if len(sys.argv) > 1:
    target = sys.argv[1]
    name = os.path.splitext(os.path.basename(target))[0]
    print(f"Target path: {target}")
    print(f"Game name  : {name}")

    script_filename = f"{name}.py"
    local_script = os.path.join(SCRIPTS_DIR, script_filename)
    raw_url = f"{RAW_BASE_URL}/{script_filename}"
    file_page_url = f"https://github.com/SeedOfAnarky/NviteAuto/blob/main/NviteAuto/Scripts/{script_filename}"

    # ── Check local Scripts folder first ──────────────────────────────────────
    if os.path.isfile(local_script):
        print(f"\nFound cached script: {local_script}")
        print(f"Running script with target: {target}\n")
        print("-" * 60)
        subprocess.run([sys.executable, local_script, target], check=False)

    # ── Not cached — try to download from repo ────────────────────────────────
    else:
        print(f"\nNo cached script found. Checking repo for: {script_filename}")

        exists = None
        try:
            req = urllib.request.Request(raw_url, method="HEAD")
            with urllib.request.urlopen(req, timeout=8) as resp:
                exists = resp.status == 200
        except urllib.error.HTTPError:
            exists = False
        except Exception as e:
            print(f"(Could not reach repo: {e})")
            exists = None

        if exists:
            print(f"Found a match! Downloading {script_filename}...")
            try:
                urllib.request.urlretrieve(raw_url, local_script)
                print(f"Downloaded to: {local_script}")
                print(f"Running script with target: {target}\n")
                print("-" * 60)
                subprocess.run([sys.executable, local_script, target], check=False)
            except Exception as e:
                print(f"\nERROR downloading or running script: {e}")
                print(f"You can review it manually at:\n{file_page_url}")
                webbrowser.open(file_page_url)

        elif exists is False:
            print(f"No script named '{script_filename}' found in the repo.")
            print("Opening the Scripts folder so you can browse manually:")
            print(REPO_FOLDER_URL)
            webbrowser.open(REPO_FOLDER_URL)

        else:
            print("Could not reach GitHub. No cached script available either.")
            print(f"Scripts repo: {REPO_FOLDER_URL}")

else:
    print("No path was passed in.")
    print(f"Scripts repo: {REPO_FOLDER_URL}")

input("\nPress Enter to close...")
