from auth import create_account, login
from vault import add_entry, list_entries, update_entry, delete_entry
from utils import clear_screen

def main():
    clear_screen()
    while True:
        print("\n🔐 \033[1;32mWelcome to VaultZilla CLI!\033[0m 🦖 ")
        print("\033[0;36mWhere our PINcredible 💥 encryption devours weak security\033[0m")
        print("\033[0;34mBought to by Apps2U and Copilot AI, copyright pending 2025 SBuckler...\033[0m")
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("\033[0;32mChoose an option: \033[0m").strip()
        if choice == "1":
            result = create_account()
            if result:
                username, pin = result
                session(username, pin)
        elif choice == "2":
            result = login()
            if result:
                username, pin = result
                session(username, pin)
        elif choice == "3":
            print("👋 Goodbye.")
            break
        else:
            print("❌ Invalid choice.")

def session(username, pin):
    while True:
        print(f"\n🔓 Logged in as {username}")
        print("1. Add Entry")
        print("2. List Entries")
        print("3. Update Password")
        print("4. Delete Entry")
        print("5. Logout")
        choice = input("\033[0;32mChoose an option: \033[0m").strip()

        if choice == "1":
            add_entry(username, pin)
        elif choice == "2":
            clear_screen()
            print("🔐 Welcome to SecurePass")
            list_entries(username, pin)
        elif choice == "3":
            update_entry(username, pin)
        elif choice == "4":
            delete_entry(username, pin)
        elif choice == "5":
            clear_screen()
            print("🔒 Logged out.")
            input("Press Enter to continue...")
            break
        else:
            clear_screen()
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()