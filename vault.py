import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from pathlib import Path
from utils import clear_screen


def derive_key(pin, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(pin.encode()))

def get_vault_path(username):
    return Path(f"data/users/{username}.vault")

def load_vault(username, pin):
    path = get_vault_path(username)
    if not path.exists():
        return []

    with open(path, "rb") as f:
        encrypted = f.read()
    key = derive_key(pin, username)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted)

def save_vault(username, pin, entries):
    path = get_vault_path(username)
    key = derive_key(pin, username)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(entries).encode())
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(encrypted)

def add_entry(username, pin):
    entries = load_vault(username, pin)
    service = input("Service name: ")
    user = input("Username: ")
    password = input("Password: ")
    url = input("URL: ")
    entries.append({"service": service, "username": user, "password": password, "url": url})
    save_vault(username, pin, entries)
    print("✅ Entry added.")

def list_entries(username, pin):
    clear_screen()
    entries = load_vault(username, pin)
    print("🔐 \033[1;32mVaultZilla!! Keeping your cedentials safe since 2025...\033[0m 🦖 \n")
    if not entries:
        print("🔒 Vault is empty.")
        return True  # screen was cleared
    for i, entry in enumerate(entries, 1):
        print(f"{i} \033[1;34mService: \033[0m{entry['service']} - "
              f"\033[1;34mUsername: \033[0m {entry['username']} - "
              f"\033[1;34mURL: \033[0m @{entry['url']} - "
              f"\033[1;34mPassword: \033[0m {entry['password']}")
    return True  # screen was cleared

def update_entry(username, pin):
    entries = load_vault(username, pin)
    if not entries:
        print("🔒 Vault is empty.")
        return

    for i, entry in enumerate(entries, 1):
        print(f"{i}. {entry['service']} — {entry['username']} @ {entry['url']}")

    try:
        choice = int(input("Select entry number to update: "))
        if 1 <= choice <= len(entries):
            new_password = input("Enter new password: ")
            entries[choice - 1]["password"] = new_password
            save_vault(username, pin, entries)
            print("✅ Password updated.")
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Please enter a valid number.")

def delete_entry(username, pin):
    entries = load_vault(username, pin)
    if not entries:
        print("🔒 Vault is empty.")
        return

    for i, entry in enumerate(entries, 1):
        print(f"{i}. {entry['service']} — {entry['username']} @ {entry['url']}")

    try:
        choice = int(input("Select entry number to delete: "))
        if 1 <= choice <= len(entries):
            removed = entries.pop(choice - 1)
            save_vault(username, pin, entries)
            print(f"🗑️ Deleted entry for {removed['service']}.")
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Please enter a valid number.")

