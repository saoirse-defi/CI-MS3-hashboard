from flask import Flask, redirect, url_for, Blueprint, render_template
from flask_login import LoginManager, login_required
from run import app
from logic.models import User
from datetime import datetime, date
import time
from dateutil import parser

views = Blueprint('views', __name__)


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