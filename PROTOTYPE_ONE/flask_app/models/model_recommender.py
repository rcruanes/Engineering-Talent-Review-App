from flask_app.config.mysqlconnection import connectToMySQL # Connecting to the DB

from flask_app.models import model_user, model_nominee, model_recommender #importing necessary model files for relationships



DATABASE = "wdc_talent_review_new_final_product_complete_db"

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





#Read All Nominees with Associated Recommender (DOESN'T need DATA passed in the parameter From JOINS (Relationship One to Many) )
    @classmethod
    def get_all_nominees_recommender(cls):
        # This query fetches the info from recommenders and nominees tables by joining them to the users.id
        query = """
        SELECT * 
        FROM 
            recommenders 
        JOIN 
            nominees ON recommenders.nominee_id = nominees.id
        JOIN 
            users ON recommenders.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        # print(results)


        #Need to extract all the information for the User and relabel the shared attribute names
        #Always relabel the id, created_at, and updated_at 
        if results:
            # Creating an empty list to append the results from the query which returns a list of dictionaries
            all_nominees_recommenders = []
            # for loop to pull the dictionaries for joined tables from results
            for result in results:
                # Creating an instance of Recommender
                recommender = cls(result) 
                # Creating instance of Nominee (Make sure to relable the shared attribute names with other table(s))
                nominee_data = {
                    "id": result["nominees.id"], 
                    "user_id": result["nominees.user_id"], 
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "department_name": result["department_name"],
                    "job_category": result["job_category"],
                    "email": result["email"],
                    "nominator_qualification": result["nominator_qualification"],
                    "created_at": result["nominees.created_at"],
                    "updated_at": result["nominees.updated_at"]
                }
                #Now Need to add the recommender onto the nominee
                # Make sure to IMPORT the JOINING table MODEL_FILE and NOT the Class!
                nominee = model_nominee.Nominee(nominee_data)


                #Now taking the Nominee instance and attach an attribute 
                #Instances are like dictionaries, if key doesn't exist it adds the key to the dictionaries
                    # so if the attribute doesn't exist then it'll add that attribute
                nominee.recommender = recommender
                # Now appending the nominee instance to the empty list 
                all_nominees_recommenders.append(nominee) # This will give back an Object of Nominee 
            return all_nominees_recommenders
        
    # returning False will give an error if the Nominator deleted the assosiated Nominee or hasn't created one yet
        return [] # You could iterate over an empty array so when there are no results it won't break 


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
    


# Read Method to retrieve all recommendations with associated recommender and nominee information
    @classmethod
    def get_all_recommendations_with_details(cls):
        # This query fetches the first and last names of the nominator, recommender, and nominee by joining the recommenders, nominees, and users tables 
        query = """
        SELECT
            nominees.id As nominee_id,
            recommenders.id AS recommender_id,
            u1.first_name AS nominator_first_name, 
            u1.last_name AS nominator_last_name, 
            u2.first_name AS recommender_first_name, 
            u2.last_name AS recommender_last_name,
            nominees.first_name AS nominee_first_name, 
            nominees.last_name AS nominee_last_name
        FROM recommenders
        JOIN nominees ON recommenders.nominee_id = nominees.id
        JOIN users u1 ON nominees.user_id = u1.id
        JOIN users u2 ON recommenders.user_id = u2.id
        """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        if results:
            nominee_data = []
            # for loop to pull the dictionaries for joined tables
            for result in results:
                nominee_data.append({
                    "nominee_id": result["nominee_id"],
                    "recommender_id": result["recommender_id"],
                    "nominator_first_name": result["nominator_first_name"],
                    "nominator_last_name": result["nominator_last_name"],
                    "recommender_first_name": result["recommender_first_name"],
                    "recommender_last_name": result["recommender_last_name"],
                    "nominee_first_name": result["nominee_first_name"],
                    "nominee_last_name": result["nominee_last_name"]
                })
            return nominee_data
        return []



#NEEDS TO BE ALTERED SINCE NEW SCHEMA WAS CREATED
# # Read Method to retrieve ONE recommendations and Nomination with associated recommender and nominee information
    @classmethod
    def get_recommendation_details_by_recommender_id(cls, recommender_id):
#NEEDS TO BE ALTERED SINCE NEW SCHEMA WAS CREATED
        query = """
        SELECT 
            nominees.id AS nominee_id,
            recommenders.id AS recommender_id,
            u1.first_name AS nominator_first_name, 
            u1.last_name AS nominator_last_name, 
            u2.first_name AS recommender_first_name, 
            u2.last_name AS recommender_last_name,
            nominees.first_name AS nominee_first_name, 
            nominees.last_name AS nominee_last_name,
            nominees.department_name AS nominee_department_name,
            nominees.job_category AS nominee_job_category,
            nominees.email AS nominee_email,
            nominees.nominator_qualification AS nominee_nominator_qualification,
            ind.ic_q1, ind.ic_q2, ind.ic_q3, ind.ic_q4, ind.ic_q5,
            pmc.prjmc_q1, pmc.prjmc_q2, pmc.prjmc_q3, pmc.prjmc_q4, pmc.prjmc_q5,
            plc.pplmc_q1, plc.pplmc_q2, plc.pplmc_q3, plc.pplmc_q4, plc.pplmc_q5,
            edu.college_name, edu.location, edu.degree, edu.program, edu.graduation_year,
            prof.employer, prof.title, prof.start_year, prof.end_year, prof.principal_job_function, prof.principal_responsibility,
            act.nominator_activity_name, act.nominator_activity_year , act.nominator_activity_description, act.nominee_qualification, 
            act.nominee_activity_name, act.nominee_activity_year, act.nominee_activity_description,
            aw.nominator_award_name, aw.nominator_award_year, aw.nominator_award_description, aw.nominee_award_name ,aw.nominee_award_year ,aw.nominee_award_description
        FROM recommenders
        JOIN nominees ON recommenders.nominee_id = nominees.id
        JOIN users u1 ON nominees.user_id = u1.id
        JOIN users u2 ON recommenders.user_id = u2.id
        LEFT JOIN individuals_contributions_forms ind ON recommenders.id = ind.recommender_id
        LEFT JOIN projects_managers_contributions_forms pmc ON recommenders.id = pmc.recommender_id
        LEFT JOIN peoples_managers_contributions_forms plc ON recommenders.id = plc.recommender_id
        LEFT JOIN nominees_educations_histories edu ON nominees.id = edu.nominee_id
        LEFT JOIN nominees_professionals_histories prof ON nominees.id = prof.nominee_id
        LEFT JOIN activities_qualifications_forms act ON nominees.id = act.nominee_id
        LEFT JOIN awards_qualifications_forms aw ON nominees.id = aw.nominee_id
        WHERE recommenders.id = %(recommender_id)s
        """
        results = connectToMySQL(DATABASE).query_db(query, (recommender_id))
        if results:
            # Assuming there's only one row of results because recommender_id should be unique
            result = results[0]
            return {
                "nominee_id": result["nominee_id"],
                "recommender_id": result["recommender_id"],
                "nominator_first_name": result["nominator_first_name"],
                "nominator_last_name": result["nominator_last_name"],
                "recommender_first_name": result["recommender_first_name"],
                "recommender_last_name": result["recommender_last_name"],
                "nominee_first_name": result["nominee_first_name"],
                "nominee_last_name": result["nominee_last_name"],
                "nominee_department_name":result["nominee_department_name"],
                "nominee_job_category":result["nominee_job_category"],
                "nominee_email":result["nominee_email"],
                "nominee_nominator_qualification":result["nominee_nominator_qualification"],
                "ic_q1": result.get("ic_q1", ""),
                "ic_q2": result.get("ic_q2", ""),
                "ic_q3": result.get("ic_q3", ""),
                "ic_q4": result.get("ic_q4", ""),
                "ic_q5": result.get("ic_q5", ""),
                "prjmc_q1": result.get("prjmc_q1", ""),
                "prjmc_q2": result.get("prjmc_q2", ""),
                "prjmc_q3": result.get("prjmc_q3", ""),
                "prjmc_q4": result.get("prjmc_q4", ""),
                "prjmc_q5": result.get("prjmc_q5", ""),
                "pplmc_q1": result.get("pplmc_q1", ""),
                "pplmc_q2": result.get("pplmc_q2", ""),
                "pplmc_q3": result.get("pplmc_q3", ""),
                "pplmc_q4": result.get("pplmc_q4", ""),
                "pplmc_q5": result.get("pplmc_q5", ""),
                # Additional fields
                "education": {
                    "college_name": result.get("college_name", ""),
                    "location": result.get("location", ""),
                    "degree": result.get("degree", ""),
                    "program": result.get("program", ""),
                    "graduation_year": result.get("graduation_year", "")
                },
                "professional_history": {
                    "employer": result.get("employer", ""),
                    "title": result.get("title", ""),
                    "start_year": result.get("start_year", ""),
                    "end_year": result.get("end_year", ""),
                    "principal_job_function": result.get("principal_job_function", ""),
                    "principal_responsibility": result.get("principal_responsibility", "")
                },
                "activities": {
                    "nominator_activity_name": result.get("nominator_activity_name", ""),
                    "nominator_activity_year": result.get("nominator_activity_year", ""),
                    "nominator_activity_description": result.get("nominator_activity_description", ""),
                    "nominee_qualification": result.get("nominee_qualification", ""),
                    "nominee_activity_name": result.get("nominee_activity_name", ""),
                    "nominee_activity_year": result.get("nominee_activity_year", ""),
                    "nominee_activity_description": result.get("nominee_activity_description", ""),
                },
                "awards": {
                    "nominator_award_name": result.get("nominator_award_year", ""),
                    "nominator_award_year": result.get("nominator_award_year", ""),
                    "nominator_award_description": result.get("nominator_award_description", ""),
                    "nominee_award_name": result.get("nominee_award_name", ""),
                    "nominee_award_year": result.get("nominee_award_year", ""),
                    "nominee_award_description": result.get("nominee_award_description", ""),
                }
            }
        return None  # If no results







############################################# UPDATE (Returns No DATA but NEEDS it for PARAMETERS) #############################################
    #Update Nominee by ID 
    @classmethod
    def update_one_recomendation(cls, data):
        query = "UPDATE recommenders SET work_contributions=%(work_contributions)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)





############################################# DELETE (Returns No DATA but NEEDS it for PARAMETERS) #############################################
############################################# DELETE (Returns No DATA but NEEDS it for PARAMETERS) #############################################
# Check if Nominee Id exist (FOR NOMINATOR)
    @classmethod
    def check_exists_by_nominee_id(cls, data):
        query = "SELECT COUNT(*) AS count FROM recommenders WHERE nominee_id=%(nominee_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result[0]['count'] > 0

# Delete by Nominee Id (FOR NOMINATOR)
    @classmethod
    def delete_by_nominee_id(cls, data):
        query = "DELETE FROM recommenders WHERE nominee_id=%(nominee_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    


# Delete (id) (FOR RECOMMENDER)
    @classmethod
    def delete_one_recomendation(cls, data):
        query = "DELETE FROM recommenders WHERE id=%(id)s;"
        # DELETING it doesn't return anything back if it's successful
        return connectToMySQL(DATABASE).query_db(query, data)




############################################# VALIDATION #############################################
############################################# VALIDATION #############################################
# Need to Add validation for the Work_contributions here.






