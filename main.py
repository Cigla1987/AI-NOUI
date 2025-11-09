
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, Response
from flask_sock import Sock
from bcrypt import hashpw, gensalt, checkpw
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from db import get_db_conn, save_project_db

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecret')
sock = Sock(app)

# Initialize Gemini client
# ...existing Gemini initialization code...
# MEMORY DB
users = {}
projects = {}
next_id = 1

# WebSocket endpoint for Arduino communication
@sock.route('/ws/arduino')
def arduino_ws(ws):
    print("WebSocket connection established with Arduino")
    while True:
        data = ws.receive()
        if data is None:
            break
        print(f"Received from Arduino: {data}")
        ws.send("ACK")
    print("WebSocket connection closed")

# AUTH routes
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        if email in users:
            flash('Email taken')
            return redirect('/register')
        global next_id
        users[email] = {
            'id': next_id,
            'pw': hashpw(request.form['password'].encode(), gensalt()).decode(),
            'name': request.form['name']
        }
        projects[next_id] = []
        next_id += 1
        flash('Registered! Login now')
        return redirect('/login')
    return render_template('login.html', title='Register', action='/register')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = users.get(request.form['email'])
        print("Login attempt:", request.form['email'], "Found user:", user)
        if user and checkpw(request.form['password'].encode(), user['pw'].encode()):
            session['user_id'] = user['id']
            return redirect('/project-overview')
        flash('Wrong email/password')
    return render_template('login.html', title='Login', action='/login')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    return redirect('/project-overview')


# Additional routes for side menu navigation

from flask import render_template_string


@app.route('/create-project')
def create_project():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('create_project.html', title='Create Project')

@app.route('/project-overview')
def project_overview():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('project_overview.html', title='Project Overview')

@app.route('/project-buildup')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('project_buildup.html')


@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('settings.html', title='Settings')

# ...existing AI, code generation, and other routes...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
