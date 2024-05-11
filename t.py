from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['autograder']
students_collection = db['tasks']

new_student = {
    "id":2,
    "name": "task2",
    "status": "graded",
}

# Insert the new student document into the collection
result = students_collection.insert_one(new_student)

# Print the inserted document's ID
print("Inserted ID:", result.inserted_id)
