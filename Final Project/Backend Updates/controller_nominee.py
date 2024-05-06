
from flask_app import app
from flask import render_template, redirect, request, session
from flask import jsonify
from functools import wraps
from flask_app.models.model_nominee import Nominee
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_app.models.model_user import User
import logging
from flask_app.models.model_education import NomineesEducationHistory

# import the class from model_user.py
from flask_app.models import model_nominee, model_user, model_education

############################################# RESTFUL ROUTE ARCHITECTURE #############################################
                                ################# table_name/id(if possible)/action #################
                                            #user/new -> DISPLAY ROUTE - Registration
                                            #user/create -> ACTION ROUTE - Creating a user
                                            #user/<int:id> -> DISPLAY   ROUTE  
                                            #user/<int:id>/edit -> DISPLAY ROUTE  
                                            #user/<int:id>/update -> ACTION ROUTE  
                                            #user/<int:id>/delete -> ACTION ROUTE  



############################################# CREATE | SAVE ROUTES #############################################

def restrict_access_based_on_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract UUID from the Authorization header
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                uuid = auth_header.split('Bearer ')[1]
                # Set the UUID in the session
                session['uuid'] = uuid
            # Check if 'uuid' exists in session and get the user_id
            user_id = session.get('uuid')
            if user_id is None:
                return jsonify({'error': 'User not authenticated'}), 401
            
            # Get the role of the logged-in user
            #user_role = model_user.User.get_user_role(user_id)
            #if user_role != role:
                #return jsonify({'error': f'Access restricted to {role}'}), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/nominee/create', methods=['POST'])
@jwt_required()
def nominee_create():
    user_id = get_jwt_identity()
    print("Received UserID from JWT:", user_id)
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    try:
        nominee_data = {
            'user_id': user_id,
            'first_name': request.json['first_name'],
            'last_name': request.json['last_name'],
            'department_name': request.json['department_name'],
            'job_category': request.json['job_category'],
            'email': request.json['email'],
            'nominator_qualification': request.json['nominator_qualification']
        }
        nominee_id = Nominee.create(nominee_data)
        if nominee_id:
            return jsonify({'message': 'Nominee created successfully', 'id': nominee_id}), 201
        else:
            return jsonify({'error': 'Failed to create nominee'}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing data for key: {e}'}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500
############################################# READ | DISPLAY ROUTE #############################################
#Display Route Once Clicked on New Nominee from Common Dashboard
@app.route('/nominee/dashboard')
#@model_user.User.restrict_access_based_on_role('Nominator')  # Only the Nominator can access this route
def nominee_dashboard():


    nominees = model_nominee.Nominee.get_all_nominees_nominator()
    nominees_data = [nominee.to_dict() for nominee in nominees]  # Serialize each nominee

    context = {
        'all_nominees_nominator': nominees_data,
        'all_nominees': [nominee.to_dict() for nominee in model_nominee.Nominee.get_all_nominees()],
        'all_users': [user.to_dict() for user in model_user.User.get_all()]  # Assuming you have a similar method in User model
    }
    return jsonify(context)




#Display Route Form to Create New Nominee 
@app.route('/nominee/new')
# Call Validation to check the User Role from the decorator from User
#@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
def nominee_new():
    # call the get.all() classmethod to get all users
    #users = User.get_all()   # could also call the gell_all() this way 
    #print(users) #  print all users to terminal
    return render_template('nominee_new.html') # easier to call it like this


#Display Show Info of Selected Nominee by ID Route
@app.route('/nominee/<int:id>/info', methods=['GET'])
def nominee_show_one(id):
    nominee = model_nominee.Nominee.get_one_nominee({'id': id})
    educations = model_education.NomineesEducationHistory.get_one_edu({'nominee_id': id})
    if not nominee:
        return jsonify({'error': 'Nominee not found'}), 404
    nominee_dict = nominee.to_dict()
    nominee_dict['educations'] = [edu.to_dict() for edu in educations]
    return jsonify(nominee_dict), 200


@app.route('/recommender/dashboard', methods=['GET'])
@jwt_required()
def recommender_dashboard():
    try:
        all_nominees_with_nominators = Nominee.get_all_nominees_nominator()
        nominees_data = [nominee.to_dict() for nominee in all_nominees_with_nominators]
        return jsonify(nominees_data), 200
    except Exception as e:
        app.logger.error("Error while fetching dashboard data: %s", str(e))
        return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500


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
#@model_user.User.restrict_access_based_on_role('Nominator') # Only the Nominator can access this route
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
@app.route('/nominee/<int:id>/update', methods=['PUT'])
@jwt_required()
def update_nominee(id):
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Malformed request, please send valid JSON'}), 400

    if not model_nominee.Nominee.validator_nominee_info(data):
        return jsonify({'error': 'Validation failed'}), 422

    nominee = model_nominee.Nominee.get_one_nominee({'id': id})
    if not nominee:
        return jsonify({'error': 'Nominee not found'}), 404

    try:
        update_result = model_nominee.Nominee.update_one_nominee({'id': id, **data})
        if update_result:
            return jsonify({'error': 'Submission Failed'}), 400
        else:
            return jsonify({'message': 'Nominee Updated successfully'}), 200
    except Exception as e:
        app.logger.error(f'Failed to update nominee: {e}')
        return jsonify({'error': str(e)}), 500

############################################# DELETE ROUTES #############################################

# DELETE Action Nominee by ID Route
@app.route('/nominee/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def nominee_delete(id):
    try:
        # Fetch the nominee based on ID to ensure it exists
        nominee = model_nominee.Nominee.get_one_nominee({'id': id})
        if not nominee:
            return jsonify({'error': 'Nominee not found'}), 404

        # Assuming the user is authorized and the nominee exists
        model_nominee.Nominee.delete_one({'id': id})
        return jsonify({'message': 'Nominee successfully deleted'}), 200
    except Exception as e:
        # Log the exception details to understand what went wrong
        app.logger.error(f'Error deleting nominee: {str(e)}')
        return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500


@app.route('/nominees/nominator', methods=['GET'])
def get_nominees_with_nominators():
    try:
        logging.info("Fetching all nominees with nominators")
        nominees = Nominee.get_all_nominees_nominator()
        return jsonify([nominee.to_dict() for nominee in nominees]), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500
    


@app.route('/nominee/<int:nominee_id>/education/add', methods=['POST'])
@jwt_required()
def add_nominee_education(nominee_id):
    try:
        data = request.get_json()
        # Include nominee_id in the data dictionary before passing it to the model
        data['nominee_id'] = nominee_id
        result = NomineesEducationHistory.create_education(data)
        if result:
            return jsonify({'message': 'Education added successfully', 'id': result}), 201
        else:
            return jsonify({'error': 'Failed to add education'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/nominee/education/<int:edu_id>/edit', methods=['PUT'])
def update_nominee_education(edu_id):
    data = request.get_json()  # Get data from the request body
    data['id'] = edu_id  # Ensure the education ID is included in the data
    if NomineesEducationHistory.update_one_edu(data):
        return jsonify({"message": "Education updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update education"}), 400  # More specific error handling can be beneficial


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

