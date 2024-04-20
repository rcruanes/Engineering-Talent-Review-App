from flask_app import app
from flask import render_template, redirect, request, session

# import the class files from models folder
from flask_app.models import  model_individual_contribution_form, model_nominee, model_recommender, model_user


############################################# READ | SELECT DISPLAY ROUTE #############################################

#Display Recommender Dashboard Route
@app.route('/review/dashboard')
# Using Decorator to Call Validation from model_user to check the User Role 
@model_user.User.restrict_access_based_on_role('ReviewCommittee') # Only the Recommender can access this route
def review_committee_dashboard():
    # # Check to see if User in session( )
    # if 'uuid' not in session:
    #     return redirect('/') # if User not in session then logout

    #Using Context to pass data from model with neccessary queries 
    context = {
        'all_nominees_nominator' : model_nominee.Nominee.get_all_nominees_nominator(), # make sure querry in model class is correct
        'all_nominees' : model_nominee.Nominee.get_all_nominees(),
        'all_users' : model_user.User.get_all(),
    }

    return render_template('recommender_dashboard.html', **context)
