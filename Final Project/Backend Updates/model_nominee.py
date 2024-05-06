
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app import bcrypt # importing bycrpt
from flask import flash # importing flash
import re # importing regax


from flask_app.models import model_user # imported file for relationships query ( 1 to Many)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DATABASE = "wdc_prototype_recommender_db_two"


# Creating a class Nominee with a list of dictionaries(attributes)
class Nominee:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.department_name = data['department_name']
        self.job_category = data['job_category']
        self.email = data['email']
        self.nominator_qualification = data['nominator_qualification']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'department_name': self.department_name,
            'job_category': self.job_category,
            'email': self.email,
            'nominator_qualification': self.nominator_qualification,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
            'nominator': {
                'first_name': self.nominator.first_name if hasattr(self, 'nominator') else '',
                'last_name': self.nominator.last_name if hasattr(self, 'nominator') else ''
            } if hasattr(self, 'nominator') else {}
        }
    # # used in show_user.html
    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"
    
############################################# CRUD FUNCTIONALITIES #############################################
   ############################## Consistent Naming Convention  #######################
                                    # create, 
                                    # get_all, get_many, get_one, 
                                    # update_one, update_many, 
                                    # delete_one, delete_many


############################################# CREATE #############################################
    # the data of dictionar passed in is from (request.form) through html in user/create Action route
    @classmethod 
    def create(cls, data): # anything inside this method will be refered to as data 
        # which can be assigned to a variable like used below (result) for better understanding and usage
        # add all column names and add all the values
        query = "INSERT INTO nominees ( user_id, first_name, last_name, department_name, job_category, email, nominator_qualification) VALUES ( %(user_id)s, %(first_name)s, %(last_name)s, %(department_name)s, %(job_category)s, %(email)s, %(nominator_qualification)s );"
        # come back as the new row id
        # if the query id is bad it'll come back as false
        result = connectToMySQL(DATABASE).query_db(query, data) # if you see color for data then value is true (helps to know to pass the data from query)
        # returning user id since a Insert query returns an Int Id of the row
        return result # returns the id back to the sever


############################################# READ (DATA type Returned is list of dictionaries) #############################################
#Read One Needs Data passed in parameter  
    @classmethod # retrieving ONE document from here
    def get_one_nominee(cls, data):
        query = "SELECT * FROM nominees WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        # RESULT is in a LIST, even if we get ONE result/object it is an LIST so return the first index in a list
        if results:
            return cls(results[0]) 
        return False
        # to display info we need to feed an id by going to nominees.html and creating a <a>link in the for loop give it a <th> as well

    
# #Read All Basic no need to pass in data 
    @classmethod
    def get_all_nominees(cls): # Getting all of the nominees
        query = "SELECT * FROM nominees;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results: # check to see if there's any objects 
            all_nominees = [] # the data will return a list of dictionaries
            for nominee_single in results: # appending all of the objects 
                all_nominees.append( cls(nominee_single) )
            return all_nominees # now we return the list of dictionaries
        return False


#Read All DOESN'T need DATA passed in the parameter From JOINS (Relationship One to Many)
    @classmethod
    def get_all_nominees_nominator(cls):
        #Joining the Nominees table (Primary - leftside) with the Users table (SEcondary- rightside) 
            # to get the Creater of Object
        query = "SELECT * FROM nominees JOIN users ON users.id = nominees.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        # print(results)
        #Need to extract all the information for the User and relabel the shared attribute names
        #Always relabel the id, created_at, and updated_at will match 
        if results:
            # This is a list of all nominees and each nominees has a nominator attribute attached to it 
            all_nominees_nominators = []
            for dict in results: # for loop to pull the dictionaries for joined table the Users
                # Creating an instance of Nominee
                nominee = cls(dict)
                    # Creating instance of User
                user_data = {   
                    # Relabeling all same attributes between tables / Classes 
                    'id': dict['users.id'],
                    'first_name': dict['users.first_name'], 
                    'last_name': dict['users.last_name'],
                    'email': dict['users.email'],
                    'created_at': dict['users.created_at'],
                    'updated_at': dict['users.updated_at'],
                    # No need for Relabeling these attributes only belong to Users table / Class
                    'pw': dict['pw'],
                    'role':dict['role'], 
                }
                #Now Need to add the User onto the Nominee
                # Make sure to IMPORT the JOINING table model_FILE and NOT the Class!
                user = model_user.User(user_data) # This is the User instance 
                #Now taking the Nominee instance and attach an attribute 
                #Instances are like dictionaries, if key doesn't exist it adds the key to the dictionaries
                # so if the attribute doesn't exist then it'll add that attribute
                nominee.nominator = user # nominator doesn't exist so it'll add it to the user instance created above
                # Now appending the nominee instance to the empty list 
                all_nominees_nominators.append(nominee)
            return all_nominees_nominators # This will give back an Object of User 
        # returning False will give an error if the Nominator deleted the assosiated Nominee or hasn't created one yet
        return [] # You could iterate over an empty array so when there are no results it won't break 



############################################# UPDATE (Returns No DATA) #############################################
    #Update Nominee by ID 
    @classmethod
    def update_one_nominee(cls, data):
        query = "UPDATE nominees SET first_name=%(first_name)s, last_name=%(last_name)s, department_name = %(department_name)s, job_category=%(job_category)s,email=%(email)s, nominator_qualification=%(nominator_qualification)s, updated_at=NOW() WHERE id = %(id)s;" 
        return connectToMySQL(DATABASE).query_db(query, data)


############################################# DELETE (Returns No DATA) #############################################
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM nominees WHERE id=%(id)s;"
        # if we're DELETING it doesn't return anything back if it's successful
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_nominees_with_min_recommendations(cls):
        query = """
        SELECT n.*, COUNT(r.id) AS recommendation_count
        FROM nominees n
        JOIN recommenders r ON n.id = r.nominee_id
        GROUP BY n.id
        HAVING COUNT(r.id) >= 3;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        return [cls(row) for row in results] if results else []
            



############################################# VALIDATION #############################################

#VALIDATION FOR NOMINEE FORM ##########################
    @staticmethod
    def validator_nominee_info(data):
        is_valid = True

        if len(data['first_name']) < 1:
            flash('field is required', 'err_nominees_first_name_nominator')
            is_valid = False
        if len(data['last_name']) < 1:
            flash('field is required', 'err_nominees_last_name_nominator')
            is_valid = False
        if len(data['department_name']) < 1:
            flash('field is required', 'err_nominees_department_name_nominator')
            is_valid = False
        if len(data['job_category']) < 1:
            flash('field is required', 'err_nominees_job_category_nominator')
            is_valid = False
        if len(data['email']) < 1:
            flash('field is required', 'err_nominees_email_nominator')
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!",'err_nominees_email_nominator')
            is_valid = False

        if len(data['nominator_qualification']) < 1:
            flash('field is required', 'err_nominees_nominator_qualification_nominator')
            is_valid = False

        return is_valid
    
