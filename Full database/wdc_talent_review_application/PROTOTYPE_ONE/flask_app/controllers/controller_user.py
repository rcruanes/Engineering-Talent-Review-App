
from flask_app import app, bcrypt
from flask import render_template, redirect, request, session

# import the class from model_user.py
from flask_app.models import model_user

############################################# RESTFUL ROUTE ARCHITECTURE #############################################
                                ################# table_name/id(if possible)/action #################
                                            #user/new -> DISPLAY ROUTE - Registration
                                            #user/create -> ACTION ROUTE - Creating a user
                                            #user/<int:id> -> DISPLAY   ROUTE  
                                            #user/<int:id>/edit -> DISPLAY ROUTE  
                                            #user/<int:id>/update -> ACTION ROUTE  
                                            #user/<int:id>/delete -> ACTION ROUTE  

# Define role options to have the select options for role attribute with datatype ENUM of tuple
role_options = ['Nominator', 'Recommender', 'Review Committee']
# Context processor to make role options available globally
@app.context_processor
def inject_role_options():
    return dict(role_options=role_options)


############################################# (START) REGISTER - LOGIN - LOGOUT ROUTES #############################################

#Create User Action Route (Registration) 
@app.route('/user/create', methods=['POST']) #Creating a new user and storing user id in session
def user_create():
    # Validations is  being caled / ran in the Model User file / class @staticmethod
        # passing in validator to see if any of the info is false during sign up 
    if not model_user.User.validator_register(request.form):
        return redirect('/') # if any of the info is false during registration it''' redirect with flash messages
    # Hashing password using Bcrypt (make sure to import bcrypy in necessary files: model, controller, __init__)
    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    data = {
        **request.form,
        'pw': hash_pw
    }
    # Create(save) the user from data which returns an id once sign up is successful
    id = model_user.User.create(data)
    print('id') #Using this for terminal checks errors 
    # Storing user id in session
    session['uuid'] = id # can use seesion to check if a user is logged in or not
    return redirect('/dashboard') # this route is a common landing page 


#Logging Existing User Action Route 
@app.route('/user/login', methods=['POST'])
def user_login():
    #Validation is being caled / ran in the Model User file / class @staticmethod
    model_user.User.validator_login(request.form) # passing in validator to see if any of the info is false during sign up 
    # print(model_user.User.validator_login(request.form))
    return redirect('/') # if any of the info is false during registration it''' redirect with flash messages (make sure to import flash)


#Logout User Action Route 
@app.route('/user/logout', methods=['GET'])
def user_logout():
    #using session to logout user
    del session['uuid']
    return redirect('/')
############################################# (END) REGISTER - LOGIN - LOGOUT ROUTES #############################################


#Display Route 
@app.route("/users")
def users():
    # call the get.all() classmethod to get all users
    #users = User.get_all()   # could also call the gell_all() this way 
    #print(users) # don't have to print this here
    return render_template("users.html", users=model_user.User.get_all()) # easier to call it like this

# Display Route
@app.route( '/user/new')
def new():
    return render_template("create.html")




    # return redirect("/users")


# @app.route('/user/edit/<int:id>')
# def edit(id):
#     data = {
#         "id": id
#     }
#     return render_template("edit_user.html", user=User.get_one(data))


# @app.route("/user/update", methods=['POST'])
# def updated():
#     User.update(request.form) # since we are using a hidden input 
#     return redirect('/users')

# @app.route('/user/destroy/<int:id>')
# def destroy(id):
#     data = {
#         "id":id
#     }
#     User.destroy(data)
#     return redirect('/users')


# @app.route('/user/show/<int:id>')
# def show(id):
#     data = {
#         "id": id
#     }
#     return render_template("show_user.html", user=User.get_one(data))



