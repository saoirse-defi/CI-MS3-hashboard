from flask import Flask, redirect, url_for, Blueprint, render_template
from flask_login import LoginManager, login_required
from run import app
from . import models
from datetime import datetime, date
import time
from dateutil import parser

views = Blueprint('views', __name__)


@views.route("/")
def index():
    return render_template("index.html")


@views.route('/signup', methods=['GET', 'POST'])
def signup():
    return User().signup()


@views.route('/login', methods=['GET', 'POST']) 
def login():
    return render_template("login.html")


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))