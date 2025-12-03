from flask import Flask, request, jsonify  # використовуємо необхідні модулі Flask
from flask_sqlalchemy import SQLAlchemy  # для роботи з базою даних
from werkzeug.security import generate_password_hash, check_password_hash  # для хешування паролів
import jwt  # для створення та перевірки JWT токенів
import datetime  # для роботи з датами та часом
from functools import wraps  # для створення декораторів

# init
app = Flask(__name__)  # створюємо екземпляр Flask додатку
app.config['SECRET_KEY'] = 'your_secret_key'  # секретний ключ для JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # налаштування бази даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # вимикаємо відстеження змін

db = SQLAlchemy(app)  # створюємо екземпляр SQLAlchemy


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # унікальний ідентифікатор користувача
    username = db.Column(db.String(150), unique=True, nullable=False)  # ім'я користувача
    password = db.Column(db.String(150), nullable=False)  # хешований пароль
    email = db.Column(db.String(150), unique=True, nullable=False)  # електронна пошта
    role = db.Column(db.String(50), default='user')  # роль користувача


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # отримуємо токен з заголовка
        if not token:
            return jsonify({
                "status": 401,
                "success": False,
                "message": "Token is missing!"
            }), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()

            if not current_user:
                return jsonify({
                    "status": 404,
                    "success": False,
                    "message": "User not found!"
                }), 404

        except Exception as e:
            print(e)
            return jsonify({
                "status": 401,
                "success": False,
                "message": "Token is invalid!"
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/register', methods=['POST'])
def register():
    try:
        payload = request.get_json()  # отримуємо JSON дані з запиту
        if User.query.filter_by(username=payload['username']).first():
            return jsonify({
                "status": 400,
                "success": False,
                "message": "Username already exists"
            }), 400
        if User.query.filter_by(email=payload['email']).first():
            return jsonify({
                "status": 400,
                "success": False,
                "message": "Email already exists"
            }), 400

        hashed_password = generate_password_hash(payload['password'])  # хешуємо пароль
        new_user = User(
            username=payload['username'],
            password=hashed_password,
            email=payload['email'],
            role=payload.get('role', 'user')
        )
        db.session.add(new_user)  # додаємо нового користувача до сесії
        db.session.commit()  # зберігаємо зміни в базі даних

        return jsonify({
            "status": 201,
            "success": True,
            "data": payload,
            "message": "User registered successfully"
        }), 201
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "success": False,
            "message": str(e)
        }), 500


@app.route('/api/login', methods=['POST'])
def login():
    try:
        payload = request.get_json()  # отримуємо JSON дані з запиту
        user = User.query.filter_by(username=payload['username']).first()  # шукаємо користувача за ім'ям
        if not user or not check_password_hash(user.password, payload['password']):
            return jsonify({
                "status": 401,
                "success": False,
                "message": "Invalid username or password"
            }), 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            "status": 200,
            "success": True,
            "message": "Login endpoint hit",
            "data": {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "token": token,
                "token_type": "Bearer"
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "success": False,
            "message": str(e)
        }), 500


# users
@app.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    return {
        "status": 200,
        "success": True,
        "message": "User profile endpoint hit",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    }


@app.route('/api/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    user = User.query.filter_by(id=current_user.id).first()
    if user.role != 'admin':
        return {
            "status": 403,
            "success": False,
            "message": "You do not have permission to access this resource"
        }, 403

    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        output.append(user_data)
    return {
        "status": 200,
        "success": True,
        "message": "All users retrieved successfully",
        "data": output
    }, 200


# update user by id
@app.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if current_user.id != user_id and current_user.role != 'admin':
        return jsonify({
            "status": 403,
            "success": False,
            "message": "You do not have permission to update this user"
        }), 403
    payload = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({
            "status": 404,
            "success": False,
            "message": "User not found"
        }), 404
    if 'username' in payload:
        user.username = payload['username']
    if 'email' in payload:
        user.email = payload['email']
    if 'role' in payload:
        if current_user.role != 'admin':
            return jsonify({
                "status": 403,
                "success": False,
                "message": "Only admin can change user roles"
            }), 403
        user.role = payload['role']
    db.session.commit()
    return jsonify({
        "status": 200,
        "success": True,
        "message": "User updated successfully",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 200


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if current_user.role != 'admin':
        return jsonify({
            "status": 403,
            "success": False,
            "message": "You do not have permission to delete this user",
            "delete_form_link": "some link to delete form"
        }), 403
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({
            "status": 404,
            "success": False,
            "message": "User not found"
        }), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        "status": 200,
        "success": True,
        "message": "User deleted successfully"
    }), 200


@app.route('/api/users/roles', methods=['GET'])
@token_required
def get_user_roles(current_user):
    if current_user.role != 'admin' and current_user.role != 'root':
        return jsonify({
            "status": 403,
            "success": False,
            "message": "You do not have permission to access user roles"
        }), 403
    desc_of_roles = {
        "root": "Has all permissions including managing admin users.",
        "admin": "Can manage regular users and view all data.",
        "moderator": "Can view and moderate user content.",
        "manager": "Can manage specific resources and view reports.",
        "user": "Can view and edit their own data only.",
        "guest": "Has limited access to view public data only."
    }
    return jsonify({
        "status": 200,
        "success": True,
        "message": "User roles retrieved successfully",
        "data": desc_of_roles
    }), 200


# default routes
@app.route('/')
def index():
    return jsonify({
        "status": 200,
        "success": True,
        "message": "Welcome to the Flask JWT Authentication API"
    }), 200


@app.route('/api/health')
def health_check():
    return jsonify({
        "status": 200,
        "success": True,
        "message": "API is healthy"
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # створюємо всі таблиці в базі даних
    app.run(debug=True, port=8000)  # запускаємо додаток у режимі налагодження
