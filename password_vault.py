from cryptography.fernet import Fernet
import os
import getpass
import re

# Load or create the encryption key
def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
fernet = Fernet(key)

CREDENTIALS_FILE = "vault.txt"

# Save encrypted credential
def encrypt_and_store(site, username, password):
    data = f"{site}|{username}|{password}"
    encrypted = fernet.encrypt(data.encode())
    with open(CREDENTIALS_FILE, "ab") as f:
        f.write(encrypted + b"\n")
    print("[+] Credential stored securely.")

# Read and decrypt all credentials
def read_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        print("[-] No credentials stored yet.")
        return
    with open(CREDENTIALS_FILE, "rb") as f:
        lines = f.readlines()
        for line in lines:
            try:
                decrypted = fernet.decrypt(line.strip()).decode()
                site, username, password = decrypted.split("|")
                print(f"Site: {site} | Username: {username} | Password: {password}")
            except:
                print("[-] Could not decrypt one entry.")

# Password strength checker
def password_strength(password):
    length = len(password) >= 8
    upper = re.search(r"[A-Z]", password)
    lower = re.search(r"[a-z]", password)
    digit = re.search(r"\d", password)
    symbol = re.search(r"\W", password)

    score = sum([length, bool(upper), bool(lower), bool(digit), bool(symbol)])
    levels = {
        5: "Strong",
        4: "Good",
        3: "Fair",
        2: "Weak",
        1: "Very Weak",
        0: "Very Weak"
    }
    print(f"[!] Password Strength: {levels[score]}")

# CLI menu
def menu():
    while True:
        print("\n--- Password Vault ---")
        print("1. Add New Credential")
        print("2. View Credentials")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            site = input("Enter site name: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            password_strength(password)
            encrypt_and_store(site, username, password)

        elif choice == "2":
            read_credentials()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
