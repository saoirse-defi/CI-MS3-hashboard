from flask import Flask, jsonify
import pymongo


class User:

    def signup(self):
        user = {
            "_id": "",
            "name": "",
            "email": "",
            "eth": "",
            "password": "",
            "password_confirm": ""
        }
        
        return jsonify(user), 200