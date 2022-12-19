import datetime
from gettext import npgettext
from app import app
from app import db
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date, datetime
import re

my_cursor = db.my_cursor


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    if 'SSN' in session:
        return render_template('public/templates/staffPage.html')
    else:
        flash('You are logged out. Please login again to continue')
        return render_template('public/templates/home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'SSN' in session:                # Checking for session login
        return redirect(url_for('staffPage'))

    if request.method == 'POST':
        firstName = request.form['fname']
        lastName = request.form['lname']
        password = request.form['password']
        SSN = request.form['SSN']

        if ((firstName == '' or lastName == '' or password == '' or SSN == '')):
            flash('Please fill the form', category='error')
            return redirect(url_for('login'))

        idssn = my_cursor.execute(
            f"SELECT ReceptionistSSN FROM RECEPTIONIST WHERE ReceptionistFirstName = '{firstName}' AND ReceptionistLastName ='{lastName}' ")
        ExistedSSN = my_cursor.fetchone()

        query = my_cursor.execute(
            f"SELECT ReceptionistPass FROM RECEPTIONIST WHERE ReceptionistFirstName = '{firstName}' AND ReceptionistLastName ='{lastName}'")
        Existedpass = my_cursor.fetchone()

        usna = my_cursor.execute(
            f"SELECT ReceptionistFirstName FROM RECEPTIONIST WHERE ReceptionistFirstName = '{firstName}' AND ReceptionistLastName ='{lastName}'")
        ExistedFirstName = my_cursor.fetchone()

        usna2 = my_cursor.execute(
            f"SELECT ReceptionistLastName FROM RECEPTIONIST WHERE ReceptionistFirstName = '{firstName}' AND ReceptionistLastName ='{lastName}'")
        ExistedLastName = my_cursor.fetchone()

        if (ExistedFirstName == None and ExistedLastName == None and Existedpass == None and ExistedSSN == None):
            flash('User not Found', category='error')
            return redirect(url_for('login'))

        elif (firstName == str(ExistedFirstName[0]) and lastName == str(ExistedLastName[0]) and str(password) == str(Existedpass[0]) and int(SSN) == int(ExistedSSN[0])):
            session['SSN'] = SSN  # saving session for login
            flash('Logged in', category="success")

            return redirect(url_for('staffPage'))

        else:
            flash('Wrong Creditentials', category="error")
    return render_template('/public/templates/login.html')

    # my_cursor.execute("SELECT StaffFirstName FROM STAFF")
    #    rv = my_cursor.fetchall()
    # my_cursor.execute(f" SELECT * FROM PRODUCT WHERE label = '{username}' ")

    # query = (" INSERT INTO STAFF (staffID,StaffFirstName,StaffLastName,StaffSpecialization) VALUES (%s,%s,%s,%s)" )
    #  my_cursor.execute(query,(okas,username,password,em))

    # my_cursor.execute("SELECT StaffFirstName FROM STAFF")
    # rv = my_cursor.fetchall()

    # print(rv)

    #


@app.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == 'POST':
        receptionistSSN = request.form['SSN']
        receptionistFirstName = request.form['fname']
        receptionistLastName = request.form['lname']
        receptionistPass = request.form['password']
        confpass = request.form['confpass']
        receptionistAddress = request.form['address']
        receptionistPhoneNumber = request.form['pnumber']
        receptionistGender = request.form['gender']

        query = my_cursor.execute(
            f"SELECT receptionistSSN FROM RECEPTIONIST")
        existedssn = my_cursor.fetchall()
        for i in range(0, len(existedssn)):

            if receptionistSSN == int(existedssn[i][0]):
                flash('SSN already taken')
                return redirect(url_for('signup'))

        query = my_cursor.execute(
            f"SELECT ReceptionistFirstName FROM RECEPTIONIST WHERE ReceptionistFirstName = '{receptionistFirstName}' ")
        existedFirstName = my_cursor.fetchone()
        query = my_cursor.execute(
            f"SELECT ReceptionistLastName FROM RECEPTIONIST WHERE ReceptionistLastName = '{receptionistLastName}' ")
        existedLastName = my_cursor.fetchone()

        if existedFirstName != None and existedLastName != None:
            if receptionistFirstName == str(existedFirstName[0]) and receptionistLastName == str(existedLastName[0]):
                flash('Username already taken')
                return redirect(url_for('signup'))

        if receptionistPass != confpass:
            flash('Passwords do not match')
            return redirect(url_for('signup'))

        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pattern = re.compile(regex)

        match = re.search(pattern, receptionistPass)

        if match:
            user = ("INSERT INTO RECEPTIONIST (ReceptionistSSN,ReceptionistFirstName,ReceptionistLastName,ReceptionistPass, ReceptionistAddress, ReceptionistGender, ReceptionistPhoneNumber) VALUES (%s,%s,%s,%s,%s,%s,%s)")

            my_cursor.execute(
                user, (receptionistSSN, receptionistFirstName, receptionistLastName, receptionistPass, receptionistAddress, receptionistGender,  receptionistPhoneNumber))
            db.mydb.commit()
            flash('Staff Registred Successfully', category='info')
            return redirect(url_for('login'))
        else:
            flash(
                'Password should contain one Uppercase, one special character, one numeric character')
        return redirect(url_for('signup'))

    return render_template('/public/templates/signup.html')


@app.route('/staffPage')
def staffPage():
    if 'SSN' in session:
        query = my_cursor.execute(
            f"SELECT ReceptionistFirstName FROM RECEPTIONIST WHERE ReceptionistSSN = '{session['SSN']}' ")
        existedFirstName = my_cursor.fetchone()
        query = my_cursor.execute(
            f"SELECT ReceptionistLastName FROM RECEPTIONIST WHERE ReceptionistSSN = '{session['SSN']}' ")
        existedLastName = my_cursor.fetchone()
        if existedFirstName != None and existedLastName != None:
            return render_template('/public/templates/staffPage.html', name=existedFirstName[0] + ' ' + existedLastName[0])
    return render_template('/public/templates/staffPage.html')


@app.route('/create_patient', methods=["GET", "POST"])
def create_patient():
    if 'SSN' in session:
        if request.method == 'POST':
            patientSSN = request.form['pSSN']
            patientFirstName = request.form['fname']
            patientLastName = request.form['lname']
            patientAge = request.form['age']
            patientAddress = request.form['address']
            patientGender = request.form['gender']
            patientPhoneNumber = request.form['pnumber']
            patientFamilyNumber = request.form['fnumber']
            roomNumber = request.form['roomNB']
            patientEnteringDateRoom = request.form['PEDR']
            patientLeavingDateRoom = request.form['PLDR']
            rdate = datetime.now()
            query = my_cursor.execute(
                f"SELECT patientSSN FROM PATIENT WHERE patientSSN = '{patientSSN}' ")
            existedSSN = my_cursor.fetchone()

            if existedSSN == None:

                user = ("INSERT INTO PATIENT (patientSSN,patientFirstName,patientLastName,patientAge, patientAddress, patientGender, patientPhoneNumber, patientFamilyNumber, patientEnteringDateRoom, patientLeavingDateRoom, RegistrationDate, receptionistSSN, roomNb) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

                userssn = session['SSN']
                my_cursor.execute(
                    user, (patientSSN, patientFirstName, patientLastName, patientAge, patientAddress, patientGender,  patientPhoneNumber, patientFamilyNumber, patientEnteringDateRoom, patientLeavingDateRoom, rdate, userssn, roomNumber))
                db.mydb.commit()
                flash('Patient creation initiated successfully', category='info')
                return redirect(url_for('staffPage'))

            else:
                flash('Patient with this SSN ID already exists', category='info')
                return redirect(url_for('create_patient'))
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))

    return render_template('/public/templates/create_patient.html')


@app.route('/newMedicine', methods=["GET", "POST"])
def newMedicine():
    if 'SSN' in session:
        if request.method == 'POST':
            MedicineName = request.form['mName']
            MedicineType = request.form['mType']
            CompanyName = request.form['mCompany']
            ExpiryDate = request.form['mDate']
            MedicinePrice = request.form['mPrice']
            DoctorSSN = request.form['DSSN']

            query = my_cursor.execute(
                f"SELECT MedicineName FROM Medicine WHERE MedicineName = '{MedicineName}' ")
            existedName = my_cursor.fetchone()

            if existedName == None:

                user = (
                    "INSERT INTO MEDICINE (MedicineName,MedicineType,CompanyName,ExpiryDate, MedicinePrice, DoctorSSN) VALUES (%s,%s,%s,%s,%s,%s)")

                userssn = session['SSN']
                my_cursor.execute(
                    user, (MedicineName, MedicineType, CompanyName, ExpiryDate, MedicinePrice, DoctorSSN))
                db.mydb.commit()
                flash('Medicine creation initiated successfully', category='info')
                return redirect(url_for('newMedicine'))

            else:
                flash('Medicine with this name already exists', category='info')
                return redirect(url_for('newMedicine'))
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))

    return render_template('public/templates/newMedicine.html')


@app.route('/update_patient')
def update_patient():
    if 'SSN' in session:
        usern = session['SSN']
        # print(usern)
        query = my_cursor.execute(
            f"SELECT * FROM PATIENT ")
        updatep = my_cursor.fetchall()
        db.mydb.commit()
        ldate = date.today()

        if not updatep:
            flash('No patients exists in database', category='error')
            return redirect(url_for('update_patient'))
        else:
            flash('Welcome', category='info')
            return render_template('public/templates/update_patient.html', updatep=updatep, ldate=ldate)
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))


@app.route('/editpatientdetail/<id>', methods=['GET', 'POST'])
def editpatientdetail(id):
    print("id is : ", id)
    if 'SSN' in session:
        # print("inside edit")

        query = my_cursor.execute(
            f"SELECT * FROM PATIENT WHERE PatientSSN = '{id}'")
        editpat = my_cursor.fetchall()
        # print(editpat)

        if request.method == 'POST':
            print("inside editpat post mtd")
            pfname = request.form['npfname']
            plname = request.form['nplname']
            age = request.form['nage']
            address = request.form['naddress']
            room = request.form['nroomNb']
            pPhoneNumber = request.form['nppn']
            fPhoneNumber = request.form['nfpn']

            user = (
                f"UPDATE PATIENT SET PatientFirstName = %s, PatientLastName = %s, PatientAge = %s, PatientAddress= %s, PatientPhoneNumber =%s, PatientFamilyNumber=%s, RoomNb=%s WHERE PatientSSN = '{id}'")

            my_cursor.execute(
                user, (pfname, plname, age, address, pPhoneNumber, fPhoneNumber, room))
            db.mydb.commit()

            if user == None:
                flash('Something Went Wrong')
                return redirect(url_for('update_patient'))
            else:
                flash('Patient update initiated successfully')
                return redirect(url_for('update_patient'))
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))

    return render_template('public/templates/editpatientdetail.html', editpat=editpat)


@app.route('/deletepatientdetail', methods=['GET', 'POST'])
def deletepatientdetail():

    if 'SSN' in session:
        if request.method == 'POST':
            deleteid = request.form['delete']
            # print("inside del")
            query = my_cursor.execute(
                f"DELETE FROM PATIENT WHERE PatientSSN='{deleteid}'")
            updatep = my_cursor.execute(query)
            db.mydb.commit()

            if updatep:
                flash('Something Went Wrong')
                return redirect(url_for('update_patient'))
            else:
                flash('Patient deletion initiated successfully')
                return redirect(url_for('update_patient'))

    return render_template('update_patient.html', updatep=updatep)


@app.route('/update_medicine')
def update_medicine():
    if 'SSN' in session:
        usern = session['SSN']
        # print(usern)
        query = my_cursor.execute(
            f"SELECT * FROM MEDICINE ")
        updateM = my_cursor.fetchall()
        db.mydb.commit()
        ldate = date.today()

        if not updateM:
            flash('No Medicine exists in database', category='error')
            return redirect(url_for('update_medicine'))
        else:
            flash('Welcome', category='info')
            return render_template('public/templates/update_medicine.html', updateM=updateM, ldate=ldate)
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))


@app.route('/editMedicinedetail/<name>', methods=['GET', 'POST'])
def editMedicinedetail(name):
    print("name is : ", name)
    if 'SSN' in session:
        # print("inside edit")

        query = my_cursor.execute(
            f"SELECT * FROM MEDICINE WHERE MedicineName = '{name}'")
        editMed = my_cursor.fetchall()
        # print(editMed)

        if request.method == 'POST':
            print("inside editMed post mtd")
            nMtype = request.form['nMtype']
            nCompanyName = request.form['nCompanyName']
            nExpiryDate = request.form['nExpiryDate']
            nMedicinePrice = request.form['nMedicinePrice']

            user = (
                f"UPDATE MEDICINE SET MedicineType = %s, CompanyName = %s, ExpiryDate= %s, MedicinePrice =%s  WHERE MedicineName = '{name}'")

            my_cursor.execute(
                user, (nMtype, nCompanyName, nExpiryDate, nMedicinePrice))
            db.mydb.commit()

            if user == None:
                flash('Something Went Wrong')
                return redirect(url_for('update_medicine'))
            else:
                flash('Medicine update initiated successfully')
                return redirect(url_for('update_medicine'))
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))

    return render_template('public/templates/editMedicinedetail.html', editMed=editMed)


@app.route('/deleteMedicinedetail', methods=['GET', 'POST'])
def deleteMedicinedetail():

    if 'SSN' in session:
        if request.method == 'POST':
            deleteName = request.form['delete']
        # print("inside del")
            query = my_cursor.execute(
                f"DELETE FROM MEDICINE WHERE MedicineName='{deleteName}'")
            updateM = my_cursor.execute(query)
            db.mydb.commit()

            if updateM:
                flash('Something Went Wrong')
                return redirect(url_for('update_medicine'))
            else:
                flash('Medicine deletion initiated successfully')
                return redirect(url_for('update_medicine'))

    return render_template('public/templates/update_medicine.html', updateM=updateM)


@app.route('/searchPatient', methods=['GET', 'POST'])
def searchPatient():
    if 'SSN' in session:
        if request.method == 'POST':
            pSSN = request.form['pSSN']

            if pSSN != "":
                query = my_cursor.execute(
                    f"SELECT * FROM PATIENT WHERE PatientSSN = '{pSSN}'")
                searchpat = my_cursor.fetchall()

                if searchpat == []:
                    flash('No Patients with  this ID exists')
                    return redirect(url_for('searchPatient'))
                else:
                    flash('Patient Found')
                    return render_template('public/templates/searchPatient.html', searchpat=searchpat)

            if pSSN == "":
                flash('Enter SSN to search')
                return redirect(url_for('searchPatient'))

    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))

    return render_template('public/templates/searchPatient.html')


@app.route('/searchMedicine', methods=['GET', 'POST'])
def searchMedicine():
    if 'SSN' in session:
        if request.method == 'POST':
            mName = request.form['mName']

            if mName != "":
                query = my_cursor.execute(
                    f"SELECT * FROM MEDICINE WHERE MedicineName = '{mName}'")
                searchMed = my_cursor.fetchall()

                if searchMed == []:
                    flash('No Medicine with this Name exists')
                    return redirect(url_for('searchMedicine'))
                else:
                    flash('Medicine Found')
                    return render_template('public/templates/searchMedicine.html', searchMed=searchMed)

            if mName == "":
                flash('Enter Name to search')
                return redirect(url_for('searchMedicine'))

    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))

    return render_template('public/templates/searchMedicine.html')


@app.route('/showAllDoctors')
def showAllDoctors():
    if 'SSN' in session:
        usern = session['SSN']
        # print(usern)
        query = my_cursor.execute(
            f"SELECT * FROM DOCTOR ")
        showD = my_cursor.fetchall()

        if not showD:
            flash('No Doctors exists in database', category='error')
            return redirect(url_for('staffPage'))
        else:
            flash('Welcome', category='info')
            return render_template('public/templates/showAllDoctors.html', showD=showD)
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))


@app.route('/showAllNurses')
def showAllNurses():
    if 'SSN' in session:
        usern = session['SSN']
        # print(usern)
        query = my_cursor.execute(
            f"SELECT * FROM NURSE ")
        showN = my_cursor.fetchall()

        if not showN:
            flash('No Nurses exists in database', category='error')
            return redirect(url_for('staffPage'))
        else:
            flash('Welcome', category='info')
            return render_template('public/templates/showAllNurses.html', showN=showN)
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))


@app.route('/showAllRooms')
def showAllRooms():
    if 'SSN' in session:
        usern = session['SSN']
        # print(usern)
        query = my_cursor.execute(
            f"SELECT * FROM ROOM ")
        showR = my_cursor.fetchall()

        if not showR:
            print('ok')
            flash('No Rooms exists in database', category='error')
            return redirect(url_for('staffPage'))
        else:
            flash('Welcome', category='info')
            return render_template('public/templates/showAllRooms.html', showR=showR)
    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('SSN', None)
    flash('logged out successfully .')
    return redirect(url_for('home'))


@app.route('/booking', methods=["GET", "POST"])
def booking():
    if 'SSN' in session:
        if request.method == 'POST':
            AppointmentDate = request.form['AppDate']
            AppointmentTime = request.form['AppTime']
            PatientSSN = request.form['patSSN']
            DoctorSSN = request.form['DSSN']

            user = (
                "INSERT INTO APPOINTMENT (PatientSSN,DoctorSSN,AppointmentTime,AppointmentDate) VALUES (%s,%s,%s,%s)")

            serssn = session['SSN']
            my_cursor.execute(
                user, (PatientSSN, DoctorSSN, AppointmentTime, AppointmentDate))
            db.mydb.commit()
            flash('Appointment creation initiated successfully', category='info')
            return redirect(url_for('staffPage'))

    else:
        flash('You are logged out. Please login again to continue')
        return redirect(url_for('login'))

    return render_template('public/templates/booking.html')


@app.route('/inv')
def inv():
    return render_template('public/templates/billing.html')
