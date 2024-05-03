
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app import bcrypt # importing bycrpt
from flask import flash # importing flash
import re # importing regax

from flask_app.models import model_user # imported file for relationships query ( 1 to Many)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


DATABASE = "wdc_talent_review_new_final_product_complete_db"
# Creating a class Nominee with a list of dictionaries(attributes)
class Nominee:
    def __init__( self , data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.department_name = data['department_name']
        self.job_category = data['job_category']
        self.email = data['email']
        self.nominator_qualification = data['nominator_qualification'] #text
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # Make sure that full_name formatted as a method call with ()
        self.full_name = f"{self.first_name.capitalize()} {self.last_name.capitalize()}"


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
                    # left side the key is the name used to access through jinja2 and right side is value from data
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



    #READ Nominees FULL INFORMATION BY NOMINEE_ID FOR REVIEW COMMITTEE
    @classmethod
    def get_nomiees_full_review_by_nominee_id(cls, nominee_id):
        query = """
        SELECT 
            n.id AS nominee_id,
            n.first_name AS nominee_first_name,
            n.last_name AS nominee_last_name,
            n.email AS nominee_email,
            n.department_name AS nominee_department_name,
            n.job_category AS nominee_job_category,
            n.nominator_qualification,
            edu.college_name, edu.location, edu.degree, edu.program, edu.graduation_year,
            prof.employer, prof.title, prof.start_year, prof.end_year, prof.principal_job_function, prof.principal_responsibility,
            act.nominator_activity_name, act.nominator_activity_year, act.nominator_activity_description, 
            act.nominee_activity_name, act.nominee_activity_year, act.nominee_activity_description,
            aw.nominator_award_name, aw.nominator_award_year, aw.nominator_award_description, 
            aw.nominee_award_name, aw.nominee_award_year, aw.nominee_award_description,
            rec.work_contributions,
            ind.ic_q1 AS individual_q1, ind.ic_q2 AS individual_q2, ind.ic_q3 AS individual_q3, ind.ic_q4 AS individual_q4, ind.ic_q5 AS individual_q5,
            pmc.prjmc_q1 AS project_q1, pmc.prjmc_q2 AS project_q2, pmc.prjmc_q3 AS project_q3, pmc.prjmc_q4 AS project_q4, pmc.prjmc_q5 AS project_q5,
            plc.pplmc_q1 AS people_q1, plc.pplmc_q2 AS people_q2, plc.pplmc_q3 AS people_q3, plc.pplmc_q4 AS people_q4, plc.pplmc_q5 AS people_q5,
            u.first_name AS nominator_first_name, u.last_name AS nominator_last_name,
            u2.first_name AS recommender_first_name, u2.last_name AS recommender_last_name
        FROM nominees n
        JOIN users u ON n.user_id = u.id
        LEFT JOIN nominees_educations_histories edu ON n.id = edu.nominee_id
        LEFT JOIN nominees_professionals_histories prof ON n.id = prof.nominee_id
        LEFT JOIN activities_qualifications_forms act ON n.id = act.nominee_id
        LEFT JOIN awards_qualifications_forms aw ON n.id = aw.nominee_id
        LEFT JOIN recommenders rec ON n.id = rec.nominee_id
        LEFT JOIN users u2 ON rec.user_id = u2.id
        LEFT JOIN individuals_contributions_forms ind ON rec.id = ind.recommender_id
        LEFT JOIN projects_managers_contributions_forms pmc ON rec.id = pmc.recommender_id
        LEFT JOIN peoples_managers_contributions_forms plc ON rec.id = plc.recommender_id
        WHERE n.id = %(nominee_id)s;
        """
        data = {"nominee_id": nominee_id}
        try:
            results = connectToMySQL(DATABASE).query_db(query, data)
            if results:
                return results[0]  # Return the first result if expecting only one row per nominee
            else:
                return None  # Return None if no results found
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Return None or handle the error as appropriate











############################################# UPDATE (Returns No DATA) #############################################
    #Update Nominee by ID 
    @classmethod
    def update_one_nominee(cls, data):
        query = "UPDATE nominees SET first_name=%(first_name)s, last_name=%(last_name)s, department_name = %(department_name)s, job_category=%(job_category)s,email=%(email)s, nominator_qualification=%(nominator_qualification)s, updated_at=NOW() WHERE id = %(id)s;" 
        return connectToMySQL(DATABASE).query_db(query, data)


############################################# DELETE (Returns No DATA) #############################################
############################################# DELETE (Returns No DATA) #############################################
# Delete a Nominee 
    @classmethod
    def delete_one_nominee(cls, data):
        query = "DELETE FROM nominees WHERE id=%(id)s;"
        # if we're DELETING it doesn't return anything back if it's successful
        return connectToMySQL(DATABASE).query_db(query, data)



############################################# VALIDATION #############################################
############################################# VALIDATION #############################################

#VALIDATION FOR NOMINEE FORM ##########################
    @staticmethod
    def validator_nominee_info(data):
        is_valid = True

        if len(data['first_name']) < 3:
            flash('field is required', 'err_nominees_first_name_nominator')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('field is required', 'err_nominees_last_name_nominator')
            is_valid = False
        if len(data['department_name']) < 3:
            flash('field is required', 'err_nominees_department_name_nominator')
            is_valid = False
        if len(data['job_category']) < 3:
            flash('field is required', 'err_nominees_job_category_nominator')
            is_valid = False
        if len(data['email']) < 1:
            flash('field is required', 'err_nominees_email_nominator')
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!",'err_nominees_email_nominator')
            is_valid = False

        if len(data['nominator_qualification']) < 3:
            flash('field is required', 'err_nominees_nominator_qualification_nominator')
            is_valid = False

        return is_valid
    
