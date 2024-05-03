from flask_app.config.mysqlconnection import connectToMySQL # Connecting to the DB
from flask import flash # importing flash
from flask_app.models import model_user, model_nominee, model_recommender #importing necessary model files for relationships


DATABASE = "wdc_talent_review_new_final_product_complete_db"

# People Manager Contribution Class filled out by the Recommender
class PeopleManagerContributionForm:
    def __init__(self, data):
        self.id = data['id']
        self.recommender_id = data['recommender_id']
        self.pplmc_q1 = data['pplmc_q1']
        self.pplmc_q2 = data['pplmc_q2']
        self.pplmc_q3 = data['pplmc_q3']
        self.pplmc_q4 = data['pplmc_q4']
        self.pplmc_q5 = data['pplmc_q5']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']




############################################# CRUD FUNCTIONALITIES #############################################
   ############################## Consistent Naming Convention  #######################
                                    # create, 
                                    # get_all, get_many, get_one, 
                                    # update_one, update_many, 
                                    # delete_one, delete_many


############################################# CREATE / Insert Takes in Argument (cls, data) and Returns (an int as which is Id) #############################################
# Create People Manager contribution Form
    @classmethod
    def create_people_manager_contribution(cls,data): # takes in two arguments cls and data 
        # Insert Query to save data from form to database 
        query = " INSERT INTO peoples_managers_contributions_forms (recommender_id, pplmc_q1, pplmc_q2, pplmc_q3, pplmc_q4, pplmc_q5) VALUES ( %(recommender_id)s,%(pplmc_q1)s,%(pplmc_q2)s,%(pplmc_q3)s,%(pplmc_q4)s,%(pplmc_q5)s ); "
        # explicitly storing the returned id of the inserted value 
        people_manager_contribution_id = connectToMySQL(DATABASE).query_db(query, data)
        # retuns an id so make sure to use get method to retrieve the actual data for the object / instance
        return people_manager_contribution_id




############################################# READ (DATA type Returned is list of dictionaries) #############################################
############################################# READ (DATA type Returned is list of dictionaries) #############################################
    #Read One by Recommender ID
    @classmethod
    def get_one_by_recommender_id(cls, data):
        #query to Select all from recommender id
        query = "SELECT * FROM peoples_managers_contributions_forms WHERE recommender_id = %(recommender_id)s LIMIT 1;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            print('Get Answers By Recommender ID From People Contribution', results)
            return cls(results[0])
        return None



    # READ ALL of the People Manger Contribution Answers from Associated Recommender
    @classmethod
    def get_all_peoples_managers_contributions_from_recommender(cls): # read all doesn't need data passed in
        # Query to Join the peoples_managers_contributions_forms table (Primary - leftside) with the Recommenders table (Secondary - rightside)
        # to get the accsiated Recommenders with the form
        # This query returns data from the database as a LIST OF DICTIONARIES
        # query = "SELECT * FROM recommenders JOIN peoples_managers_contributions_forms on recommenders.id = individuals_questions.recommender_id;"
        query = "SELECT * FROM peoples_managers_contributions_forms JOIN recommenders on recommenders.id = peoples_managers_contributions_forms.recommender_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        # print(results)

        # check for results
        if results:
            # Create an empty list to append the returned objects later
            # This is a list of all the answers for the peoples_managers_contributions_forms questions by the recommenders
            all_peoples_managers_contributions_from_recommender = []

            # For loop to iterate over returned data from the database  
            for dict in results: #results contains the list of dictionaries objects / instances
                nominee_people_contribution = cls(dict) # Creating an instance of People Question
                
                # Now Creating an instance of Recommender to relable any shared attribute's name between the JOINED tables, individuals_questions & recommenders
                # MUST relables are: id, created_at(), and updated_at() 
                # Relabel names should be plural following the table naming convention from MySQL
                recommender_data = {
                    'id': dict['recommenders.id'],
                    'nominee_id': dict['nominee_id'],
                    'user_id' : dict['user_id'],
                    'work_contributions': dict['work_contributions'],
                    'created_at': dict['recommenders.created_at'],
                    'updated_at': dict['recommenders.updated_at'],
                }
                # Now need to add the Recommender onto the Individual question
                # Make sure to IMPORT the JOINING table model_FILE and NOT the Class to avoid Ciruclar Imorts
                recommender = model_recommender.Recommender(recommender_data) 

                # Using the created individual_question instance we can now attach / call / add an attribute
                # Instances are like dictionaries if the key doesn't exist then it'll add key to the dictionary
                # In this case if the attribute doesn't exist then it'll add that attribute
                nominee_people_contribution.recommender = recommender

                # Now append the individual_question instance to the empty list
                all_peoples_managers_contributions_from_recommender.append(nominee_people_contribution)

            # Returns list of objects after the loop completes
            return all_peoples_managers_contributions_from_recommender
        
        # Returning an empty array / list when result is False so the code / website does't break
        return []






############################################# UPDATE (Returns No DATA) #############################################
    #Update One Form by ID 
    @classmethod
    def update_one_people_manager_contribution_form(cls, data):
        query = "UPDATE peoples_managers_contributions_forms SET pplmc_q1=%(pplmc_q1)s, pplmc_q2=%(pplmc_q2)s, pplmc_q3=%(pplmc_q3)s, pplmc_q4=%(pplmc_q4)s, pplmc_q5=%(pplmc_q5)s, updated_at=NOW() WHERE id = %(id)s;" 
        return connectToMySQL(DATABASE).query_db(query, data)





############################################# DELETE (Returns No DATA but NEEDS it for PARAMETERS) #############################################
############################################# DELETE (Returns No DATA but NEEDS it for PARAMETERS) #############################################
# Check if Recommender Id exist
    @classmethod
    def check_exists_by_recommender_id(cls, data):
        query = "SELECT COUNT(*) AS count FROM peoples_managers_contributions_forms WHERE recommender_id=%(recommender_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result[0]['count'] > 0

# Delete by Recommender Id
    @classmethod
    def delete_by_recommender_id(cls, data):
        query = "DELETE FROM peoples_managers_contributions_forms WHERE recommender_id=%(recommender_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    


# Delete by (id) 
    @classmethod
    def delete_one_recomendation(cls, data):
        query = "DELETE FROM peoples_managers_contributions_forms WHERE id=%(id)s;"
        # DELETING it doesn't return anything back if it's successful
        return connectToMySQL(DATABASE).query_db(query, data)






############################################# VALIDATION #############################################

#VALIDATION FOR Recommender FORM ##########################
    @staticmethod
    def validator_people_manager_contribution_info(data):
        is_valid = True
        if len(data['pplmc_q1']) < 1:
            flash('field is required', 'err_nominees_pplmc_q1_recommender')
            is_valid = False
        return is_valid
