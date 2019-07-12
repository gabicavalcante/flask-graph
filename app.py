import os
from os.path import join, dirname

from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
login = LoginManager(app)

from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
import json 

from models import User

import pandas as pd
import matplotlib.pyplot as plt

# Assign spreadsheet filename to `file`
file = './data/reservas-pendentes.xlsx'

# Load spreadsheet
df = pd.read_excel(file, index_col=0)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(401)
def unauthorized_access(e):
    # note that we set the 404 status explicitly
    return render_template('401.html'), 401

@app.route("/")
def index():
    return redirect(url_for('report'))
 
#@login_required
@app.route("/add/user", methods=['GET', 'POST'])
def add_user_form():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = User(
                username=username,
                email=email,
                password=User.generate_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            return "User added. user id={}".format(user.id)
        except Exception as e:
            return(str(e))
    return render_template("create_user.html")
 

#@login_required
@app.route("/report", methods=['GET'])
def report():   
    df['DT_Necessidade'] = pd.to_datetime(df['DT_Necessidade'])
    graph = df['NU_QTde_atend'].groupby(
        df['DT_Necessidade'].dt.to_period('M')).sum().reset_index()

    bar_labels=graph.DT_Necessidade
    bar_values=graph.NU_QTde_atend
    return render_template('chart.html', title='NU_QTde_atend x DT_Necessidade', max=17000, labels=bar_labels, values=bar_values)

@app.route('/line')
def line():
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)

@app.route('/pie')
def pie():
    pie_labels = labels
    pie_values = values
    return render_template('pie_chart.html', title='Bitcoin Monthly Price in USD', max=17000, set=zip(values, labels, colors))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('get_all_devices'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
 
        try:
            user = User.query.filter_by(email=email).first() 
            if User.verify_hash(password, user.password):
                login_user(user, remember=True)
                return redirect(url_for('get_all_devices'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
        except Exception as e:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()