from flask_app import app
from flask import flash
from flask import render_template, redirect, request, session

# import the class files from models folder
from flask_app.models import   model_nominee, model_recommender, model_user, model_individual_contribution_form, model_project_manager_contribution_form, model_people_manager_contribution_form

############################################# RESTFUL ROUTE ARCHITECTURE #############################################
                                ################# table_name/id(if possible)/action #################
                                            #user/new -> DISPLAY ROUTE - Registration
                                            #user/create -> ACTION ROUTE - Creating a user
                                            #user/<int:id> -> DISPLAY   ROUTE  
                                            #user/<int:id>/edit -> DISPLAY ROUTE  
                                            #user/<int:id>/update -> ACTION ROUTE  
                                            #user/<int:id>/delete -> ACTION ROUTE  



############################################# CREATE | SAVE | INSERT ROUTES #############################################
############################################# CREATE | SAVE | INSERT ROUTES #############################################
#Display New Recommendation Form Route
@app.route('/recommend/new')
@model_user.User.restrict_access_based_on_role('Recommender') # Only the Recommender can access this route
def recommend_new():

    # STILL NEED TO CALL VALIDATIONS FROM MODEL #############
    
    # Trying to live display the selected Nominee info
    nominee = model_nominee.Nominee.get_one_nominee({'id': id})

    #Context is a dictionary of data from database  to access / display to html
    context = {
        'all_nominees' : model_nominee.Nominee.get_all_nominees(),  # Display list of nominees to select from 
        'nominee' : nominee,
    }
    return render_template('recommendation_new.html', **context)



#CREATE New Recommendation Action Route
@app.route('/recommendation/create', methods=['POST'])
@model_user.User.restrict_access_based_on_role('Recommender') # Only the Recommender can access this route
def recommend_create():

    # Using try and except blocks to handle errors: 
        # accessing form data(request.form), session['uuid'] , form fields ('a', 'b',...),and calling methods
    try:
        print("Form Data Received", request.form)
        print("Session UUID:", session['uuid'])

        # STILL NEED TO CALL VALIDATIONS FROM MODEL FOR FORM #############

        # Getting the selected contribution(s) from submitted for work_contributions by Recommender 
        work_contributions = request.form.getlist('work_contributions[]')
        data = {
            **request.form,
            'user_id' : session['uuid'],
            'work_contributions' : work_contributions,
        }
        print("Data to be inserted:", data)
        
        #Creating data for recommenders table and retrieve the foreign key (recommender_id) for Individuals_questions table
        recommender_id = model_recommender.Recommender.create_recommendation(data)
        print("This is recommender_id:", recommender_id)

        # Check if recommender_id exists
        if recommender_id:
            # INDIVIDUAL CONTRIBURION: Retreiving the input from submitted form 
            individual_questions_data = {
                'recommender_id': recommender_id,
                'ic_q1': request.form['ic_q1'],
                'ic_q2': request.form['ic_q2'],
                'ic_q3': request.form['ic_q3'],
                'ic_q4': request.form['ic_q4'],
                'ic_q5': request.form['ic_q5'],
            }
            #Save the attributes to the individuals_contributions_forms table
            model_individual_contribution_form.IndividualContributionForm.create_individual_contribution(individual_questions_data)

            # PROJECT MANAGER: Retreive the data from form
            project_manager_questions_data = {
                'recommender_id': recommender_id,
                'prjmc_q1': request.form['prjmc_q1'],
                'prjmc_q2': request.form['prjmc_q2'],
                'prjmc_q3': request.form['prjmc_q3'],
                'prjmc_q4': request.form['prjmc_q4'],
                'prjmc_q5': request.form['prjmc_q5'],
            }

            #Save the attributes to the projects_managers_contributions_forms table
            model_project_manager_contribution_form.ProjectManagerContributionForm.create_project_manager_contribution(project_manager_questions_data)

            # PEOPLE MANAGER: Retreive the data from form
            people_manager_questions_data = {
                'recommender_id': recommender_id,
                'pplmc_q1': request.form['pplmc_q1'],
                'pplmc_q2': request.form['pplmc_q2'],
                'pplmc_q3': request.form['pplmc_q3'],
                'pplmc_q4': request.form['pplmc_q4'],
                'pplmc_q5': request.form['pplmc_q5'],
            }
            # Save the attributes to the  peoples_managers_contributions_forms table
            model_people_manager_contribution_form.PeopleManagerContributionForm.create_people_manager_contribution(people_manager_questions_data)

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
    # Check to see if User in session( )
    if 'uuid' not in session:
        return redirect('/') # if User not in session then logout
    
    # This is the USER ID NOT THE RECOMMENDER_ID!!
    user_id = session['uuid']  # Fetch USER ID from session
    user = model_user.User.get_one({'id': user_id})
    
    #Using Context to pass data from model with neccessary queries 
    context = {
            'all_users' : model_user.User.get_all(), #displaying name of User in Session
            'user' : user, #displaying the recommenders_name
            'all_nominees_nominator' : model_nominee.Nominee.get_all_nominees_nominator(), #displaying the Nominator info associated with Nominees make sure query in model class is correct
            'all_nominees_recommender': model_recommender.Recommender.get_all_nominees_recommender(), # displaying the recommender info associated with Nominees 
        }
    print("This is the User Id in Session:", user_id )

    return render_template('recommender_dashboard.html', **context)



#Display Recommendation Info of Associated Nominee by Recommender ID Route
@app.route('/recommender/<int:id>/recommendation/info')
@model_user.User.restrict_access_based_on_role('Recommender') # Only the Recommender can access this route
def nominee_show_recommendation_info(id):
    # Check if User id is loggen-in
    if 'uuid' not in session:
        return redirect('/') # redirect to Home page
    
    recommender = model_recommender.Recommender.get_one_recommender({'id':id})

        # Using session to check if logged-in user is the Recommender(creator) of this Nominee Form 
    if not recommender or 'uuid' not in session or session['uuid'] != recommender.user_id:
        flash('You do not have permission to View this recommendation.', 'error')
        return redirect('/dashboard')  # Redirect with an error message

    # Fetching nominee_id from recommender using the get_one method
    nominee = model_nominee.Nominee.get_one_nominee({'id': recommender.nominee_id})
    print('Nominee Id:', nominee.id)
    if not nominee:
        flash('Nominee details not found.', 'error')
        return redirect('/dashboard')  # Redirect if nominee details is in valid
    # Spliting work_contributions into a set
    current_contributions = set(recommender.work_contributions.split(','))
    # fetching the  workcontribution answers information by the get_one_by method using the recommender_id to pass in context
    ind_contribution = model_individual_contribution_form.IndividualContributionForm.get_one_by_recommender_id({'recommender_id': recommender.id})
    prj_contribution = model_project_manager_contribution_form.ProjectManagerContributionForm.get_one_by_recommender_id({'recommender_id': recommender.id})
    ppl_contribution = model_people_manager_contribution_form.PeopleManagerContributionForm.get_one_by_recommender_id({'recommender_id': recommender.id})


    #Passing in the fected data to display in form if value exist and other reasons
    context = {
        'user': model_user.User.get_one({'id':id}),
        'all_users': model_user.User.get_all(),
        'nominee': nominee,
        'recommender': recommender,
        'current_contributions': current_contributions,
        'ind_contribution': ind_contribution,
        'prj_contribution': prj_contribution,
        'ppl_contribution': ppl_contribution,
    }

    return render_template('show_one_recommendation_info.html', **context)


############################################# UPDATE | EDIT ROUTES #############################################
############################################# UPDATE | EDIT ROUTES #############################################
# Display Route Edit Recommendation Form for Nominee by Recommender
@app.route('/recommender/<int:id>/edit/nominee')
# Only the Recommender can access this route
@model_user.User.restrict_access_based_on_role('Recommender')
def edit_nominee_recommendation(id): #id being passed in is from the the html  edit link button
    # Debugging: making sure the correct id is passed in, not the Nominee but the Recommender 
    print("Passed ID for editing:", id)

    #Checking to see if User is loggin-in
    if 'uuid' not in session:
        flash('You must be logged in to edit recommendations.', 'error')
        return redirect('/')  

    #Getting the recommender.id by calling the get_one method 
    recommender = model_recommender.Recommender.get_one_recommender({'id': id})
    print('Recommender Id', recommender.id if recommender else None) # Debugging to ensure if id matches passed in id for editing
    
    #Debugging: Ensure the recommender exists and the logged-in user matches the recommender's user_id
    print('Recommender User Id:', recommender.user_id if recommender else None)

    # Using session to check if logged-in user is the Recommender(creator) of this Nominee Form 
    if not recommender or 'uuid' not in session or session['uuid'] != recommender.user_id:
        flash('You do not have permission to edit this recommendation.', 'error')
        return redirect('/dashboard')  # Redirect with an error message

    # Fetching nominee_id from recommender using the get_one method
    nominee = model_nominee.Nominee.get_one_nominee({'id': recommender.nominee_id})
    print('Nominee Id:', nominee.id)
    if not nominee:
        flash('Nominee details not found.', 'error')
        return redirect('/dashboard')  # Redirect if nominee details is in valid

    # Fethcing the current work_contributions which is stored as a comma-separated string in the database
    current_contributions = set(recommender.work_contributions.split(',')) if recommender.work_contributions else set()

    # fetching the  workcontribution answers information by the get_one_by method using the recommender_id to pass in context
    ind_contribution = model_individual_contribution_form.IndividualContributionForm.get_one_by_recommender_id({'recommender_id': recommender.id})
    prj_contribution = model_project_manager_contribution_form.ProjectManagerContributionForm.get_one_by_recommender_id({'recommender_id': recommender.id})
    ppl_contribution = model_people_manager_contribution_form.PeopleManagerContributionForm.get_one_by_recommender_id({'recommender_id': recommender.id})
    #Debugging to see if the correct answeres are fetched
    # print('Individual Contributions Questions:',ind_contribution.id if ind_contribution else None)
    # print('Individual Contributions Questions:',ind_contribution.ic_q1 if ind_contribution else None)

    #Passing in the fected data to display in form if value exist and other reasons
    context = {
        'nominee': nominee,
        'recommender': recommender,
        'all_nominees' : model_nominee.Nominee.get_all_nominees(),
        'current_contributions': current_contributions,
        'ind_contribution': ind_contribution,
        'prj_contribution': prj_contribution,
        'ppl_contribution': ppl_contribution,
    }

    return render_template('recommender_edit_nominee_info.html', **context)




#Update Recommendation form Action Route (Update Returns Nothing)
@app.route('/recommender/<int:id>/update/nominee', methods=['POST'])
@model_user.User.restrict_access_based_on_role('Recommender')  # Only the Recommender can access this route
def update_nominee_recomendation(id):
    try:
        print("Form Data Received", request.form )

        recommender = model_recommender.Recommender.get_one_recommender({'id': id})
        if not recommender or session.get('uuid') != recommender.user_id:
            flash("You do not have permission to update this recommendation.", "error")
            return redirect('/recommender/dashboard')

        # Prepare the data dictionary for updating
        work_contributions = ','.join(request.form.getlist('work_contributions[]'))  # Combining all checked contributions into a single string
        data = {
            'id': id,
            'work_contributions': work_contributions  # This will update the SET type correctly in MySQL
        }

        #Save / Update the Info from form
        model_recommender.Recommender.update_one_recomendation(data)

        print('Recommender Id:', recommender.id)
        # Check if recommender_id exists
        if recommender:
            # INDIVIDUAL CONTRIBURION: Retreiving the input from submitted form 
            individual_questions_data = {
                **request.form,
                'id':id
            }
            #Save the attributes to the individuals_contributions_forms table
            model_individual_contribution_form.IndividualContributionForm.update_one_individual_contribution_form(individual_questions_data)
            
            # PROJECT MANAGER: Retreive the data from form
            project_manager_questions_data = {
                **request.form,
                'id':id
            }
            #Save the attributes to the projects_managers_contributions_forms table
            model_project_manager_contribution_form.ProjectManagerContributionForm.update_one_project_manager_contribution_form(project_manager_questions_data)
            
            # PEOPLE MANAGER: Retreive the data from form
            people_manager_questions_data = {
                **request.form,
                'id':id
            }
            # Save the attributes to the  peoples_managers_contributions_forms table
            model_people_manager_contribution_form.PeopleManagerContributionForm.update_one_people_manager_contribution_form(people_manager_questions_data)
            return redirect('/recommender/dashboard')
        else:
            return redirect('/recommend/new')

#  Exception block if error is encountered to print message to console
    except Exception as e:
        # Print or log the exception for debugging
        print("An error occurred:", str(e))
        return redirect('/recommend/new')  # Redirect to the new recommendation form with an error message





############################################# DELETE ROUTES #############################################
############################################# DELETE ROUTES #############################################

# # DELETE Action Nominee Recommendation by ID Route
@app.route('/recommender/<int:id>/delete/')
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Recommender') # Only the Nominator can access this route
def recommender_delete(id):
    #Using the Nominee ID to Limit Access for Deleting Nominee Form
    recommender = model_recommender.Recommender.get_one_recommender({'id':id}) # Getting the Nominee Id from Database
    # Check if a nominee object is retrieved
    if recommender:
        # Using session to check if logged-in user is the Nominator(creator) of this Nominee
        if 'uuid' in session and session['uuid'] == recommender.user_id:
            model_recommender.Recommender.delete_one_recomendation({'id':id})
            return redirect('/recommender/dashboard') #Redirect after successful delete
    # Redirect to dashboard 
    return redirect('/dashboard')


# DELETE Action Nominee by nominee ID Route
@app.route('/recommender/<int:id>/delete/nominee')
@model_user.User.restrict_access_based_on_role('Recommender')  # Only the Recommender can access this route
def recommendation_delete(id):
    # Validations to see if the id passed in is the same as the nominee and User in Session
    recommender = model_recommender.Recommender.get_one_recommender({'id':id}) # Getting the Nominee Id from Database
    if not recommender or 'uuid' not in session or session['uuid'] != recommender.user_id:
        flash('You do not have permission to delete this nominee.', 'error')
        return redirect('/dashboard')

    # Try Deleting dependent records first foreign key(fk) with nominee_id
    try:

        # check and delete nominee_id for education histories
        ind_contribution_exist = model_individual_contribution_form.IndividualContributionForm.check_exists_by_recommender_id({'recommender_id': id})
        if ind_contribution_exist:
            model_individual_contribution_form.IndividualContributionForm.delete_by_recommender_id({'recommender_id': id})

        # check and delete nominee_id for professional histories
        prj_contribution_exist = model_project_manager_contribution_form.ProjectManagerContributionForm.check_exists_by_recommender_id({'recommender_id': id})
        if prj_contribution_exist:
            model_project_manager_contribution_form.ProjectManagerContributionForm.delete_by_recommender_id({'recommender_id': id})

        # check and delete nominee_id for professional histories
        ppl_contribution_exist = model_people_manager_contribution_form.PeopleManagerContributionForm.check_exists_by_recommender_id({'recommender_id': id})
        if ppl_contribution_exist:
            model_people_manager_contribution_form.PeopleManagerContributionForm.delete_by_recommender_id({'recommender_id': id})

        # After all related records are checked and deleted, deleting the nominee
        model_recommender.Recommender.delete_one_recomendation({'id': id})
        flash('Nominee successfully deleted.', 'success')

    except Exception as e:
        flash(f"Failed to delete nominee due to: {str(e)}", 'error')

    return redirect('/recommender/dashboard')







#Update Nominee Basic info form Action Route (Update Returns Nothing)

# @app.route('/recommender/<int:id>/update/nominee', methods=['POST'])
# # Call Validation to check the User Role from the decorator from User
# @model_user.User.restrict_access_based_on_role('Recommender') # Only the Recommender can access this route
# def update_nominee_recomendation(id): # Passing an argument id from action post request

#     # Using the Recommender ID to Limit Access for Updating Recommendation Form
#     recommender = model_recommender.Recommender.get_one_recommender({'id': id}) # Getting the Nominee Id from Database 
#     # the get method returns a boolean
#     if recommender: #if there's an object returned (so the website doesn't crash)
#         # Using session to check if logged-in user is the Recommender(creator) of this form associated with Nominee
#         if 'uuid' in session and session['uuid'] == recommender.user_id:
#             #Validations for Form
#             # if not model_nominee.Nominee.validator_nominee_info(request.form):
#             #     return redirect(f'/nominee/{id}/edit') # MAKE SURE F STRING is Used to pass in ID
#             #Preventing info / data being leaked 
#             #Since Update_one() targerts an Id from the Update query which is not in the id from the form (html) but has potential to alter other nominee's info
#             #Using data dictionary and passing in everything from this extracted request form(**reques.form) 
#             #Then passing in id from the form 
#             data = {
#                 **request.form,
#                 'id':id
#             }
#             #Save / Update the Info 
#             model_recommender.Recommender.update_one_recomendation(data)
#             return redirect('/recommender/dashboard')
    
#     return redirect('/dashboard')


