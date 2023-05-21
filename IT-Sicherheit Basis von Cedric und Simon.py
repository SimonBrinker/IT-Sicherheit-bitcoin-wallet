# -*- coding: utf-8 -*-
"""IT-Sicherheit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GsUGU67AOqA8NhYGm1H10G9eL2g8UJG1

# Dies ist das IT-Sicherheit Projekt von Cedric Kranz und Simon Brinker
###Matrikelnummer Cedric Kranz: 018335576
###Matrikelnummer Simon Brinker: 018335448

# Libarys zum erstellen des Wallets und zum Transferieren von Bitcoins
"""

# pip install ecdsa

# pip install base58

import secrets
import ecdsa
import random
import hashlib
import base58
import struct

"""# Wallet Informationen generieren"""

# Generiert aus dem Private Key einen Public Key von dem sich nicht auf den Private Key zurückschließen lässt
def private_Key_To_Public_Key(s):
    # Dafür wird der ECDSA (Elliptic Curve Digital Signature Algorithm) genutzt
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(s), curve=ecdsa.SECP256k1)
    # Zudem bekommt der Private Key noch den Prefix 04
    return (bytes.fromhex("04") + sk.verifying_key.to_string())

# Generiert aus dem Public Key die Public Adresse
def get_public_address(public_key):
    # Als erstes wird die SHA256 Hashfunktion auf den Public Key angewendet
    address = hashlib.sha256(public_key).digest()

    # Danach wird ein neues Hash-Objekt vom Typ Ripemd160 erzeugt und als h gespeichert
    h = hashlib.new('ripemd160')

    # Darauf folgend wird der gehashte Public Key noch einmal gehasht diesmal von der Ripemd160 Hashfunktion
    h.update(address)

    # Der Hashwert wird aus dem Hashobjekt h in die Variable h gespeichert und returned
    address = h.digest()

    return address

# Generiert die Testnet Adresse aus dem Public Key
def get_testnet_address(public_key):

    # Speichert das Prefix Byte (0x6f) in eine Variable, dieses Prefix Byte wird dazu genutzt zu zeigen das es sich um eine Testnet Adresse handelt
    prefix = b'\x6f'

    # Als erstes wird die SHA256 Hashfunktion auf den Public Key angewendet
    hash_1 = hashlib.sha256(public_key).digest()

    # Danach wird das Ergebnis mit der Hashfunktion Ripemd160 gehasht
    hash_2 = hashlib.new('ripemd160', hash_1).digest()

    # Fügt den Prefix hinzu
    prefix_hash = prefix + hash_2

    # Danach wird auf das Ergebnis zwei mal die SHA256 Hashfunktion angewendet
    hash_3 = hashlib.sha256(prefix_hash).digest()
    hash_4 = hashlib.sha256(hash_3).digest()

    # Fügt die ersten 4 Bytes vom vierten Hash dem Prefix + Ripemd160 hinzu
    address_bytes = prefix_hash + hash_4[:4]

    # Kodiert die Adress Bytes in Base58
    address = base58.b58encode(address_bytes)

    # Gibt die Adresse zurück
    return address

# 32 byte (256 bit) private key wird generiert
# from_private_key = secrets.token_hex(32)

# Wir benutzen vortan immer denselben Private Key zum Senden von Bitcoin nämlich den folgenden
from_private_key = "5193a511277489573f1e1a392debaa305441b4fd474ece51e451940c8f7dfe9d"
print("from private Key: " + str(from_private_key))

# 512 Bit Public Key wird generiert
from_public_key = private_Key_To_Public_Key(from_private_key)

# unkompriemierte Schlüssel starten mit 04, kompriemierte Schlüssen starten mit 02 oder 03
print("from public Key: " + from_public_key.hex())

# Sende Adresse wird aus dem Public Key generiert
from_address = get_testnet_address(from_public_key)
print("from-Address: " + str(from_address.decode('utf-8')))

# 32 byte (256 bit) private key wird generiert
# to_private_key = secrets.token_hex(32)

# Wir benutzen vortan immer denselben Private Key zum empfangen von Bitcoin nämlich den folgenden
to_private_key = "d69270374a80a77191fe2ee49e533c60c66db0af89f15f2fee6ab1aafd2c3438"

# Empfang Adresse wird aus dem Public Key generiert der aus dem Private Key generiert wird
to_address = get_testnet_address(private_Key_To_Public_Key(to_private_key))
print("to-Address: " + str(to_address.decode('utf-8')))

"""# Transaktion"""

# Ist die Methode für den "Pay to Public Key Hash"
def get_p2pkh_script(pub_key:bytes):

    # Fügt Hex Wert als Byte der Variable script hinzu
    script = bytes.fromhex("76a914")

    # Fügt den Public Key der Variable script hinzu
    script += pub_key

    # Fügt noch einen Hexwert als Bytes der Variable Script hinzu und gibt diese zurück
    script += bytes.fromhex("88ac")
    return script

# Fügt die eingegebenen Daten plus ein Paar extra Daten in ein Dictionary
def get_raw_transaction(from_addr:bytes, to_addr:bytes, transaction_hash, output_index, satoshis_spend):

    # Erstellt das Dictionary und fügt ein paar daten hinzu
    # Für einige Daten werden oben schon beschriebene Methoden genutzt für andere werden Standartiesierte Daten verwendet
    transaction = {}
    transaction["version"] = 1
    transaction["num_inputs"] = 1

    transaction["transaction_hash"] = bytes.fromhex(transaction_hash)[::-1]
    transaction["output_index"] = output_index

    transaction["sig_script_length"] = 25
    transaction["sig_script"] = get_p2pkh_script(from_addr)

    transaction["sequence"] = 0xffffffff
    transaction["num_outputs"] = 1
    transaction["satoshis"] = satoshis_spend
    transaction["pubkey_length"] = 25
    transaction["pubkey_script"] = get_p2pkh_script(to_addr)
    transaction["lock_time"] = 0
    transaction["hash_code_type"] = 1

    # Gibt das Dicitonary zurück
    return transaction

# Verpackt die Daten aus dem Dicitonary in die Richtigen Formate
def get_packed_transaction(transaction_dict):

    # Hier wertden einige Daten aus dem Dicitonary in der Richtigen Binärdatenfolge gespeichert
    # "<" sateht für "Little-Endian" Byte folge und das "L" für eubeb 4 Byte Unsigned integer
    # Da es zu viel aufwand wird werde ich nicht auf alle verschiedenen Binärfolgen eingehen
    raw_transaction  = struct.pack("<L", transaction_dict["version"])
    raw_transaction += struct.pack("<B", transaction_dict["num_inputs"])
    tx_in  = struct.pack("32s", transaction_dict["transaction_hash"])
    tx_in += struct.pack("<L", transaction_dict["output_index"]) 
    tx_in += struct.pack("<B", transaction_dict["sig_script_length"])
    tx_in += struct.pack(str(transaction_dict["sig_script_length"]) + "s", transaction_dict["sig_script"])
    tx_in += struct.pack("<L", transaction_dict["sequence"])
    
    # raw_transaction und tx_in wurden unterschiedlich formatiert und werden nun zusammengefügt
    raw_transaction += tx_in

    raw_transaction += struct.pack("<B", transaction_dict["num_outputs"]) 
    tx_out  = struct.pack("<q", transaction_dict["satoshis"])
    tx_out += struct.pack("<B", transaction_dict["pubkey_length"])
    tx_out += struct.pack("25s", transaction_dict["pubkey_script"]) 

    # raw_transaction und tx_out wurden unterschiedlich formatiert und werden nun zusammengefügt
    raw_transaction += tx_out
    raw_transaction += struct.pack("<L", transaction_dict["lock_time"])

    # falls das Dicitonary einen Hash code Type hat wird dieser auch formatiert und angehangen
    if "hash_code_type" in transaction_dict:
        raw_transaction += struct.pack("<L", transaction_dict["hash_code_type"])

    return raw_transaction

# Signiert die Transaktion
def get_transaction_signature(transaction, private_key):

    # Hier wird die transaction gepacked und in einer Variable gespeichert
    packed_raw_transaction = get_packed_transaction(transaction)

    # Die Transaction wird dann mit der SHA256 Hashfunktion gehast und abgespeichert
    hash = hashlib.sha256(hashlib.sha256(packed_raw_transaction).digest()).digest()

    # Man generiert via Methoden den Public Key aus dem Private Key
    public_key = private_Key_To_Public_Key(private_key)

    # Der Key wird durch den Private Key der via Ecdsa kodiert wird signiert
    key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)

    # Die Signatur wird in einer Variable gespeichert
    signature = key.sign_digest(hash, sigencode=ecdsa.util.sigencode_der_canonize)

    # Es wird noch der Hash code Type hinzugefügt
    signature += bytes.fromhex("01")

    # Die länge der Singatur, die Signatur, die Länge des Public Key und der Public Key werden aneinandergehangen
    sigscript = struct.pack("<B", len(signature))
    sigscript += signature
    sigscript += struct.pack("<B", len(public_key))
    sigscript += public_key

    # Die Signatur wird dann zurückgegeben
    return sigscript

# Diese Methode erstellt eine Signed Transaction mithilfe der oben Beschriebenen Methoden
def get_signed_transaction(from_addr, from_private_key, to_addr, transaction_hash, output_index, satoshis):

    # Es werden durch die oben gezeigten Methoden eine raw transaction erstellt und diese kriegt eine Signatur
    raw = get_raw_transaction(from_addr, to_addr, transaction_hash, output_index, satoshis)
    signature = get_transaction_signature(raw, from_private_key)
    
    # Es werden noch ein paar Einträge dem Dictionary hinzugefügt bevor die Transaction verpackt und zurück gegeben wird
    raw["sig_script_length"] = len(signature)
    raw["sig_script"] = signature
    del raw["hash_code_type"]

    return get_packed_transaction(raw)

"""# Testen der Transaktionen"""

# Hier werden Beispiel Daten erstellt und eingetragen und dann durch die oben genannten Methoden zu einer fertigen transaction verpackt und ausgegeben
txid_to_spent = "772abf33c6cbddaf5202aa344fcf69c92c730fcb48bc042add2b0b9191b01abe"

satoshis_to_spent = 1000
from_address = get_public_address(from_public_key)
to_public_key = private_Key_To_Public_Key(to_private_key)
to_address = get_public_address(to_public_key)
print(f"to_address: {to_address.hex()}")
signature = get_signed_transaction(from_address, from_private_key, to_address, txid_to_spent, 1, satoshis_to_spent)

print()
print("Transaction hex:")
print(signature.hex())

"""# Beschreibung der hier verwendeten Hash Algorithmen

**SHA256**
Der "secure hash algorithm " ist ein Algorithmus, der vom US-amerikanischen Nation Institute of Standarts standatisiert wurde. Er funktioniert indem die Nachricht über 64 Runden, mit viel logischen Funktionen mit anderen Konstanten gehasht wird

**RIPEMD-160**
Der "RACE Integrity Primitives Evaluation Message Digest" ist eine Hashfunktion die 1996 erstmals von Hans Dobbertin, Antoon Bosselaers und Bart Preneel in Europa entwickelt und publiziert wurde. Der Hashalgorithmus arbeitet auf 512 Bit Blöcken und führt zwei parallele Funktionen mit jeweils fünf Runden aus

**ECDSA**
Der "Elliptic Curve Digital Signature Algorithm" ist eine Variant des Digital Signature Algorithm. Für diesen Algorithmus muss man sich auf Kurvenparameter einigen diese werden hier von den erstellern des Bitcoin vorgegeben

# Bewertung der Hashfunktionen

Ich würde den SHA256 Algorithmus sicherer als den RIPEMD-160 einordnen, da er SHA256 Algorithmus Runden mit viel logischen Funktionen vornimmt während es bei dem RIPEMD-160 nur fünf Runden mit zwei Funktionen sind. Zudem gleicht sich der RIPEMD-160 Algorythmus dem veralteten SHA-1 Algorithmuswährendessen SHA256 zu der Gruppe der SHA-2 Algorithmen gehört die fortschrittlicher sind.
"""