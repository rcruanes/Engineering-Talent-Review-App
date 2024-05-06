
from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, url_for
from flask import make_response
from flask_app.models import model_user
from flask_app.models.model_user import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_app.models.model_recommender import Recommender
from flask_app.models.model_individual_contribution_form import IndividualContributionForm


# import the class from model_user.py


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
from flask import jsonify, abort

@app.route('/user/create', methods=['POST'])
def user_create():
    data = request.get_json()
    
    # Validate the user registration data
    if not User.validator_register(data):
        return jsonify({'error': 'Validation failed'}), 400

    # Hash the password and update the data dictionary
    hashed_pw = bcrypt.generate_password_hash(data['pw']).decode('utf-8')
    data['pw'] = hashed_pw

    try:
        # Attempt to create a new user in the database
        user_id = User.create(data)
        if user_id:
            # Create a new JWT token for the newly registered user
            # It's crucial to include the user's role when creating the JWT token for proper access control
            user_info = User.get_one({'id': user_id})
            if not user_info:
                return jsonify({'error': 'User creation successful but unable to retrieve user details'}), 500
            
            access_token = create_access_token(identity={'id': user_info.id, 'role': user_info.role})
            # Optionally, store the user's ID and role in the session
            session['user_id'] = user_info.id
            session['role'] = user_info.role
            # Return the success message with the JWT token and user role
            return jsonify({
                'message': 'User created successfully',
                'id': user_info.id,
                'access_token': access_token,
                'role': user_info.role
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 400
    except Exception as e:
        # If there's an exception, return an error message
        return jsonify({'error': str(e)}), 500



#Logging Existing User Action Route 
@app.route('/user/login', methods=['POST'])
def user_login():
    user = model_user.User.get_one_by_email({'email': request.json['email']})
    if user and bcrypt.check_password_hash(user.pw, request.json['pw']):
        access_token = create_access_token(identity=user.id)
        role = User.get_user_role(user.id)
        print("User role:", user.role)
        return jsonify({'access_token': access_token, 'message': 'Login successful', 'id': user.id, 'role' : user.role}), 200
    else:
        return jsonify({'error': 'Login failed'}), 401
    
#Logout User Action Route @app.route('/user/login', methods=['POST'])
def user_login():
    user = model_user.User.get_one_by_email({'email': request.json['email']})
    if user and bcrypt.check_password_hash(user.pw, request.json['pw']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})  # Include role in the identity
        return jsonify({
            'access_token': access_token,
            'role': user.role,  # Send role to the client
            'message': 'Login successful',
            'id': user.id
        }), 200
    else:
        return jsonify({'error': 'Login failed'}), 401
    
    
@app.route('/user/logout', methods=['GET'])
def user_logout():
    # Check if 'uuid' key exists in session
    del session['uuid']
############################################# (END) REGISTER - LOGIN - LOGOUT ROUTES #############################################


# User Dashboard for option to select task as the User after logging in
@app.route('/dashboard')
def dashboard():
    # Ensure the user is logged in
    if 'uuid' not in session:
        # If not logged in, redirect to the login page
        return redirect('/')  # Assuming 'login' is the endpoint name for your login page

    # Example: Fetch some data based on user_id from session
    user_id = session['uuid'] or get_jwt_identity()
    try:
        # Fetch data from database
        user_data = get_user_data(user_id)  # Replace get_user_data with your actual data retrieval function
        return jsonify(user_data), 200
    except Exception as e:
        # Handle errors and ensure a JSON response is returned
        return jsonify({'error': str(e)}), 500

    # If no data is fetched, return an empty JSON or error message
    return jsonify({'message': 'No data available'}), 404

@app.route('/user/data', methods=['GET'])
def get_user_data():
    # Check if the user is logged in
    if 'uuid' in session:
        user_id = session['uuid'] or get_jwt_identity()
        # Get the user data from the model using the user_id
        user = model_user.User.get_one({'id': user_id})  # Modify this line
        if user:
            # Return the user's first name as a JSON response
            return jsonify({
                'first_name': user.first_name
            }), 200
    # If user is not logged in or data retrieval fails, return an error
    return jsonify({'error': 'User data not found'}), 404


@app.route('/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()  # Obtain user ID from JWT token
    user = User.get_one({'id': user_id})
    if user:
        return jsonify(first_name=user.first_name), 200
    else:
        return jsonify({'error': 'User not found'}), 404




############################################# OTHER ROUTES FOR REFRENCE #############################################

# #Display Route 
# @app.route("/users")
# def users():
#     # call the get.all() classmethod to get all users
#     #users = User.get_all()   # could also call the gell_all() this way 
#     #print(users) # don't have to print this here
#     return render_template("users.html", users=model_user.User.get_all()) # easier to call it like this

# # Display Route
# @app.route( '/user/new')
# def new():
#     return render_template("create.html")

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


# @app.route('/user/<int:id>/show')
# def show(id):
#     data = {
#         "id": id
#     }
#     return render_template("show_user.html", user=User.get_one(data))

@app.route('/recommendation/create', methods=['POST'])
@jwt_required()
def recommend_create():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'work_contributions' not in data or not isinstance(data['work_contributions'], list):
        return jsonify({'error': 'Work contributions key is missing or invalid'}), 400
    if not all(key in data for key in ['nominee_id', 'answers']):
        return jsonify({'error': 'Missing necessary fields'}), 400

    # Convert work contributions list to a comma-separated string, ensuring each is a valid entry
    valid_contributions = {'individual_contributor', 'project_manager', 'people_manager'}
    contributions = [x for x in data['work_contributions'] if x in valid_contributions]
    

    recommendation_data = {
        'user_id': user_id,
        'nominee_id': data['nominee_id'],
        'work_contributions': contributions
    }

    try:
        recommender_id = Recommender.create_recommendation(recommendation_data)
        if recommender_id:
            answers = data['answers']
            individual_questions_data = {
                'recommender_id': recommender_id,
                'ic_q1': answers.get('ic_q1', ''),
                'ic_q2': answers.get('ic_q2', ''),
                'ic_q3': answers.get('ic_q3', ''),
                'ic_q4': answers.get('ic_q4', ''),
                'ic_q5': answers.get('ic_q5', ''),
            }
            IndividualContributionForm.create_individual_contribution(individual_questions_data)
            return jsonify({'message': 'Recommendation created successfully', 'recommender_id': recommender_id}), 201
        else:
            return jsonify({'error': 'Failed to create recommendation'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Include a fail-safe return in case of any other cases
    return jsonify({'error': 'Unhandled exception or path in the function'}), 500
