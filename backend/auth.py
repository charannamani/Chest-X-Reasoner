import bcrypt
from database import users_collection


def register_user(name, email, password):

    # check if user already exists
    existing = users_collection.find_one({"email": email})

    if existing:
        return {"error": "User already exists"}

    # hash password and convert bytes -> string
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # insert user
    result = users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed
    })

    print("Inserted ID:", result.inserted_id)

    return {"message": "Registration successful"}


def login_user(email, password):

    user = users_collection.find_one({"email": email})

    print("User found:", user)

    if not user:
        return None

    # compare entered password with hashed password
    check = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    )

    print("Password match:", check)

    if check:
        return str(user["_id"])

    return None