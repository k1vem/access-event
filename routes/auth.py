from flask import Blueprint, jsonify, request
from models import db, User
from utils.auth_helpers import generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", data.get("name", ""))).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    role = str(data.get("role", "user"))
    is_deaf = bool(data.get("is_deaf", False))

    if not username or len(username) > 80 or not email or "@" not in email or len(password) < 8:
        return jsonify({"error": "Укажите имя, корректный email и пароль не короче 8 символов"}), 400
    if role not in ("user", "organizer", "admin"):
        return jsonify({"error": "Недопустимая роль"}), 400
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"error": "Пользователь с таким именем или email уже существует"}), 409

    user = User(username=username, email=email, role=role, is_deaf=is_deaf, password_hash="")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"user": user.to_dict(), "token": generate_token(user.id, user.role)}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Неверный email или пароль"}), 401
    return jsonify({"user": user.to_dict(), "token": generate_token(user.id, user.role)}), 200
