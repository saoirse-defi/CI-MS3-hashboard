# Imports
import os
import uuid
import asyncio
import httpx
from os import path
from web3 import Web3
if os.path.exists("env.py"):
    import env

from flask import Flask, render_template, flash, redirect, request, session, url_for, send_from_directory
from flask_pymongo import PyMongo
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import logic.models

# Application setup

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SESSION_TYPE"] = 'filesystem'
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Decorator Functions


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

# Routes

@app.route("/")
@app.route("/index")
@login_required
def index():
    
    transactions_list = list(mongo.db.Transaction.find({"from": session['user']['eth']})) # list of cursor

    transaction_table_headings = ['Date created', 'Hash', 'To', 'From', 'Value', 'Token Involved', 'Gas Price (GWEI)', 'Gas Spent (ETH)', 'Favourite']

    def shorten(string):
        return "0x..." + string[38:]
    
    def shorten2(string):
        return "0x..." + string[62:]

    def toInt(x):
        return int(float(x))

    def threeDecimals(y):
        return "%.3f" % y
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
    if request.method == 'POST':
        search_eth = str(request.form.get('search-eth')).lower()

        async with httpx.AsyncClient() as client:
            search_result = await asyncio.gather(
                client.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={search_eth}&startblock=0&endblock=99999999&sort=asc&apikey=PQWGH496A8A1H3YV5TKWNVCPHJZ3S7ITHA')
            )
        
        print(search_result)


    return render_template("search.html", errors=errors, form=request.form)

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
