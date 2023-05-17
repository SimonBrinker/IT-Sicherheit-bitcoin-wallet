import sqlite3
from wallet import Wallet, Network
from Cryptodome.Cipher  import AES
import hashlib
import os

connection:sqlite3.Connection
cursor:sqlite3.Cursor
is_setup:bool = False
data_folder = "data"

def setup():
    global connection
    global cursor
    global is_setup
    if is_setup:
        return
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    connection = sqlite3.connect(os.path.join(data_folder, "database.db"))
    cursor = connection.cursor()
    create_table()
    is_setup = True

def create_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, network TEXT)")

def register(username:str, password:str, network:Network):
    setup()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is not None:
        print(f"User with username '{username}' alredy exists")
        return False
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, network.value))
    wallet = Wallet(username, network, True)
    store_private_key(username, password, wallet.private_key)
    connection.commit()

    return wallet

def login(username:str, password:str) -> Wallet:
    setup()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is not None:
        private_key = load_private_key(username, password)
        if private_key:
            return Wallet(username, result[1], False, private_key)
    return False

def close():
    global is_setup
    is_setup = False
    connection.commit()
    connection.close()

def store_private_key(username:str, password:str, private_key:str):
    file = open(path_to_key_folder(username), "wb")
    key = password_to_AES_key(password)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(private_key.encode())
    [ file.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file.close()

def load_private_key(username:str, password:str):
    if not os.path.exists(data_folder):
        return False
    file = open(path_to_key_folder(username), "rb")

    nonce, tag, ciphertext = [ file.read(x) for x in (16, 16, -1) ]
    file.close()
    key = password_to_AES_key(password)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data.decode()

    except ValueError:
        print("Password is wrong")
        return False
    
def password_to_AES_key(password:str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def path_to_key_folder(username:str) -> str:
    folder = os.path.join(data_folder, "users")
    if not os.path.exists(folder):
        os.makedirs(folder)
    return os.path.join(folder, username + ".bin")

def main():
    setup()
    username = "Simon"
    password = "12345"
    register(username, password, Network.TESTNET)
    wallet = login(username,password)
    print(wallet)
    close()

if __name__ == "__main__":
    main()