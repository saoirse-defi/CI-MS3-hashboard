# Imports
import os
import uuid
import asyncio
import json
import httpx
import time
from os import path
from operator import itemgetter
from web3 import Web3
if os.path.exists("env.py"):
    import env

from flask import Flask, render_template, flash, redirect, request, session, url_for, send_from_directory
from flask_pymongo import PyMongo
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import logic.models
import logic.etherscan_api

# Application setup

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SESSION_TYPE"] = 'filesystem'
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

transaction_table_headings = ['Date created', 'Hash', 'To', 'From', 'Value', 'Token Involved', 'Gas Price (GWEI)', 'Gas Spent (ETH)', 'Favourite']

# Decorator Functions

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

# Formatting functions

def shorten(string):  # formatting functions
    return "0x..." + string[38:]
    
def shorten2(string):
    return "0x..." + string[62:]

def toInt(x):
    return int(float(x))

def threeDecimals(y):
    return "%.3f" % y


# Routes

@app.route("/")
@app.route("/index")
@login_required
def index():
    transactions_list = list(mongo.db.Transaction.find({"from": session['user']['eth']})) # list of cursor query

    return render_template("index.html",
                            transactions_list=transactions_list,
                            transaction_table_headings=transaction_table_headings,
                            shorten=shorten,
                            shorten2=shorten2,
                            toInt=toInt,
                            threeDecimals=threeDecimals)


@app.route('/search', methods=['GET', 'POST'])
async def search():
    errors = {}
    transaction_list = []

    if request.method == 'POST':
        search_eth = str(request.form.get('search-eth')).lower()
        print(search_eth)

        async with httpx.AsyncClient() as client:
            eth_res, alt_res, nft_res = await asyncio.gather(
                client.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={search_eth}&startblock=0&endblock=99999999&sort=asc&apikey=PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA'),
                client.get(f'https://api.etherscan.io/api?module=account&action=tokentx&address={search_eth}&startblock=0&endblock=999999999&sort=asc&apikey=PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA'),
                client.get(f'https://api.etherscan.io/api?module=account&action=tokennfttx&address={search_eth}&startblock=0&endblock=999999999&sort=asc&apikey=PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA')
            )

            # search_result = await client.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={search_eth}&startblock=0&endblock=99999999&sort=asc&apikey=PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA')
        
        eth_result_text = eth_res.text  # process repsonses into python list
        eth_json = json.loads(eth_result_text)
        list_eth = eth_json['result']

        alt_result_text = alt_res.text  # process repsonses into python list
        alt_json = json.loads(alt_result_text)
        list_alt = alt_json['result']

        nft_result_text = nft_res.text  # process repsonses into python list
        nft_json = json.loads(nft_result_text)
        list_nft = nft_json['result']

        combined_transaction_list = list_eth + list_alt + list_nft  # combining lists

        for transaction in combined_transaction_list:  # formatting data
            data = {
                'time': time.strftime("%Y-%m-%d %H:%M", time.localtime(int(transaction['timeStamp']))),
                'hash': transaction['hash'],
                'from': transaction['from'],
                'to': transaction['to'],
                'value': str(Web3.fromWei(float(transaction['value']), 'ether')),
                'gas_price': str(Web3.fromWei(int(transaction['gasPrice']), 'ether') * int('1000000000')),
                'gas_used': str(round(Web3.fromWei(int(transaction['gasPrice']) * int(transaction['gasUsed']), 'ether'), 6)),
                'token_name': 'Ethereum',  # not working
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
        
        transaction_list.sort(reverse=True, key=itemgetter('time'))  # sort combined list by time/date

        print(transaction_list)

    return render_template("search.html", 
                            errors=errors, 
                            shorten=shorten,
                            shorten2=shorten2,
                            toInt=toInt,
                            threeDecimals=threeDecimals,
                            transaction_list=transaction_list,  # get this error only sometimes UnboundLocalError: local variable 'transaction_list' referenced before assignment Traceback (most recent call last)
                            transaction_table_headings=transaction_table_headings)


@app.route('/_save_transaction')  # background process in order to save transaction to Account fav list
def _save_transaction(data):
    logic.models.Account().fav(data)
    return redirect(url_for('search'))


@app.route('/signup2', methods=['GET', 'POST'])
def signup2():
    if request.method == 'POST':
        logic.models.Account().signup()
        return redirect(url_for('index'))
    return render_template("signup2.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logic.models.Account().login()
        return redirect(url_for('index'))

    return render_template("login.html")


@app.route('/signout')
@login_required
def signout():
    return logic.models.Account().signout()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# App config


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
