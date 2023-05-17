import blockcypher
from wallet import Wallet,Network

apiKey = "bd9e04309cd84cc49cc3dec85f17ee88"
useApi = False

def get_wallet_balance(wallet:Wallet):
    if not useApi:
        return 0.0001
    satoshis = blockcypher.get_total_balance(wallet.get_address_string(), coin_symbol=wallet.network.value, api_key=apiKey)
    return blockcypher.satoshis_to_btc(satoshis)
