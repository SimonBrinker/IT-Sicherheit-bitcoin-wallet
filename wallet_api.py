import blockcypher

apiKey = "bd9e04309cd84cc49cc3dec85f17ee88"

def get_wallet_balance(address, isMainnet:bool):
    coin_symbol = "btc"
    if not isMainnet:
        coin_symbol = 'btc-testnet'
    
    return blockcypher.get_total_balance(address, coin_symbol=coin_symbol, api_key=apiKey)