from flask_app.config.mysqlconnection import connectToMySQL # Connecting to the DB

from flask_app.models import model_user, model_nominee #importing necessary model files for relationships



DATABASE = "wdc_prototype_recommender_db_two"

#Still Need to add the correct attributes, foreign keys for the Tables associated with this model and any other ones for User Role Recommender recommendation forms based on Nominee's work contribution
# Need to Give the Recommender User Role multiple selection options for Nominee’s work contribution such as Individual Contributor, Project Manager, and People Manager
class Recommender:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.nominee_id = data['nominee_id']
        self.work_contributions = data['work_contributions'] # SET DATA with three options 1-3 Individual Contributor, Project Manager, and People Manager
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        


############################################# CRUD FUNCTIONALITIES #############################################
   ############################## Consistent Naming Convention  #######################
                                    # create, 
                                    # get_all, get_many, get_one, 
                                    # update_one, update_many, 
                                    # delete_one, delete_many


############################################# CREATE / Insert (Returns an int as which is Id) #############################################
    #Create Recommendation Form 
    @classmethod
    # Inserting all the attributes needed for the RecommenderForm attributes to choose work_contributions
    # Create method retuns back an Int of the id containing the object / instance
    def create_recommendation(cls, data): # takes in two parametes cls, and data
# *************************************Converting a List to String*********************************************************************************
        # Converting a List to String in order for Recommender to select multiple work contributions for Nominee 
        # Since work_contributions attribute is a SET Data Value from our database which is seperated by commas 
        # the original values from python which are in a LIST needs to be converted to a string
        # First get and define the list of data 
        work_contributions = data.get('work_contributions')
        # by using coma seperated values to accept multiple selections just as in defalult values from database     
        work_contributions_str = ','.join(work_contributions) #.join method allows to concatenate any number of strings
        # update the data dictionary with converted string
        data['work_contributions'] = work_contributions_str

        # Insert Query to save data from form and into database
        query = "INSERT INTO recommenders ( user_id, nominee_id, work_contributions) VALUES ( %(user_id)s, %(nominee_id)s, %(work_contributions)s );"
        # store the returned info using a Variable
        result = connectToMySQL(DATABASE).query_db(query, data)
        # retuns an id so make sure to use get method to retrieve the actual data for the object / instance
        return result



############################################# READ (DATA type Returned is list of dictionaries) #############################################
    #Read All the Recommendations
    @classmethod
    def get_all_recommendations(cls): # Takes in 1 parameter
        # Using Select Query to retrieve all the recommendations from the database
        query = "SELECT * FROM recommenders;"
        # assign the values from db to a variable
        results = connectToMySQL(DATABASE).query_db(query)
        # check to see if there's any results
        if results:
            #Create an empty list to save the retured objects / instances
            all_recommendations = []
            # for loop to append all the objects from results
            for recommendation in results:
                all_recommendations.append(cls(recommendation))
            return all_recommendations # retuns a list of objects
        
        return False

############################################# READ (DATA type Returned is list of dictionaries) #############################################
    #Read One Recommender
    @classmethod
    def get_one_recommender(cls, data):
        #Query to Select One by Id
        query = "SELECT * FROM recommenders WHERE id = %(id)s;"
        #Store the returned data list 
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            # Return the first index in the list
            return cls(results[0])
        return False

    @classmethod
    def get_recommendation_details_with_name(cls, nominee_id):  
        query = """
        SELECT r.*, u.first_name, u.last_name
        FROM recommenders r
        JOIN users u ON r.user_id = u.id
        WHERE r.nominee_id = %(nominee_id)s;
        """
        data = {'nominee_id': nominee_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        return [cls(result) for result in results] if results else []


