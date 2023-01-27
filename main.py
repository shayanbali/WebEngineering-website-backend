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

app = Flask(__name__)
app.secret_key = "shayan-bali"  # This should be kept secret


# Add login function with JWT AUTH
@app.route('/login', methods=['POST'])
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
        return jsonify({'token': token.decode('utf-8')})
    else:
        return jsonify({"msg": "Invalid credentials"}), 401
