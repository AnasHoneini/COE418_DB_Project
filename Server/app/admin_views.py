# file for views

#importing our package (treating this directory as a package)
from app import app
from flask import Flask, render_template

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html') 

@app.route('/admin/profile')
def admin_profile():
      return "<h1 style = 'color: blue'> Hello world</h1>"

#@app.route('/login')
#def login():
#   return render_template('login.html') 

#@app.route('/login/signup')
#def signup():
#    return render_template('signup.html')     