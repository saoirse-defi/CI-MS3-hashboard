import json
from web3 import Web3
import time
import logic.models
# from operator import itemgetter
import requests


def sortTime(e):
    return e['time']


def get_transactions(address):
    ''' Queries Etherscan API with ethereum address.
        Returns transaction list. '''

    transaction_list = []
    eth_res = ""
    erc_res = ""
    nft_res = ""
    list_eth = []
    list_erc = []
    list_nft = []
    count = 0

    try:
        eth_res = requests.get(
            f'https://api.etherscan.io/api?module=account'
            f'&action=txlist&address={address}&startblock'
            f'=0&endblock=99999999&sort=desc&apikey='
            f'PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA')
        erc_res = requests.get(
            f'https://api.etherscan.io/api?module=account'
            f'&action=tokentx&address={address}&startblock'
            f'=0&endblock=999999999&sort=desc&apikey='
            f'PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA')
        nft_res = requests.get(
            f'https://api.etherscan.io/api?module=account'
            f'&action=tokennfttx&address={address}&startblock'
            f'=0&endblock=999999999&sort=desc&apikey='
            f'PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA')

        eth_result_text = eth_res.text
        eth_json = json.loads(eth_result_text)
        list_eth = eth_json['result']

        erc_result_text = erc_res.text
        erc_json = json.loads(erc_result_text)
        list_erc = erc_json['result']

        nft_result_text = nft_res.text
        nft_json = json.loads(nft_result_text)
        list_nft = nft_json['result']

        complete_transaction_list = list_eth + list_erc + list_nft

        for transaction in complete_transaction_list:
            if count < 750:
                data = {
                    'time': time.strftime(
                        "%Y-%m-%d", time.localtime(
                            int(transaction['timeStamp']))),
                    'hash': transaction['hash'],
                    'from': transaction['from'],
                    'to': transaction['to'],
                    'value': str(round(Web3.fromWei(
                                    float(transaction['value']), 'ether'), 5)),
                    'gas_price': str(int(Web3.fromWei(
                                    int(transaction['gasPrice']), 'ether')
                                    * int('1000000000'))),
                    'gas_used': str(round(Web3.fromWei(
                                    int(transaction['gasPrice'])
                                    * int(transaction['gasUsed']),
                                    'ether'), 6)),
                    'token_name': 'Ethereum',
                    'token_symbol': 'ETH',
                    'contract_address': '',
                    'token_id': ''
                }

                try:
                    if transaction['tokenName']:
                        data['token_name'] = transaction['tokenName']
                except KeyError:
                    pass

                try:
                    if transaction['tokenSymbol']:
                        data['token_symbol'] = transaction['tokenSymbol']
                except KeyError:
                    pass

                try:
                    if transaction['c_address']:
                        data['contract_address'] = transaction['c_address']
                except KeyError:
                    pass

                try:
                    if transaction['tokenID']:
                        data['token_id'] = transaction['tokenID']
                except KeyError:
                    pass

                transaction_list.append(data)
                # add transactions to db using Account method
                logic.models.Account().add_transactions(data)

                count += 1
            else:
                break

        return transaction_list

    except Exception as e:
        raise Exception(e)
