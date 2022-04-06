# Imports
import os
from operator import itemgetter
from flask import (Flask, render_template, request,
                   redirect, session, url_for,
                   send_from_directory, flash)
from flask_pymongo import PyMongo
import logic.models
import logic.eth

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

favourites_table_headings = ['Date created',
                             'Hash',
                             'To',
                             'From',
                             'Value',
                             'Token Involved',
                             'Gas Price (GWEI)',
                             'Notes',
                             'Edit',
                             'Delete']


# Exception handling function
@app.errorhandler(404)
def handle_exception_404(e):
    ''' Displays exception to the user'''
    return render_template("error.html", e=e), 404


@app.errorhandler(403)
def handle_exception_403(e):
    ''' Displays exception to the user'''
    return render_template("error.html", e=e), 403


@app.errorhandler(405)
def handle_exception_405(e):
    ''' Displays exception to the user'''
    return render_template("error.html", e=e), 405


@app.errorhandler(500)
def handle_exception_500(e):
    ''' Displays exception to the user'''
    return render_template("error.html", e=e), 500


@app.errorhandler(503)
def handle_exception_503(e):
    ''' Displays exception to the user'''
    return render_template("error.html", e=e), 503


# Formatting functions
def shorten(string):
    ''' Converts Ethereum address into truncated string. '''
    return "0x..." + string[38:]


def shorten2(string):
    ''' Converts Ethereum transaction hash into truncated string. '''
    return "0x..." + string[62:]


# Routes
@app.route("/")
@app.route("/index")
@app.route("/hashboard", methods=['GET', 'POST'])
def hashboard():
    # list of cursor query
    try:
        transactions_list = list(
            mongo.db.Transaction.find(
                {"user_id": session['user']['_id']}))
        # sort combined list by time/date
        transactions_list.sort(reverse=True, key=logic.eth.sortTime)
    except Exception as e:
        raise Exception(e)

    # list of favourite transactions
    try:
        favourites_list = list(
            mongo.db.Transaction.find(
                {"user_id": session['user']['_id'], "isFav": True}))
        favourites_list.sort(reverse=True, key=itemgetter('time'))
    except Exception as e:
        raise Exception(e)

    # transaction can only be in either transaction list or fav list, not both
    for data in favourites_list:
        for _data in transactions_list:
            if data == _data:
                transactions_list.remove(_data)

    return render_template(
        "hashboard.html",
        transactions_list=transactions_list,
        favourites_list=favourites_list,
        transaction_table_headings=transaction_table_headings,
        favourites_table_headings=favourites_table_headings,
        shorten=shorten,
        shorten2=shorten2)


# Add transaction to favourites
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
                flash(f"{transaction['hash']} has been added "
                      f"to your priority list", category="success")
                return redirect(url_for('hashboard'))
        except Exception as e:
            raise Exception(f"There has been an exception: {e}")

    return render_template('favourite.html',
                           transaction=transaction,
                           shorten=shorten,
                           shorten2=shorten2)


# Delete transaction from favourites
@app.route('/delete_favourite/<transaction_id>', methods=['GET', 'POST'])
def delete_favourite(transaction_id):
    transaction = mongo.db.Transaction.find_one({"_id": transaction_id})
    try:
        if transaction['user_id'] == session['user']['_id']:
            mongo.db.Transaction.update(
                {"_id": transaction_id},
                {"$set": {"note": "", "isFav": False}})
            flash("Transaction removed from priority list.",
                  category="success")
            return redirect(url_for('hashboard'))
    except Exception as e:
        raise Exception(f"There has been an exception: {e}")


# Clear all transactions except favourites
@app.route('/clear', methods=['GET', 'POST'])
def clear():
    mongo.db.Transaction.delete_many(
        {"user_id": session['user']['_id'], 'isFav': False})
    flash("Transactions cleared!", category="success")
    return redirect(url_for('hashboard'))


# Search, bulk transaction added to db
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_eth = ""
    transaction_list = []

    if request.method == 'POST':
        search_eth = str(request.form.get('search-eth')).lower()
        if len(search_eth) == 42:
            try:
                transaction_list = logic.eth.get_transactions(search_eth)
            except Exception as e:
                print(e)
            if transaction_list is not None:
                return redirect(url_for('hashboard'))
                flash(f"Transactions added for {search_eth}",
                      category="success")
            else:
                return redirect(url_for('search'))
                flash("Results not found", category="error")
        else:
            return render_template('search.html')
            flash("Incorrect address format", category="error")

    return render_template(
        "search.html",
        shorten=shorten,
        shorten2=shorten2,
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    existing_user = mongo.db.User.find_one({
            "email": request.form.get('email')
    })

    if request.method == 'POST':
        if existing_user:
            return logic.models.Account().login()
        else:
            flash("Email address not found!", category="error")

    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if len(request.form.get('password')) > 7:
            if(request.form.get('password')
               == request.form.get('password-confirm')):
                return logic.models.Account().signup()
            else:
                flash("Passwords do not match.", category="error")
        else:
            flash("Password needs to be 8 digits or more", category="error")

    return render_template("signup.html")


@app.route('/signout')
def signout():
    try:
        if session['user']['_id']:
            return logic.models.Account().signout()
    except Exception as e:
        raise Exception(e)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

# App config


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
