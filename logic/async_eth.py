import asyncio
import httpx
import json
from web3 import Web3
import time
import logic.models
from operator import itemgetter


async def get_transactions(address):
    transaction_list = []

    async with httpx.AsyncClient() as client:
        eth_res, alt_res, nft_res = await asyncio.gather(
            client.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey=PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA'),
            client.get(f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock=0&endblock=999999999&sort=asc&apikey=PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA'),
            client.get(f'https://api.etherscan.io/api?module=account&action=tokennfttx&address={address}&startblock=0&endblock=999999999&sort=asc&apikey=PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA')
        )
      
        #  create a list for eth, erc20 & nft
        eth_result_text = eth_res.text
        eth_json = json.loads(eth_result_text)
        list_eth = eth_json['result']

        alt_result_text = alt_res.text
        alt_json = json.loads(alt_result_text)
        list_alt = alt_json['result']

        nft_result_text = nft_res.text
        nft_json = json.loads(nft_result_text)
        list_nft = nft_json['result']

        # combining lists
        combined_transaction_list = list_eth + list_alt + list_nft

        # formatting data
        for transaction in combined_transaction_list:
            data = {
                'time': time.strftime("%d-%m-%Y",
                                      time.localtime(
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
                                 * int(transaction['gasUsed']), 'ether'), 6)),
                'token_name': 'Ethereum',
                'token_symbol': 'ETH',
                'contract_address': '',
                'token_id': ''
            }

            try:
                if transaction['tokenName']:
                    data['token_name'] = transaction['tokenName']
            except KeyError:
                print("Exception")

            try:
                if transaction['tokenSymbol']:
                    data['token_symbol'] = transaction['tokenSymbol']
            except KeyError:
                print("Exception")
        
            try:
                if transaction['contractAddress']:
                    data['contract_address'] = transaction['contractAddress']
            except KeyError:
                print("Exception")

            try:
                if transaction['tokenID']:
                    data['token_id'] = transaction['tokenID']
            except KeyError:
                print("Exception")

            transaction_list.append(data)
            # add transactions to db using Account method
            logic.models.Account().add_transactions(data)

        # sort combined list by time/date
        transaction_list.sort(reverse=True, key=itemgetter('time'))

        return transaction_list

