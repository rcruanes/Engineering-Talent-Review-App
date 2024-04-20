############################################# CONSTRUCTOR #############################################
# Applying imports here allows to be accessed throughout the entire project files
from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhh"  # to use session

# we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument     
from flask_bcrypt import Bcrypt # Importing Bcrypt 
bcrypt = Bcrypt(app)



