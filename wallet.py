import ecdsa
import base58
import hashlib
import binascii
import secrets
from enum import Enum
import struct
import copy

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

    # Generiert aus dem Private Key einen Public Key von dem sich nicht auf den Private Key zurückschließen lässt
    def private_Key_To_Public_Key(self, s):
        # Dafür wird der ECDSA (Elliptic Curve Digital Signature Algorithm) genutzt
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(s), curve=ecdsa.SECP256k1)
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

    # Generiert aus dem Public Key die Public Adresse
    def get_pubkey_hash(self, public_key):
        # Als erstes wird die SHA256 Hashfunktion auf den Public Key angewendet
        address = hashlib.sha256(public_key).digest()

        # Danach wird ein neues Hash-Objekt vom Typ Ripemd160 erzeugt und als h gespeichert
        h = hashlib.new('ripemd160')

        # Darauf folgend wird der gehashte Public Key noch einmal gehasht diesmal von der Ripemd160 Hashfunktion
        h.update(address)

        # Der Hashwert wird aus dem Hashobjekt h in die Variable h gespeichert und returned
        address = h.digest()

        return address

    #endregion

    #region Transaction
    # Ist die Methode für den "Pay to Public Key Hash"
    def get_p2pkh_script(self, b58_address:str):

        # Fügt Hex Wert als Byte der Variable script hinzu
        script = bytes.fromhex("76a914")
        
        decoded_address = base58.b58decode(b58_address)
        binary_address = decoded_address[1:-4]
        script += binary_address

        # Fügt noch einen Hexwert als Bytes der Variable Script hinzu und gibt diese zurück
        script += bytes.fromhex("88ac")
        return script

    # Fügt die eingegebenen Daten plus ein Paar extra Daten in ein Dictionary
    def get_raw_transaction(self, from_addr:bytes, to_addr:str, transaction_hash:list, satoshis_spend:int, amount_to_self:int):

        # Erstellt das Dictionary und fügt ein paar daten hinzu
        # Für einige Daten werden oben schon beschriebene Methoden genutzt für andere werden Standartiesierte Daten verwendet
        transaction = {}
        transaction["version"] = 1
        transaction["num_inputs"] = len(transaction_hash)
        transaction["transaction_hash"] = []
        transaction["output_index"] = []
        transaction["sig_script_length"] = []
        transaction["sig_script"] = []
        transaction["sequence"] = []
        for i, txid in enumerate(transaction_hash):
            transaction["transaction_hash"].append(bytes.fromhex(txid['tx_hash'])[::-1])
            transaction["output_index"].append(txid['tx_output_n'])
            transaction["sig_script_length"].append(25)
            transaction["sig_script"].append(self.get_p2pkh_script(self.get_address_string()))
            transaction["sequence"].append(0xffffffff)
        
        transaction["num_outputs"] = 1
        transaction["satoshis"] = []
        transaction["pubkey_length"] = []
        transaction["pubkey_script"] = []
        transaction["satoshis"].append(satoshis_spend)
        transaction["pubkey_length"].append(25)
        transaction["pubkey_script"].append(self.get_p2pkh_script(to_addr))
        if amount_to_self > 0:
            transaction["satoshis"].append(amount_to_self)
            transaction["pubkey_length"].append(25)
            transaction["pubkey_script"].append(self.get_p2pkh_script(self.get_address_string()))
            transaction["num_outputs"] = 2
        transaction["lock_time"] = 0
        transaction["hash_code_type"] = 1

        # Gibt das Dicitonary zurück
        return transaction

    # Verpackt die Daten aus dem Dicitonary in die Richtigen Formate
    def get_packed_transaction(self, transaction_dict):

        # Hier wertden einige Daten aus dem Dicitonary in der Richtigen Binärdatenfolge gespeichert
        # "<" sateht für "Little-Endian" Byte folge und das "L" für eubeb 4 Byte Unsigned integer
        # Da es zu viel aufwand wird werde ich nicht auf alle verschiedenen Binärfolgen eingehen
        raw_transaction  = struct.pack("<L", transaction_dict["version"])
        raw_transaction += struct.pack("<B", transaction_dict["num_inputs"])
        for i in range(transaction_dict["num_inputs"]):
            tx_in  = struct.pack("32s", transaction_dict["transaction_hash"][i])
            tx_in += struct.pack("<L", transaction_dict["output_index"][i]) 
            tx_in += struct.pack("<B", transaction_dict["sig_script_length"][i])
            tx_in += struct.pack(str(transaction_dict["sig_script_length"][i]) + "s", transaction_dict["sig_script"][i])
            tx_in += struct.pack("<L", transaction_dict["sequence"][i])
            
            # tx_in wird an raw_transacton angehängt
            raw_transaction += tx_in

        raw_transaction += struct.pack("<B", transaction_dict["num_outputs"]) 
        for i in range(transaction_dict["num_outputs"]): 
            tx_out  = struct.pack("<q", transaction_dict["satoshis"][i])
            tx_out += struct.pack("<B", transaction_dict["pubkey_length"][i])
            tx_out += struct.pack("25s", transaction_dict["pubkey_script"][i]) 

            # tx_out wird an raw_transacton angehängt
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

        # Die Transaction wird dann mit der SHA256 Hashfunktion gehashed und abgespeichert
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

    def signe_transaction(self, transaction_dict, private_key):
        for i in range(transaction_dict['num_inputs']):
            temp_dict = copy.deepcopy(transaction_dict)
            for j in range(temp_dict['num_inputs']):
                if not j==i:
                    temp_dict['sig_script_length'][j] = 0
                    temp_dict['sig_script'][j] = bytes.fromhex("00")
                #print(temp_dict)
            signature = self.get_transaction_signature(temp_dict, private_key)
            transaction_dict["sig_script_length"][i] = len(signature)
            transaction_dict["sig_script"][i] = signature
        #print(transaction_dict)
        return transaction_dict

    # Diese Methode erstellt eine Signed Transaction mithilfe der oben Beschriebenen Methoden
    def get_signed_transaction(self, to_addr:str, transaction_hash, amount_in_satoshis, return_to_self_amount):
        from_addr = self.address
        from_private_key = self.private_key
        # Es werden durch die oben gezeigten Methoden eine raw transaction erstellt und diese kriegt eine Signatur
        raw = self.get_raw_transaction(from_addr, to_addr, transaction_hash, amount_in_satoshis, return_to_self_amount)
        
        # # Es werden noch ein paar Einträge dem Dictionary hinzugefügt bevor die Transaction verpackt und zurück gegeben wird

        raw = self.signe_transaction(raw, from_private_key)
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

    def send_transaction(self, target_address, amount_in_btc) -> tuple[bool, str]:
        amount_in_satoshis = int(round(float(amount_in_btc) * 100000000))
        import wallet_api

        fee_amount = wallet_api.get_transaction_fee(self)
        available_tx = wallet_api.get_spendable_transactions(self)
        if len(available_tx) == 0:
            print(f"Not enough funds")
            Exception("Not enough funds")
            return (False, "Nicht genug Guthaben")
        needed_amount = amount_in_satoshis + fee_amount
        tx_ids, change = self.select_outputs_greedy(available_tx, needed_amount)
        if tx_ids is None:
            print(f"Not enough funds")
            return (False, "Nicht genug Guthaben")
        
        #print(f"Txs to spend: {tx_ids}\nChange: {change}")
        return_to_self_amount = change - fee_amount

        # generate the transaction
        transaction_hex = self.get_signed_transaction(target_address, tx_ids, amount_in_satoshis, return_to_self_amount).hex()
        #print(f"\n\nTX hash:\n{transaction_hex}\n")
        # send the transaction
        res = wallet_api.send_transaction(self, transaction_hex)
        if 'error' in res:
            print(f"Error sending transaction:{res['error']}")
            Exception("Error sending transaction")
            return (False, res['error'])
        print(f"Sending tranaction res: {res}")
        return (True, "Erfolg")

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