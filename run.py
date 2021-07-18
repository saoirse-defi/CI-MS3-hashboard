# Imports
import os
if os.path.exists("env.py"):
    import env
# from os import path
from operator import itemgetter
from flask import Flask, render_template, redirect, request, session, url_for, send_from_directory, abort
from flask_pymongo import PyMongo
from functools import wraps
import logic.models
import logic.async_eth

# Application setup

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SESSION_TYPE"] = 'filesystem'
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

transaction_table_headings = ['Date created',
                              'Hash',
                              'To',
                              'From',
                              'Value',
                              'Token Involved',
                              'Gas Price (GWEI)',
                              'Gas Spent (ETH)',
                              'Favourite']

fav_table_headings = ['Date created',
                      'Hash',
                      'To',
                      'From',
                      'Value',
                      'Token Involved',
                      'Gas Price (GWEI)',
                      'Notes',
                      'Edit',
                      'Delete']


# Error Handling Functions
@app.errorhandler(403)
def forbidden(e):
    print(f"Error: {e}")
    return render_template('403.html')


@app.errorhandler(404)
def not_found(e):
    print(f"Error: {e}")
    return render_template('404.html')


@app.errorhandler(500)
def server_error(e):
    print(f"Error: {e}")
    return render_template('500.html')

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


def shorten(string):
    return "0x..." + string[38:]


def shorten2(string):
    return "0x..." + string[62:]


def toInt(x):
    return int(float(x))


def threeDecimals(y):
    return "%.3f" % y


# Routes
@login_required
@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    # list of cursor query
    try:
        transactions_list = list(
            mongo.db.Transaction.find(
                {"user_id": session['user']['_id']}))
        # sort combined list by time/date
        transactions_list.sort(reverse=True, key=itemgetter('time'))
    except Exception as e:
        return forbidden(e)

    # list of favourite transactions
    try:
        fav_list = list(
            mongo.db.Transaction.find(
                {"user_id": session['user']['_id'], "isFav": True}))
        fav_list.sort(reverse=True, key=itemgetter('time'))
    except Exception as e:
        return forbidden(e)

    # transaction can only be in transaction list or fav list
    for data in fav_list:
        for _data in transactions_list:
            if data == _data:
                transactions_list.remove(_data)

    return render_template("index.html",
                           transactions_list=transactions_list,
                           fav_list=fav_list,
                           transaction_table_headings=transaction_table_headings,
                           fav_table_headings=fav_table_headings,
                           shorten=shorten,
                           shorten2=shorten2,
                           toInt=toInt,
                           threeDecimals=threeDecimals)


# Add transaction to favourites
@login_required
@app.route('/favourite/<transaction_id>', methods=['GET', 'POST'])
def favourite(transaction_id):
    transaction = mongo.db.Transaction.find_one({'_id': transaction_id})

    if request.method == 'POST':
        note = request.form.get('note')
        # allow edit if the session user == transaction user_id
        try:
            if session['user']['_id'] == transaction['user_id']:
                mongo.db.Transaction.update(
                    {"_id": transaction_id}, {
                        "$set": {"note": note, "isFav": True}})
                return redirect(url_for('index'))
        except Exception as e:
            print("Exception: ", e)
            return forbidden(e)

    return render_template('favourite.html',
                           transaction=transaction,
                           shorten=shorten,
                           shorten2=shorten2)


# Delete transaction from favourites
@login_required
@app.route('/delete_fav/<transaction_id>', methods=['GET', 'POST'])
def delete_fav(transaction_id):
    transaction = mongo.db.Transaction.find_one({"_id": transaction_id})
    try:
        if transaction['user_id'] == session['user']['_id']:
            mongo.db.Transaction.update(
                {"_id": transaction_id},
                {"$set": {"note": "", "isFav": False}})
            return redirect(url_for('index'))
    except Exception as e:
        return forbidden(e)


# Clear all transactions except favourites
@login_required
@app.route('/clear', methods=['GET', 'POST'])
def clear():
    mongo.db.Transaction.remove(
        {"user_id": session['user']['_id'], 'isFav': False})

    return redirect(url_for('index'))


# Search, bulk transaction added to db
@login_required
@app.route('/search', methods=['GET', 'POST'])
async def search():
    search_eth = ""
    transaction_list = []

    if request.method == 'POST':
        search_eth = str(request.form.get('search-eth')).lower()
        transaction_list = await logic.async_eth.get_transactions(search_eth)
        return redirect(url_for('index'))

    return render_template("search.html",
                           shorten=shorten,
                           shorten2=shorten2,
                           toInt=toInt,
                           threeDecimals=threeDecimals,
                           search_eth=search_eth,
                           transaction_list=transaction_list,
                           transaction_table_headings=transaction_table_headings)


@app.route('/home', methods=['GET', 'POST'])
def home():
    transactions_list = list(
        mongo.db.Transaction.find(
            {"user_id": session['user']['_id']}))

    fav_list = list(
        mongo.db.Transaction.find(
            {"user_id": session['user']['_id'], "isFav": True}))
    return render_template('home.html',
                           transactions_list=transactions_list,
                           fav_list=fav_list,
                           shorten2=shorten2,
                           shorten=shorten)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        logic.models.Account().signup()
        return redirect(url_for('index'))
    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return logic.models.Account().login()

    return render_template("login.html")


@login_required
@app.route('/signout')
def signout():
    return logic.models.Account().signout()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

# App config


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
