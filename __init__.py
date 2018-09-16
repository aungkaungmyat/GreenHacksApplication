from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase
from secrets import *

app = Flask(__name__)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    errorMessage = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['username'] = user['localId']
            return redirect(url_for('landing_page'))
        except:
            errorMessage = 'Email or password is incorrect'
    return render_template('login.html', errorMessage=errorMessage)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    errorMessage = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['username'] = user['localId']
            return redirect(url_for('landing_page'))
        except Exception as e:
            if len(password) < 6:
                errorMessage = 'Password must be at least 6 characters'
            else:
                errorMessage = 'An account with that email already exists'
            print(e)
    return render_template('register.html', errorMessage=errorMessage)

if __name__ == '__main__':
    app.secret_key = key
    app.run(debug=True)
