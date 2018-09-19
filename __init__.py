from flask import Flask, render_template, request, redirect, url_for
import pyrebase
from secrets import *
from firebase import firebase
import json
from google.cloud import storage

# from google.cloud import storage

app = Flask(__name__)

pyre_base = pyrebase.initialize_app(config)
auth = pyre_base.auth()

python_firebase = firebase.FirebaseApplication(datebaseUrl, None)

# client = storage.Client('GreenHacks-b83ce3b13525.json')
# bucket = client.get_bucket('greenhacks-b635f.appspot.com')

# imageBlob = bucket.blob("/")

def uploadFile(file_stream, filename, content_type):
    
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('/home/amyat/GreenHacks-b83ce3b13525.json')

    # Make an authenticated API request
    bucket = storage_client.get_bucket("greenhacks-b635f.appspot.com")
    blob = bucket.blob("/" + filename)
    # blob.upload_from_filename(resume)
    blob.upload_from_string(
        file_stream,
        content_type=content_type)  


@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

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
            'UID': '4TCNxdfclKT6mkPjGZTZinRXHdx2',
            'Name': name,
            'Phone': phone,
            'Email': email,
            'School': school,
            'Major': major,
            'Year': year,
            'Link': link,
            # 'Resume': resume,
            'Tech': tech
        }
      

        send = json.dumps(applicantData)
        result = python_firebase.put('/Applicants', name = '4TCNxdfclKT6mkPjGZTZinRXHdx2', data = applicantData, params = {'print': 'pretty'})


    return render_template('application.html')

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
