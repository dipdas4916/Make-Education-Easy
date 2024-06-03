from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import sqlite3
import re
import os
import math

app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Set a secret key for session management
# Generate a secret key
app.secret_key = os.urandom(24)


def create_table():
    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()
    
    # Create the loginInformation table if it doesn't exist

    # Table for Students Login information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS StudentloginInformation (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName VARCHAR(225) NOT NULL,
            lastName VARCHAR(225) NOT NULL,
            email VARCHAR(225) UNIQUE NOT NULL,
            gender VARCHAR(225) NOT NULL,
            password VARCHAR(225) NOT NULL
        )
    ''')

    # Table for Teacher Login information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TeacherloginInformation (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName VARCHAR(225) NOT NULL,
            lastName VARCHAR(225) NOT NULL,
            email VARCHAR(225) UNIQUE NOT NULL,
            gender VARCHAR(225) NOT NULL,
            password VARCHAR(225) NOT NULL
        )
    ''')

    # Table for store the Update Details of  Techaer
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TeacherUpdateDetails (
        Email TEXT PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        MobileNo TEXT NOT NULL,
        HouseNo TEXT NOT NULL,
        StreetName TEXT NOT NULL,
        TownVillage TEXT NOT NULL,
        PostOffice TEXT NOT NULL,
        PinCode TEXT NOT NULL,
        District TEXT NOT NULL,
        Landmark TEXT NOT NULL,
        State TEXT NOT NULL,
        Qualification TEXT NOT NULL,
        Specialization TEXT NOT NULL,
        Experience TEXT NOT NULL,
        PreferredTime TEXT NOT NULL,
        TotalBatch INTEGER NOT NULL,
        Fees INTEGER NOT NULL,
        FOREIGN KEY (Email) REFERENCES TeacherloginInformation(email)
    )
''')


    # Table for store the Update Details of Student
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS StudentUpdateDetails (
        Email TEXT PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,

        MobileNo TEXT NOT NULL,
        TownVillage TEXT NOT NULL,
        PostOffice TEXT NOT NULL,
        District TEXT NOT NULL,
        State TEXT NOT NULL,
        PinCode TEXT NOT NULL,

        Qualification TEXT NOT NULL,
        
        FOREIGN KEY (Email) REFERENCES StudentloginInformation(email)
    )
''')
    #print("Data cretae for student update")

    try:
        # Table for the Student - Teacher Enroll
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS TeacherStudentEnroll (
        teacher_email VARCHAR(100) NOT NULL,
        teacher_first_name VARCHAR(100) NOT NULL,
        teacher_last_name VARCHAR(100) NOT NULL,
        
        student_email VARCHAR(100) NOT NULL,
        student_first_name VARCHAR(100) NOT NULL,
        student_last_name VARCHAR(100) NOT NULL,
        batch_location VARCHAR(100) NOT NULL,
        enrolled_subject VARCHAR(100) NOT NULL,
        review INT DEFAULT 0,

        PRIMARY KEY (teacher_email, student_email),
        FOREIGN KEY (teacher_email) REFERENCES TeacherUpdateDetails(Email),
        FOREIGN KEY (student_email) REFERENCES StudentUpdateDetails(Email)
        )
    ''')
        print("Database Create successful")
    except:
        print("Database is not created")

    

    
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Call the create_table function when the application starts
create_table()
'''
def droptable():
    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute("DROP TABLE TeacherStudentEnroll")

# Commit the transaction
    conn.commit()

# Close the cursor and connection
    cursor.close()
    conn.close()

    print("Table alter  successfully.")

droptable()
'''







@app.route('/')
def homepage():
    return render_template("Home.html")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

def create_connection():
    return sqlite3.connect("User.db")




# Validate password
def check_password(password):
    if not 8 <= len(password) <= 16:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_+=" for char in password):
        return False
    return True



# Validate email
def validate_email(email):
    # Regular expression to validate email address
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    if re.match(pattern, email):
        return True
    else:
        return False









# Register for new STUDENT
@app.route('/sregister', methods=['GET', 'POST'])
def sregister():
      # Initialize error to None
    error = None
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        gender = request.form['gender']
        
        # Perform form validation
        if not (first_name and last_name and email and password and confirm_password and gender):
            error = 'Please fill out all fields.'
            return render_template('student_register.html', error=error)

        elif not validate_email(email):
            error = 'Invalid email address. Please provide a valid Gmail address.'
            return render_template('student_register.html', error=error)

        elif not check_password(password):
            error = 'Password does not meet the criteria'
            return render_template('student_register.html', error=error)

        elif password != confirm_password:
            error = 'Passwords do not match.'
            return render_template('student_register.html', error=error)
        else:
            # Connect to the SQLite3 database
            conn = create_connection()
            cursor = conn.cursor()

            try:
                # Insert user information into the database
                cursor.execute("INSERT INTO StudentloginInformation (firstName, lastName, email, gender, password) VALUES (?, ?, ?, ?, ?)",
                               (first_name, last_name, email, gender, password))
                conn.commit()
                
                # Return a success message or redirect to another page after registration
                return "Registration successful!"
            except sqlite3.IntegrityError:
                # Handle unique constraint violation (email already exists)
                error = 'Email already exists.'
                return render_template('student_register.html', error=error)
            finally:
                # Close the database connection
                conn.close()

    # If it's a GET request or the form submission failed, render the register.html template with the error
    return render_template('student_register.html', error=error)







# Register for new TEACHER
@app.route('/tregister', methods=['GET', 'POST'])
def tregister():
    error = None  # Initialize error to None
    conn = create_connection()
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        gender = request.form['gender']
        
        try:
            # Perform form validation
            if not (first_name and last_name and email and password and confirm_password and gender):
                raise ValueError('Please fill out all fields.')
            if not validate_email(email):
                raise ValueError('Invalid email address. Please provide a valid Gmail address.')
            if not check_password(password):
                raise ValueError('Password does not meet the criteria')
            if password != confirm_password:
                raise ValueError('Passwords do not match.')

            # Connect to the SQLite3 database
            
            cursor = conn.cursor()
            
            # Insert user information into the database
            cursor.execute("INSERT INTO TeacherloginInformation (firstName, lastName, email, gender, password) VALUES (?, ?, ?, ?, ?)",
                           (first_name, last_name, email, gender, password))
            conn.commit()
                
            # Return a success message or redirect to another page after registration
            return "Registration successful!"
        except ValueError as e:
            # Assign the error message to the error variable
            error = str(e)
        except sqlite3.IntegrityError:
            # Handle unique constraint violation (email already exists)
            error = 'Email already exists.'
        finally:
            # Close the database connection
            conn.close()

    # If it's a GET request or the form submission failed, render the teacher_register.html template with the error
    return render_template('teacher_register.html', error=error)

















# STUDENT - TEACHER LOGIN 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        semail = request.form.get('semail')
        spassword = request.form.get('spassword')
        temail = request.form.get('temail')
        tpassword = request.form.get('tpassword')
        
        conn = create_connection()
        cursor = conn.cursor()
        


        # STUDENT - LOGIN CONDITION
        # Check if the provided credentials match with any student in the database
        if semail and spassword:
            cursor.execute("SELECT * FROM StudentloginInformation WHERE email=? AND password=?", (semail, spassword))
            user = cursor.fetchone()
            


            if user:
                session['user'] = semail
                session['role'] = 'student'
                return redirect(url_for('sdashboard'))
            
            

            else:
                # Invalid student credentials, display an error message
                return render_template('login.html', error='Invalid email or password.')
        
        
        # TEACHER - LOGIN CONDITION
        # Check if the provided credentials match with any teacher in the database
        elif temail and tpassword:
            cursor1 = conn.cursor()
            cursor1.execute("SELECT * FROM TeacherloginInformation WHERE email=? AND password=?", (temail, tpassword))
            user = cursor1.fetchone()
            
            if user:
                session['user'] = temail
                session['role'] = 'teacher'


                return redirect(url_for('tdashboard'))

            # Query the database to retrieve teacher information
            cursor2 = conn.cursor()
            cursor2.execute("SELECT firstName, email FROM TeacherloginInformation WHERE email = ? AND password = ?", (temail, tpassword))
            teacher_info = cursor2.fetchone()  # Assuming only one row is returned
            # If teacher_info is not None, it means the teacher exists
            
            if teacher_info:
                # Retrieve name and email from the fetched data
                teacher_name, teacher_email = teacher_info
                # Proceed to dashboard with teacher_name and teacher_email
            else:
                # Invalid teacher credentials, display an error message
                return render_template('login.html', error='Invalid email or password.')
        
        conn.close()
    
    return render_template('login.html')


#logout 
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to the login page or another appropriate location
    return redirect(url_for('login'))



# Student Dashboard
@app.route('/sdashboard')
def sdashboard():
    if 'user' in session and session['role'] == 'student':
        # Retrieve email from session
        email = session.get('user')

        # Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Query the database to retrieve student's name and email
        cursor.execute("SELECT firstName, email FROM StudentloginInformation WHERE email = ?", (email,))
        student_info = cursor.fetchone()

        cursor2 = conn.cursor()
        cursor2.execute("""
        SELECT tud.TownVillage, tud.PostOffice,tud.District, tud.State, tud.PinCode
        FROM StudentloginInformation tli
        INNER JOIN StudentUpdateDetails tud ON tli.email = tud.Email
        WHERE tli.email = ?
        """, (email,))

        address_details = cursor2.fetchone()


        if student_info:
            # Retrieve name and email from the fetched data
            student_name, student_email = student_info
            # Store student's name and email in session
            session['student_name'] = student_name
            session['student_email'] = student_email
        else:
            # Handle the case where the student's information is not found
            student_name = None
            student_email = None

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return render_template("student_dashboard.html", name=student_name, email=student_email, address=address_details)
    else:
        return redirect(url_for('login'))




# Teacher Dashboard
# Teacher Dashboard
@app.route('/tdashboard')
def tdashboard():
    if 'user' in session and session['role'] == 'teacher':
        # Retrieve email from session
        email = session.get('user')
        
        # Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

    
        # Query the database to retrieve teacher's name and email
        cursor.execute("SELECT firstName, email FROM TeacherloginInformation WHERE email = ?", (email,))
        teacher_info = cursor.fetchone()


        cursor2 = conn.cursor()
        cursor2.execute("""
        SELECT tud.HouseNo, tud.StreetName, tud.Landmark, tud.District, tud.State, tud.PinCode
        FROM TeacherloginInformation tli
        INNER JOIN TeacherUpdateDetails tud ON tli.email = tud.Email
        WHERE tli.email = ?
        """, (email,))

        address_details = cursor2.fetchone()

    
        if teacher_info:
            # Retrieve name and email from the fetched data
            teacher_name, teacher_email = teacher_info
            # Store teacher's name and email in session
            session['teacher_name'] = teacher_name
            session['teacher_email'] = teacher_email
        else:
            # Handle the case where the teacher's information is not found
            teacher_name = None
            teacher_email = None
    
        # Close the cursor and connection
        cursor.close()
        conn.close()

        return render_template("teacher_dashboard.html", name=teacher_name, email=teacher_email, address = address_details)
    else:
        return redirect(url_for('login'))


# Update Tecaher Details:
# @app.route('/teacher_update')
# def teacher_update():
#     return render_template('teacher_update.html')


@app.route('/teacher_update', methods=['POST', 'GET'])
def teacher_update():
    error = None  # Initialize error to None

    if 'user' in session and session['role'] == 'teacher':
        # Retrieve email from session
        email = session.get('user')

        # Connect to the database
        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # Fetch teacher's information from TeacherloginInformation table
        cursor.execute("SELECT firstName, lastName FROM TeacherloginInformation WHERE email = ?", (email,))
        teacher_info = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if teacher_info:
            # Retrieve name and email from the fetched data
            teacher_fname, teacher_lname = teacher_info

    if request.method == 'POST':
        # Fetching data from the form
        mobile_no = request.form['mobile_no']
        house_no = request.form['house_no']
        street_name = request.form['street_name']
        town_village = request.form['town_village']
        post_office = request.form['post_office']
        pin_code = request.form['pin_code']
        district = request.form['district']
        landmark = request.form['landmark']
        state = request.form['state']
        qualification = request.form['Qualification']
        specialization = request.form['Specialization']
        experience = request.form['experience']
        preferred_time = request.form.getlist('preferred_time')
        total_batch = request.form['total_batch']
        fees = request.form['fees']

        # Database connection
        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # SQL query to insert data into the database
        try:
            insert_query = """INSERT INTO TeacherUpdateDetails (Email,FirstName,LastName, MobileNo, HouseNo, StreetName,
                                                            TownVillage, PostOffice, PinCode, District, Landmark, State,
                                                            Qualification, Specialization, Experience, PreferredTime,
                                                            TotalBatch, Fees)
                          VALUES (?, ?, ?, ?, ?, ?, ?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            # Execute the query with the provided data
            cursor.execute(insert_query, (email,teacher_fname, teacher_lname, mobile_no, house_no, street_name, town_village,
                                           post_office, pin_code, district, landmark, state, qualification,
                                           specialization, experience, ', '.join(preferred_time), total_batch, fees))

            # Commit the transaction
            conn.commit()

            # Return a success message or redirect to another page after registration
            return "Profile Update successful!"

        except sqlite3.IntegrityError:
            # Handle unique constraint violation (email already exists)
            error = 'Email already exists.'
        finally:
            # Close the database connection
            conn.close()

    return render_template('teacher_update.html', teacher_fname=teacher_fname, teacher_lname=teacher_lname,
                           teacher_email=email, error=error)





@app.route('/student_update', methods=['POST','GET'])
def student_update():
    error = None  # Initialize error to None

    if 'user' in session and session['role'] == 'student':
        # Retrieve email from session
        email = session.get('user')

    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()

    # Fetch teacher's information from TeacherloginInformation table
    cursor.execute("SELECT firstName, lastName FROM StudentloginInformation WHERE email = ?", (email,))
    student_info = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    if student_info:
        # Retrieve name and email from the fetched data
        student_fname, student_lname = student_info

    if request.method == 'POST':
        # Fetching data from the form
        # first_name = request.form['first_name']
        # last_name = request.form['last_name']
        # email = request.form['email']
        mobile_no = request.form['mobile_no']
        
        town_village = request.form['town_village']
        post_office = request.form['post_office']
        pin_code = request.form['pin_code']
        district = request.form['district']
        
        state = request.form['state']
        qualification = request.form['Qualification']
        
        # Database connection
        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()

        # SQL query to insert data into the database
        try:
            insert_query = """INSERT INTO StudentUpdateDetails (Email, FirstName, LastName, MobileNo,
                                                            TownVillage, PostOffice, District,State,PinCode,
                                                            Qualification)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        # Execute the query with the provided data
            cursor.execute(insert_query, (email, student_fname, student_lname, mobile_no, town_village,
                                 post_office, district, state, pin_code,  qualification, ))
        
        # Commit the transaction
            conn.commit()
            # Return a success message or redirect to another page after registration
            return "Profile Update successful!"

        except sqlite3.IntegrityError:
            # Handle unique constraint violation (email already exists)
            error = 'Email already exists.'
        finally:
            # Close the database connection
            conn.close()

    return render_template('student_update.html',student_fname=student_fname, student_lname=student_lname,student_email=email,error = error)




# Search Techer By the Student Using Location and Subject name
@app.route('/search_teacher', methods=['POST'])
def search_teacher():

    # Retrieve student's email from the session
    student_email = session.get('user')

    if not student_email:
        return "User email not found in session", 404

    '''
    location = request.form.get('location')
    subject = request.form.get('subject')
    '''
    subject = request.form.get('subject')  
    locationOrPincode = request.form.get('locationOrPincode') # Convert location/pincode to lowercase
    searchOption = request.form.get('searchOption')

    #print(subject)
    #print(locationOrPincode)


    subject = subject.lower() # Convert subject to lowercase
    locationOrPincode = locationOrPincode.lower()# Convert location/pincode to lowercase

    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()

    '''
    # Execute query to fetch teachers based on location and subject
    cursor.execute("""
        SELECT FirstName, LastName,Email, TownVillage, Qualification, Specialization, Fees 
        FROM TeacherUpdateDetails 
        WHERE TownVillage = ? AND Specialization = ?
    """, (location, subject))
    teachers = cursor.fetchall()
    '''
    if searchOption == 'location':
        # Search by location
        cursor.execute("SELECT FirstName, LastName,Email, TownVillage,PinCode, Qualification, Specialization, Fees FROM TeacherUpdateDetails WHERE LOWER(TownVillage) = ? AND LOWER(Specialization) = ?", (locationOrPincode, subject))
    elif searchOption == 'pincode':
        # Search by pincode
        cursor.execute("SELECT FirstName, LastName,Email, TownVillage,PinCode, Qualification, Specialization, Fees FROM TeacherUpdateDetails WHERE LOWER(PinCode) = ? AND LOWER(Specialization) = ?", (locationOrPincode, subject))
    else:
        return "Invalid search option", 400

    teachers = cursor.fetchall()







    # Close database connection
    conn.close()

    return render_template('display_teacher.html', teachers=teachers,student_email=student_email)



# Enroll student for the Teacher
@app.route('/enroll', methods=['POST','GET'])
def enroll_student():
    # Retrieve student's email from the session
    student_email = session.get('user')

    if not student_email:
        return "User email not found in session", 404

    # Fetch student's information from the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()
    cursor.execute("SELECT firstName, lastName FROM StudentloginInformation WHERE email = ?", (student_email,))
    student_info = cursor.fetchone()

    if not student_info:
        cursor.close()
        conn.close()
        return "Student information not found", 404

    # Extract student's first name and last name
    student_first_name, student_last_name = student_info

    # Extract teacher's information from the request payload
    data = request.json
    teacher_email = data.get('teacher_email')
    teacher_first_name = data.get('teacher_first_name')
    teacher_last_name = data.get('teacher_last_name')
    subject_name = data.get('subject_name')
    location = data.get('location')

    
    # print(teacher_email)
    # print(teacher_first_name)
    # print(teacher_last_name)


    if not teacher_email or not teacher_first_name or not teacher_last_name:
        return "Invalid request. Teacher information missing", 400
    
        # Connect to the database
    cursor.execute("""
        INSERT INTO TeacherStudentEnroll (teacher_email,teacher_first_name,teacher_last_name, 
                                            student_email, student_first_name, student_last_name, enrolled_subject, batch_location)
            VALUES (?, ?, ?, ?,?, ?,?,?)
        """, (teacher_email,teacher_first_name,teacher_last_name, 
            student_email, student_first_name, student_last_name,subject_name,location))
    conn.commit()

        # Close database connection
    cursor.close()
    conn.close()

    return "Enrollment successful", 200


@app.route('/enrolled_teachers', methods=['GET'])
def enrolled_teachers():
    # Retrieve student's email from the session
    student_email = session.get('user')

    if not student_email:
        return "User email not found in session", 404

    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()

    # Fetch enrolled teachers for the student from the database
    cursor.execute("""
        SELECT teacher_email, teacher_first_name, teacher_last_name, enrolled_subject, batch_location
        FROM TeacherStudentEnroll
        WHERE student_email = ?
    """, (student_email,))
    enrolled_teachers = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Render the enrolled teachers page with the fetched data
    return render_template('enrolled_teachers.html', enrolled_teachers=enrolled_teachers)




@app.route('/enrolled_batch_teacher')
def enrolled_batch_teacher():
    # Retrieve teacher's email from the session
    teacher_email = session.get('user')

    if not teacher_email:
        return "User email not found in session", 404

    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()

    # Fetch enrolled students for the teacher
    cursor.execute("""
        SELECT student_email, student_first_name, student_last_name, enrolled_subject, batch_location
        FROM TeacherStudentEnroll
        WHERE teacher_email = ?
    """, (teacher_email,))
    enrolled_students = cursor.fetchall()

    # Close database connection
    cursor.close()
    conn.close()

    return render_template('enrolled_students.html', enrolled_students=enrolled_students)



# Check enrollment status for a teacher
@app.route('/check_enrollment', methods=['GET'])
def check_enrollment():
    # Retrieve the teacher's email from the request query parameters
    teacher_email = request.args.get('teacher_email')

    # Retrieve the student's email from the session
    student_email = session.get('user')

    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()

    # Check if the student is enrolled to the specified teacher
    cursor.execute("""
        SELECT COUNT(*) FROM TeacherStudentEnroll 
        WHERE teacher_email = ? AND student_email = ?
    """, (teacher_email, student_email))
    enrollment_count = cursor.fetchone()[0]

    # Close database connection
    cursor.close()
    conn.close()

    # Return JSON response indicating enrollment status
    return jsonify({'enrolled': enrollment_count > 0})









@app.route('/remove_student', methods=['POST'])
def remove_student():
    if request.method == 'POST':
        email = request.json.get('email')
        # Remove the student from the TeacherStudentEnroll table using the email

        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM TeacherStudentEnroll WHERE student_email=?", (email,))
            conn.commit()  # Commit the transaction
            return "Student removed successfully!", 200
        except Exception as e:
            conn.rollback()  # Rollback changes if an exception occurs
            return "Error: " + str(e), 500
        finally:
            cursor.close()
            conn.close()
    return "Invalid request", 400














@app.route('/delete_account', methods=['POST'])
def delete_account():
    if request.method == 'POST':
        email = request.json.get('email')
        
        conn = sqlite3.connect('User.db')
        cursor = conn.cursor()
        
        try:
            # Delete from StudentloginInformation table
            cursor.execute("DELETE FROM StudentloginInformation WHERE email=?", (email,))
            
            # Delete from StudentUpdateDetails table
            cursor.execute("DELETE FROM StudentUpdateDetails WHERE email=?", (email,))
            
            conn.commit()  # Commit the transaction
            return "Account deleted successfully!", 200
        except Exception as e:
            conn.rollback()  # Rollback changes if an exception occurs
            return "Error: " + str(e), 500
        finally:
            cursor.close()
            conn.close()
    return "Invalid request", 400




























@app.route('/add_review', methods=['POST'])
def add_review():
    # Retrieve data from the request
    data = request.json
    teacher_email = data.get('teacher_email')
    student_email = session.get('user')
    review = data.get('review')
    print("Teacher Email:",teacher_email)
    print("Student Email: ", student_email)
    print("Review details:", review)
    # Validate the data
    if not teacher_email or not student_email or not review:
        return "Invalid request. Missing data", 400

    # Connect to the database
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()

    # Update the review in the TeacherStudentEnroll table
    cursor.execute("""
        UPDATE TeacherStudentEnroll
        SET review = ?
        WHERE teacher_email = ? AND student_email = ?
    """, (review, teacher_email, student_email))
    conn.commit()

    # Close database connection
    cursor.close()
    conn.close()

    return "Review added successfully", 200

 

# Define route to get reviews for a teacher
@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    # Get the teacher email from the request URL
    teacher_email = request.args.get('teacher_email')

    # Query the database to fetch reviews for the specified teacher
    conn = sqlite3.connect('User.db')
    cursor = conn.cursor()
    cursor.execute("SELECT review FROM TeacherStudentEnroll WHERE teacher_email = ?", (teacher_email,))
    reviews = cursor.fetchall()

    # Calculate average review
    total_reviews = len(reviews)
    if total_reviews > 0:
        sum_reviews = sum(review[0] for review in reviews)
        avg_review = sum_reviews / total_reviews
    else:
        avg_review = 0
    print(avg_review)

    # Close database connection
    cursor.close()
    conn.close()

    # Return average review as JSON response
    return jsonify(avg_review=avg_review)











# View the user details
@app.route('/view')
def viewDetails():
    con = create_connection()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    # Fetch data from StudentloginInformation table
    cur.execute("SELECT * FROM StudentloginInformation")
    student_rows = cur.fetchall()
    
    # Fetch data from TeacherloginInformation table
    cur.execute("SELECT * FROM TeacherloginInformation")
    teacher_rows = cur.fetchall()
    # Fetch data from TeacherUpdateDetails table
    cur.execute("SELECT * FROM TeacherUpdateDetails")
    teacher_update = cur.fetchall()


    # Fetch data from StudentUpdateDetails table
    cur.execute("SELECT * FROM StudentUpdateDetails")
    student_update = cur.fetchall()

    # Fetch data from TeacherStudentEnroll table
    cur.execute("SELECT * FROM TeacherStudentEnroll")
    enroll_details = cur.fetchall()

    con.close()
    
    return render_template("view.html", student_rows=student_rows, teacher_rows=teacher_rows, teacher_update = teacher_update, student_update= student_update, enroll_details = enroll_details)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)