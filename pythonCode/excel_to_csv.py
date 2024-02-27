import csv
import sqlite3

def csv_to_txt(csv_file, txt_file, sql_query, db_path="your_database.db"):
    """
    Args:
        csv_file (str): Name of the CSV file to write formatted data to (unused).
        txt_file (str): Name of the text file to write formatted data to.
        sql_query (str): SQL query to fetch data from the database.
        db_path (str, optional): Path to the SQLite database file. Defaults to "your_database.db".
    """

    # This connects to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # This is where the query is executed
    cursor.execute(sql_query)

    # Takes in data and writes it to a file
    with open(txt_file, 'w') as txt_file:
        for row in cursor.fetchall():
            formatted_row = ["{} |".format(col.strip()) for col in row]
            stripped_info = " ".join(formatted_row) + "\n\n"
            txt_file.write(stripped_info)

    # Quits database
    conn.close()

# Example usage (replace with your desired SQL query and filename)
sql_query = "SELECT u_lastname, u_firstname, u_email, e_schoolname, p_employer FROM users JOIN education ON users.u_id = education.user_id JOIN profHistory ON users.u_id = profHistory.user_id"
csv_to_txt("output.csv", "output.txt", sql_query, "your_database.db")

print("Data written to text file:", "output.txt")

