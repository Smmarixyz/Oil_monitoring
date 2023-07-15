from flask import Flask, render_template, url_for, request, redirect, make_response, Response
import json
import matplotlib.pyplot as plt
from serial import Serial
from time import time

import uuid
from flask import Flask, request, render_template, jsonify, redirect, session, flash
import os
from flask_mail import Mail, Message
import mysql.connector
from flask_bcrypt import Bcrypt
from DBcm import UseDatabase
import smtplib
from random import random
from serial import Serial
import matplotlib.pyplot as plt
from serial import Serial
from matplotlib import style
import datetime as dta
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy.stats import norm
import statistics
import pygal
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import pickle
import numpy as np
import pandas as pd
from numpy import asarray
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot
import datetime as dt
from time import time
import seaborn as sns
import pickle
from pandas import Series
import requests
import json
import numpy as np
from tensorflow.keras.models import load_model
import json
bcrypt = Bcrypt()
app = Flask(__name__)
app.secret_key = os.urandom(24)
conn = mysql.connector.connect(host="127.0.0.1", port='3306', user="root", password="Mariari@96", database="maridb",
                               auth_plugin="mysql_native_password")
cursor = conn.cursor()
cursor = conn.cursor(buffered=True)


@app.route('/')
def login():
    return render_template("new login.html")


@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/home')
def home():
    if 'serial_number' in session:
        return render_template('homedemo.html')
    else:
        return redirect('/dashboard')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    Register_Number = request.form.get('Register_Number')
    cursor.execute("SELECT *FROM muthuari WHERE Register_Number=%s", [Register_Number])
    result1 = cursor.fetchall()
    if result1 == None:
        flash('Register_Number Not valid', category='error')
        return redirect('/dashboard')
    email = request.form.get('email')
    cursor.execute("SELECT *FROM muthuari WHERE email=%s", [email])
    result2 = cursor.fetchone()
    if result2 == None:
        flash('Enter valid  mail id', category='error')
        return redirect('/dashboard')
    password = request.form.get('password')
    cursor.execute("SELECT *FROM muthuari WHERE password =%s", [password])
    result3 = cursor.fetchone()

    if result3 == None:
        flash('password invalid', category='error')
        return redirect('/dashboard')

    cursor.execute("""SELECT *FROM muthuari WHERE Register_Number=%s AND email =%s AND password=%s """,
                   [Register_Number, email, password])
    muthuari = cursor.fetchone()

    print(muthuari)
    if len(muthuari) > 0:
        return render_template('homedemo.html')

    else:
        return redirect("/dashboard")


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    if len(name) < 5:
        flash(' Name must be greater than 4 character.', category='error')
        return redirect('/dashboard')
    email = request.form.get('uemail')
    cursor.execute("SELECT *FROM muthuari WHERE email=%s", [email])
    result5 = cursor.fetchone()
    print(result5)
    if result5 != None:
        flash('Email already exists', category='error')
        return redirect('/dashboard')

    password = request.form.get('upassword')
    if len(password) < 5:
        flash('password must be greater than 5 character.', category='error')
        return redirect('/dashboard')

    cursor.execute(
        """ INSERT INTO muthuari (Serial_Number,Name,email,password) VALUES (NULL,'{}','{}' ,'{}' )""".format(
            name, email, password))
    conn.commit()
    reg1 = 'ARI2208'
    reg2 = str(random.randrange(16, 91))
    reg = reg1 + reg2

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('marimuthuari96@gmail.com', 'vqdajyaigzkauigt')
    msg = 'hello,your register number is  ' + str(reg)

    server.sendmail('marimuthuari96@gmail.com', [email], msg)
    server.quit()

    cursor.execute("UPDATE muthuari SET Register_Number=%s WHERE email=%s ",
                   (reg, email))
    conn.commit()
    flash("User Registered Successfully and register number sent to your EmailID", category='success')
    return redirect('/dashboard')
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        New_password = request.form['New_password']
        confirm_password = request.form['confirm_password']

        if New_password == confirm_password:
            cursor.execute("SELECT *FROM muthuari WHERE email=%s AND password=%s", [email, password])
            result6 = cursor.fetchone()
            print(result6)

            if result6 == None:

                flash('password not created', category='error')
                return redirect('/change_password')
            else:
                cursor.execute("UPDATE muthuari SET password=%s WHERE email=%s AND password=%s ",
                               (New_password, email, password))
                conn.commit()

                flash('password changed successfully', category='success')
                return redirect('/dashboard')
        else:
            flash('password not match', category='error')
            return redirect('/change_password')
    return render_template('change.html')
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        email = request.form['email']

        cursor.execute("SELECT *FROM muthuari WHERE email=%s ", [email])
        result7 = cursor.fetchone()

        if result7 != None:

            OTP = ''.join([str(random.randint(0, 9)) for i in range(4)])

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            server.login('marimuthuari96@gmail.com', 'klltxlgkitjdjacv')

            msg = 'hello,your OTP is ' + str(OTP)

            server.sendmail('marimuthuari96@gmail.com', [email], msg)
            server.quit()

            cursor.execute("UPDATE muthuari SET OTP=%s WHERE email=%s ",
                           (OTP, email))
            conn.commit()

            flash('OTP sent Successfully')
            return redirect('/Reset_password')
        else:
            flash('OTP not sent')
            return redirect('/dashboard')
    return render_template('forgot.html')
@app.route('/Reset_password', methods=['GET', 'POST'])
def Reset_password():
    if request.method == "POST":
        OTP = request.form.get('OTP')
        New_password = request.form.get('New_password')
        confirm_password = request.form.get('confirm_password')
        cursor.execute("SELECT *FROM muthuari WHERE OTP=%s ", [OTP])
        result8 = cursor.fetchone()
        if result8 != None:
            cursor.execute("UPDATE muthuari SET password=%s WHERE OTP=%s  ",
                           (New_password, OTP))
            conn.commit()
            flash('password changed successfully', category='success')
            return redirect('/dashboard')
        else:
            flash('password not Changed', category='error')
            return redirect('/dashboard')
    return render_template('reset.html')
@app.route('/charts', methods=["GET", "POST"])
def main():
    return render_template('demo 1.html')
@app.route('/data', methods=["GET", "POST"])
def animate():
    ser = Serial(
        port='COM14',
        baudrate=115200,
        timeout=None)
    def adddata(data):
        '''a function to add the data to the text file'''
        date = time()
        h = str(date) + ',' + str(data)
        fh = open('example51.txt', 'a')
        fh.write(h)
    while 1:
        ''' infinit loop'''
        while (ser.inWaiting() == 0):
            '''wait for the data from serial'''
            pass
        a = str(ser.readline().decode('utf-8'))
        adddata(a)
        '''add the data to the txt file'''
        if ser.is_open == True:
            print("\nAll right, serial port now open. Configuration:\n")
        dateconv = dta.datetime.fromtimestamp
        '''define the function that gonna convert the unix time to date'''
        graph_data = open('example51.txt', 'r').read()
        '''read the data from the txt file'''
        lines = graph_data.split('\n')
        ''' split the lines as a list'''
        xs = []
        ''' x axis the tempurature'''
        ys = []
        ss = []
        ts = []
        rs = []
        for line in lines:
            list = line.split(',')
            result = len(list)
            if (result == 3):
                a, b, c, = line.split(',')
                a = float(a)
                b1 = float(b)
                c1 = float(c)
            a1 = time()
            data = [a1 * 1000, b1, c1]
            response = make_response(json.dumps(data))
            response.content_type = 'application/json'
        return response
model = load_model('lstm_model1.h5')
@app.route('/predict', methods=["GET", "POST"])
def main1():
    return render_template('prediction email.html')
@app.route('/Predictiondata', methods=["GET", "POST"])
def predict():
    def add_data(data):
        '''A function to add the data to the text file'''
        date = datetime.now().timestamp()
        h = str(date) + ',' + str(data)
        with open('example50.txt', 'a') as fh:
            fh.write(h + '\n')  # Append a newline character to separate lines

    # Initialize lists to store the extracted data
    xs = []
    combined_data = []
    rescaled_prediction = []
    with open('example50.txt', 'r') as graph_data_file:
        graph_data = graph_data_file.readlines()  # Read all lines

    for line in graph_data:
        lst = line.strip().split(',')
        if len(lst) == 3:
            a, b, c = lst
            a = float(a)

            c1 = float(c)
            a1 = dt.datetime.now()
            xs.append(a1)
            combined_data.append(c1)

            preprocessed_data = np.array(combined_data)
            input_data = np.reshape(preprocessed_data, (-1, 1))
            predictions = model.predict(input_data)

            original_min = 0
            original_max = 1
            desired_min = 12.00
            desired_max = 40.00

            rescaled_prediction1 = ((predictions - original_min) / (original_max - original_min)) * (
                    desired_max - desired_min) + desired_min

            rescaled_prediction1 = rescaled_prediction1.astype(float).tolist()
            rescaled_prediction.append(rescaled_prediction1[-1])

    # Prepare the data to send for the current iteration
    data = {
        "xs": [x.timestamp() * 1000 for x in xs],
        "combined_data": combined_data,
        "rescaled_prediction": rescaled_prediction
    }
    print(data)

    # Convert the data to JSON
    response_data = json.dumps(data)

    # Create the Flask response object with the JSON data
    response = Response(response_data, content_type='application/json')
    return response




@app.route('/logout')
def logout():
    return redirect('/')
if __name__ == '__main__':
    app.debug = True
    app.run()
