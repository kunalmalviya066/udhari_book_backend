from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt  # ✅ Correct import
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import config
from datetime import timedelta

app = Flask(__name__)

# 🔹 Database Configuration
app.config["MYSQL_HOST"] = config.DB_HOST
app.config["MYSQL_USER"] = config.DB_USER
app.config["MYSQL_PASSWORD"] = config.DB_PASSWORD
app.config["MYSQL_DB"] = config.DB_NAME
app.config["JWT_SECRET_KEY"] = config.SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

mysql = MySQL(app)
bcrypt = Bcrypt(app)  # ✅ Correct initialization
jwt = JWTManager(app)

# 🔹 Register User
@app.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    mobile = data.get("mobile")
    password = data.get("password")

    if not mobile or not password:
        return jsonify({"error": "Mobile and Password required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")  # ✅ Correct method

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO users (mobile, password) VALUES (%s, %s)", (mobile, hashed_password))
        mysql.connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

# 🔹 Login User
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    mobile = data["mobile"]
    password = data["password"]

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, password FROM users WHERE mobile = %s", (mobile,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.check_password_hash(user[1], password):  # ✅ Correct password check
        access_token = create_access_token(identity=str(user[0]))
        return jsonify({"token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401
# 🔹 Add Customer
@app.route("/add_customer", methods=["POST"])
@jwt_required()
def add_customer():
    user_id = get_jwt_identity()  # Get logged-in user ID
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    name = data.get("name")
    mobile = data.get("mobile")
    balance = data.get("balance", 0)

    if not name or not mobile:
        return jsonify({"error": "Name and Mobile required"}), 400

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO customers (user_id, name, mobile, balance) VALUES (%s, %s, %s, %s)",
            (user_id, name, mobile, balance),
        )
        mysql.connection.commit()
        return jsonify({"message": "Customer added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

# 🔹 Get Customers (Only Logged-In User's Customers)
@app.route("/customers", methods=["GET"])
@jwt_required()
def get_customers():
    user_id = get_jwt_identity()  # ✅ Get the logged-in user's ID

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, mobile, balance FROM customers WHERE user_id = %s", (user_id,))
    customers = cursor.fetchall()
    cursor.close()

    return jsonify([{"name": c[0], "mobile": c[1], "balance": c[2]} for c in customers]), 200



# 🔹 Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)
