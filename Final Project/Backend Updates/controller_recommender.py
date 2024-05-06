from flask import Flask, render_template, redirect, request, session, jsonify
from flask_app.models.model_user import User
from flask_app.models.model_nominee import Nominee
from flask_app.models.model_individual_contribution_form import IndividualContributionForm
from flask_app.models.model_recommender import Recommender
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

app = Flask(__name__)

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


@app.route('/recommender/dashboard', methods=['GET'])
@jwt_required()
def recommender_dashboard():
    try:
        # Assuming get_jwt_identity() will give us the current user's ID
        current_user_id = get_jwt_identity()
        current_user = User.get_one({'id': current_user_id})
        all_nominees_with_nominators = Nominee.get_all_nominees_with_nominators()
        nominees_data = [nominee.to_dict() for nominee in all_nominees_with_nominators]
        
        # Also include current user's first name
        return jsonify({
            'nominees': nominees_data,
            'recommender_name': current_user.first_name if current_user else 'Recommender'
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500


# Assuming 'model_user' and other model imports are defined correctly

@app.route('/recommend/new', methods=['GET'])
@jwt_required()
def recommend_new():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Fetch user-specific or general info if needed
        return render_template('recommendation_new.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendation/create', methods=['POST'])
@jwt_required()
def recommend_create():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    try:
        data = request.json
        if 'work_contributions' not in data:
            return jsonify({'error': 'work_contributions key is missing'}), 400

        work_contributions = data['work_contributions']  # Directly access the list
        # Process work_contributions and other data...
        return jsonify({'message': 'Recommendation created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/nominees/nominator', methods=['GET'])
def get_nominees_with_nominators():
    try:
        nominees = Nominee.get_all_nominees_with_nominators()
        return jsonify([nominee.to_dict() for nominee in nominees]), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500


@app.route('/review/nominee/<int:nominee_id>/details')
@jwt_required()
def get_nominee_details(nominee_id):
    try:
        details = Recommender.get_recommendation_details_with_name(nominee_id)
        if details:
            return jsonify([detail.to_dict() for detail in details]), 200
        return jsonify({'error': 'No details found for this nominee'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500