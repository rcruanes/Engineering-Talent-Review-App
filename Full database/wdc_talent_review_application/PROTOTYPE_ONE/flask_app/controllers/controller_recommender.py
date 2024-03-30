from flask_app import app
from flask import render_template, redirect, request, session

# Import the class from model files
from flask_app.models import model_nominee, model_user

# Recommender Dashboard Route
@app.route('/recommender/dashboard')
def recommender_dashboard():
    # Retrieve all nominees associated with the recommender
    # You may need to adjust this method in the model_nominee class
    # to retrieve nominees based on recommender ID.
    context = {
        'all_nominees': model_nominee.Nominee.get_all_nominees_for_recommender(session['uuid']),
        'all_nominees_nominator': model_nominee.Nominee.get_all_nominees_nominator(), # make sure queiry in model class is correct
        'all_nominees': model_nominee.Nominee.get_all_nominees(),
    }
    return render_template('recommender_dashboard.html', **context)

# Display Route to Show Info of Selected Nominee
@app.route('/recommender/nominee/<int:id>/info')
def show_nominee_info(id):
    # Retrieve nominee info by ID
    nominee = model_nominee.Nominee.get_one({'id': id})
    return render_template('nominee_info.html', nominee=nominee)

# Display Route Form to Edit the Selected Existing Nominee
@app.route('/recommender/nominee/<int:id>/edit')
def edit_nominee(id):
    # Retrieve nominee info by ID
    nominee = model_nominee.Nominee.get_one({'id': id})
    return render_template("nominee_edit_nominee_info.html", nominee=nominee)

# Update Nominee Basic info form Route (Update Returns Nothing)
@app.route('/recommender/nominee/<int:id>/update', methods=['POST'])
def update_nominee(id):
    # Validations
    if not model_nominee.Nominee.validator_nominee_info(request.form):
        return redirect(f'/recommender/nominee/{id}/edit')
    
    # Update nominee info
    data = {
        **request.form,
        'id': id
    }
    model_nominee.Nominee.update_one_nominee(data)
    return redirect("/recommender/dashboard")

# DELETE Action Nominee by ID Route
@app.route('/recommender/nominee/<int:id>/delete')
def nominee_delete(id):
    model_nominee.Nominee.delete_one({'id': id})
    return redirect('/recommender/dashboard')
