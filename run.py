import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
import pymongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hashboard_db'
app.config['MONGO_URI'] = ''

from website import views


