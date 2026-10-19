from flask import Blueprint, jsonify, request
from models import db, User
from utils.auth_helpers import hash_password, verify_password, generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", data.get("name", ""))).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    if not username or not email or len(password) < 8:
        return jsonify({"error":"Укажите имя, email и пароль не короче 8 символов"}), 400
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"error":"Пользователь с таким именем или email уже существует"}), 409
    user = User(username=username, email=email, password_hash=hash_password(password), is_deaf=bool(data.get("is_deaf", False)))
    db.session.add(user); db.session.commit()
    return jsonify({"user":user.to_dict(), "token":generate_token(user.id, user.role)}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error":"Неверный email или пароль"}), 401
    return jsonify({"user":user.to_dict(), "token":generate_token(user.id, user.role)})
