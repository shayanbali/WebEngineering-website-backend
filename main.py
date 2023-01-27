import mysql
import jwt
from flask import Flask, request, jsonify

# Connect to database
HOST = "mysql-cc-hw1-shayanbali-shayanbali3-bfff.aivencloud.com"
PORT = 27978
USER = "avnadmin"
PASSWORD = "AVNS_9XBFtm4jwXZQkSpUlig"
DATABASE = "defaultdb"
mydb = mysql.connector.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

mycursor = mydb.cursor(buffered=True)


#Add table users
mycursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY,created_at TIMESTAMP NOT NULL DEFAULT NOW(),updated_at TIMESTAMP,deleted_at TIMESTAMP,username VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL);")


app = Flask(__name__)
app.secret_key = "shayan-bali"  # This should be kept secret





# Add login function with JWT AUTH
@app.route('/api/users/login', methods=['POST'])
def login():
    # Get user's login credentials
    username = request.json['username']
    password = request.json['password']

    # Authenticate user's credentials
    mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = mycursor.fetchone()

    if user:
        # Generate JWT token
        token = jwt.encode({'username': user[1]}, app.secret_key, algorithm='HS256')
        return jsonify({'token': token.decode('utf-8')}), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401





# Check user JWT and verify it
@app.route('/protected', methods=['GET'])
def protected():
    # Get JWT token from request headers
    token = request.headers.get('Authorization')

    # Verify JWT token
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        mycursor.execute("SELECT * FROM users WHERE username = %s", (payload['username'],))
        user = mycursor.fetchone()
        if user:
            return jsonify({"msg": "Access granted"}), 200
        else:
            return jsonify({"msg": "Invalid token"}), 401
    except jwt.DecodeError:
        return jsonify({"msg": "Invalid token"}), 401

4


# Add new user to website
@app.route('/api/users', methods=['POST'])
def create_user():
    # Get new user's credentials from request data
    username = request.json['username']
    password = request.json['password']

    # Insert new user into the database
    mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    mydb.commit()

    return jsonify({"msg": "User created successfully"}), 200
