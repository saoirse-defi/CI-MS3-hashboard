import os
from flask import Flask, render_template, flash, redirect, request, session, url_for
from flask_login import LoginManager, login_required
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from logic.models import User

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECREY_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_user")
def get_user():
    users = mongo.db.Users.find()
    return render_template("users.html", users=users)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST']) 
def login():
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    return redirect(url_for('views.login'))


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)


