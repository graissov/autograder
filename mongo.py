from flask import Flask, request, render_template, jsonify
import json
from flask_cors import CORS
from flask_mysqldb import MySQL
import mysql.connector
import sys
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"]="mongodb+srv://gani:NZCEmb9FckXF3IIX@cluster0.kjbmlx8.mongodb.net/"

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['autograder']
students_collection = db['students']
tasks_collection = db['tasks']
bonuses_collection = db['bonuses']

#Creating a connection cursor
CORS(app)


@app.route('/students', methods=['GET', 'POST'])
def get_students():
    # Retrieve the list of students from the MongoDB collection
    students = list(students_collection.find())
    print("mongo",students)
    # Remove the '_id' field from each student document
    for student in students:
        student.pop('_id')


    # Return the list of students as JSON
    return jsonify(students)



@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Retrieve the list of tasks from the MongoDB collection
    tasks = list(tasks_collection.find())

    # Remove the '_id' field from each task document
    for task in tasks:
        task.pop('_id')

    print("AGWsaodfijk",tasks)

    # Return the list of tasks as JSON
    return jsonify(tasks)




@app.route('/update_students', methods=['POST'])
def update_students():
    print("here")
    # Get the updated student data and the entire task object from the request's JSON payload
    request_data = request.json
    updated_students = request_data.get('students', [])
    task = request_data.get('task', {})
    print(task,"task")

    # Update the student data in the database
    for updated_student in updated_students:
        print("updated_student",  updated_student)
        student_id = updated_student['andrewid']
        fields_to_update = {}
        for field, value in updated_student.items():
            if field != 'andrewid':
                fields_to_update[field] = value

        # Update the student data in the MongoDB collection
        result = students_collection.update_one({"andrewid": student_id}, {"$set": fields_to_update})
        print(result)


    # Update the task status in the MongoDB collection
    task_id = task.get('id')
    task_status = task.get('status')
    tasks_collection.update_one({"id": task_id}, {"$set": {"status": task_status}})

    # Return a success message
    return jsonify({"message": "Students and task updated successfully"})

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        data = request.json
        print(data)
        task_name = data['name']
        
        # Add the new task to the tasks collection
        new_task = {
            'name': task_name,
            'status': 'ungraded',
            'deadline': data['deadline'],
            'weight': data['weight'],
        }
        tasks_collection = db['tasks']
        inserted_task = tasks_collection.insert_one(new_task)
        
        # Update the students collection
        students_collection = db['students']
        students_collection.update_many({}, {"$push": {"tasks": {task_name: None}}})
        
        return jsonify({"message": "New task added successfully", "task_id": str(inserted_task.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/get_bonuses', methods=['GET'])
def get_bonuses():
    try:
        bonuses = list(bonuses_collection.find({}, {"_id": 0}))  # Exclude the '_id' field

        # Return the list of bonuses as JSON
        return jsonify(bonuses)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/save_student_bonuses', methods=['POST'])
def save_student_bonuses():
    try:
        data = request.json
        student_identifier = data['studentIdentifier']
        selected_bonuses = data['selectedBonuses']

        # Find the student document by their identifier
        student = students_collection.find_one({'andrewid': student_identifier})

        if student:
            # Update the 'bonuses' field for the student with the selected bonuses
            students_collection.update_one(
                {'_id': student['_id']},
                {'$set': {'bonuses': selected_bonuses}}
            )

            # Calculate the bonus_total based on the selected bonuses
            bonus_total = sum(
                bonus['amount'] for bonus in selected_bonuses if 'amount' in bonus
            )

            # Calculate the new total_score for the student
            total_score = student['score'] + bonus_total

            # Update the 'total_score' field for the student
            students_collection.update_one(
                {'_id': student['_id']},
                {'$set': {'total_score': total_score}}
            )

            # Update the 'bonus_total' field for the student
            students_collection.update_one(
                {'_id': student['_id']},
                {'$set': {'bonus_total': bonus_total}}
            )

            return jsonify({"message": f"Bonuses saved for student with identifier {student_identifier}", "bonus_total": bonus_total})
        else:
            return jsonify({"error": f"Student with identifier {student_identifier} not found"})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run()
