import blockcypher
import wallet

api_key = "bd9e04309cd84cc49cc3dec85f17ee88"
use_api = True

def get_wallet_balance(wallet:wallet.Wallet):
    if not use_api:
        return 0.0001
    
    satoshis = blockcypher.get_confirmed_balance(wallet.get_address_string(), coin_symbol=wallet.network.value, api_key=api_key)
    
    return blockcypher.satoshis_to_btc(satoshis)

def get_transactions(wallet:wallet.Wallet):
    
    transactions = blockcypher.get_address_full(wallet.get_address_string(), coin_symbol=wallet.network.value, api_key=api_key)

    return transactions

def get_spendable_transactions(wallet:wallet.Wallet):

    return blockcypher.get_address_details(wallet.get_address_string(), api_key = api_key, coin_symbol = wallet.network.value, unspent_only = True)['txrefs']

def send_transaction(wallet:wallet.Wallet, transaction_hash) -> dict:
    return blockcypher.pushtx(transaction_hash, coin_symbol = wallet.network.value, api_key = api_key)

def get_transaction_fee(wallet:wallet.Wallet):
    fees = blockcypher.get_blockchain_fee_estimates(coin_symbol=wallet.network.value, api_key=api_key)
    return fees['low_fee_per_kb'] // 4

"""
    for transaction in transactions['txs']:
        print("Transaktionshash:", transaction['hash'])
        print("Bestätigungen:", transaction['confirmations'])
        print("Eingehende Transaktionen:")
        for input_tx in transaction['inputs']:
            print("  Von:", input_tx['addresses'][0])
            print("  Wert:", input_tx['output_value'])
        print("Ausgehende Transaktionen:")
        for output_tx in transaction['outputs']:
            print("  An:", output_tx['addresses'][0])
            print("  Wert:", output_tx['value'])
        if 'spent' in output_tx and output_tx['spent']:
            print("  Ausgabe bereits verbraucht")
        else:
            print("  Ausgabe noch nicht verbraucht")
        print("----------")"""