import sys
import os
import glob
import shutil
import subprocess
import configparser

# ── Paths ─────────────────────────────────────────────────────────────────────
INSTALL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # up one from Scripts\

# ── Game-specific config ───────────────────────────────────────────────────────
SHIPPING_EXE_NAME = "BackroomsLostRunners-Win64-Shipping.exe"  # update this per game
CONFIG_PATH = os.path.join(INSTALL_DIR, "Scripts", "config.ini")

# ── Load config ───────────────────────────────────────────────────────────────
config = configparser.ConfigParser()

if not os.path.isfile(CONFIG_PATH):
    print(f"ERROR: config.ini not found at:\n  {CONFIG_PATH}")
    input("\nPress Enter to close...")
    sys.exit(1)

config.read(CONFIG_PATH)

DLL_FILENAME = config.get("A", "dll_filename", fallback="SteamVersion.dll")
CLI_FILENAME = config.get("S", "cli_filename", fallback="s.CLI.exe")


def VersionUpdater(exe_path: str):
    """Copies the DLL from the A folder into the game's Steamworks directory."""

    game_dir = os.path.dirname(exe_path)
    dest_dir = os.path.join(game_dir, "Engine", "Binaries", "ThirdParty", "Steamworks", "Steamv157", "Win64")
    dest_file = os.path.join(dest_dir, DLL_FILENAME)
    source_file = os.path.join(INSTALL_DIR, "A", DLL_FILENAME)

    print(f"DLL      : {DLL_FILENAME}")
    print(f"Source   : {source_file}")
    print(f"Dest     : {dest_file}")

    if not os.path.isfile(source_file):
        print(f"\nERROR: {DLL_FILENAME} not found in A folder:\n  {source_file}")
        return False

    if not os.path.isdir(dest_dir):
        print(f"\nERROR: Target directory not found:\n  {dest_dir}")
        return False

    try:
        shutil.copy2(source_file, dest_file)
        print(f"\n{DLL_FILENAME} updated successfully.")
        return True
    except Exception as e:
        print(f"\nERROR copying file: {e}")
        return False


def ShippingUpdater(exe_path: str):
    """Finds the *Win64-Shipping.exe and passes it to the CLI tool."""

    game_dir = os.path.dirname(exe_path)
    binaries_dir = os.path.join(game_dir, "BackroomsLostRunners", "Binaries", "Win64")
    s_cli = os.path.join(INSTALL_DIR, "S", CLI_FILENAME)

    print(f"CLI      : {CLI_FILENAME}")
    print(f"Binaries : {binaries_dir}")
    print(f"CLI path : {s_cli}")

    if not os.path.isfile(s_cli):
        print(f"\nERROR: {CLI_FILENAME} not found:\n  {s_cli}")
        return False

    if not os.path.isdir(binaries_dir):
        print(f"\nERROR: Binaries directory not found:\n  {binaries_dir}")
        return False

    shipping_exe = os.path.join(binaries_dir, SHIPPING_EXE_NAME)

    if not os.path.isfile(shipping_exe):
        print(f"\nERROR: {SHIPPING_EXE_NAME} not found in:\n  {binaries_dir}")
        return False
    print(f"Shipping : {shipping_exe}")
    print(f"\nRunning {CLI_FILENAME}...")

    try:
        result = subprocess.run([s_cli, shipping_exe], check=False)
        print(f"\n{CLI_FILENAME} exited with code {result.returncode}")
    except Exception as e:
        print(f"\nERROR running {CLI_FILENAME}: {e}")
        return False

    # ── Rename files after CLI finishes ───────────────────────────────────────
    unpacked = shipping_exe + ".unpacked.exe"
    backup   = os.path.splitext(shipping_exe)[0] + ".bak"

    print(f"\nRenaming original  : {os.path.basename(shipping_exe)} -> {os.path.basename(backup)}")
    print(f"Renaming unpacked  : {os.path.basename(unpacked)} -> {os.path.basename(shipping_exe)}")

    try:
        if not os.path.isfile(unpacked):
            print(f"\nERROR: Unpacked file not found:\n  {unpacked}")
            return False

        os.rename(shipping_exe, backup)
        os.rename(unpacked, shipping_exe)
        print("\nFiles renamed successfully.")
        return True
    except Exception as e:
        print(f"\nERROR renaming files: {e}")
        return False


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("BackroomsLostRunners - Version Updater")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("ERROR: No exe path provided.")
    else:
        VersionUpdater(sys.argv[1])
        print()
        ShippingUpdater(sys.argv[1])

    input("\nPress Enter to close...")
