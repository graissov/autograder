from flask import Flask, request, render_template, jsonify
import json
from flask_cors import CORS
from flask_mysqldb import MySQL
import mysql.connector
import sys
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"]="mongodb+srv://gani:NZCEmb9FckXF3IIX@cluster0.kjbmlx8.mongodb.net/"

client = MongoClient('mongodb://localhost:27017/')
db = client['autograder']
students_collection = db['students']
tasks_collection = db['tasks']
bonuses_collection = db['bonuses']

CORS(app)


@app.route('/students', methods=['GET', 'POST'])
def get_students():
    students = list(students_collection.find())
    print("mongo",students)
    for student in students:
        student.pop('_id')


    return jsonify(students)



@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(tasks_collection.find())

    for task in tasks:
        task.pop('_id')

    print("AGWsaodfijk",tasks)

    return jsonify(tasks)




@app.route('/update_students', methods=['POST'])
def update_students():
    print("here")
    request_data = request.json
    updated_students = request_data.get('students', [])
    task = request_data.get('task', {})
    print(task,"task")

    for updated_student in updated_students:
        print("updated_student",  updated_student)
        student_id = updated_student['andrewid']
        fields_to_update = {}
        for field, value in updated_student.items():
            if field != 'andrewid':
                fields_to_update[field] = value

        result = students_collection.update_one({"andrewid": student_id}, {"$set": fields_to_update})
        print(result)


    task_id = task.get('id')
    task_status = task.get('status')
    tasks_collection.update_one({"id": task_id}, {"$set": {"status": task_status}})

    return jsonify({"message": "Students and task updated successfully"})

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        data = request.json
        print(data)
        task_name = data['name']
        
        new_task = {
            'name': task_name,
            'status': 'ungraded',
            'deadline': data['deadline'],
            'weight': data['weight'],
        }
        tasks_collection = db['tasks']
        inserted_task = tasks_collection.insert_one(new_task)
        
        students_collection = db['students']
        students_collection.update_many({}, {"$push": {"tasks": {task_name: None}}})
        
        return jsonify({"message": "New task added successfully", "task_id": str(inserted_task.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/get_bonuses', methods=['GET'])
def get_bonuses():
    try:
        bonuses = list(bonuses_collection.find({}, {"_id": 0})) 

        return jsonify(bonuses)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/save_student_bonuses', methods=['POST'])
def save_student_bonuses():
    try:
        data = request.json
        student_identifier = data['studentIdentifier']
        selected_bonuses = data['selectedBonuses']

        student = students_collection.find_one({'andrewid': student_identifier})

        if student:
            students_collection.update_one(
                {'_id': student['_id']},
                {'$set': {'bonuses': selected_bonuses}}
            )

            bonus_total = sum(
                bonus['amount'] for bonus in selected_bonuses if 'amount' in bonus
            )

            total_score = student['score'] + bonus_total

            students_collection.update_one(
                {'_id': student['_id']},
                {'$set': {'total_score': total_score}}
            )

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
