import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import re
import random
import base64
import string

app = Flask(__name__)


app.secret_key = '12345678'


try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin123',
        database='hospital'
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")


@app.route('/')
def index():
    return redirect(url_for('patient_login'))

@app.route('/patient_signup', methods=['GET'])
def patient_signup():
    return render_template('psignup.html')

@app.route('/patient_login', methods=['GET'])
def patient_login():
    return render_template('plogin.html')

@app.route('/doctor_login', methods=['GET'])
def doctor_login():
    return render_template('dlogin.html')
    

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  
        password = request.form.get('password')
        print(email,password) 
        query = "SELECT user_id FROM USERS WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        print(user)
        if user:
            # Authentication successful, redirect to the home page
            print('User found')
            session['user_id'] = user[0]
            return redirect(url_for('phome'))
        # If authentication fails, redirect back to login page or handle accordingly
        else:
            flash('Invalid username or password', 'error')
    return redirect(url_for('patient_login'))

@app.route('/doclogin', methods=['POST'])
def doclogin():
    if request.method == 'POST':
        name = request.form.get('name')  
        password = request.form.get('password')
        query = "SELECT doctor_id FROM doctors WHERE doc_name = %s AND Password = %s"
        cursor.execute(query, (name, password))
        user = cursor.fetchone()
        print(user)
        if user:
            # Authentication successful, redirect to the home page
            print('User found')
            session['doctor_id'] = user[0]
            return redirect(url_for('dhome'))
        # If authentication fails, redirect back to login page or handle accordingly
        else:
            flash('Invalid username or password', 'error')
    return redirect(url_for('doctor_login'))

@app.route('/register', methods=['POST'])   
def register():
    if request.method == 'POST':
        name = request.form.get('name')  
        email = request.form.get('email') 
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phoneno = request.form.get('phoneno')
        profile_image = request.files['profile_image'] if 'profile_image' in request.files else None

        form_data = {
            'name': name,
            'email': email,
            'phoneno': phoneno
        }

        # Validate name
        if not name.isalpha():
            flash('Please enter your name without any special characters or numbers.')
            return render_template('psignup.html', form_data=form_data)

        # Validate phoneno format
        string_phoneno = str(phoneno)
        if len(string_phoneno) != 10:
            flash('Invalid phone number. Please enter a valid 10-digit phone number.')
            return render_template('psignup.html', form_data=form_data)
        elif string_phoneno[0] == '0':
            flash('Invalid phone number. Please enter a valid 10-digit phone number.')
            return render_template('psignup.html', form_data=form_data)

        # Validate password strength
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%!]).{8,}$', password):
            flash('Password must contain at least one uppercase letter, one digit, and one special character (@, #, $, %, or !), and be at least 8 characters long.')
            return render_template('psignup.html', form_data=form_data)

        # Check password confirmation
        if password != confirm_password:
            flash('Passwords do not match.')
            return render_template('psignup.html', form_data=form_data)

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_email = cursor.fetchone()
            if existing_email:
                flash('Email already exists.')
                return render_template('psignup.html', form_data=form_data)

            # Insert new user into the database
            if profile_image:
                profile_image_blob = profile_image.read()
                cursor.execute("INSERT INTO users (name, email, password, phoneno, profile_image) VALUES (%s, %s, %s, %s, %s)",
                               (name, email, password, phoneno, profile_image_blob))
            else:
                cursor.execute("INSERT INTO users (name, email, password, phoneno) VALUES (%s, %s, %s, %s)",
                               (name, email, password, phoneno))

            db.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('patient_login'))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            flash('Error occurred during registration. Please try again.')
            return redirect(url_for('patient_login'))

    return render_template('psignup.html')

# Patient Routes
@app.route('/phome')
def phome():
    if session.get('user_id') is None:
        return redirect(url_for('patient_login'))
    try:
        # Fetch user data including profile image
        cursor.execute("SELECT name, profile_image FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()

        if user:
            name = user[0]
            profile_image_blob = user[1] if user[1] else None

            if profile_image_blob:
                profile_image = base64.b64encode(profile_image_blob).decode('utf-8')
            else:
                profile_image = None
        else:
            flash('User not found.', 'error')
            return redirect(url_for('patient_login'))

        return render_template('phome.html', name=name, profile_image=profile_image)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error fetching user data.', 'error')
        return redirect(url_for('patient_login'))
    
@app.route('/categories')
def categories():
    if session.get('user_id') is None:
        return redirect(url_for('patient_login'))    
    try:

        cursor.execute("SELECT name, profile_image FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()

        if user:
            name = user[0]
            profile_image_blob = user[1] if user[1] else None

            if profile_image_blob:
                profile_image = base64.b64encode(profile_image_blob).decode('utf-8')
            else:
                profile_image = None

        # Fetch doctors categorized by specialty including profile_image
        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Pediatricians',))
        pediatricians = cursor.fetchall()

        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Neurologists',))
        neurologists = cursor.fetchall()

        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Cardiologists',))
        cardiologists = cursor.fetchall()

        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Endocrinologists',))
        endocrinologists = cursor.fetchall()

        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Psychiatrists',))
        psychiatrists = cursor.fetchall()

        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Dermatologists',))
        dermatologists = cursor.fetchall()

        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Oncologists',))
        oncologists = cursor.fetchall()

        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Gastroenterologists',))
        gastroenterologists = cursor.fetchall()

        cursor.execute("SELECT doc_name, bio, ratings, profile_image, doctor_id FROM Doctors WHERE specialty = %s", ('Radiologists',))
        radiologists = cursor.fetchall()

        return render_template('categories.html', 
                               pediatricians=pediatricians,
                               neurologists=neurologists,
                               cardiologists=cardiologists,
                               endocrinologists=endocrinologists,
                               psychiatrists=psychiatrists,
                               dermatologists=dermatologists,
                               oncologists=oncologists,
                               gastroenterologists=gastroenterologists,
                               radiologists=radiologists,profile_image=profile_image,name=name)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error fetching doctors data.', 'error')
        return redirect(url_for('phome'))

@app.route('/doctor/<int:doctor_id>', methods=['GET'])   
def doctor_details(doctor_id):
    if session.get('user_id') is None:
        return redirect(url_for('patient_login'))
    # Fetch doctor details from database
    cursor.execute("SELECT name, profile_image FROM users WHERE user_id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if user:
        name = user[0]
        profile_image_blob = user[1] if user[1] else None

        if profile_image_blob:
            profile_image = base64.b64encode(profile_image_blob).decode('utf-8')
        else:
            profile_image = None
    cursor.execute('SELECT doctor_id, doc_name, specialty, bio, ratings, profile_image FROM doctors WHERE doctor_id = %s', (doctor_id,))
    doctor = cursor.fetchone()
    print(doctor)
    if not doctor:
        # Handle case where doctor_id doesn't exist
        return render_template('error.html', message='Doctor not found'), 404
    
    return render_template('doc.html', doctor=doctor, profile_image=profile_image,name=name)

# Route for requesting appointment
@app.route('/request_appointment/<int:doctor_id>')
def request_appointment(doctor_id):
    if session.get('user_id') is None:
        return redirect(url_for('patient_login'))
    # Get patient_id from session
    patient_id = session.get('user_id')

    cursor.execute("SELECT name, profile_image FROM users WHERE user_id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if user:
        name = user[0]
        profile_image_blob = user[1] if user[1] else None

        if profile_image_blob:
            profile_image = base64.b64encode(profile_image_blob).decode('utf-8')
        else:
            profile_image = None

    # Insert into database
    cursor.execute('INSERT INTO Appointments (patient_id, doctor_id, status) VALUES (%s, %s, %s)',
                    (patient_id, doctor_id, 'requested'))
    db.commit()
    print('Appointment requested successfully')
    return redirect(url_for('appointments',profile_image=profile_image,name=name))  # Redirect to home page or appropriate URL after request
    

@app.route('/appointments')
def appointments():
    if session.get('user_id') is None:
        return redirect(url_for('patient_login'))
    user_id = session['user_id']
    try:
        cursor.execute("SELECT name, profile_image FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()

        if user:
            name = user[0]
            profile_image_blob = user[1] if user[1] else None

            if profile_image_blob:
                profile_image = base64.b64encode(profile_image_blob).decode('utf-8')
            else:
                profile_image = None

        # Fetch appointments for the current user
        cursor.execute('''
            SELECT a.appointment_id, d.doc_name, d.specialty, a.status, a.appointment_date, a.gmeet_link
            FROM Appointments a
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            WHERE a.patient_id = %s
        ''', (user_id,))
        appointments = cursor.fetchall()

        # Separate appointments into past and current based on status
        current_appointments = []
        past_appointments = []

        for appointment in appointments:
            if appointment[3] in ['requested', 'accepted']:
                current_appointments.append(appointment)
            elif appointment[3] in ['concluded', 'rejected']:
                past_appointments.append(appointment)

        # Pass data to appointments.html template
        return render_template('appointments.html', current_appointments=current_appointments, past_appointments=past_appointments, profile_image=profile_image,name=name)

    except mysql.connector.Error as err:
        print(f"Error fetching appointments: {err}")
        return render_template('appointments.html', current_appointments=[], past_appointments=[])

@app.route('/about')
def about():
    if session.get('user_id') is None:
        return redirect(url_for('patient_login'))  
    cursor.execute("SELECT name, profile_image FROM users WHERE user_id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if user:
        name = user[0]
        profile_image_blob = user[1] if user[1] else None

        if profile_image_blob:
            profile_image = base64.b64encode(profile_image_blob).decode('utf-8')
        else:
            profile_image = None
  
    return render_template('about.html',profile_image=profile_image,name=name)

@app.route('/dabout')
def dabout():
    if session.get('doctor_id') is None:
        return redirect(url_for('doctor_login'))
    
    cursor.execute("SELECT doc_name, profile_image FROM doctors WHERE doctor_id = %s", (session['doctor_id'],))
    user = cursor.fetchone()
    if user:
        profile_image = user[1]
    return render_template('dabout.html',profile_image=profile_image)

@app.route('/dhome')
def dhome():
    if session.get('doctor_id') is None:
        return redirect(url_for('doctor_login'))
    doctor_id = session['doctor_id']  # Assuming doctor_id is stored in the session
    try:
        cursor.execute("SELECT doc_name, profile_image FROM doctors WHERE doctor_id = %s", (session['doctor_id'],))
        user = cursor.fetchone()
        if user:
            profile_image = user[1]
        # Fetch pending appointments ('requested' or 'accepted')
        cursor.execute('''
            SELECT Users.name AS patient_name, Appointments.appointment_date, Appointments.status, Appointments.appointment_id, Appointments.gmeet_link 
            FROM Appointments 
            JOIN Users ON Appointments.patient_id = Users.user_id 
            WHERE Appointments.doctor_id = %s AND Appointments.status IN ('requested', 'accepted')
        ''', (doctor_id,))
        pending_appointments = cursor.fetchall()
        
        # Fetch finished appointments ('rejected' or 'concluded')
        cursor.execute('''
            SELECT Users.name AS patient_name, Appointments.appointment_date, Appointments.status, Appointments.appointment_id, Appointments.gmeet_link
            FROM Appointments 
            JOIN Users ON Appointments.patient_id = Users.user_id 
            WHERE Appointments.doctor_id = %s AND Appointments.status IN ('rejected', 'concluded')
        ''', (doctor_id,))
        finished_appointments = cursor.fetchall()
        
        return render_template('dhome.html', pending_appointments=pending_appointments, finished_appointments=finished_appointments, profile_image=profile_image)
    
    except mysql.connector.Error as err:
        print(f"Error fetching appointments data: {err}")
        return render_template('dhome.html', pending_appointments=[], finished_appointments=[])


@app.route('/patient_profile')
def patient_profile():
    if session.get('user_id') is None:
        return redirect(url_for('patient_login'))
    user_id = session['user_id']
    try:
        # Fetch user data from the database
        cursor.execute('SELECT name, email, phoneno, profile_image FROM Users WHERE user_id = %s', (user_id,))
        user_data = cursor.fetchone()
        
        if user_data:
            user_name, user_email, user_phoneno, profile_image = user_data
            if profile_image:
                profile_image = base64.b64encode(profile_image).decode('utf-8')
            return render_template('pprofile.html', user_name=user_name, user_email=user_email, user_phoneno=user_phoneno, profile_image=profile_image)
        else:
            return render_template('pprofile.html', user_name=None, user_email=None, user_phoneno=None, profile_image=None)
    
    except mysql.connector.Error as err:
        print(f"Error fetching user data: {err}")
        return render_template('pprofile.html', user_name=None, user_email=None, user_phoneno=None, profile_image=None)

@app.route('/doctor_profile')
def doctor_profile():
    if session.get('doctor_id') is None:
        return redirect(url_for('doctor_login'))
    doctor_id = session['doctor_id']  # Assuming doctor_id is stored in the session
    try:
        cursor.execute('''
            SELECT doc_name, profile_image, specialty, bio 
            FROM Doctors 
            WHERE doctor_id = %s
        ''', (doctor_id,))
        doctor = cursor.fetchone()
        if doctor:
            doc_name, profile_image, specialty, bio = doctor
        else:
            doc_name, profile_image, specialty, bio = "", "", "", ""

        return render_template('dprofile.html', doc_name=doc_name, profile_image=profile_image, specialty=specialty, bio=bio)
    
    except mysql.connector.Error as err:
        print(f"Error fetching doctor's profile data: {err}")
        return render_template('dprofile.html', doc_name="", profile_image="", specialty="", bio="")
    
@app.route('/reschedule_appointment/<int:appointment_id>', methods=['POST'])
def reschedule_appointment(appointment_id):
    if session.get('doctor_id') is None:
        return redirect(url_for('doctor_login'))
    new_date = request.form['new_date']
    new_time = request.form['new_time']
    new_datetime = f"{new_date} {new_time}:00"
    # Generate random gmeet_link
    gmeet_link = 'https://meet.google.com/' + ''.join(random.choice(string.ascii_lowercase) for _ in range(3)) + '-' + ''.join(random.choice(string.ascii_lowercase) for _ in range(4)) + '-' + ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
    affirmation = 'accepted' 
    try:
        cursor.execute('''
            UPDATE Appointments
            SET appointment_date = %s, gmeet_link = %s, status = %s
            WHERE appointment_id = %s
        ''', (new_datetime, gmeet_link, affirmation, appointment_id))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error rescheduling appointment: {err}")

    return redirect(url_for('dhome'))

@app.route('/conclude_appointment/<int:appointment_id>', methods=['POST'])
def conclude_appointment(appointment_id):
    if session.get('doctor_id') is None:
        return redirect(url_for('doctor_login'))
    try:
        finish = 'concluded'
        cursor.execute('''
            UPDATE Appointments
            SET status = %s
            WHERE appointment_id = %s
        ''', (finish, appointment_id))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error concluding appointment: {err}")
    return redirect(url_for('dhome'))

@app.route('/reject_appointment/<int:appointment_id>', methods=['POST'])
def reject_appointment(appointment_id):
    if session.get('doctor_id') is None:
        return redirect(url_for('doctor_login'))
    rejection_status = 'rejected'
    try:
        cursor.execute('''
            UPDATE Appointments
            SET status = %s
            WHERE appointment_id = %s
        ''', (rejection_status, appointment_id))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error rejecting appointment: {err}")

    return redirect(url_for('dhome'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if session.get('user_id') is None:
        return redirect(url_for('patient_login'))
    # Get the form data
    new_email = request.form['profileEmail']
    profile_image = request.files['profileImage']
    # Assuming user_id is stored in session or passed somehow
    user_id = session['user_id'] # Replace this with the actual user_id
    try:
        if profile_image:
            profile_image_data = profile_image.read()
            cursor.execute('''
                UPDATE Users
                SET profile_image = %s
                WHERE user_id = %s
            ''', (profile_image_data, user_id))
        if new_email:
            cursor.execute('''
                UPDATE Users
                SET email = %s
                WHERE user_id = %s
            ''', (new_email, user_id))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error updating profile: {err}")
        db.rollback()

    return redirect(url_for('patient_profile'))

@app.route('/plogout')
def plogout():
    session.pop('user_id', None)
    return redirect(url_for('patient_login'))
@app.route('/dlogout')
def dlogout():
    session.pop('doctor_id', None)
    return redirect(url_for('doctor_login'))

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/register', methods=['POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirm_password')
#         phoneno = request.form.get('phoneno')
#         profile_image = request.files['profile_image'] if 'profile_image' in request.files else None

#         # Validate name
#         if not name:
#             flash('Please enter your name.')
#             return redirect(url_for('psignup'))

#         # Validate email format
#         if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
#             flash('Invalid email address.')
#             return redirect(url_for('psignup'))

#         # Validate phone number
#         if not re.match(r'^\d{10}$', phoneno):
#             flash('Invalid phone number. Please enter a valid 10-digit phone number.')
#             return redirect(url_for('psignup'))

#         # Validate password strength
#         if not re.match(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%!]).{8,}$', password):
#             flash('Password must contain at least one uppercase letter, one digit, and one special character (@, #, $, %, or !), and be at least 8 characters long.')
#             return redirect(url_for('psignup'))

#         # Confirm password match
#         if password != confirm_password:
#             flash('Passwords do not match. Please re-enter your passwords.')
#             return redirect(url_for('psignup'))

#         db, cursor = connect_to_database()

#         try:
#             # Check if email already exists
#             cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#             existing_email = cursor.fetchone()
#             if existing_email:
#                 flash('Email already exists.')
#                 return redirect(url_for('psignup'))

#             # Insert new user into the database
#             if profile_image:
#                 profile_image_blob = profile_image.read()
#                 cursor.execute("INSERT INTO users (name, email, password, phoneno, profile_image) VALUES (%s, %s, %s, %s, %s)",
#                                (name, email, password, phoneno, profile_image_blob))
#             else:
#                 cursor.execute("INSERT INTO users (name, email, password, phoneno) VALUES (%s, %s, %s, %s)",
#                                (name, email, password, phoneno))

#             db.commit()
#             flash('Registration successful. Please log in.')
#             return redirect(url_for('plogin'))

#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             flash('Error occurred during registration. Please try again.')
#             return redirect(url_for('plogin'))

#         finally:
#             cursor.close()
#             db.close()

#     return render_template('psignup.html')

# Doctor Routes
