from flask_app.config.mysqlconnection import connectToMySQL # Connecting to the DB

from flask_app.models import model_user, model_nominee, model_recommender #importing necessary model files for relationships


DATABASE = "wdc_prototype_recommender_db_two"

# Individual Work contribution Class filled out by the Recommender
class IndividualContributionForm:
    def __init__(self, data):
        self.id = data['id']
        self.recommender_id = data['recommender_id']
        self.a = data['ic_q1']
        self.b = data['ic_q2']
        self.c = data['ic_q3']
        self.d = data['ic_q4']
        self.f = data['ic_q5']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']




############################################# CRUD FUNCTIONALITIES #############################################
   ############################## Consistent Naming Convention  #######################
                                    # create, 
                                    # get_all, get_many, get_one, 
                                    # update_one, update_many, 
                                    # delete_one, delete_many


############################################# CREATE / Insert (Returns an int as which is Id) #############################################
# Create Individual Work contribution Form
    @classmethod
    def create_individual_contribution(cls, data):
        # Insert query to save data from form to database which returns the Id number of the row inserted 
        query = "INSERT INTO individuals_questions (recommender_id, ic_q1, ic_q2, ic_q3, ic_q4, ic_q5) VALUES ( %(recommender_id)s,%(ic_q1)s,%(ic_q2)s,%(ic_q3)s,%(ic_q4)s,%(ic_q5)s );"
        # explicitly storing the returned id of the inserted value 
        individual_contribution_id = connectToMySQL(DATABASE).query_db(query, data)
        # retuns an id so make sure to use get method to retrieve the actual data for the object / instance
        return individual_contribution_id
    





############################################# READ (DATA type Returned is list of dictionaries) #############################################
    #Read One 


    #Read All the Individual Question Answers
    @classmethod
    def get_all_individual_contributions(cls): # read all doesn't need data passed in
        # Using Select * query to retrieve all the individual question answers
        query = "SELECT * FROM individuals_questions;"
        # Need to assign the values from the database to a variable
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            # Create an empty list to store the list of objects / instances
            all_individual_answers = []
            # Now append the list of objects/ instances from cls
            # Using for loop to append
            for individual_question in results:
                all_individual_answers.append(cls(individual_question))
            return all_individual_answers # returns a list of objects
        return False



    # READ ALL of the Individual Work Contribution Answers from Associated Recommender
    @classmethod
    def get_all_individuals_contributions_from_recommender(cls): # read all doesn't need data passed in
        # Query to Join the Indivisuals_questions table (Primary - leftside) with the Recommenders table (Secondary - rightside)
        # to get the accsiated Recommenders with the form
        # This query returns data from the database as a LIST OF DICTIONARIES
        # query = "SELECT * FROM recommenders JOIN individuals_questions on recommenders.id = individuals_questions.recommender_id;"
        query = "SELECT * FROM individuals_questions JOIN recommenders on recommenders.id = individuals_questions.recommender_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        # print(results)

        # check for results
        if results:
            # Create an empty list to append the returned objects later
            # This is a list of all the answers for the IC questions by the recommenders
            all_individuals_contributions_from_recommenders = []

            # For loop to iterate over returned data from the database  
            for dict in results: #results contains the list of dictionaries objects / instances
                nominee_individual_contribution = cls(dict) # Creating an instance of Individual Question
                
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
                nominee_individual_contribution.recommender = recommender

                # Now append the individual_question instance to the empty list
                all_individuals_contributions_from_recommenders.append(nominee_individual_contribution)

            # Returns list of objects after the loop completes
            return all_individuals_contributions_from_recommenders
        
        # Returning an empty array / list when result is False so the code / website does't break
        return []
    
    @classmethod
    def get_nominee_contributions(cls, nominee_id):
        query = """
        SELECT 
            r.*, 
            i.ic_q1, i.ic_q2, i.ic_q3, i.ic_q4, i.ic_q5,
            u.first_name, u.last_name  # Ensure these fields are selected
        FROM 
            recommenders r
        JOIN 
            individuals_questions i ON r.id = i.recommender_id
        JOIN 
            users u ON r.user_id = u.id  # Join with users to get name information
        WHERE 
            r.nominee_id = %(nominee_id)s;
        """
        data = {'nominee_id': nominee_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return results
        return []






