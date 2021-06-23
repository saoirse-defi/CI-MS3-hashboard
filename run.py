import os
from flask import Flask, render_template, redirect, url_for, flask_login
from flask.ext.login import LoginManager
from flask.ext.pymongo import Pymongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hashboard_db'
app.config['MONGO_URI'] = ''

from website import views


