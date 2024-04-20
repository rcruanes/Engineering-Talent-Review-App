# Need to import all the controller files created to navigate the requested routes from client 
    # Or else the Error Message " The request URL was not found on the server..." will show up on when trying to load html page
from flask_app import app
from flask_app.controllers import controller_user, controller_routes, controller_nominee, controller_recommender, controller_review

if __name__ == "__main__":
    app.run(debug=True)