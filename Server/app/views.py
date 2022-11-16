# file for views

#importing our package (treating this directory as a package)
from app import app
from flask import Flask, render_template

@app.route('/')
def hello_world():
    return render_template('public/index.html') 


@app.route('/login')
def login():
    return render_template('/public/login.html') 

@app.route('/signup')
def signup():
    return render_template('public/signup.html')     