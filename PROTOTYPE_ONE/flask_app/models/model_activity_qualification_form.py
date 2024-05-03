from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app import bcrypt # importing bycrpt
from flask import flash # importing flash


from flask_app.models import model_user # imported file for relationships query ( 1 to Many)


DATABASE = "wdc_talent_review_new_final_product_complete_db"


# Creating a class for nominee's and Nominatory Activity Qualification
class ActivityQualificationForm:
    def __init__( self , data):
        self.id = data['id']
        self.nominee_id = data['nominee_id']
        self.nominator_activity_name = data['nominator_activity_name']
        self.nominator_activity_year = data['nominator_activity_year']
        self.nominator_activity_description = data['nominator_activity_description']
        self.nominee_qualification = data['nominee_qualification']
        self.nominee_activity_name = data['nominee_activity_name']
        self.nominee_activity_year = data['nominee_activity_year']
        self.nominee_activity_description = data['nominee_activity_description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



############################################# CRUD FUNCTIONALITIES #############################################
   ############################## Consistent Naming Convention  #######################
                                    # create, 
                                    # get_all, get_many, get_one, 
                                    # update_one, update_many, 
                                    # delete_one, delete_many


############################################# CREATE #############################################
############################################# CREATE #############################################
    #Create one 
    #Data of dictionary passed in is from (request.form) through html in create Action route
    @classmethod 
    def create_activity(cls, data): # anything inside this method will be refered to as data 
        # which can be assigned to a variable like used below: (result) for better understanding and usage
        # add all column names and add all the values
        query = """
        INSERT INTO activities_qualifications_forms ( nominee_id, nominator_activity_name, nominator_activity_year, 
        nominator_activity_description, nominee_qualification, nominee_activity_name, nominee_activity_year, nominee_activity_description ) 
        VALUES ( %(nominee_id)s, %(nominator_activity_name)s, %(nominator_activity_year)s, %(nominator_activity_description)s, 
        %(nominee_qualification)s, %(nominee_activity_name)s, %(nominee_activity_year)s, %(nominee_activity_description)s);
        """
        # come back as the new row id 
        # if the query id is bad it'll come back as false
        result = connectToMySQL(DATABASE).query_db(query, data) # if you see color for data then value is true (helps to know to pass the data from query)
        # returning user id since a Insert query returns an Int Id of the row
        return result # returns the id back to the sever




############################################# READ (DATA type Returned is list of dictionaries) #############################################
############################################# READ (DATA type Returned is list of dictionaries) #############################################
# READ ONE: Retrieve a single activity qualification record by NOMINEE ID
    @classmethod
    def get_one_by_nominee_id(cls, data):
        query = "SELECT * FROM activities_qualifications_forms WHERE nominee_id = %(nominee_id)s LIMIT 1;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            print('Get One By Nominee Id:', results)
            return cls(results[0])
        return None




############################################# UPDATE | EDIT ROUTES #############################################
############################################# UPDATE | EDIT ROUTES #############################################
#Update One Form by ID 
    @classmethod
    def update_activity_qualification(cls, data):
        query = """
        UPDATE activities_qualifications_forms 
        SET 
            nominator_activity_name=%(nominator_activity_name)s, 
            nominator_activity_year=%(nominator_activity_year)s, 
            nominator_activity_description=%(nominator_activity_description)s, 
            nominee_qualification=%(nominee_qualification)s, 
            nominee_activity_name=%(nominee_activity_name)s, 
            nominee_activity_year=%(nominee_activity_year)s, 
            nominee_activity_description=%(nominee_activity_description)s, 
            updated_at=NOW() 
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)





############################################# DELETE (Returns No DATA) #############################################
############################################# DELETE (Returns No DATA) #############################################
# Check if Nominee Id exist(FOR NOMINATOR USE ONLY)
    @classmethod
    def check_exists_by_nominee_id(cls, data):
        query = "SELECT COUNT(*) AS count FROM activities_qualifications_forms WHERE nominee_id=%(nominee_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result[0]['count'] > 0


# Delete by Nominee Id(FOR NOMINATOR USE ONLY)
    @classmethod
    def delete_by_nominee_id(cls, data):
        query = "DELETE FROM activities_qualifications_forms WHERE nominee_id=%(nominee_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


















############################################# VALIDATION #############################################
############################################# VALIDATION #############################################

#VALIDATION FOR Activity Qualification FORM ##########################
    @staticmethod
    def validator_activity_qualification(data):
        is_valid = True

        if len(data['nominator_activity_name']) < 3:
            flash('Activity name must be at least 3 characters.', 'err_nominees_nominator_activity_name')
            is_valid = False

        if data['nominator_activity_year'] and (int(data['nominator_activity_year']) < 1900 or int(data['nominator_activity_year']) > 2024):
            flash('Year must be between 1900 and 2024.', 'err_nominees_nominator_activity_year')
            is_valid = False

        if len(data['nominator_activity_description']) < 3:
            flash('Description must be at least 10 characters long.', 'err_nominees_nominator_activity_description')
            is_valid = False

        if len(data['nominee_qualification']) < 3:
            flash('Nominee Description must be at least 10 characters long.', 'err_nominees_nominee_qualification')
            is_valid = False

        if len(data['nominee_activity_name']) < 3:
            flash('Activity name must be at least 3 characters.', 'err_nominees_nominee_activity_name')
            is_valid = False

        if data['nominee_activity_year'] and (int(data['nominee_activity_year']) < 1900 or int(data['nominee_activity_year']) > 2024):
            flash('Year must be between 1900 and 2024.', 'err_nominees_nominee_activity_year')
            is_valid = False

        if len(data['nominee_activity_description']) < 3:
            flash('Description must be at least 10 characters long.', 'err_nominees_nominee_activity_description')
            is_valid = False

        return is_valid
    
