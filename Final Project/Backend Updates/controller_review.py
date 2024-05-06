from flask_app import app
from flask import render_template, redirect, request, session, jsonify
from flask import jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_jwt_extended import jwt_required
from flask_app import app
from flask_app.models.model_individual_contribution_form import IndividualContributionForm
from flask_app.models.model_nominee import Nominee

# import the class files from models folder
from flask_app.models import  model_individual_contribution_form, model_nominee, model_recommender, model_user


############################################# READ | SELECT DISPLAY ROUTE #############################################

#Display Recommender Dashboard Route
@app.route('/review/dashboard')
#@model_user.User.restrict_access_based_on_role('ReviewCommittee') # Only the Review Committee can access this route
def review_committee_dashboard():
    try:
        nominees_nominator = model_nominee.Nominee.get_all_nominees_nominator()
        nominees = model_nominee.Nominee.get_nominees_with_min_recommendations()
        users = model_user.User.get_all()

        context = {
            'all_nominees_nominator': [nominee.to_dict() for nominee in nominees_nominator],
            'all_nominees': [nominee.to_dict() for nominee in nominees],
            'all_users': [user.to_dict() for user in users]
        }

        return jsonify(context)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/review/nominee/<int:nominee_id>/details')
@jwt_required()
def get_nominee_details(nominee_id):
    try:
        nominee = Nominee.get_one_nominee({'id': nominee_id})
        if not nominee:
            return jsonify({'error': 'Nominee not found'}), 404
        
        details = IndividualContributionForm.get_nominee_contributions(nominee_id)
        if not details:
            details = []
        
        details.insert(0, {'nominee_name': f"{nominee.first_name} {nominee.last_name}"})
        return jsonify(details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500