from flask_app.config.mysqlconnection import connectToMySQL # Connecting to the DB

from flask_app.models import model_user, model_nominee, model_recommender #importing necessary model files for relationships


DATABASE = "wdc_talent_review_new_final_product_complete_db"
class ReviewCommittee:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.nominee_id = data['nominee_id']
        self.rank_individual_contribution = data['rank_individual_contribution'] #Int
        self.rank_project_lead_contribution = data['rank_project_lead_contribution'] #Int
        self.rank_people_manager_contribution = data['rank_people_manager_contribution'] #Int
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
    def create_review(cls, data): # takes in two parametes cls, and data

        # Insert Query to save data from form and into database
        query = "INSERT INTO reviews_committees ( user_id, nominee_id, rank_individual_contribution, rank_project_lead_contribution, rank_people_manager_contribution) VALUES ( %(user_id)s, %(nominee_id)s, %(rank_individual_contribution)s, %(rank_project_lead_contribution)s, %(rank_people_manager_contribution)s );"
        # store the returned info using a Variable
        result = connectToMySQL(DATABASE).query_db(query, data)
        # retuns an id so make sure to use get method to retrieve the actual data for the object / instance
        return result




############################################# READ (DATA type Returned is list of dictionaries) #############################################
    #Read All the Recommendations
    @classmethod
    def get_all_reviews(cls): # Takes in 1 parameter
        # Using Select Query to retrieve all the recommendations from the database
        query = "SELECT * FROM reviews_committees;"
        # assign the values from db to a variable
        results = connectToMySQL(DATABASE).query_db(query)
        # check to see if there's any results
        if results:
            #Create an empty list to save the retured objects / instances
            all_reviews = []
            # for loop to append all the objects from results
            for review in results:
                all_reviews.append(cls(review))
            return all_reviews # retuns a list of objects
        
        return []
