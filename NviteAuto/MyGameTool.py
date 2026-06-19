import sys
import os
import webbrowser
import urllib.request
import urllib.error

print("=" * 60)
print("MyGameTool - test")
print("=" * 60)

REPO_FOLDER_URL = "https://github.com/SeedOfAnarky/NviteAutoInstall/tree/main/NviteAuto/Scripts"
RAW_BASE_URL = "https://raw.githubusercontent.com/SeedOfAnarky/NviteAutoInstall/main/NviteAuto/Scripts"

if len(sys.argv) > 1:
    target = sys.argv[1]
    name = os.path.splitext(os.path.basename(target))[0]
    print(f"Target path: {target}")
    print(f"Game name  : {name}")

    script_filename = f"{name}.py"
    file_page_url = f"https://github.com/SeedOfAnarky/NviteAutoInstall/blob/main/NviteAuto/Scripts/{script_filename}"
    raw_url = f"{RAW_BASE_URL}/{script_filename}"

    print(f"\nLooking for a matching script: {script_filename}")

    # Just check if it exists, we do NOT download or run it.
    exists = None
    try:
        req = urllib.request.Request(raw_url, method="HEAD")
        with urllib.request.urlopen(req, timeout=8) as resp:
            exists = resp.status == 200
    except urllib.error.HTTPError:
        exists = False
    except Exception as e:
        print(f"(Could not check automatically: {e})")
        exists = None  # unknown, fall back to opening the folder

    if exists:
        print("Found a match! Opening it in your browser for you to review:")
        print(file_page_url)
        webbrowser.open(file_page_url)
    elif exists is False:
        print(f"No script named '{script_filename}' was found in the repo.")
        print("Opening the Scripts folder so you can browse manually:")
        print(REPO_FOLDER_URL)
        webbrowser.open(REPO_FOLDER_URL)
    else:
        print("Opening the Scripts folder so you can browse manually:")
        print(REPO_FOLDER_URL)
        webbrowser.open(REPO_FOLDER_URL)

    print("\nNothing was downloaded or run automatically.")
    print("Review the script on GitHub, then download it yourself if it looks right.")
else:
    print("No path was passed in.")

input("\nPress Enter to close...")
