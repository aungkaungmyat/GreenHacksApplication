from flask import Flask, render_template, request, redirect, url_for
import pyrebase
from secrets import *

app = Flask(__name__)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('landing_page'))
    else:
        return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)
