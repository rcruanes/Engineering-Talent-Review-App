
from flask_app import app
from flask import render_template, redirect, request, session

# import the class from model_user.py
from flask_app.models import model_nominee, model_user

############################################# RESTFUL ROUTE ARCHITECTURE #############################################
                                ################# table_name/id(if possible)/action #################
                                            #user/new -> DISPLAY ROUTE - Registration
                                            #user/create -> ACTION ROUTE - Creating a user
                                            #user/<int:id> -> DISPLAY   ROUTE  
                                            #user/<int:id>/edit -> DISPLAY ROUTE  
                                            #user/<int:id>/update -> ACTION ROUTE  
                                            #user/<int:id>/delete -> ACTION ROUTE  



############################################# CREATE | SAVE ROUTES #############################################
#CREATE New Nominee Action Route for New Nominee Form
@app.route('/nominee/create', methods=['POST'])
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def nominee_create():
    #Validations
    if not model_nominee.Nominee.validator_nominee_info(request.form):
        # print(model_nominee.Nominee.validator(request.form))
        return redirect('/nominee/new') # This will redirect to the same form page if validations failed
    
    #Create Nominee
        #Creating data dictionary to pass user id using session along with request.form
        #this is better than using session through hidden inputs in html to avoid end user to edit the form
    data = {
        **request.form,
        'user_id': session['uuid']
    }
    model_nominee.Nominee.create(data) # Storing the object in database
    return redirect('/nominee/dashboard') # Once form was submitted successfully redirect to the list of Users nominations



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
@app.route('/nominee/<int:id>/info')
def nominee_show_one(id):
    # Check if User id is loggen-in
    if 'uuid' not in session:
        return redirect('/') # redirect to Home page
    nominee = model_nominee.Nominee.get_one_nominee({'id': id})
    user_role = model_user.User.get_user_role_from_session()
    if nominee:
            # print(session['uuid'])
            context = {
                'nominee' : nominee,
                'user_role': user_role,
                'all_nominees' : model_nominee.Nominee.get_all_nominees(),
                'user' : model_user.User.get_one({'id': id})
            }
            return render_template('show_one_nominee_info.html', **context)

    return redirect('/dashboard')





# #Display Show All the Nominees Info
# @app.route('/nominee/show/all')
# def nominee_show_all():
#     # Check if User id is loggen-in
#     if 'uuid' not in session:
#         return redirect('/') # redirect to Home page
#     context = {
#         'all_nominees' : model_nominee.Nominee.get_all_nominees(),
#     }

#     return render_template('show_all_nominee.html', **context)







############################################# UPDATE | EDIT ROUTES #############################################

#Display Route Form to Edit the Selected Existing Nominee
@app.route('/nominee/<int:id>/edit')
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def edit_nominee(id): #Passing ID as an argument 
    #Using Nominee ID to set Access limitation to editing a Nominee form 
    nominee = model_nominee.Nominee.get_one_nominee({'id': id}) # Getting the Nominee by ID
    #Check if the Object is retrieved since it returns a boolean from get method
    if nominee:
        # Using session to check if logged-in user is the Nominator(creator) of the Nominee 
        if 'uuid' in session and session['uuid'] == nominee.user_id:
            # Using context to pass in any CRUD functionalites / data to html 
            context = {
                'nominee':nominee,
            }
            return render_template('nominee_edit_nominee_info.html', **context)
    # IF no user found Redirect User to Nominee dashboard
    return redirect('/dashboard')


#Update Nominee Basic info form Action Route (Update Returns Nothing)
@app.route('/nominee/<int:id>/update', methods=['POST'])
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def update_nominee(id): # Passing an argument ID 

    # Using the Nominee ID to Limit Access for Updating Nominee Form
    nominee = model_nominee.Nominee.get_one_nominee({'id': id}) # Getting the Nominee Id from Database 
    # the get method returns a boolean
    if nominee: #if there's an object returned (so the website doesn't crash)
        # Using session to check if logged-in user is the Nominator(creator) of this Nominee
        if 'uuid' in session and session['uuid'] == nominee.user_id:
            #Validations for Form
            if not model_nominee.Nominee.validator_nominee_info(request.form):
                return redirect(f'/nominee/{id}/edit') # MAKE SURE F STRING is Used to pass in ID
            #Preventing info / data being leaked 
            #Since Update_one() targerts an Id from the Update query which is not in the id from the form (html) but has potential to alter other nominee's info
            #Using data dictionary and passing in everything from this extracted request form(**reques.form) 
            #Then passing in id from the foem 
            data = {
                **request.form,
                'id':id
            }
            #Save / Update the Info 
            model_nominee.Nominee.update_one_nominee(data)
            return redirect('/nominee/dashboard')
    
    return redirect('/dashboard')



############################################# DELETE ROUTES #############################################

# DELETE Action Nominee by ID Route
@app.route('/nominee/<int:id>/delete')
# Call Validation to check the User Role from the decorator from User
@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def nominee_delete(id):
    #Using the Nominee ID to Limit Access for Deleting Nominee Form
    nominee = model_nominee.Nominee.get_one_nominee({'id': id}) # Getting the Nominee Id from Database
    # Check if a nominee object is retrieved
    if nominee:
        # Using session to check if logged-in user is the Nominator(creator) of this Nominee
        if 'uuid' in session and session['uuid'] == nominee.user_id:
            model_nominee.Nominee.delete_one({'id': id})
            return redirect('/nominee/dashboard') #Redirect after successful delete
    # Redirect to dashboard 
    return redirect('/dashboard')




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

