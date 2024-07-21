import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
def login(username, password, preferred_name):
    json_path = "testing-project-2f261-firebase-adminsdk-boek8-6945570a63.json"
    cred = credentials.Certificate(json_path)
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testing-project-2f261-default-rtdb.firebaseio.com/'
})
    database = db.reference()
    new_data = {"username": username, "password": password, "preferred_name": preferred_name, "Summaries": []}
    database.child("Users").child(username).set(new_data)

    summary = "this is my summary of the conversation"

    # Retrieve the existing list of summaries
    existing_summaries = database.child("Users").child(username).child("Summaries").get() or []
    # Append the new summary to the list
    existing_summaries.append(summary)
    # Write the updated list back to the database
    database.child("Users").child(username).child("Summaries").set(existing_summaries)

    # Retrieve the existing list of summaries
    existing_summaries = database.child("Users").child(username).child("Summaries").get() or []
    # Append the new summary to the list
    existing_summaries.append(summary)
    # Write the updated list back to the database
    database.child("Users").child(username).child("Summaries").set(existing_summaries)
