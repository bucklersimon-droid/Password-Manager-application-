# VaultZilla - Secure Password Manager

VaultZilla is a simple, secure, and fun command-line password manager.
It lets you create accounts, store login credentials, and retrieve them
safely using encryption.

---

## Features
- 🔐 Secure storage of usernames and passwords
- 🧂 Salted and hashed PINs for account protection
- 🦖 VaultZilla mascot adds a playful touch
- 🗂 Each user has their own encrypted vault file
- 🎨 CLI output styled with bold and colored text

---

## Installation
1. Download `VaultZilla.exe` from the `dist` folder.
2. Place it anywhere on your computer (Desktop, Documents, etc.).
3. Double-click `VaultZilla.exe` to launch the app.
   - No Python installation is required; everything is bundled.

---

## Usage
When you run VaultZilla, you’ll see a menu with options like:

1.	Create Account
2. 	Login
3. 	Add Password Record
4. 	View Password Records
5. 	Exit


### Creating an Account
- Choose **Create Account**.
- Enter a username.
- Enter a PIN (used to protect your vault).
- VaultZilla will generate a salt and hash for your PIN and create
  an encrypted vault file for your account.

### Logging In
- Choose **Login**.
- Enter your username and PIN.
- If correct, VaultZilla unlocks your vault.

### Adding Records
- After login, choose **Add Password Record**.
- Enter the site/service name, username, and password.
- VaultZilla encrypts and stores the record in your vault file.

### Viewing Records
- After login, choose **View Password Records**.
- VaultZilla decrypts and displays your stored credentials.

---

## Security Notes
- PINs are hashed with a random salt using PBKDF2-HMAC.
- Vault files are encrypted with a Fernet key derived from your PIN.
- **Important:** A short PIN (like 4 digits) can be brute-forced.
  For stronger protection, use a longer alphanumeric PIN.
- Keep your `users.json` and vault files safe — if someone gets both,
  they could attempt brute-force attacks.

---
## 📜 Licensing & Attribution

This project is released under the MIT License. You are free to use, modify, and distribute the code, provided that the original copyright notice and license terms are included.

### Dependencies
The Password Manager application is built with Python’s standard library modules and one third‑party library:

- `os`, `sys`, `json`, `hashlib`, `base64`, `secrets`, `getpass` (Python standard library)
- `cryptography.fernet` (Apache License 2.0) – https://cryptography.io/

### Attribution
All original code in this repository is the work of [Simon Buckler](https://github.com/bucklersimon-droid).  
If you build upon this project, please include a reference back to this repository:  
[Password-Manager-application](https://github.com/bucklersimon-droid/Password-Manager-application-)

The `cryptography` library is developed and maintained by the Python Cryptographic Authority (PyCA).  
Use of this library is subject to the terms of the Apache License 2.0, which requires:
- Preservation of copyright notices and license text in redistributions.
- Clear attribution to the original authors.
- No use of trademarks from the project without permission.
- No warranty is provided by the authors.

### Notes
- Project icon generated with Microsoft Copilot AI. and remain the IP of Simon Buckler.
- Developed as part of VU Certificate III Information Technology (CyberSec stream) coursework.

---
