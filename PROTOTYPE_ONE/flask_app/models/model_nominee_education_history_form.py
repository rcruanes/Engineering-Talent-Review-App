from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app import bcrypt # importing bycrpt
from flask import flash # importing flash
import re # importing regax

from flask_app.models import model_user # imported file for relationships query ( 1 to Many)


DATABASE = "wdc_talent_review_new_final_product_complete_db"


# Creating a class for nominee's education input with a list of dictionaries(attributes)
class NomineeEducationHistory:
    def __init__( self , data):
        self.id = data['id']
        self.nominee_id = data['nominee_id']
        self.college_name = data['college_name']
        self.location = data['location']
        self.degree = data['degree']
        self.program = data['program']
        self.graduation_year = data['graduation_year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



############################################# CRUD FUNCTIONALITIES #############################################
   ############################## Consistent Naming Convention  #######################
                                    # create, 
                                    # get_all, get_many, get_one, 
                                    # update_one, update_many, 
                                    # delete_one, delete_many


############################################# CREATE #############################################
    # the data of dictionar passed in is from (request.form) through html in user/create Action route
    @classmethod 
    def create_nominee_education_history(cls, data): # anything inside this method will be refered to as data 
        # which can be assigned to a variable like used below (result) for better understanding and usage
        # add all column names and add all the values
        query = "INSERT INTO nominees_educations_histories ( nominee_id, college_name, location, degree, program, graduation_year) VALUES ( %(nominee_id)s, %(college_name)s, %(location)s, %(degree)s, %(program)s, %(graduation_year)s);"
        # come back as the new row id
        # if the query id is bad it'll come back as false
        result = connectToMySQL(DATABASE).query_db(query, data) # if you see color for data then value is true (helps to know to pass the data from query)
        # returning user id since a Insert query returns an Int Id of the row
        return result # returns the id back to the sever


############################################# READ (DATA type Returned is list of dictionaries) #############################################
############################################# READ (DATA type Returned is list of dictionaries) #############################################
#Read One Needs Data passed in parameter  
    @classmethod # retrieving ONE document from here
    def get_one_nominee_education_history(cls, data):
        query = "SELECT * FROM nominees_educations_histories WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        # RESULT is in a LIST, even if we get ONE result/object it is an LIST so return the first index in a list
        if results:
            print('Get One Query Education Nominee:', results)
            return cls(results[0]) 
        return False
        # to display info we need to feed an id by going to nominees.html and creating a <a>link in the for loop give it a <th> as well



    # Read One Form by Nominee ID
    @classmethod
    def get_one_by_nominee_id(cls, data):
        query = "SELECT * FROM nominees_educations_histories WHERE nominee_id = %(nominee_id)s LIMIT 1;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            print('Get One By Nominee Id:', results)
            return cls(results[0])
        return None




    #Read All Basic no need to pass in data 
    @classmethod
    def get_all_nominees_education_histories(cls): # Getting all of the nominees edu history
        query = "SELECT * FROM nominees_educations_histories;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results: # check to see if there's any objects 
            all_nominees_educations = [] # the data will return a list of dictionaries
            for nominee_single in results: # appending all of the objects 
                all_nominees_educations.append( cls(nominee_single) )
            return all_nominees_educations # now we return the list of dictionaries
        return False






############################################# UPDATE (Returns No DATA) #############################################
############################################# UPDATE (Returns No DATA) #############################################
    #Update One Form by ID 
    @classmethod
    def update_nominee_education_history(cls, data):
        query = "UPDATE nominees_educations_histories SET college_name=%(college_name)s, location=%(location)s, degree = %(degree)s, program=%(program)s, graduation_year=%(graduation_year)s, updated_at=NOW() WHERE id = %(id)s;" 
        return connectToMySQL(DATABASE).query_db(query, data)



############################################# DELETE (Returns No DATA) #############################################
############################################# DELETE (Returns No DATA) #############################################
# Check if Nominee Id exist(FOR NOMINATOR)
    @classmethod
    def check_exists_by_nominee_id(cls, data):
        query = "SELECT COUNT(*) AS count FROM nominees_educations_histories WHERE nominee_id=%(nominee_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result[0]['count'] > 0


    # Delete by Nominee Id(FOR NOMINATOR)
    @classmethod
    def delete_by_nominee_id(cls, data):
        query = "DELETE FROM nominees_educations_histories WHERE nominee_id=%(nominee_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)




############################################# VALIDATION #############################################
############################################# VALIDATION #############################################

#VALIDATION FOR award Qualification FORM ##########################
    @staticmethod
    def validator_edu_history(data):
        is_valid = True

        if len(data['college_name']) < 3:
            flash('College name must be at least 3 characters.', 'err_nominees_college_name')
            is_valid = False

        if len(data['location']) < 3:
            flash('Location must be at least 3 characters.', 'err_nominees_location')
            is_valid = False

        if len(data['degree']) < 3:
            flash('College name must be at least 3 characters.', 'err_nominees_degree')
            is_valid = False

        if len(data['program']) < 3:
            flash('Program name must be at least 3 characters.', 'err_nominees_program')
            is_valid = False

        if data['graduation_year'] and (int(data['graduation_year']) < 1900 or int(data['graduation_year']) > 2024):
            flash('Year must be between 1900 and 2024.', 'err_nominees_graduation_year')
            is_valid = False

        return is_valid