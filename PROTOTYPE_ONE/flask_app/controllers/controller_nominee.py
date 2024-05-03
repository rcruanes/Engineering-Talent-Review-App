
from flask_app import app
from flask import render_template, redirect, request, session, flash

# import the class from model_user.py
from flask_app.models import model_nominee, model_activity_qualification_form, model_award_qualification_form, model_nominee_education_history_form, model_nominee_professional_history_form, model_user, model_recommender

############################################# RESTFUL ROUTE ARCHITECTURE #############################################
                                ################# table_name/id(if possible)/action #################
                                            #user/new -> DISPLAY ROUTE - Registration
                                            #user/create -> ACTION ROUTE - Creating a user
                                            #user/<int:id> -> DISPLAY   ROUTE  
                                            #user/<int:id>/edit -> DISPLAY ROUTE  
                                            #user/<int:id>/update -> ACTION ROUTE  
                                            #user/<int:id>/delete -> ACTION ROUTE  



############################################# CREATE | SAVE ROUTES #############################################
############################################# CREATE | SAVE ROUTES #############################################
#CREATE New Nominee Action Route for New Nominee Form
@app.route('/nominee/create', methods=['POST'])
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def nominee_create():
#VALIDATIONS:
    #Nominee basic Info Validations
    if not model_nominee.Nominee.validator_nominee_info(request.form):
        # print(model_nominee.Nominee.validator(request.form))
        return redirect('/nominee/new') # This will redirect to the same form page if validations failed
    
    #Nominee Activity Qualifications Validations
    if not model_activity_qualification_form.ActivityQualificationForm.validator_activity_qualification(request.form):
        return redirect('/nominee/new')
    
    #Nominee Award Qualifications Validations
    if not model_award_qualification_form.AwardQualificationForm.validator_award_qualification(request.form):
        return redirect('/nominee/new')
    
    #Nominee Education Qualifications Validations
    if not model_nominee_education_history_form.NomineeEducationHistory.validator_edu_history(request.form):
        return redirect('/nominee/new')

    #Nominee Professional Qualifications Validations
    if not model_nominee_professional_history_form.NomineeProfessionalHistory.validator_prf_history(request.form):
        return redirect('/nominee/new')


#Create Nominee
    #Creating data dictionary to pass user id using session along with request.form
    #this is better than using session through hidden inputs in html to avoid end user to edit the form
    data = {
        **request.form,
        'user_id': session['uuid']
    }

    # Storing the object in database from the data dictionary
    # Setting the nominee_id to the passed in data to use for the nominee_id attribute for other Tables associated with the nominee ID
    nominee_id = model_nominee.Nominee.create(data) 
    print("This is nominee_id", nominee_id)

    if nominee_id:

        # ACTIVITY QUALIFICATION DATA: Retreiving the input from submitted form 
        activity_data = {
            'nominee_id': nominee_id,
            'nominator_activity_name': request.form.get('nominator_activity_name'),
            'nominator_activity_year': request.form.get('nominator_activity_year'),
            'nominator_activity_description': request.form.get('nominator_activity_description'),
            'nominee_qualification': request.form.get('nominee_qualification'),
            'nominee_activity_name': request.form.get('nominee_activity_name'),
            'nominee_activity_year': request.form.get('nominee_activity_year'),
            'nominee_activity_description': request.form.get('nominee_activity_description')
        }
        #Save the result to the activities_qualifications_forms table
        model_activity_qualification_form.ActivityQualificationForm.create_activity(activity_data) #Passing in data argument from method call


        # AWARD QUALIFICATION DATA: Retrieving the input from submitted form
        award_data = {
            'nominee_id': nominee_id,
            'nominator_award_name': request.form.get('nominator_award_name'),
            'nominator_award_year': request.form.get('nominator_award_year'),
            'nominator_award_description': request.form.get('nominator_award_description'),
            'nominee_award_name': request.form.get('nominee_award_name'),
            'nominee_award_year': request.form.get('nominee_award_year'),
            'nominee_award_description': request.form.get('nominee_award_description')
        }
        model_award_qualification_form.AwardQualificationForm.create_award(award_data)


        # NOMINEE EDUCATION HISTORY DATA: Retreiving the input from submitted form 
        nominee_education_data = {
            'nominee_id': nominee_id,
            'college_name': request.form['college_name'],
            'location': request.form['location'],
            'degree': request.form['degree'],
            'program': request.form['program'],
            'graduation_year': request.form['graduation_year'],
        }
        #Save the result to the nominees_educations_histories table
        model_nominee_education_history_form.NomineeEducationHistory.create_nominee_education_history(nominee_education_data)


        # NOMINEE PROFESSIONAL HISTORY DATA: Retreiving the input from submitted form 
        nominee_professional_data = {
            'nominee_id': nominee_id,
            'employer': request.form['employer'],
            'title': request.form['title'],
            'start_year': request.form['start_year'],
            'end_year': request.form['end_year'],
            'principal_job_function': request.form['principal_job_function'],
            'principal_responsibility': request.form['principal_responsibility'],
        }
        #Save the result to the nominees_professionals_histories table
        model_nominee_professional_history_form.NomineeProfessionalHistory.create_nominee_professional_history(nominee_professional_data)

        # Once form was submitted successfully redirect to the list of Users nominations
        return redirect('/nominee/dashboard')
    # If the Nominee doesn't exist
    return redirect('/dashboard') 





############################################# READ | DISPLAY ROUTE #############################################
############################################# READ | DISPLAY ROUTE #############################################
#Display Route Once Clicked on New Nominee from Common Dashboard
@app.route('/nominee/dashboard')
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def nominee_dashboard():
    # Allows for html to use the items in the context to display in front end
    #Could add more since it's a list of dictinaries
    #Make sure to inject in html using the new created attribute(s) from get methods 
    context = {
        'all_nominees_nominator': model_nominee.Nominee.get_all_nominees_nominator(), # make sure query in model class is correct
        'all_nominees': model_nominee.Nominee.get_all_nominees(),
        'all_users': model_user.User.get_all(),
    }
    return render_template('nominee_dashboard.html', **context)



#Display Route Form to Create New Nominee 
@app.route('/nominee/new')
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def nominee_new():
    # call the get.all() classmethod to get all users
    #users = User.get_all()   # could also call the gell_all() this way 
    #print(users) #  print all users to terminal
    return render_template('nominee_new.html') # easier to call it like this




#Display Show Info of Selected Nominee by ID Route
@app.route('/nominee/<int:id>/nomination/info')
# @model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def nominee_show_nomination_info(id):
    # Check if User id is loggen-in
    if 'uuid' not in session:
        return redirect('/') # redirect to Home page
    nominee = model_nominee.Nominee.get_one_nominee({'id': id})
    # recommender = model_recommender.Recommender.get_one_recommender({'id':id})
    # user_role = model_user.User.get_user_role_from_session()
    if nominee:
        
            # fetching the activity qualification information by the get_one method using the nominee_id to pass in context
            activity_qualification = model_activity_qualification_form.ActivityQualificationForm.get_one_by_nominee_id({'nominee_id': id})

            # fetching the award qualification information by the get_one method using the nominee_id to pass in context
            award_qualification = model_award_qualification_form.AwardQualificationForm.get_one_by_nominee_id({'nominee_id': id})

            # fetching the nominee education information by the get_one method using the nominee_id to pass in context
            edu_history = model_nominee_education_history_form.NomineeEducationHistory.get_one_by_nominee_id({'nominee_id': id})
            # print("Education History ID:", edu_history.id if edu_history else None)
            # print("Education History ID:", edu_history.college_name if edu_history else None)

            # fetching the nominee professiona information by the get_one method using the nominee_id to pass in context
            prf_history = model_nominee_professional_history_form.NomineeProfessionalHistory.get_one_by_nominee_id({'nominee_id': id})
            # print("Professional History ID:", prf_history.id if prf_history else None)
            # print("Professional History ID:", prf_history.employer if prf_history else None)

            # print(session['uuid'])
            context = {
                'all_users': model_user.User.get_all(), # Displaying current User in session,
                'nominee' : nominee,
                'activity_qualification': activity_qualification,
                'award_qualification': award_qualification,
                'edu_history': edu_history,
                'prf_history': prf_history,
                # 'all_nominees_recommender': model_recommender.Recommender.get_all_nominees_recommender(),
                # 'user' : model_user.User.get_one({'id': id}),
            }
            return render_template('show_one_nomination_info.html', **context)

    return redirect('/dashboard')




############################################# UPDATE | EDIT ROUTES #############################################
############################################# UPDATE | EDIT ROUTES #############################################

#Display Route Form to EDIT the Selected Existing Nominee
@app.route('/nominee/<int:id>/edit')
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def edit_nominee(id): #Passing ID as an argument 
    # print('Form Route ID PASSED IN:', id)
    # print('USER IN Session UUID:', session.get('uuid'))

    #Using Nominee ID to set Access limitation to editing a Nominee form 
    nominee = model_nominee.Nominee.get_one_nominee({'id': id}) # Getting the Nominee by ID
    # print('Nominee ID:', nominee.id if nominee else None)
    # print('Nominee USER ID:', nominee.user_id if nominee else None)

    # Using the object, 'uuid, and session to check if logged-in user is the Nominator(creator) of the Nominee 
    if not nominee or 'uuid' not in session or session['uuid'] != nominee.user_id:
        flash('You do not have permission to edit this nominee.', 'error')
        return redirect('/dashboard')
    
    # fetching the activity qualification information by the get_one method using the nominee_id to pass in context
    activity_qualification = model_activity_qualification_form.ActivityQualificationForm.get_one_by_nominee_id({'nominee_id': id})

    # fetching the award qualification information by the get_one method using the nominee_id to pass in context
    award_qualification = model_award_qualification_form.AwardQualificationForm.get_one_by_nominee_id({'nominee_id': id})

    # fetching the nominee education information by the get_one method using the nominee_id to pass in context
    edu_history = model_nominee_education_history_form.NomineeEducationHistory.get_one_by_nominee_id({'nominee_id': id})
    # print("Education History ID:", edu_history.id if edu_history else None)

    # fetching the nominee professiona information by the get_one method using the nominee_id to pass in context
    prf_history = model_nominee_professional_history_form.NomineeProfessionalHistory.get_one_by_nominee_id({'nominee_id': id})
    # print("Professional History ID:", prf_history.id if prf_history else None)

    # Using context to pass in any CRUD functionalites / data to html 
    context = {
        'nominee':nominee, #Using the key from fetched get_one_by_nominee_id to display existing value from input
        'activity_qualification': activity_qualification,
        'award_qualification': award_qualification,
        'edu_history': edu_history,
        'prf_history': prf_history 
        }
    return render_template('nominee_edit_nominee_info.html', **context)






# UPDATE Nominee info form Action Route (Update Returns Nothing)
@app.route('/nominee/<int:id>/update', methods=['POST'])
@model_user.User.restrict_access_based_on_role('Nominator')
def update_nominee(id):
    # Ensure the current user is allowed to update the nominee
    nominee = model_nominee.Nominee.get_one_nominee({'id': id})
    if not nominee or 'uuid' not in session or session['uuid'] != nominee.user_id:
        flash('You do not have permission to edit this nominee.', 'error')
        return redirect('/dashboard')

    # if not model_nominee.Nominee.validator_nominee_info(request.form):
    #     return redirect(f'/nominee/{id}/edit')
# Validate all parts before proceeding to update
    all_valid = model_nominee.Nominee.validator_nominee_info(request.form)
    all_valid &= model_activity_qualification_form.ActivityQualificationForm.validator_activity_qualification(request.form)
    all_valid &= model_award_qualification_form.AwardQualificationForm.validator_award_qualification(request.form)
    all_valid &= model_nominee_education_history_form.NomineeEducationHistory.validator_edu_history(request.form)
    all_valid &= model_nominee_professional_history_form.NomineeProfessionalHistory.validator_prf_history(request.form)

    if not all_valid:
        return redirect(f'/nominee/{id}/edit')

    # If all validations pass, update records
    model_nominee.Nominee.update_one_nominee({**request.form, 'id': id})
    model_activity_qualification_form.ActivityQualificationForm.update_activity_qualification({**request.form, 'id': id})
    model_award_qualification_form.AwardQualificationForm.update_award_qualification({**request.form, 'id': id})
    model_nominee_education_history_form.NomineeEducationHistory.update_nominee_education_history({**request.form, 'id': id})
    model_nominee_professional_history_form.NomineeProfessionalHistory.update_nominee_professional_history({**request.form, 'id': id})

    # Retrieving nominee data from submitte form and passing in id  
    nominee_data = {
        **request.form,
        'id': id
    }
    model_nominee.Nominee.update_one_nominee(nominee_data)


    # Retrieve and update activity qualification
    # Assuming there is a one-to-one relationship 
    activity_qualification = model_activity_qualification_form.ActivityQualificationForm.get_one_by_nominee_id({'nominee_id': id})
    if activity_qualification:
        print('activity_qualification nominee_id:', activity_qualification if activity_qualification else None)
        activity_qualification_data = {
            **request.form,
            'id': activity_qualification.id  # Using the ID from get_one method
        }
        model_activity_qualification_form.ActivityQualificationForm.update_activity_qualification(activity_qualification_data)


    # Retrieve and update activity qualification
    # Assuming there is a one-to-one relationship 
    award_qualification = model_award_qualification_form.AwardQualificationForm.get_one_by_nominee_id({'nominee_id': id})
    if award_qualification:
        print('award_qualification nominee_id:', award_qualification if award_qualification else None)
        award_qualification_data = {
            **request.form,
            'id': award_qualification.id  # Using the ID from get_one method
        }
        model_award_qualification_form.AwardQualificationForm.update_award_qualification(award_qualification_data)


    # Retrieve and update education history
    # Assuming there is a one-to-one relationship between nominee and education history
    edu_history = model_nominee_education_history_form.NomineeEducationHistory.get_one_by_nominee_id({'nominee_id': id})
    if edu_history:
        print('edu_histor nominee_id:', edu_history if edu_history else None)
        education_history_data = {
            **request.form,
            'id': edu_history.id  # setting the TABLE ID from the submmitted form
        }
        model_nominee_education_history_form.NomineeEducationHistory.update_nominee_education_history(education_history_data)


    # Retrieve and update professional history
    # one-to-one relationship between nominee and professional history
    prf_history = model_nominee_professional_history_form.NomineeProfessionalHistory.get_one_by_nominee_id({'nominee_id': id})
    if prf_history:
        print('edu_histor nominee_id:', prf_history if prf_history else None)
        professional_history_data = {
            **request.form,
            'id': prf_history.id,
        }
        model_nominee_professional_history_form.NomineeProfessionalHistory.update_nominee_professional_history(professional_history_data)

    flash('Nominee information updated successfully.', 'success')
    return redirect('/nominee/dashboard')






############################################# DELETE ROUTES #############################################
############################################# DELETE ROUTES #############################################
# DELETE Nominee by nominee ID Action Route
@app.route('/nominee/<int:id>/delete')
@model_user.User.restrict_access_based_on_role('Nominator')  # Only the Nominator can access this route
def nominee_delete(id):
    # Validations to see if the id passed in is the same as the nominee and User in Session


    nominee = model_nominee.Nominee.get_one_nominee({'id': id})
    if not nominee or 'uuid' not in session or session['uuid'] != nominee.user_id:
        flash('You do not have permission to delete this nominee.', 'error')
        return redirect('/dashboard')

    # Try Deleting dependent records first foreign key(fk) with nominee_id
    try:
        # check and delete nominee_id for recommenders
        recommenders_exist = model_recommender.Recommender.check_exists_by_nominee_id({'nominee_id': id})
        if recommenders_exist:
            return redirect('/nominee/dashboard')
            # model_recommender.Recommender.delete_by_nominee_id({'nominee_id': id})

        # check and delete nominee_id for activity qualification
        activity_qualification_exist = model_activity_qualification_form.ActivityQualificationForm.check_exists_by_nominee_id({'nominee_id': id})
        if activity_qualification_exist:
            model_activity_qualification_form.ActivityQualificationForm.delete_by_nominee_id({'nominee_id': id})

        # check and delete nominee_id for awards qualification
        award_qualification_exist = model_award_qualification_form.AwardQualificationForm.check_exists_by_nominee_id({'nominee_id': id})
        if award_qualification_exist:
            model_award_qualification_form.AwardQualificationForm.delete_by_nominee_id({'nominee_id': id})

        # check and delete nominee_id for education histories
        edu_histories_exist = model_nominee_education_history_form.NomineeEducationHistory.check_exists_by_nominee_id({'nominee_id': id})
        if edu_histories_exist:
            model_nominee_education_history_form.NomineeEducationHistory.delete_by_nominee_id({'nominee_id': id})

        # check and delete nominee_id for professional histories
        prf_histories_exist = model_nominee_professional_history_form.NomineeProfessionalHistory.check_exists_by_nominee_id({'nominee_id': id})
        if prf_histories_exist:
            model_nominee_professional_history_form.NomineeProfessionalHistory.delete_by_nominee_id({'nominee_id': id})

        # After all related records are checked and deleted, deleting the nominee
        model_nominee.Nominee.delete_one_nominee({'id': id})
        flash('Nominee successfully deleted.', 'success')

    except Exception as e:
        flash(f"Failed to delete nominee due to: {str(e)}", 'error')

    return redirect('/nominee/dashboard')



############################################# OTHER ROUTES FOR REFRENCE #############################################
############################################# OTHER ROUTES FOR REFRENCE #############################################

#Display Route Form to Edit Existing Nominee
# @app.route('/nominee/edit/<int:id>')
# def edit(id):
#     data = {
#         'id': id
#     }
#     return render_template('edit_user.html', user=User.get_one(data))


# EDIT Action Nominee by ID Route
# @app.route('/user/update', methods=['POST'])
# def updated():
#     User.update(request.form) # since we are using a hidden input 
#     return redirect('/users')

#Display Route to Show Info of Noiminee by ID
# @app.route('/user/show/<int:id>')
# def show(id):
#     data = {
#         'id': id
#     }
#     return render_template('show_user.html', user=User.get_one(data))

