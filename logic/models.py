import uuid
from flask import jsonify, session, redirect, request, url_for
from werkzeug.security import generate_password_hash
from run import mongo


class Account():

    def signup(self):
        account = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        account['password'] = generate_password_hash(account['password'])

        if(mongo.db.User.find_one({'email': account['email']})):
            return jsonify({'error': 'Email already in use.'})

        if mongo.db.User.insert_one(account):
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

    def add_transactions(self, data):
        mongo.db.Transaction.insert_one({
                    "_id": uuid.uuid4().hex,
                    "user_id": session['user']['_id'],
                    "time": data['time'],
                    "hash": data['hash'],
                    "to": data['to'],
                    "from": data['from'],
                    "value": data['value'],
                    "gas_price": data['gas_price'],
                    "gas_used": data['gas_used'],
                    "token_symbol": data['token_symbol'],
                    "contract_address": data['contract_address'],
                    "token_id": data['token_id'],
                    "note": "",
                    "isFav": False
        })
        return True
