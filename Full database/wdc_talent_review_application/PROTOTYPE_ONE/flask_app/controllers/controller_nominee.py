
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




############################################# READ | DISPLAY ROUTE #############################################

#Display Route Once Clicked on New Nominee from Common Dashboard
@app.route('/nominee/dashboard')
def nominee_dashboard():
    #Validation to check the User Role type

    # Allows for html to use the items in the context to display in front end
    #Could add more things to it it's a list of dictinaries
    #makes sure to inject in html using the new created attribute(s) from get methods
    context = {
        'all_nominees_nominator': model_nominee.Nominee.get_all_nominees_nominator(), # make sure queiry in model class is correct
        'all_nominees': model_nominee.Nominee.get_all_nominees(),
    }
    return render_template('nominee_dashboard.html', **context)


#Display Route Form to Create New Nominee 
@app.route('/nominee/new')
def nominee_new():
    # call the get.all() classmethod to get all users
    #users = User.get_all()   # could also call the gell_all() this way 
    #print(users) # don't have to print this here
    return render_template('nominee_new.html') # easier to call it like this

#Display Route To Show Info of Selected Nominee
@app.route('/nominee/<int:id>/info')
def show_nominee_info():
    return render_template('nominee_info.html')

############################################# CREATE | SAVE ROUTES #############################################

#CREATE New Nominee Action Route for New Nominee Form
@app.route('/nominee/create', methods=['POST'])
def nominee_create():
    #Validations
    if not model_nominee.Nominee.validator_nominee_info(request.form):
        # print(model_nominee.Nominee.validator(request.form))
        return redirect('/nominee/new') # This will redirect to the same form page if validations didn't pass
    
    #Create Nominee
        #Creating data dictionary to pass user id using session along with request.form
        #this is better than using session through hidden inputs in html to avoid from end user from editing form
    data = {
        **request.form,
        'user_id': session['uuid']
    }
    model_nominee.Nominee.create(data)
    return redirect('/nominee/dashboard') # Once form was submitted successfully show th list of Users nominations


############################################# UPDATE | EDIT ROUTES #############################################

#Display Route Form to Edit the Selected Existing Nominee
@app.route('/nominee/<int:id>/edit')
def edit_nominee(id):
    context = {
        'nominee': model_nominee.Nominee.get_one_nominee({'id': id}),
    }
    return render_template("nominee_edit_nominee_info.html", **context)

#Update Nominee Basic info form Route (Update Returns Nothing)
@app.route('/nominee/<int:id>/update', methods=['POST'])
def update_nominee(id):
    #Validations
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
    return redirect("/nominee/dashboard")

#Display Route Form to Edit Existing Nominee
# @app.route('/nominee/edit/<int:id>')
# def edit(id):
#     data = {
#         "id": id
#     }
#     return render_template("edit_user.html", user=User.get_one(data))


# EDIT Action Nominee by ID Route
# @app.route("/user/update", methods=['POST'])
# def updated():
#     User.update(request.form) # since we are using a hidden input 
#     return redirect('/users')

#Display Route to Show Info of Noiminee by ID
# @app.route('/user/show/<int:id>')
# def show(id):
#     data = {
#         "id": id
#     }
#     return render_template("show_user.html", user=User.get_one(data))




############################################# DELETE ROUTES #############################################

# DELETE Action Nominee by ID Route
@app.route('/nominee/<int:id>/delete')
def nominee_delete(id):
    model_nominee.Nominee.delete_one({'id': id})
    return redirect('/nominee/dashboard')


