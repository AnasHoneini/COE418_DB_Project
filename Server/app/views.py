# file for views

#importing our package (treating this directory as a package)
from app import app
from flask import Flask, render_template

@app.route('/')
def home():
    return render_template('public/templates/home.html') 

@app.route('/login')
def login():
    return render_template('/public/templates/login.html') 

@app.route('/signup')
def signup():
    return render_template('/public/templates/signup.html')     

@app.route('/booking')
def booking():
    return render_template('/public/templates/booking.html') 

@app.route('/booking-room')
def booking_room():
    return render_template('/public/templates/booking_room.html')     