from flask_app import app
from flask import render_template, redirect, request, session



#Display Route for Common Login / Sign up Page
@app.route('/')
def index():
    # Checking if the user IS in session (logged-in)
    if 'uuid' in session:
        return redirect('/dashboard') # If true then take the user to common landing page
    return render_template('register.html') # if not show login / sign up page


#Dashboard for option to select task as the user a common use
@app.route('/dashboard')
def dashboard():
    # Checking if the user is NOT in session (logged-in)
    if 'uuid' not in session:
        return redirect('/') # if not then have sent them to login / signup page
    return render_template('dashboard.html')