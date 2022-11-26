# file for views

#importing our package (treating this directory as a package)
from app import app
from flask import Flask, render_template, request, redirect

@app.route('/')
def home():
    return render_template('public/templates/home.html') 

@app.route('/login')
def login():
    return render_template('/public/templates/login.html') 

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":

       req = request.form

       username = req["name"]
       email = req["email"]
       password = req["password"]
       print(username,email,password)
       return redirect(request.url)

    return render_template('/public/templates/signup.html')     

@app.route('/booking', methods=["GET", "POST"])
def booking():
    return render_template('/public/templates/booking.html') 

@app.route('/booking-room')
def booking_room():
    return render_template('/public/templates/booking_room.html')     