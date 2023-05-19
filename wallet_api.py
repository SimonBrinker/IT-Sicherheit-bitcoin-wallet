import blockcypher
from wallet import Wallet,Network

apiKey = "bd9e04309cd84cc49cc3dec85f17ee88"
useApi = False

def get_wallet_balance(wallet:Wallet):
    if not useApi:
        return 0.0001
    
    satoshis = blockcypher.get_total_balance(wallet.get_address_string(), coin_symbol=wallet.network.value, api_key=apiKey)
    
    return blockcypher.satoshis_to_btc(satoshis)

def get_transactions(wallet:Wallet):
    if not useApi:
        return None
    
    transactions = blockcypher.get_address_full(wallet.get_address_string(), coin_symbol=wallet.network.value, api_key=apiKey)

    return transactions

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