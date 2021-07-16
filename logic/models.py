import uuid
from flask import jsonify, session, redirect, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
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

        return redirect(url_for('index'))

    def signout(self):
        session.clear()
        return redirect(url_for('login'))

    def login(self):
        existing_user = mongo.db.User.find_one({
            "email": request.form.get('email')
        })

        if existing_user:
            if check_password_hash(existing_user['password'], request.form.get('password')):
                print('password true')
                return self.start_session(existing_user)
            else:
                print('password did not match')  # need to add a warning message
                return redirect(url_for('login'))

        return jsonify({"error": "Email address not found"}), 401

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
