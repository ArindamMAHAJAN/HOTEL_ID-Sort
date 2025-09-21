import mimetypes
import pytz
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

from pymongo import MongoClient
from bson import ObjectId
import pytesseract
from PIL import Image
import io
import datetime
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

import os

# Login credentials from environment variables
VALID_USERNAME = os.getenv('LOGIN_USERNAME', 'Arindam56')
VALID_PASSWORD = os.getenv('LOGIN_PASSWORD', 'Arindam75')

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['ID']
collection = db['guests']
access_logs = db['access_logs']

@app.before_request
def log_access():
    if request.endpoint != 'static':
        access_logs.insert_one({
            'path': request.path,
            'method': request.method,
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'timestamp': datetime.now(timezone.utc)
        })

from datetime import datetime

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            flash('You were successfully logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    max_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', max_date=max_date)

@app.route('/upload', methods=['POST'])
def upload():
    room = request.form['room']
    date = request.form['date']
    files = request.files.getlist('id_image')
    
    for file in files:
        if file:
            # Read image
            image_data = file.read()
            mimetype = mimetypes.guess_type(file.filename)[0].split('/')[1] if mimetypes.guess_type(file.filename)[0] else 'jpeg'
            text = ""
            try:
                image = Image.open(io.BytesIO(image_data))
                
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Extract text with OCR
                text = pytesseract.image_to_string(image)
            except Exception as e:
                # Log error or handle unsupported format
                print(f"Error processing {file.filename}: {e}")
            
            # Store in MongoDB
            from datetime import datetime, timezone
            collection.insert_one({
                'room': room,
                'date': date,
                'image': image_data,  # Store binary
                'mimetype': mimetype,
                'extracted_text': text,
                'upload_time': datetime.now(timezone.utc).replace(tzinfo=pytz.UTC)
            })
    
    return redirect(url_for('view'))

@app.route('/view')
def view():
    from datetime import datetime

    # Sort by date desc, then room
    guests = list(collection.find().sort([('date', -1), ('room', 1)]))
    print("Fetched guests:", len(guests))
    # Convert image binary to base64 for display
    for guest in guests:
        if 'image' in guest:
            import base64
            guest['image_base64'] = base64.b64encode(guest['image']).decode('utf-8')

        # Debug print upload_time type and value
        if 'upload_time' in guest and guest['upload_time']:
            print(f"upload_time type: {type(guest['upload_time'])}, value: {guest['upload_time']}")
            utc_time = guest['upload_time']
            local_tz = pytz.timezone('America/New_York')  # Change to your local timezone
            guest['upload_time_local'] = utc_time.astimezone(local_tz)
        else:
            guest['upload_time_local'] = None

    # Group guests by room
    grouped_guests = {}
    for guest in guests:
        room = guest.get('room', 'Unknown')
        if room not in grouped_guests:
            grouped_guests[room] = []
        grouped_guests[room].append(guest)

    return render_template('view.html', grouped_guests=grouped_guests)

@app.route('/logs')
def logs():
    logs_list = list(access_logs.find().sort('timestamp', -1))
    return render_template('logs.html', logs=logs_list)

if __name__ == '__main__':
    access_logs.insert_one({
        'event': 'startup',
            'timestamp': datetime.now(timezone.utc)
    })

    # Generate self-signed SSL certificate if not exists
    cert_file = 'ssl_cert.crt'
    key_file = 'ssl_cert.key'
    try:
        ssl_context = (cert_file, key_file)
        app.run(debug=True, host='0.0.0.0', port=5001, ssl_context=ssl_context)
    except OSError as e:
        if "Address already in use" in str(e):
            print("Port 5001 is already in use. Trying port 5000 instead.")
            try:
                app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context)
            except Exception as e2:
                print(f"Failed to start on port 5000: {e2}")
        else:
            print(f"Error starting server: {e}")
    except Exception:
        make_ssl_devcert('./ssl_cert', host='localhost')
        ssl_context = ('ssl_cert.crt', 'ssl_cert.key')
        app.run(debug=True, host='0.0.0.0', port=5001, ssl_context=ssl_context)
