import os
import subprocess
import sys

def find_firefox_install():
    possible_paths = [
        r"C:\Program Files\Mozilla Firefox",
        r"C:\Program Files (x86)\Mozilla Firefox"
    ]
    for path in possible_paths:
        if os.path.exists(os.path.join(path, "nss3.dll")):
            return path
    return None

def main():
    print("🔐 Firefox Password Decryptor")

    decrypt_script = input("Enter full path to firefox_decrypt.py:\n> ").strip('"')
    profile_dir = input("Enter full path to Firefox profile folder (contains logins.json & key4.db):\n> ").strip('"')

    # Validate files
    if not os.path.isfile(decrypt_script):
        print(f"❌ Script not found: {decrypt_script}")
        return
    if not os.path.isfile(os.path.join(profile_dir, "logins.json")):
        print("❌ logins.json not found in selected directory.")
        return
    if not os.path.isfile(os.path.join(profile_dir, "key4.db")):
        print("❌ key4.db not found in selected directory.")
        return

    # Find NSS library
    nss_path = find_firefox_install()
    if not nss_path:
        print("❌ Could not find Firefox's nss3.dll. Is Firefox installed?")
        return

    # Change working dir to NSS path and run the script
    print(f"\n🚀 Running firefox_decrypt from: {nss_path}")
    os.chdir(nss_path)

    subprocess.run([
        sys.executable,
        decrypt_script,
        profile_dir
    ])

if __name__ == "__main__":
    main()
