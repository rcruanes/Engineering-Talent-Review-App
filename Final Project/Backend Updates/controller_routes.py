from flask_app import app
from flask import render_template, redirect, request, session

# This Controller file is for any common use for the users such as the landing login / register page

#Display Route for Common Login / Sign up  Landing Page
@app.route('/')
def home_page():
    # Checking if the user IS in session (logged-in)
    if 'uuid' in session:
        return redirect('/dashboard') # If true then take the user to common landing page
    return render_template('register.html') # if not show login / sign up page


