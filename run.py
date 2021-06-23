import os
from flask import Flask, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask.ext.pymongo import Pymongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hashboard_db'

from website import views


