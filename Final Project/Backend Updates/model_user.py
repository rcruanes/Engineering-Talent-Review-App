
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt # importing bycrpt
from flask import flash, session, redirect # importing flash, session,
from functools import wraps #
import re # importing regax


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DATABASE= "wdc_prototype_recommender_db_two"
# creating a list of dictionaries with a for Class(table) User
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.role = data['role']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # Assuming you want to capitalize names when you retrieve them
        self.full_name = f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def to_dict(self):
        """Convert a User instance into a dictionary."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
############################################# CRUD FUNCTIONALITIES #############################################
    ############################## Consistent Naming Convention  #######################
                                    # create, 
                                    # get_all, get_many, get_one, 
                                    # update_one, update_many, 
                                    # delete_one, delete_many



############################################# CREATE / Insert (Returns an int as which is Id) #############################################
    # the data of dictionar passed in is from (request.form) through html in user/create Action route
    @classmethod #Classmethod is used for the entire class 
    def create(cls, data): # anything inside this method will be refered to as data 
        # which can be assigned to a variable like used below (result) for better understanding and usage
        # Creating, Saving, Insert gives back the id(int) as data 
        query = "INSERT INTO users (first_name, last_name, email, pw, role) VALUES ( %(first_name)s , %(last_name)s, %(email)s, %(pw)s, %(role)s);"
        # if the query id is bad it'll come back as false
        # explicitly storing the returned id of the inserted value
        user_id = connectToMySQL(DATABASE).query_db(query, data) # if you see data highlighted then data is true (helps to know to if we need to pass the data from query)
        # returning user id since a Insert query returns an Int Id of the row
        return user_id 



############################################# READ / Get (Return list of dictionaries) #############################################
#Read One by the ID (Returns data in a dictionary)
    @classmethod # retrieving ONE object from here
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
        # RESULT is in a LIST, even if we get ONE DOCUMENT it is a LIST
        # return cls(result[0])
        # to display info we need to feed it an id by going to users.html and creating a <a>link in the for loop give it a <th> as well 


# Read One by the email
    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
        # if len(results) < 1:
            # return False
            return cls(results[0]) # doing the same as the commented two lines above
        # RESULT is in a LIST, even if we get ONE DOCUMENT it is an LIST
        # return cls(result[0])
        # now we need to feed it an id by going to users.html and creating a <a>link in the for loop give it a <th> as well

# Read One by Role
    @classmethod
    def get_user_role(cls, user_id):
        query = "SELECT role FROM users WHERE id = %(user_id)s ;"  # Query to fetch role using user ID
        results = connectToMySQL(DATABASE).query_db(query, {'user_id': user_id})
        if results:
            return results[0]['role']  # Return the role
        return None  # Return None if no results


#Read All 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_users = [] #empty list to get the list of classes / instances
        if results:
            for user in results:
                all_users.append( cls(user) ) # when appening we will get a list of class instances
            return all_users
        return False



############################################# UPDATE (Returns No DATA) #############################################
    @classmethod
    def update_one(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW() WHERE id = %(id)s;" # the id is coming from our hidden input
        # if we're UPDATING it doesn't return anything back successful
        return connectToMySQL(DATABASE).query_db(query, data)


############################################# DELETE (Returns No DATA) #############################################
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM users WHERE id=%(id)s;"
        # if we're DELETING it doesn't return anything back if it's successful
        return connectToMySQL(DATABASE).query_db(query, data)
    



############################################# VALIDATION #############################################
    
#VALIDATION FOR REGISTER ##########################
    @staticmethod # staticmethod is mainly used for validations
    def validator_register(data):
        is_valid = True

        if len(data['first_name']) < 1:
            flash('field is required', 'err_users_first_name_register')
            is_valid = False

        if len(data['last_name']) < 1:
            flash('field is required', 'err_users_last_name_register')
            is_valid = False

        if len(data['email']) < 1:
            flash('field is required', 'err_users_email_register')
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!",'err_users_email_register')
            is_valid = False

        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            if potential_user:
                flash('Email already in use', 'err_users_email_register')
                is_valid = False

        if len(data['pw']) < 1:
            flash('field is required', 'err_users_pw_register')
            is_valid = False

        if len(data['confirm_pw']) < 1:
            flash('field is required', 'err_users_confirm_pw_register')
            is_valid = False

        if data['pw'] != data['confirm_pw']:
            flash('Passwords do not match', 'err_users_confirm_pw_register')
            is_valid = False
            
        if data['role'] not in ['Nominator', 'Recommender', 'Review Committee']:
            flash('Please Select a Role', 'err_users_role_register')
            is_valid = False

        return is_valid



# VALIDATION FOR LOGIN ##########################
    @staticmethod
    def validator_login(data): # validation, checking hash, and storing the id into session after login
        is_valid = True

        if len(data['email']) < 1:
            flash('field is required', 'err_users_email_login')
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email",'err_users_email_login')
            is_valid = False
        else:
            #if the email doesn't exit in the database then user get a error message
            potential_user = User.get_one_by_email({'email': data['email']})
            # print("***************")
            # print(potential_user)
            if not potential_user:
                flash('Invalid Credentials!', 'err_users_email_login')
                is_valid = False

            # check the hash password matches the key from data
            elif not bcrypt.check_password_hash(potential_user.pw, data['pw']):
                flash('Invalid Credentials!', 'err_users_pw_login')
                is_valid = False
            else:
                # store the id into session but make sure not to store the whole user instance or else error will accur
                session['uuid'] = potential_user.id #once logged in store the uuid in session
            
        if len(data['pw']) < 1:
            flash('field is required', 'err_users_pw_login')
            is_valid = False
            
        return is_valid



# VALIDATIONS FOR RESTRICTING ACCESS BASED ON USER ROLES ##############
    @staticmethod
    # Decorator "restrict_access_based_on_role" is for controlling access based on user roles
    def restrict_access_based_on_role(required_role): #passing in an argument to the decotator function that is the route handler function (required_role)
        # ^ Decorator function allows you to extend or modify the behavior of other functions and methods.(higher-order function)
        # Decorator can be used for logging, authentication, or input validation. It can also catch return values
        # AS well as RESTRICT access to functions or methods based on certain conditions
        # In this case User Roles / Permissions for routes

        def access_control_wrapper(func):
            # Preserves function metadata such as name and docstring, make sure to import wraps from functools
            @wraps(func)
            # defining nested wrapper function to pass in two arguments
            # when decorator function is called it will actually call this wrapper function, hence "decoration" 
            # passing in two parameters *args , **kwargs (common naming convention)
            # *args is for the "arguments" which is used to pass in a variable number of positional arguments to a function. Allows the function to accept any number of positional arguments, it's important to know these arguments are in a tuple. 
            # **kwargs is for "keyword arguments" which is used to pass in a variabe number of keyword arguments to a function. Allows the function to accept any number of keyword arguments, it's important to know these arguments are in a dictionary.

            # The inner wrapper function access_control_wrapper is used to wrap the original function and apply the access control logic
            def wrapper(*args, **kwargs): # this wrapper function can accept any number of positional and keyword arguments. 

                # Check if 'uuid' is in session
                if 'uuid' in session:
                    user_id = session['uuid']
                    # Get user from database using the user_id
                    user = User.get_one({'id': user_id})
                    # Check if user exists and has the required role
                    if user and user.role == required_role:
                        # IF User has the required role, allow access to the route
                        return func(*args, **kwargs)
                    # If user is not logged-in or doesn't have the required role, then redirect 
                return redirect('/dashboard')
            return wrapper
        return access_control_wrapper


# VALIDATIONS to GET USER ROLE IN SESSION ##############
    @staticmethod
    def get_user_role_from_session():
        # Check if 'uuid' key exists in the session
        if 'uuid' in session:
            # If it does we extract the user ID
            user_id = session['uuid']
            # Use the get_one method to get the user object from DB on the user ID
            user = User.get_one({'id': user_id})
            # If there is a existing Object 
            if user:
                return user.role # returns the user role
        return None