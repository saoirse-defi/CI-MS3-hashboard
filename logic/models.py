import uuid
import json
from flask import Flask, jsonify, session, redirect, request, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo
from run import mongo
from . import etherscan_api


class User(UserMixin):

    def signup(self):
        user = {
            "name": "",
            "email": "",
            "eth": "",
            "password": "",
            "password_confirm": ""
        }
        
        return jsonify(user), 200
    
    def is_active(self):
        return True
   
    def start_session(self, user):
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200
    
    def signout(self):
        session.clear()
        return redirect('/')


class Account():

    def signup(self):
        account = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "eth": request.form.get('eth'),
            "password": request.form.get('password')
        }

        account['password'] = generate_password_hash(account['password'])

        if(mongo.db.User.find_one({'email': account['email']})):
            return jsonify({'error': 'Email already in use.'})

        if mongo.db.User.insert_one(account):
            self.add_transactions(account)
            return self.start_session(account)

        return jsonify({'error': 'Signup failed'}), 400
    
    def start_session(self, account):
        del account['password']
        session['logged_in'] = True
        session['user'] = account

        return jsonify(account), 200

    def signout(self):
        session.clear()
        return redirect(url_for('login'))
    
    def login(self):
        existing_user = mongo.db.User.find_one({
            "email": request.form.get('email')
        })

        if existing_user:
            return self.start_session(existing_user)
        
        return jsonify({"error": "Invalid login details"}), 401
    
    def add_transactions(self, account):
        transaction_list = etherscan_api.etherscan_transactions(account['eth'])
        transaction_list_alt = etherscan_api.erc20_transactions(account['eth'])
        transaction_list_nft = etherscan_api.nft_transactions(account['eth'])

        for transaction in transaction_list:
            if mongo.db.Transaction.find_one({
                "hash": transaction['hash']
            }):
                continue
            else:
                try:
                    mongo.db.Transaction.insert_one({
                        "_id": uuid.uuid4().hex,
                        "time": transaction['time'],
                        "hash": transaction['hash'],
                        "to": transaction['to'],
                        "from": transaction['from'],
                        "value": transaction['value'],
                        "error": transaction['error'],
                        "gas_price": transaction['gas_price'],
                        "gas_used": transaction['gas_used'],#
                        "token_symbol": "ETH",
                        "contract_address": "",
                        "token_id": ""
                    })
                    print('Document added to database')
                except:
                    print('Error connection to database')
        
        for transaction in transaction_list_alt:
            if mongo.db.Transaction.find_one({
                "hash": transaction['hash']
            }):
                continue
            else:
                try:
                    mongo.db.Transaction.insert_one({
                        "_id": uuid.uuid4().hex,
                        "time": transaction['time'],
                        "hash": transaction['hash'],
                        "to": transaction['to'],
                        "from": transaction['from'],
                        "value": transaction['value'],
                        "error": transaction['error'],
                        "gas_price": transaction['gas_price'],
                        "gas_used": transaction['gas_used'],
                        "token_symbol": transaction['token_symbol'],
                        "contract_address": transaction['contract_address'],
                        "token_id": ""
                    })
                    print('Document added to database')
                except:
                    print('Error connection to database')

        for transaction in transaction_list_nft:
            if mongo.db.Transaction.find_one({
                "hash": transaction['hash']
            }):
                continue
            else:
                try:
                    mongo.db.Transaction.insert_one({
                        "_id": uuid.uuid4().hex,
                        "time": transaction['time'],
                        "hash": transaction['hash'],
                        "to": transaction['to'],
                        "from": transaction['from'],
                        "value": transaction['value'],
                        "error": transaction['error'],
                        "gas_price": transaction['gas_price'],
                        "gas_used": transaction['gas_used'],
                        "token_symbol": transaction['token_symbol'],
                        "contract_address": transaction['contract_address'],
                        "token_id": transaction['token_id']
                    })
                    print('Document added to database')
                except:
                    print('Error connection to database')
        
        return True


class Transaction():

    def __init__(self, _data):
        self.id = uuid.uuid4().hex
        self.data = _data
