from flask_app import app
from flask import render_template, redirect, request, session
from collections import defaultdict

# import the class files from models folder
from flask_app.models import   model_user, model_nominee, model_recommender, model_review_committee, model_nominee_education_history_form, model_nominee_professional_history_form, model_individual_contribution_form, model_project_manager_contribution_form, model_people_manager_contribution_form





############################################# CREATE | SAVE | INSERT ROUTES #############################################
############################################# CREATE | SAVE | INSERT ROUTES #############################################
#CREATE New Review for Nominee Action Route
@app.route('/review/create', methods=['POST'])
@model_user.User.restrict_access_based_on_role('ReviewCommittee')
def review_create():
    if 'uuid' not in session:
        return redirect('/')

    user_id = session['uuid']  # Fetch USER ID from session
    user = model_user.User.get_one({'id': user_id})

    try:
        print("Form Data Received", request.form)
        
        nominee_id = request.form.get('nominee_id')
        if not nominee_id:
            print("Nominee ID not provided.")
            return redirect('/review/dashboard')

        data = {
            'rank_individual_contribution': request.form.get('rank_individual_contribution'),
            'rank_project_lead_contribution': request.form.get('rank_project_lead_contribution'),
            'rank_people_manager_contribution': request.form.get('rank_people_manager_contribution'),
            'nominee_id': nominee_id,
            'user_id': user.id,
        }

        print("Data to be inserted:", data)
        model_review_committee.ReviewCommittee.create_review(data)
        return redirect('/review/dashboard')
    except Exception as e:
        print("An error occurred:", str(e))
        return redirect('/recommend/new')




############################################# READ | SELECT DISPLAY ROUTE #############################################
############################################# READ | SELECT DISPLAY ROUTE #############################################

#Display Recommender Dashboard Route
@app.route('/review/dashboard')
# Using Decorator to Call Validation from model_user to check the User Role 
@model_user.User.restrict_access_based_on_role('ReviewCommittee') # Only the Recommender can access this route
def review_committee_dashboard():
    # # Check to see if User in session( )
    if 'uuid' not in session:
        return redirect('/') # if User not in session then logout
            # This is the USER ID NOT THE RECOMMENDER_ID!!
    user_id = session['uuid']  # Fetch USER ID from session
    user = model_user.User.get_one({'id': user_id})
    
    # recommender = model_recommender.Recommender.get_one_recommender({'id': id})
    # nominee = model_nominee.Nominee.get_one_nominee({'id': id})

    #Using Context to pass data from model with neccessary queries 
    context = {
        # 'nominee': model_nominee.Nominee.get_one_nominee({'id': id}),
        'user' : user,
        'all_nominees_info': model_recommender.Recommender.get_all_recommendations_with_details(),
        'all_reviews': model_review_committee.ReviewCommittee.get_all_reviews()
    }

    return render_template('review_comittee_dashboard.html', **context)


#Display Nominee Info of Selected Nominee by ID Route
@app.route('/review/<int:nominee_id>/nomination/info')
def review_show_nominee_info(nominee_id):
    if 'uuid' not in session:
        return redirect('/')  # Redirect to home if not logged in

    nominee_details = model_nominee.Nominee.get_nomiees_full_review_by_nominee_id(nominee_id)
    print('NOMINEE DETAIL', nominee_details)
    if not nominee_details:
        return "Nominee information not found", 404  # Or redirect to a suitable error page or dashboard

        # Preparing context for rendering, parsing the complex data structure as needed
    context = {
        'nominee': nominee_details
    }
    return render_template('show_one_review_comittee.html', **context)
