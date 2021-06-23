import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
import pymongo


app = Flask(__name__)

#  app.config['MONGO_DBNAME'] = 'hashboard_db'
#  app.config['MONGO_URI'] = ''

from logic import views

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
