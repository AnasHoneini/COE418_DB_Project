# file for views

#importing our package (treating this directory as a package)
from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for, session, flash
import re

my_cursor = db.my_cursor

    
@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    #if 'username' in session:
       return render_template('public/templates/home.html')
    #else:
     #   flash('You are logged out. Please login again to continue')
      #  return redirect( url_for('home') )  
@app.route('/login', methods=["GET", "POST"])
def login():
    #if 'username' in session:                # Checking for session login
     #   return redirect( url_for('home') )

    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        SSN = request.form['SSN']

        idssn= my_cursor.execute(f"SELECT StaffID FROM Staff WHERE StaffFirstName = '{username}'")
        SSNExcuted = my_cursor.fetchone()
        
        query = my_cursor.execute(f"SELECT Pass FROM Staff WHERE StaffFirstName = '{username}'")
        pass1 = my_cursor.fetchone()
        
        usna= my_cursor.execute(f"SELECT StaffFirstName FROM Staff WHERE StaffFirstName = '{username}'")
        name = my_cursor.fetchone()
        
        if name[0] == None:
            flash('User Not Found', category='error')
            return redirect( url_for('login') )

        elif ( username == str(name[0]) and str(password) == str(pass1[0]) and int(SSN)==int(SSNExcuted[0]) ) :
            session['username'] = username  # saving session for login
            return redirect( url_for('home') )

        else:
            flash('Wrong Credentials. Check Username and Password Again', category="error")        
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
           
           #
@app.route('/signup', methods=["GET", "POST"])
def signup():
        if request.method == 'POST':
            SSN = request.form['SSN']
            username = request.form['name']
            password = request.form['password']
            confpass=request.form['confpass']

            query = my_cursor.execute(f"SELECT StaffFirstName FROM Staff WHERE StaffFirstName = '{username}' ")
            existedname = my_cursor.fetchone()
            
            if existedname != None:
                if username == str(existedname[0]):
                    flash('Username already taken')
                    return redirect( url_for('signup') )
               
            if password != confpass:
                flash('Passwords do not match')
                return redirect( url_for('signup') )

            regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pattern = re.compile(regex)

            match = re.search(pattern, password)
        
            if match:
                user = ("INSERT INTO STAFF (staffID,StaffFirstName,StaffLastName,Pass,StaffSpecialization) VALUES (%s,%s,%s,%s,%s)" )
                my_cursor.execute(user,(SSN,username,username,password, 'das'))
                db.mydb.commit()
                flash('Staff Registred Successfully', category='info')
                return redirect( url_for('login') )
            else:
                flash('Password should contain one Uppercase, one special character, one numeric character')
                return redirect( url_for('signup') )
            
                
            
        return render_template('/public/templates/signup.html')     



@app.route('/booking')
def booking():
        return render_template('/public/templates/booking.html')     

@app.route('/booking-room')
def booking_room():
    return render_template('/public/templates/booking_room.html')  





@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('logged out successfully .')
    return redirect( url_for('login') )       