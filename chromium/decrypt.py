import os
import json
import base64
import sqlite3
import shutil
import win32crypt
from Crypto.Cipher import AES

BROWSERS = {
    "Chrome": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
    "Brave": os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data"),
    "Edge": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data"),
    "Opera": os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable")
}

def get_encryption_key(local_state_path):
    with open(local_state_path, "r", encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]  # remove DPAPI prefix
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_password(buff, key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1])
        except:
            return ""

def list_profiles(browser_path):
    profiles = []
    for entry in os.listdir(browser_path):
        if os.path.isdir(os.path.join(browser_path, entry)) and (
            entry.startswith("Profile") or entry in ["Default", "Opera Stable"]
        ):
            profiles.append(entry)
    return profiles

def main():
    print("Available browsers with detected user data:\n")
    options = []
    for browser, path in BROWSERS.items():
        if os.path.exists(path):
            print(f"[{len(options)+1}] {browser}")
            options.append((browser, path))

    if not options:
        print("No supported Chromium browsers found.")
        return

    choice = int(input("\nSelect browser [number]: ")) - 1
    if choice < 0 or choice >= len(options):
        print("Invalid choice.")
        return

    browser, browser_path = options[choice]
    profiles = list_profiles(browser_path)

    print(f"\nAvailable profiles for {browser}:")
    for i, p in enumerate(profiles):
        print(f"[{i+1}] {p}")

    profile_choice = int(input("\nSelect profile [number]: ")) - 1
    if profile_choice < 0 or profile_choice >= len(profiles):
        print("Invalid profile.")
        return

    profile = profiles[profile_choice]
    login_db = os.path.join(browser_path, profile, "Login Data")
    local_state = os.path.join(browser_path, "Local State")

    if not os.path.exists(login_db) or not os.path.exists(local_state):
        print("Login Data or Local State file not found.")
        return

    key = get_encryption_key(local_state)
    temp_db = os.path.join(os.environ['TEMP'], f"LoginDataTemp_{browser}.db")
    shutil.copyfile(login_db, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    for row in cursor.fetchall():
        url, username, encrypted_password = row
        decrypted = decrypt_password(encrypted_password, key)
        if username or decrypted:
            print(f"\nURL: {url}\nUsername: {username}\nPassword: {decrypted}")

    cursor.close()
    conn.close()
    os.remove(temp_db)

if __name__ == "__main__":
    main()
