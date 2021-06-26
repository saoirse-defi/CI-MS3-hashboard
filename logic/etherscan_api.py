from flask import request
import requests
import time
from web3 import Web3
from statistics import mode


def etherscan_transactions(address):
    API_KEY = "PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA"

    url = "https://api.etherscan.io/api?module=account&action=txlist&address=" + address + "&startblock=0&endblock=99999999&sort=asc&apikey=" + API_KEY
          
    response = requests.get(url)
    response_json = response.json()
    transactions = response_json.get("result")

    transaction_list = []

    for transaction in transactions:
        data = {
            'time': time.strftime("%Y-%m-%d %H:%M", time.localtime(int(transaction['timeStamp']))),
            'hash': transaction['hash'],
            'from': transaction['from'],
            'to': transaction['to'],
            'value': Web3.fromWei(float(transaction['value']), 'ether'),  # in Gwei
            'error': transaction['isError'],
            'gas_price': Web3.fromWei(int(transaction['gasPrice']), 'ether') * int('1000000000'),
            'gas_used': round(Web3.fromWei(int(transaction['gasPrice']) * int(transaction['gasUsed']), 'ether'), 6),
            'starred': False
        }
        transaction_list.append(data)
    
    return transaction_list


def erc20_transactions(address):
    API_KEY = "PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA"
    url = "https://api.etherscan.io/api?module=account&action=tokentx&address=" + address + "&startblock=0&endblock=999999999&sort=asc&apikey=" + API_KEY

    response = requests.get(url)
    response_json = response.json()
    erc20 = response_json.get("result")

    erc20_transaction_list = []

    for transaction in erc20:
        data = {
            'time': time.strftime("%Y-%m-%d %H:%M", time.localtime(int(transaction['timeStamp']))),
            'hash': transaction['hash'],
            'from': transaction['from'],
            'to': transaction['to'],
            'value': Web3.fromWei(float(transaction['value']), 'ether'),  # in Gwei
            'gas_price': Web3.fromWei(int(transaction['gasPrice']), 'ether') * int('1000000000'),
            'gas_used': round(Web3.fromWei(int(transaction['gasPrice']) * int(transaction['gasUsed']), 'ether'), 6),
            'token_name': transaction['tokenName'],
            'token_symbol': transaction['tokenSymbol'],
            'contract_address': transaction['contractAddress']
        }

        erc20_transaction_list.append(data)
    
    return erc20_transaction_list


def nft_transactions(address):
    API_KEY = "PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA"
    url = "https://api.etherscan.io/api?module=account&action=tokennfttx&address=" + address + "&startblock=0&endblock=999999999&sort=asc&apikey=" + API_KEY

    response = requests.get(url)
    response_json = response.json()
    erc721 = response_json.get("result")

    erc721_transaction_list = []

    for transaction in erc721:
        data = {
            'time': time.strftime("%Y-%m-%d %H:%M", time.localtime(int(transaction['timeStamp']))),
            'hash': transaction['hash'],
            'from': transaction['from'],
            'to': transaction['to'],
            'gas_price': Web3.fromWei(int(transaction['gasPrice']), 'ether') * int('1000000000'),
            'gas_used': round(Web3.fromWei(int(transaction['gasPrice']) * int(transaction['gasUsed']), 'ether'), 6),
            'token_name': transaction['tokenName'],
            'token_symbol': transaction['tokenSymbol'],
            'contract_address': transaction['contractAddress'],
            'token_id': int(transaction['tokenID'])
        }

        erc721_transaction_list.append(data)
    
    return erc721_transaction_list


def etherscan_gas():
    API_KEY = "PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA"
    url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=" + API_KEY

    response = requests.get(url)
    response_json = response.json()
    gas_price_dict = response_json.get("result")

    return gas_price_dict


def find_total_gas_spent(items):
    total = 0
    for item in items:
        total += item['gas_used']
    
    return round(total, 3)


def find_highest_gas(items):
    highest_gas = 0
    for item in items:
        if(highest_gas < item['gas_price']):
            highest_gas = item['gas_price']
    
    return highest_gas


def find_average_gas(items):
    total = 0
    for item in items:
        total += item['gas_price']
 
    average = total / len(items)
    return round(average, 0)


def find_fav_coins(items):
    coins = []
    for item in items:
        coins.append(item['token_symbol'])
    
    fav_coins = list(dict.fromkeys(coins))  # new list containing no duplicates
    return fav_coins

    
def find_fav_coin_names(items):
    coins = []
    for item in items:
        coins.append(item['token_name'])
    
    fav_coins = list(dict.fromkeys(coins))  # new list containing no duplicates
    return fav_coins


def find_fav_token(items):
    coins = []
    for item in items:
        coins.append(item['token_name'])
    
    return mode(coins)