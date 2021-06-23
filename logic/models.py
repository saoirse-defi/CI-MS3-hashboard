from flask import Flask, jsonify


class User:

    def signup(self):
        user = {
            "_id": "",
            "email": "",
            "eth": "",
            "password": "",
            "password_confirm": ""
        }
        
        return jsonify(user), 200