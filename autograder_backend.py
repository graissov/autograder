from flask import Flask, request, render_template, jsonify
import json
from flask_cors import CORS
from flask_mysqldb import MySQL
import mysql.connector
import sys

app = Flask(__name__)

#Creating a connection cursor
CORS(app)

@app.route('/areas', methods=['GET', 'POST'])
def get_areas():
    # connect to the database
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1', database='concept_maps')
    cursor = cnx.cursor()

    # execute the SQL query to retrieve the list of areas
    query = ("SELECT DISTINCT area FROM objects")
    cursor.execute(query)

    # retrieve the results and create a list of areas
    areas = [area[0] for area in cursor]

    # close the database connection
    cursor.close()
    cnx.close()

#change the code below to return students with id, name, score from the database freshmen_immigration
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
    # Get the updated student data from the request's JSON payload
    # Get the updated student data and the entire task object from the request's JSON payload
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

    # Commit the changes to the database
    cnx.commit()

    # Close the database connection
    cursor.close()
    cnx.close()

    # Return a success message
    return jsonify({"message": "Students updated successfully"})


def get_objects():

    # connect to the database
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1', database='concept_maps')
    cursor = cnx.cursor()


    # execute the SQL query to retrieve the list of objects for the selected area
    query = ("SELECT * FROM objects")
    cursor.execute(query)
    print("here is the curosr:")
    print(cursor)

    # retrieve the results and create a list of objects
    objects = []
    for (id, parent_id, title, areas, related_concepts) in cursor:
        related_concepts = related_concepts.split(",")
        obj = {"id": id, "parent_id": parent_id, "title": title, "info": "some info", "related_concepts":related_concepts}
        objects.append(obj)

    # close the database connection
    cursor.close()
    cnx.close()

    # return the list of objects as JSON
    return jsonify(objects)


@app.route('/submit', methods=['POST'])
def submit():
    # ADD uniqueness check
    input1 = request.form['input1']
    input3 = request.form.getlist('selected_options[]')
        

    print("hello",",".join(input3))

    # connect to the database
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1', database='concept_maps')
    cursor = cnx.cursor()
    for concept in input3:
        # Execute the select query
        select_query = "SELECT related_concepts FROM objects WHERE title = '"+concept+"'"
        cursor.execute(select_query)

        # Retrieve the result
        result = cursor.fetchone()

        # Extract the related_concepts value
        related_concepts = result[0] if result else None
        print("Related Concepts:", related_concepts)
        if related_concepts == "":
            related_concepts = input1
        else:
            related_concepts = related_concepts + "," + input1

        # Execute the update query
        update_query = "UPDATE objects SET related_concepts = '"+related_concepts +"' WHERE title = '"+concept+"'"
        cursor.execute(update_query)
        cnx.commit()




    insert_query = "INSERT INTO objects (title, related_concepts) VALUES (%s, %s)"
    values = (input1,",".join(input3),)
    cursor.execute(insert_query, values)
    cnx.commit()
    cnx.close()

    return 'Form submitted successfully!'


# Function to retrieve unique titles from the objects table
def get_unique_titles():
    cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1', database='concept_maps')
    cursor = cnx.cursor()
    print('Hello world!', file=sys.stderr)

    query = "SELECT DISTINCT title FROM objects"
    cursor.execute(query)
    result = [title[0] for title in cursor.fetchall()]

    cnx.close()

    return result

@app.route('/titles', methods=['GET'])
def titles():
    unique_titles = get_unique_titles()
    return jsonify(unique_titles)


#running the app
if __name__ == '__main__':
    app.run(debug=True)

    