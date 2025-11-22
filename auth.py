import json
import base64
import hashlib
import getpass
import os
from pathlib import Path

USER_DB = Path("data/users.json")

def load_users():
    if USER_DB.exists():
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    USER_DB.parent.mkdir(parents=True, exist_ok=True)
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def hash_pin(pin, salt=None):
    if not salt:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, 100_000)
    return base64.b64encode(salt).decode(), base64.b64encode(key).decode()

def create_account():
    users = load_users()
    username = input("Enter username (name.surname): ").strip().lower()
    if username in users:
        print("❌ Account already exists.")
        return None

    pin = getpass.getpass("Create a 4-digit PIN: ")
    salt, pin_hash = hash_pin(pin)
    users[username] = {"salt": salt, "pin_hash": pin_hash}
    save_users(users)
    print("✅ Account created.")
    return username, pin

def login():
    users = load_users()
    username = input("Enter username: ").strip().lower()
    if username not in users:
        print("❌ Account not found.")
        return None

    pin = getpass.getpass("Enter PIN: ")
    salt = base64.b64decode(users[username]["salt"])
    _, pin_hash = hash_pin(pin, salt)
    if pin_hash == users[username]["pin_hash"]:
        print("✅ Login successful.")
        return username, pin
    else:
        print("❌ Incorrect PIN.")
        return None