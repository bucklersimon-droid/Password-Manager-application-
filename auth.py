import json #json files used for users (with hashed pins) and vault entries
import base64 #base64 encoding for hashed pins
import hashlib #hashlib for hashing pins
import getpass #getpass for secure pin input
import os #os for clear screen function and file handling
import time #time for pauses after messages prior to clearing screen
from pathlib import Path #path library for file paths
from utils import clear_screen #clear screen function in utilities file

USER_DB = Path("data/users.json") #path to user database file
#variable USER_DB is set to the path "data/users.json", folder and file
#where account information will be stored.


def load_users(): #load users from JSON file
    if USER_DB.exists():
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}


def save_users(users): #save users to JSON file
    USER_DB.parent.mkdir(parents=True, exist_ok=True) #create data folder
    with open(USER_DB, "w") as f: #put users data into JSON file
        json.dump(users, f)


#hash the PIN with salt (salt = random string to ensure PIN hash uniqueness)
def hash_pin(pin, salt=None): 
    if not salt:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, 100_000)
    return base64.b64encode(salt).decode(), base64.b64encode(key).decode()


#create account function
# removes white space and forces lower case for usernames
def create_account():
    users = load_users()
    username = input("Enter username (name.surname): ").strip().lower()
    if username in users:
        print("❌ Account already exists.")
        time.sleep(1.5) #pause 1.5 seconds then continue
        clear_screen()
        return None

    pin = getpass.getpass("Create a 4-digit PIN: ")
    salt, pin_hash = hash_pin(pin)
    users[username] = {"salt": salt, "pin_hash": pin_hash}
    save_users(users)
    print("✅ Account created.")
    time.sleep(1.5) #pause 1.5 seconds then continue
    clear_screen()
    return username, pin
    #Use of a 4 digit PIN was thought to be an improvement on post-it notes
    #worth noting the PIN is not restricted to 4 characters or even numerics


def login(): #login function
    users = load_users()
    username = input("Enter username: ").strip().lower()
    if username not in users:
        print("❌ Account not found.")
        time.sleep(1.5) #pause 1.5 seconds then continue
        clear_screen()
        return None

    pin = getpass.getpass("Enter PIN: ") #user input PIN no text showing
    salt = base64.b64decode(users[username]["salt"]) #decode stored PIN/salt
    _, pin_hash = hash_pin(pin, salt)
    if pin_hash == users[username]["pin_hash"]: #match PIN to stored hash
        clear_screen()
        print("🔐 \033[1;32mVaultZilla!! Keeping your cedentials safe since "
          "2025...\033[0m 🦖 \n")
        print("✅ Login successful.")
        time.sleep(1.5) #pause 1.5 seconds then continue
        return username, pin
    else: #else error message for incorrect PIN
        print("❌ Incorrect PIN.")
        time.sleep(1.5) #pause 1.5 seconds then continue
        clear_screen()
        return None