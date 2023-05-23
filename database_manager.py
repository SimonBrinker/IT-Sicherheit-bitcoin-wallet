import sqlite3
from wallet import Wallet, Network
from Cryptodome.Cipher import AES
import hashlib
import os
import typing
import ecdsa

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

def register(username:str, password:str, network:Network, createNew:bool, private_key="") -> typing.Tuple[bool | Wallet, str]:
    setup()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is not None:
        print(f"User with username '{username}' alredy exists")
        return (False, f"Benutzer existiert schon")
    #check if the private key is valid
    if not private_key == "":
        if not validate_private_key(private_key):
            return (False, "Private Key ist nicht gültig")
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, network.value))
    wallet = Wallet(username, network, createNew, private_key)
    store_private_key(username, password, wallet.private_key)
    connection.commit()

    return (wallet, "Erfolg")

def login(username:str, password:str) -> Wallet:
    setup()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        #Kein Benutzer
        return False
    
    network:Network
    if result[1] == Network.TESTNET.value:
        network = Network.TESTNET
    else:
        network = Network.MAINNET
    if result is not None:
        private_key = load_private_key(username, password)
        if private_key:
            return Wallet(username, network, False, private_key)
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
    with open(path_to_key_folder(username), "rb") as file:
        nonce, tag, ciphertext = [ file.read(x) for x in (16, 16, -1) ]
        
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

def validate_private_key(private_key):
    # Check length
    if len(private_key.strip()) != 64:
        return False

    # Check hexadecimal format
    if not all(c in '0123456789abcdefABCDEF' for c in private_key):
        return False

    #  Check for zero or all-one values
    if private_key.strip('0') == '' or private_key.strip('F') == '':
        return False

    # Calculate public key
    try:
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    except:
        return False
    return True

def main():
    setup()
    username = "Simon"
    password = "12345"
    register(username, password, Network.TESTNET, True)
    wallet = login(username,password)
    print(wallet)
    close()

if __name__ == "__main__":
    main()