import json #JSON for data storage
import base64 #base64 for encoding
import time #time for pauses
#import encryption modules for secure data handling
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
#import pathlib for file path handling
from pathlib import Path
#import clear screen function from utilities file
from utils import clear_screen


def derive_key(pin, salt): #derive encryption key from PIN
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), #256 bit SHA hashing algorithm
        length=32, #length of key 32 bytes
        salt=salt.encode(), #salt encoded to bytes
        iterations=100_000, #number of iterations for key derivation
    ) #then return the derived key (next line)
    return base64.urlsafe_b64encode(kdf.derive(pin.encode()))


def get_vault_path(username): #get path to user's vault file
    return Path(f"data/users/{username}.vault")


def load_vault(username, pin): #load vault entries from encrypted file
    path = get_vault_path(username)
    if not path.exists():
        return []

    with open(path, "rb") as f:
        encrypted = f.read()
    key = derive_key(pin, username)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted)


def save_vault(username, pin, entries): #save vault entries to encrypted file
    path = get_vault_path(username)
    key = derive_key(pin, username)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(entries).encode())
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(encrypted)


def add_entry(username, pin): #add a new entry to the vault
    entries = load_vault(username, pin)
    service = input("Service name: ")
    user = input("Username: ")
    password = input("Password: ")
    url = input("URL: ")
    entries.append({"service": service, "username": user, 
                    "password": password, "url": url})
    save_vault(username, pin, entries)
    print("✅ Entry added.")
    time.sleep(1.5) #pause 1.5 seconds then continue
    clear_screen()
    list_entries(username, pin)


def list_entries(username, pin): #Display all entries in the vault
    clear_screen()
    entries = load_vault(username, pin)
    print("🔐 \033[1;32mVaultZilla!! Keeping your cedentials safe since "
          "2025...\033[0m 🦖 \n")
    if not entries:
        print("🔒 Vault is empty.")
        return True  # screen was cleared
    for i, entry in enumerate(entries, 1):
        print(f"{i} \033[1;34mService: \033[0m{entry['service']} - "
              f"\033[1;34mUsername: \033[0m {entry['username']} - "
              f"\033[1;34mURL: \033[0m @{entry['url']} - "
              f"\033[1;34mPassword: \033[0m {entry['password']}")
    return True  # screen was cleared


def update_entry(username, pin): #update an existing entry's password
    entries = load_vault(username, pin)
    if not entries:
        print("🔒 Vault is empty.")
        time.sleep(1.5) #pause 1.5 seconds then continue
        clear_screen()
        return

    for i, entry in enumerate(entries, 1): #display entries to choose from for update
        print(f"{i}. {entry['service']} — {entry['username']} @ {entry['url']}")

    try: #user selection with error handling
        choice = int(input("\033[38;5;208mSelect entry number to update: \033[0m"))
        if 1 <= choice <= len(entries):
            new_password = input("Enter new password: ")
            entries[choice - 1]["password"] = new_password
            save_vault(username, pin, entries)
            print("✅ Password updated.")
            time.sleep(1.5) #pause 1.5 seconds then continue
            clear_screen()
            list_entries(username, pin)
        else:
            print("❌ Invalid selection.")
            time.sleep(1.5) #pause 1.5 seconds then continue
            clear_screen()
    except ValueError:
        print("❌ Please enter a valid number.")
        time.sleep(1.5) #pause 1.5 seconds then continue
        clear_screen()


def delete_entry(username, pin): #delete an entry from the vault
    entries = load_vault(username, pin)
    if not entries:
        print("🔒 Vault is empty.")
        time.sleep(1.5) #pause 1.5 seconds then continue
        clear_screen()
        return

    for i, entry in enumerate(entries, 1): #display entries to choose from for deletion
        print(f"{i}. {entry['service']} — {entry['username']} @ {entry['url']}")

    try: #user selection with error handling
        choice = int(input("\033[38;5;208mSelect entry number to delete: \033[0m"))
        if 1 <= choice <= len(entries):
            removed = entries.pop(choice - 1)
            save_vault(username, pin, entries)
            print(f"🗑️ Deleted entry for {removed['service']}.")
            time.sleep(1.5) #pause 1.5 seconds then continue
            clear_screen()
            list_entries(username, pin)
        else:
            print("❌ Invalid selection.")
            time.sleep(1.5) #pause 1.5 seconds then continue
            clear_screen()
    except ValueError:
        print("❌ Please enter a valid number.")
        time.sleep(1.5) #pause 1.5 seconds then continue
        clear_screen()

