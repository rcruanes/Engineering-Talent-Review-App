from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_nominee  # Import if you need to create relationships

DATABASE = "wdc_prototype_recommender_db_two"  # Adjust the database name as needed

class NomineesEducationHistory:
    def __init__(self, data):
        self.id = data['id']
        self.nominee_id = data['nominee_id']
        self.college_name = data['college_name']
        self.location = data['location']
        self.degree = data['degree']
        self.program = data['program']
        self.graduation_year = data['graduation_year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    def to_dict(self):
        return {
            'id': self.id,
            'college_name': self.college_name,
            'location': self.location,
            'degree': self.degree,
            'program': self.program,
            'graduation_year': self.graduation_year.strftime("%Y") if self.graduation_year else None
        }

    ############################################# CRUD FUNCTIONALITIES #############################################
    # Create
    @classmethod
    def create_education(cls, data):
        query = """
            INSERT INTO nominees_educations_histories
            (nominee_id, college_name, location, degree, program, graduation_year)
            VALUES (%(nominee_id)s, %(college_name)s, %(location)s, %(degree)s, %(program)s, %(graduation_year)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Read All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM nominees_educations_histories;"
        results = connectToMySQL(DATABASE).query_db(query)
        educations = []
        for item in results:
            educations.append(cls(item))
        return educations

    # Read One
    @classmethod
    def get_one_edu(cls, data):
        query = "SELECT * FROM nominees_educations_histories WHERE nominee_id = %(nominee_id)s;"
        # Ensure that `nominee_id` is extracted from the `data` dictionary
        results = connectToMySQL(DATABASE).query_db(query, {'nominee_id': data['nominee_id']})
        if not results:
            return []  # Return an empty list if the query failed or no records found
        educations = []
        for item in results:
            educations.append(cls(item))
        return educations

    # Update
    @classmethod
    def update_one_edu(cls, data):
        query = """
            UPDATE nominees_educations_histories
            SET college_name=%(college_name)s, location=%(location)s, degree=%(degree)s, program=%(program)s, graduation_year=%(graduation_year)s
            WHERE id = %(id)s;
        """
        try:
            connectToMySQL(DATABASE).query_db(query, data)
            return True
        except Exception as e:
            print("Failed to update education:", e)
            return False
        
    # Delete
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM nominees_educations_histories WHERE id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query, data)

    ############################################# VALIDATION #############################################
    @staticmethod
    def validate_education(education_data):
        is_valid = True
        # Add validation rules as needed
        if 'college_name' not in education_data or len(education_data['college_name']) < 2:
            is_valid = False
        # More validations can be added here
        return is_valid
