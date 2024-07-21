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

    # Get user data from the database
    user_data = database.child("Users").child(username).get()

    # Check if username exists in the database
    if user_data is not None:
        user_data_val = user_data
        # Check if password matches
        if "password" in user_data_val and user_data_val["password"] == password:
            # Return the list of summaries
            return user_data_val.get("Summaries", [])
        else:
            print("Incorrect password")
            return None
    else:
        # Username does not exist, add new user
        new_data = {"username": username, "password": password, "preferred_name": preferred_name, "Summaries": []}
        database.child("Users").child(username).set(new_data)
        return []
