from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import config
from models import db, User
from functools import wraps

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        print("Received Login Request for:", username)  # Debugging

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
            config.JWT_SECRET,
            algorithm="HS256"
        )

        print("Generated Token:", token)  # Debugging
        return jsonify({"token": token})
    except Exception as e:
        print("Error in Login API:", str(e))  # Debugging
        return jsonify({"error": "Internal Server Error"}), 500

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token is missing"}), 403

        try:
            token_splitted = token.split(" ")[1]  # Handle 'Bearer <token>' format
            decoded = jwt.decode(token_splitted, config.JWT_SECRET, algorithms=["HS256"])
            user_id = decoded["user_id"]

            # Fetch the user from the database
            current_user = User.query.get(user_id)
            if not current_user:
                return jsonify({"error": "User not found"}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403
        except Exception as e:
            return jsonify({"error": str(e)}), 403

        return f(current_user, *args, **kwargs)  # Pass current_user explicitly

    return decorated_function



@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid data"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201