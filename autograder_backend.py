from flask import Flask, request, render_template, jsonify
import json
from flask_cors import CORS
from flask_mysqldb import MySQL
import mysql.connector
import sys
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"]="mongodb+srv://gani:NZCEmb9FckXF3IIX@cluster0.kjbmlx8.mongodb.net/"



CORS(app)





@app.route('/students', methods=['GET', 'POST'])
def get_students():
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1', database='freshmen_immigration')
    cursor = cnx.cursor()

    # Execute the SQL query to retrieve the list of students
    query = ("SELECT * FROM students")
    cursor.execute(query)

    # Get the column names from cursor.description
    column_names = [desc[0] for desc in cursor.description]

    # Retrieve the results and create a list of students as dictionaries
    students = []
    for student_data in cursor:
        student = dict(zip(column_names, student_data))
        students.append(student)

    # Close the database connection
    cursor.close()
    cnx.close()

    # Return the list of students as JSON
    print(students)
    return jsonify(students)

@app.route('/tasks', methods=['GET', 'POST'])
def get_tasks():
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1', database='freshmen_immigration')
    cursor = cnx.cursor()

    # Execute the SQL query to retrieve the list of tasks
    query = ("SELECT * FROM tasks")
    cursor.execute(query)

    # Get the column names from cursor.description
    column_names = [desc[0] for desc in cursor.description]

    # Retrieve the results and create a list of tasks as dictionaries
    tasks = []
    for task_data in cursor:
        task = dict(zip(column_names, task_data))
        print(task)
        tasks.append(task)

    # Close the database connection
    cursor.close()
    cnx.close()

    # Return the list of tasks as JSON
    print(tasks)
    return jsonify(tasks)


@app.route('/update_students', methods=['POST'])
def update_students():

    request_data = request.json
    updated_students = request_data.get('students', [])
    task = request_data.get('task', {})
    print(task)
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1', database='freshmen_immigration')
    cursor = cnx.cursor()

    # Get the list of all fields in the students table
    query = "SHOW COLUMNS FROM students"
    cursor.execute(query)
    columns = [column[0] for column in cursor.fetchall()]

    # Update the student data in the database
    for updated_student in updated_students:
        student_id = updated_student['id']
        fields_to_update = {}
        for column in columns:
            if column in updated_student:
                fields_to_update[column] = updated_student[column]

        # Generate the dynamic SQL query to update the student data
        query = f"UPDATE students SET {', '.join([f'{field}=%s' for field in fields_to_update.keys()])} WHERE id=%s"
        cursor.execute(query, list(fields_to_update.values()) + [student_id])

    task_id = task.get('id')
    task_status = task.get('status')
    query = ("UPDATE tasks SET status=%s WHERE id=%s")
    cursor.execute(query, (task_status, task_id))


    cnx.commit()


    cursor.close()
    cnx.close()

    # Return a success message
    return jsonify({"message": "Students updated successfully"})


@app.route('/add-task', methods=['POST'])
def update_tasks():
    request_data = request.json
    





#running the app
if __name__ == '__main__':
    app.run(debug=True)

    
