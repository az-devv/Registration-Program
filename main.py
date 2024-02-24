import hashlib
import json
import re


def get_new_user_id(users):
    if not users:
        return 1
    latest_user_id = max(int(list(user.keys())[0].split("user")[1]) for user in users)
    return latest_user_id + 1


def is_valid_username(username):
    return bool(re.match("^[a-zA-Z0-9]+$", username))


def is_username_taken(username, users):
    return any(username == list(user.values())[0]['user'] for user in users)


def verify_user(username, password, users):
    hashed_username = hashlib.sha256(username.encode('utf-8')).hexdigest()
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    for user_entry in users:
        stored_user_data = list(user_entry.values())[0]
        if stored_user_data["hasheduser"] == hashed_username and stored_user_data["hashedpw"] == hashed_password:
            return True

    return False


response = int(input("[1] Sign-in\n[2] Sign-up\n> "))
print()

if response == 2:
    user = input("Username: ")

    if not is_valid_username(user):
        print("Invalid username. Username must contain only letters and numbers.")
        exit()

    passw = input("Password: ")

    hashed_username = hashlib.sha256(user.encode('utf-8')).hexdigest()
    hashed_password = hashlib.sha256(passw.encode('utf-8')).hexdigest()

    try:
        with open('db.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"users": []}

    if is_username_taken(user, data["users"]):
        print("Username is already taken. Please choose a different username.")
        exit()

    new_user_id = get_new_user_id(data["users"])

    user_data = {"id": new_user_id, "hasheduser": hashed_username, "hashedpw": hashed_password}

    data["users"].append({f"user{new_user_id}": user_data})

    with open('db.json', 'w') as file:
        json.dump(data, file, indent=2)

elif response == 1:
    username = input("Username: ")
    password = input("Password: ")

    try:
        with open('db.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("No users in the database. Please sign up first.")
        exit()

    if verify_user(username, password, data["users"]):
        print("Sign-in successful!")
    else:
        print("Incorrect username or password.")

else:
    exit()
