import pymongo

mongoURI = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongoURI)

db = client["Eatwise"]
users= db["user_credentials"]
food_history = db["user_food_history"]

def check_user_by_email(email):   # For "/register, /login"
    return users.find_one({"email":email},{'_id':0})

def check_user_by_email_and_password(email,password):   # For "/register, /login"
    return users.find_one({"email":email, "password":password},{'_id':0})

def check_user_by_session(session_token):   # For "UA func"
    return users.find_one({"session_token":session_token},{'_id':0})

def insert_user(name,email,password):   # For "/register"
    users.insert_one({"name":name,"email":email,"password":password})

def update_user_session(email,session_token):   # For "/login"
    users.update_one({"email":email},{'$set':{"session_token": session_token}})

def delete_user(session_token):    # For "UA func"
    users.delete_one({"session_token":session_token})

def insert_history_data(data):
    food_history.insert_one(data)

def find_history_user(email, start_date, end_date):
    query = {"email":email, "Date": {"$gte":start_date, "$lte":end_date}}
    return list(food_history.find(query,{'_id':0}))
    # return list(food_history.find({"email":email},{'_id':0}))

if __name__ == "__main__":
    print(check_user_by_email("tanaya.lemolite@gmail.com"))