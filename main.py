#Importing functions from other file/modules
from auth import create_account, login
from vault import add_entry, list_entries, update_entry, delete_entry
from utils import clear_screen
#Importing time module for pauses
import time


def main(): #main() function runs automatically on program start
    clear_screen()
    while True:
        print("\n🔐 \033[1;32mWelcome to VaultZilla CLI!\033[0m 🦖 ")
        print("\033[0;36mWhere our PINcredible 💥 encryption devours weak "
              "security\033[0m")
        print("\033[0;34mBought to you by \033[1;31mApps2U \033[0;34m"
              "and \033[0;31mCopilot AI\033[0;34m, copyright pending 2025 "
              "SBuckler...\033[0m")
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("\033[38;5;208mChoose an option: \033[0m").strip()
        if choice == "1": #user input login options previous 2 lines
            result = create_account() #create account option
            if result:
                username, pin = result
                session(username, pin)
        elif choice == "2": #login option
            result = login()
            if result:
                username, pin = result
                session(username, pin)
        elif choice == "3": #exit to shut down software
            print("👋 Goodbye.")
            time.sleep(1.5) #pauses for 1.5 seconds before exiting
            break
        else:
            print("❌ Invalid choice.")
            time.sleep(1.5) #pause 1.5 seconds then continue
            clear_screen() #clear screen and return to menu


def session(username, pin): #page 2 options after login
    while True:
        print(f"\n🔓 \033[0;33mLogged in as \033[1;35m{username}\033[0m]")
        print("1. Add Entry")
        print("2. List Entries")
        print("3. Update Password")
        print("4. Delete Entry")
        print("5. Logout")
        choice = input("\033[38;5;208mChoose an option: \033[0m").strip()

        if choice == "1": #add entry option
            add_entry(username, pin)
        elif choice == "2": #list entries option
            clear_screen()
            print("🔐 Welcome to SecurePass")
            list_entries(username, pin)
        elif choice == "3": #update a password option
            update_entry(username, pin)
        elif choice == "4": #delete an entry option
            delete_entry(username, pin)
        elif choice == "5": #logout option
            clear_screen()
            print("🔒 Logged out.")
            time.sleep(1.5) #pause 1.5 seconds then continue
            clear_screen()
            break
        else:
            print("❌ Invalid choice.")
            time.sleep(1.5) #pause 1.5 seconds then continue
            clear_screen() #clear screen and return to menu


if __name__ == "__main__": #call main() function to start program 
    main()