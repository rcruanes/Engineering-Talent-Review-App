from flask_app import app
from flask import render_template, redirect, request, session

# import the class files from models folder
from flask_app.models import  model_individual_contribution_form, model_nominee, model_recommender, model_user

############################################# RESTFUL ROUTE ARCHITECTURE #############################################
                                ################# table_name/id(if possible)/action #################
                                            #user/new -> DISPLAY ROUTE - Registration
                                            #user/create -> ACTION ROUTE - Creating a user
                                            #user/<int:id> -> DISPLAY   ROUTE  
                                            #user/<int:id>/edit -> DISPLAY ROUTE  
                                            #user/<int:id>/update -> ACTION ROUTE  
                                            #user/<int:id>/delete -> ACTION ROUTE  



############################################# CREATE | SAVE | INSERT ROUTES #############################################
#Display New Recommendation Form Route
@app.route('/recommend/new')
@model_user.User.restrict_access_based_on_role('Recommender') # Only the Recommender can access this route
def recommend_new():

    # STILL NEED TO CALL VALIDATIONS FROM MODEL #############
    
    # Trying to live display the selected Nominee info
    nominee = model_nominee.Nominee.get_one_nominee({'id': id})
    recommender_id = model_recommender.Recommender.get_one_recommender({'id': id})
    #Context is a dictionary of data from database  to access / display to html
    context = {
        'all_nominees' : model_nominee.Nominee.get_all_nominees(),  # Display list of nominees to select from 
        'nominee' : nominee,
        'recommender_id' : recommender_id,
    }
    return render_template('recommendation_new.html', **context)



#CREATE New Recommendation Action Route
@app.route('/recommendation/create', methods=['POST'])
@model_user.User.restrict_access_based_on_role('Recommender') # Only the Recommender can access this route
def recommend_create():
    # Using try and except blocks to handle errors: 
        # accessing form data(request.form), session['uuid'] , form fields ('a', 'b',...),and calling methods
    try:

            # STILL NEED TO CALL VALIDATIONS FROM MODEL #############

        # Getting the selected contribution(s) from submitted for work_contributions by Recommender 
        work_contributions = request.form.getlist('work_contributions[]')
        data = {
            **request.form,
            'user_id' : session['uuid'],
            'work_contributions' : work_contributions,
        }
        
        #Creating data for recommenders table and retrieve the foreign key (recommender_id) for Individuals_questions table
        recommender_id = model_recommender.Recommender.create_recommendation(data)
        
        # Check if recommender_id exists
        if recommender_id:
            # Retreiving the input from submitted form 
            individual_questions_data = {
                'recommender_id': recommender_id,
                'ic_q1': request.form['ic_q1'],
                'ic_q2': request.form['ic_q2'],
                'ic_q3': request.form['ic_q3'],
                'ic_q4': request.form['ic_q4'],
                'ic_q5': request.form['ic_q5'],
            }
            #Save the attributes to the individuals_questions table
            model_individual_contribution_form.IndividualContributionForm.create_individual_contribution(individual_questions_data)
            return redirect('/recommender/dashboard')
        else:
            return redirect('/recommend/new')

#  Exception block if error is encountered to print message to console
    except Exception as e:
        # Print or log the exception for debugging
        print("An error occurred:", str(e))
        return redirect('/recommend/new')  # Redirect to the new recommendation form with an error message





############################################# READ | SELECT DISPLAY ROUTE #############################################

#Display Recommender Dashboard Route
@app.route('/recommender/dashboard')
# Using Decorator to Call Validation from model_user to check the User Role 
@model_user.User.restrict_access_based_on_role('Recommender') # Only the Recommender can access this route
def recommender_dashboard():
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


