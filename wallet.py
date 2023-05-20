import ecdsa
import base58
import hashlib
import binascii
import secrets
from enum import Enum
import struct

class Network(Enum):
    MAINNET = "btc"
    TESTNET = "btc-testnet"

class Wallet(object):
    def __init__(self, username:str, network:Network, create_new:bool, private_key = ""):
        self.username = username
        self.network = network
        if create_new:
            self.private_key = secrets.token_hex(32)
        else:
            self.private_key = private_key
        
        self.public_key = self.get_public_key()
        self.address = self.get_public_address()


    #region Keys

    # Generiert aus dem Private Key einen Public Key von dem sich nicht auf den Private Key zurückschließen lässt
    def get_public_key(self):
        # Dafür wird der ECDSA (Elliptic Curve Digital Signature Algorithm) genutzt
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(self.private_key), curve=ecdsa.SECP256k1)
        # Zudem bekommt der Private Key noch den Prefix 04
        return (bytes.fromhex("04") + sk.verifying_key.to_string())

    # Generiert die Testnet Adresse aus dem Public Key
    def get_public_address(self):

        if self.network == Network.TESTNET:
            # Speichert das Prefix Byte (0x6f) in eine Variable, dieses Prefix Byte wird dazu genutzt zu zeigen das es sich um eine Testnet Adresse handelt
            prefix = b'\x6f'
        else:
            prefix = b'\x00'

        # Als erstes wird die SHA256 Hashfunktion auf den Public Key angewendet
        hash_1 = hashlib.sha256(self.public_key).digest()

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

    #endregion

    #region Transaction
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
    def get_raw_transaction(self, from_addr:bytes, to_addr:bytes, transaction_hash, output_index, satoshis_spend):

        # Erstellt das Dictionary und fügt ein paar daten hinzu
        # Für einige Daten werden oben schon beschriebene Methoden genutzt für andere werden Standartiesierte Daten verwendet
        transaction = {}
        transaction["version"] = 1
        transaction["num_inputs"] = 1

        transaction["transaction_hash"] = bytes.fromhex(transaction_hash)[::-1]
        transaction["output_index"] = output_index

        transaction["sig_script_length"] = 25
        transaction["sig_script"] = self.get_p2pkh_script(from_addr)

        transaction["sequence"] = 0xffffffff
        transaction["num_outputs"] = 1
        transaction["satoshis"] = satoshis_spend
        transaction["pubkey_length"] = 25
        transaction["pubkey_script"] = self.get_p2pkh_script(to_addr)
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
    def get_transaction_signature(self, transaction, private_key):

        # Hier wird die transaction gepacked und in einer Variable gespeichert
        packed_raw_transaction = self.get_packed_transaction(transaction)

        # Die Transaction wird dann mit der SHA256 Hashfunktion gehast und abgespeichert
        hash = hashlib.sha256(hashlib.sha256(packed_raw_transaction).digest()).digest()

        # Man generiert via Methoden den Public Key aus dem Private Key
        public_key = self.private_Key_To_Public_Key(private_key)

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
    def get_signed_transaction(self, to_addr, transaction_hash, output_index, satoshis):
        from_addr = self.address
        from_private_key = self.private_key
        # Es werden durch die oben gezeigten Methoden eine raw transaction erstellt und diese kriegt eine Signatur
        raw = self.get_raw_transaction(from_addr, to_addr, transaction_hash, output_index, satoshis)
        signature = self.get_transaction_signature(raw, from_private_key)
        
        # Es werden noch ein paar Einträge dem Dictionary hinzugefügt bevor die Transaction verpackt und zurück gegeben wird
        raw["sig_script_length"] = len(signature)
        raw["sig_script"] = signature
        del raw["hash_code_type"]

        return self.get_packed_transaction(raw)
    

    # Wählt die txids aus die für eine transaktion verwendet werden sollen
    # Von: https://www.oreilly.com/library/view/mastering-bitcoin/9781491902639/ch05.html
    def select_outputs_greedy(self, unspent, min_value):
        # Fail if empty.
        if not unspent:
            return None
        # Partition into 2 lists.
        lessers = [utxo for utxo in unspent if utxo['value'] < min_value]
        greaters = [utxo for utxo in unspent if utxo['value'] >= min_value]
        key_func = lambda utxo: utxo['value']
        if greaters:
            # Not-empty. Find the smallest greater.
            min_greater = min(greaters)
            change = min_greater['value'] - min_value
            return [min_greater], change
        # Not found in greaters. Try several lessers instead.
        # Rearrange them from biggest to smallest. We want to use the least
        # amount of inputs as possible.
        lessers.sort(key=key_func, reverse=True)
        result = []
        accum = 0
        for utxo in lessers:
            result.append(utxo)
            accum += utxo['value']
            if accum >= min_value:
                change = accum - min_value
                return result, change
        # No results found.
        return None, 0

    #endregion

    #region strings

    def get_address_string(self) -> str:
        return self.address.decode()

    #endregion

    def send_transaction(self, target_address, amount_in_btc):
        amount_in_satoshis = int(round(float(amount_in_btc) * 100000000))
        import wallet_api

        available_tx = wallet_api.get_spendable_transactions(self)

        tx_ids, change = self.select_outputs_greedy(available_tx, amount_in_satoshis)
        if tx_ids is None:
            print(f"Not enough funds")
            return
        
        print(f"Txs to spend: {tx_ids}\nChange: {change}")


        # generate the transaction
        transaction_hex = self.get_signed_transaction()
        print(f"\n\nTX hash:\n{transaction_hex}\n")
        # send the transaction
        # wallet_api.send_transaction(transaction_hex)

    def __str__(self) -> str:
        res = ""
        res += "BTC-Private-Key: " + self.private_key + "\n"
        res += "BTC-Public-Key: " + self.public_key.hex() + "\n"
        res += "BITCOIN PUBLIC ADDRESS: " + self.address.decode('utf-8') + "\n"
        return res


# To check address:
# https://www.bitaddress.org/bitaddress.org-v3.3.0-SHA256-dec17c07685e1870960903d8f58090475b25af946fe95a734f88408cef4aa194.html?testnet=true

def main():
    wallte = Wallet(Network.TESTNET, True)
    print(wallte)

if __name__ == "__main__":
    main()