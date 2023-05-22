import blockcypher # Import des Moduls blockcypher
import wallet # Import des Moduls wallet

api_key = "bd9e04309cd84cc49cc3dec85f17ee88" # API-Schlüssel für die Verbindung mit Blockcypher
use_api = True # Flag, um zu bestimmen, ob die API verwendet werden soll

# Diese Funktion gibt den Kontostand des Wallets zurück.
def get_wallet_balance(wallet:wallet.Wallet):
    if not use_api:
        return 0.0001 # Rückgabe eines Standardwerts, wenn use_api False ist
    
    # Abrufen des Kontostands in Satoshis über die Blockcypher-API mit der angegebenen Wallet
    satoshis = blockcypher.get_confirmed_balance(wallet.get_address_string(), coin_symbol=wallet.network.value, api_key=api_key)
    
    # Umrechnung des Kontostands von Satoshis in BTC und Rückgabe
    return blockcypher.satoshis_to_btc(satoshis)

# Diese Funktion ruft die Transaktionen eines Wallets über die Blockcypher-API ab.
def get_transactions(wallet:wallet.Wallet):
    
    # Abrufen der Transaktionen über die Blockcypher-API mit der angegebenen Public adress
    transactions = blockcypher.get_address_full(wallet.get_address_string(), coin_symbol=wallet.network.value, api_key=api_key)

    return transactions # Rückgabe der abgerufenen Transaktionen

# Diese Funktion ruft die noch nicht ausgegebenen Transaktionen eines Wallets über die Blockcypher-API ab.
def get_spendable_transactions(wallet:wallet.Wallet):

    # Nur noch nicht ausgegebene Transaktionen werden zurückgegeben
    return blockcypher.get_address_details(wallet.get_address_string(), api_key = api_key, coin_symbol = wallet.network.value, unspent_only = True)['txrefs']

# Diese Funktion boradcastet eine Transaktion über die Blockcypher-API.
def send_transaction(wallet:wallet.Wallet, transaction_hash) -> dict:

    # Rückgabe der Ergebnisse als Dictionary
    return blockcypher.pushtx(transaction_hash, coin_symbol = wallet.network.value, api_key = api_key)

# Diese Funktion gibt die Transaktionsgebühr für eine Wallet über die Blockcypher-API zurück.
def get_transaction_fee(wallet:wallet.Wallet):

    # Abrufen der Transaktionsgebühren über die Blockcypher-API für das angegebene Network
    fees = blockcypher.get_blockchain_fee_estimates(coin_symbol=wallet.network.value, api_key=api_key)

    # Rückgabe der niedrigsten Gebühr pro Kilobyte (KB), aufgeteilt durch 4 nach unten abgerundet
    return fees['low_fee_per_kb'] // 4