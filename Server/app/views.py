from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for, session, flash
import re

my_cursor = db.my_cursor

@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    #if 'SSN' in session:
        return render_template('public/templates/home.html')
    #else:
    #    flash('You are logged out. Please login again to continue')
    #    return redirect( url_for('login') )

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'username' in session:                # Checking for session login
       return redirect( url_for('home') )

    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        rSSN = request.form['rSSN']

        idssn= my_cursor.execute(f"SELECT ReceptionistSSN FROM RECEPTIONIST WHERE ReceptionistFirstName = '{username}'")
        ExistedSSN = my_cursor.fetchone()
        
        query = my_cursor.execute(f"SELECT ReceptionistPass FROM RECEPTIONIST WHERE ReceptionistFirstName = '{username}'")
        Existedpass = my_cursor.fetchone()
        
        usna= my_cursor.execute(f"SELECT ReceptionistFirstName FROM RECEPTIONIST WHERE ReceptionistFirstName = '{username}'")
        Existedname = my_cursor.fetchone()
        
        if (Existedname == None and Existedpass == None and ExistedSSN == None) :
            flash('User Not Found', category='error')
            return redirect( url_for('login') )

        elif ( username == str(Existedname[0]) and str(password) == str(Existedpass[0]) and int(rSSN)==int(ExistedSSN[0]) ) :
            session['username'] = username  # saving session for login
            return redirect( url_for('staffPage') )
        #add conditions
        else:
            flash('Wrong Credentials. Check SSN, Username or Password Again', category="error")        
    return render_template('/public/templates/login.html') 

       #my_cursor.execute("SELECT StaffFirstName FROM STAFF")  
        #    rv = my_cursor.fetchall()
       #my_cursor.execute(f" SELECT * FROM PRODUCT WHERE label = '{username}' ")
       
       #query = (" INSERT INTO STAFF (staffID,StaffFirstName,StaffLastName,StaffSpecialization) VALUES (%s,%s,%s,%s)" )
          #  my_cursor.execute(query,(okas,username,password,em))
           
            #my_cursor.execute("SELECT StaffFirstName FROM STAFF")  
            #rv = my_cursor.fetchall()

           # print(rv)

           #
           
@app.route('/signup', methods=["GET", "POST"])
def signup():

        if request.method == 'POST':
            receptionistSSN = request.form['rSSN']
            receptionistFirstName = request.form['fname']
            receptionistLastName = request.form['lname']
            receptionistPass = request.form['password']
            confpass = request.form['confpass']
           # receptionistAddress = request.form['address']
            #receptionistPhoneNumber = request.form['pnumber']
            #receptionistGender = request.form['gender']

            query = my_cursor.execute(f"SELECT ReceptionistFirstName FROM RECEPTIONIST WHERE ReceptionistFirstName = '{receptionistFirstName}' ")
            existedname = my_cursor.fetchone()
            
            if existedname != None:
                if receptionistFirstName == str(existedname[0]):
                    flash('Username already taken')
                    return redirect( url_for('signup', response = receptionistFirstName),  )
               
            if receptionistPass != confpass:
                flash('Passwords do not match')
                return redirect( url_for('signup') )

            regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pattern = re.compile(regex)

            match = re.search(pattern, receptionistPass)

            if match:
                user = ("INSERT INTO RECEPTIONIST (ReceptionistSSN,ReceptionistFirstName,ReceptionistLastName,ReceptionistPass) VALUES (%s,%s,%s,%s)" )
                #user = ("INSERT INTO RECEPTIONIST (ReceptionistSSN,ReceptionistFirstName,ReceptionistLastName,ReceptionistPass, ReceptionistAddress, ReceptionistPhoneNumber, ReceptionistGender) VALUES (%s,%s,%s,%s,%s,%s,%s)" )
                #receptionistFirstName,receptionistLastName,receptionistPass,receptionistAddress, receptionistPhoneNumber, receptionistGender )
                my_cursor.execute(user,(receptionistSSN,receptionistFirstName,receptionistLastName,receptionistPass))
                db.mydb.commit()
                flash('Staff Registred Successfully', category='info')
                return redirect( url_for('login') )
            else:
                flash('Password should contain one Uppercase, one special character, one numeric character')
                return redirect( url_for('signup') )
            
                
            
        return render_template('/public/templates/signup.html')     

   

@app.route('/create_patient')
def booking():
    
#    if request.method == 'POST':
#        patientSSN = request.form['pSSN']
#        patientFirstName = request.form['fname']
#        patientLastName = request.form['lname']
#        patientAge = request.form['age']
#        patientAddress = request.form['address']
#        patientPhoneNumber = request.form['pnumber']
#        patientFamilyNumber = request.form['fnumber']

   return render_template('/public/templates/booking.html')     

@app.route('/booking-room')
def booking_room():
    return render_template('/public/templates/booking_room.html')  

@app.route('/staffPage')
def staffPage():
    return render_template('/public/templates/staffPage.html')  

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('logged out successfully .')
    return redirect( url_for('home') )       