import blockcypher
from wallet import Network

apiKey = "bd9e04309cd84cc49cc3dec85f17ee88"

def get_wallet_balance(address, network:Network):
    return blockcypher.get_total_balance(address, coin_symbol=network.value, api_key=apiKey)
