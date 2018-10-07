from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase
from secrets import *
from firebase import firebase
import json
from google.cloud import storage

app = Flask(__name__)

pyre_base = pyrebase.initialize_app(config)
auth = pyre_base.auth()

python_firebase = firebase.FirebaseApplication(config['databaseURL'], None)

def uploadFile(file_stream, filename, content_type):
    # Explicitly use service account credentials by specifying the private key
    storage_client = storage.Client.from_service_account_json('./GreenHacks-b83ce3b13525.json')

    # Make an authenticated API request
    bucket = storage_client.get_bucket(config['storageBucket'])
    blob = bucket.blob("/" + session['username'])
    # blob.upload_from_filename(resume)
    blob.upload_from_string(
        file_stream,
        content_type=content_type)

@app.route('/')
def landing_page():
    if session:
        return render_template('index.html', user=session['username'])
    else:
        return render_template('index.html', user=None)

@app.route('/sponsors')
def sponsors_page():
    if session:
        return render_template('sponsors.html', user=session['username'])
    else:
        return render_template('sponsors.html', user=None)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    errorMessage = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print(auth.get_account_info(user['idToken']))
            print(user)
            session['username'] = user['localId']
            return redirect(url_for('landing_page'))
        except:
            errorMessage = 'Email or password is incorrect'
    return render_template('login.html', errorMessage=errorMessage, user=None)

@app.route('/application', methods=['GET', 'POST'])
def application_page():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        school = request.form['school']
        major = request.form['major']
        year = request.form['year']
        link = request.form['link']
        resume = request.files['resume']
        tech = request.form['tech']
        uploadFile(resume.read(), resume.filename, resume.content_type)

        applicantData = {
            'UID': session['username'],
            'Name': name,
            'Phone': phone,
            'Email': email,
            'School': school,
            'Major': major,
            'Year': year,
            'Link': link,
            'Tech': tech
        }

        send = json.dumps(applicantData)
        result = python_firebase.put('/Applicants', name = session['username'], data = applicantData, params = {'print': 'pretty'})
        return render_template('display-message.html', message='Thank you for applying! We will send you an email regarding your admission when we review your application.', user=session['username'])

    if python_firebase.get('/Applicants/' + session['username'], None) is not None:
        return render_template('display-message.html', message='You have already sent an application. We will email you when we make a decision on your application.', user=session['username'])

    return render_template('application.html', user=session['username'])

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
    return render_template('register.html', errorMessage=errorMessage, user=None)

@app.route('/reset-password', methods=['GET', 'POST'])
def  reset_password():
    errorMessage = ''
    if request.method == 'POST':
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
            return render_template('display-message.html', message='A password reset email will be sent to you shortly.')
        except:
            errorMessage = 'Invalid email'
    return render_template('reset-password.html', errorMessage=errorMessage, user=None)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('landing_page'))

if __name__ == '__main__':
    app.secret_key = key
    app.run(debug=True)
