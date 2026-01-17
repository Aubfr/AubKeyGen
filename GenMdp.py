import json
import os
import random
import time

DATA_FILE = "data.json"

ASCII = """
  ___        _     
 / _ \      | |    
/ /_\ \_   _| |__  
|  _  | | | | '_ \ 
| | | | |_| | |_) |
\_| |_/\__,_|_.__/ 
"""

print(ASCII)

# ---------- UTILS ----------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- START / LOGIN ----------

def start():
    print("Welcome to AubKeyGen !")
    username = input("Enter your username : ")
    password = input("Set a password : ")
    password2 = input("Confirm password : ")

    if password != password2:
        print("Passwords do not match.")
        start()
        return

    data = {
        "login": {
            "Username": username,
            "Password": password
        },
        "passwords": []
    }

    save_data(data)
    print("Account created successfully !")
    gen()

def login():
    data = load_data()
    password = input("Please enter your password : ")

    if password != data["login"]["Password"]:
        print("Incorrect password.")
        time.sleep(0.5)
        login()
        return

    gen()

# ---------- CORE ----------

def gen():
    while True:
        print("""
1. Show all passwords
2. Create a new password
3. Change master password
4. Credits
5. Exit
""")

        choice = input("--> ")

        if choice == "1":
            show_passwords()

        elif choice == "2":
            create_password()

        elif choice == "3":
            change_master_password()

        elif choice == "4":
            print("AubKeyGen made by Aub")

        elif choice == "5":
            print("Bye !")
            break

        else:
            print("Invalid choice.")

# ---------- FEATURES ----------

def show_passwords():
    data = load_data()
    passwords = data.get("passwords", [])

    if not passwords:
        print("No passwords saved.")
        return

    print("\nSaved passwords :")
    for pwd in passwords:
        print(f"- {pwd['name']} : {pwd['password']}")

def create_password():
    length = int(input("Password length (3 to 20) : "))
    if length < 3 or length > 20:
        print("Invalid length.")
        return

    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789.ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(random.choice(alphabet) for _ in range(length))

    print("Generated password :", key)

    save = input("Do you want to save it ? (y/n) : ")
    if save.lower() != "y":
        return

    name = input("Name for this password : ")

    data = load_data()
    data["passwords"].append({
        "name": name,
        "password": key
    })

    save_data(data)
    print("Password saved successfully !")

def change_master_password():
    data = load_data()
    new_password = input("Enter new master password : ")
    data["login"]["Password"] = new_password
    save_data(data)
    print("Master password updated !")

# ---------- MAIN ----------

data = load_data()

if not data:
    start()
else:
    print(f"Hey {data['login']['Username']} !")
    login()
