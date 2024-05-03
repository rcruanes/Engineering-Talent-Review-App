from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app import bcrypt # importing bycrpt
from flask import flash # importing flash


from flask_app.models import model_user # imported file for relationships query ( 1 to Many)


DATABASE = "wdc_talent_review_new_final_product_complete_db"

# Creating a class for nominee's and Nominatory Award Qualification
class AwardQualificationForm:
    def __init__(self, data):
        self.id = data['id']
        self.nominee_id = data['nominee_id']
        self.nominator_award_name = data['nominator_award_name']
        self.nominator_award_year = data['nominator_award_year']
        self.nominator_award_description = data['nominator_award_description']
        self.nominee_award_name = data['nominee_award_name']
        self.nominee_award_year = data['nominee_award_year']
        self.nominee_award_description = data['nominee_award_description']
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

    # Create an award qualification 
    @classmethod
    def create_award(cls, data):
        query = """
        INSERT INTO awards_qualifications_forms (nominee_id, nominator_award_name, nominator_award_year, nominator_award_description, 
        nominee_award_name, nominee_award_year, nominee_award_description) 
        VALUES (%(nominee_id)s, %(nominator_award_name)s, %(nominator_award_year)s, %(nominator_award_description)s, 
        %(nominee_award_name)s, %(nominee_award_year)s, %(nominee_award_description)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)



############################################# READ (DATA type Returned is list of dictionaries) #############################################
############################################# READ (DATA type Returned is list of dictionaries) #############################################
    # Retrieve a single award qualification record by nominee ID
    @classmethod
    def get_one_by_nominee_id(cls, data):
        query = "SELECT * FROM awards_qualifications_forms WHERE nominee_id = %(nominee_id)s LIMIT 1;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return None
    


############################################# UPDATE | EDIT ROUTES #############################################
############################################# UPDATE | EDIT ROUTES #############################################
    #Update One Form by ID 

    @classmethod
    def update_award_qualification(cls, data):
        query = """
        UPDATE awards_qualifications_forms 
        SET 
            nominator_award_name=%(nominator_award_name)s, 
            nominator_award_year=%(nominator_award_year)s, 
            nominator_award_description=%(nominator_award_description)s, 
            nominee_award_name=%(nominee_award_name)s, 
            nominee_award_year=%(nominee_award_year)s, 
            nominee_award_description=%(nominee_award_description)s, 
            updated_at=NOW() 
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)



############################################# DELETE (Returns No DATA) #############################################
############################################# DELETE (Returns No DATA) #############################################
# Check if Nominee Id exist(FOR NOMINATOR USE ONLY)
    @classmethod
    def check_exists_by_nominee_id(cls, data):
        query = "SELECT COUNT(*) AS count FROM awards_qualifications_forms WHERE nominee_id=%(nominee_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result[0]['count'] > 0


# Delete by Nominee Id(FOR NOMINATOR USE ONLY)
    @classmethod
    def delete_by_nominee_id(cls, data):
        query = "DELETE FROM awards_qualifications_forms WHERE nominee_id=%(nominee_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)






############################################# VALIDATION #############################################
############################################# VALIDATION #############################################

#VALIDATION FOR award Qualification FORM ##########################
    @staticmethod
    def validator_award_qualification(data):
        is_valid = True

        if len(data['nominator_award_name']) < 3:
            flash('award name must be at least 3 characters.', 'err_nominees_nominator_award_name')
            is_valid = False

        if data['nominator_award_year'] and (int(data['nominator_award_year']) < 1900 or int(data['nominator_award_year']) > 2024):
            flash('Year must be between 1900 and 2024.', 'err_nominees_nominator_award_year')
            is_valid = False

        if len(data['nominator_award_description']) < 3:
            flash('Description must be at least 10 characters long.', 'err_nominees_nominator_award_description')
            is_valid = False

        if len(data['nominee_award_name']) < 3:
            flash('award name must be at least 3 characters.', 'err_nominees_nominee_award_name')
            is_valid = False

        if data['nominee_award_year'] and (int(data['nominee_award_year']) < 1900 or int(data['nominee_award_year']) > 2024):
            flash('Year must be between 1900 and 2024.', 'err_nominees_nominee_award_year')
            is_valid = False

        if len(data['nominee_award_description']) < 3:
            flash('Description must be at least 10 characters long.', 'err_nominees_nominee_award_description')
            is_valid = False

        return is_valid