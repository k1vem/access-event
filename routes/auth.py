from flask import Blueprint, jsonify, request
from models import db, User
<<<<<<< HEAD
from utils.auth_helpers import generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = data.get("role", "user")
    is_deaf = bool(data.get("is_deaf", False))
    
    if not username or len(username) > 50: return jsonify({"message": "Некорректное имя"}), 400
    if "@" not in email or "." not in email.split("@")[-1]: return jsonify({"message": "Некорректный email"}), 400
    if len(password) < 8: return jsonify({"message": "Пароль от 8 символов"}), 400
    if role not in ("user", "organizer", "admin"): return jsonify({"message": "Недопустимая роль"}), 400
    if User.query.filter_by(email=email).first(): return jsonify({"message": "Email занят"}), 400
    if User.query.filter_by(username=username).first(): return jsonify({"message": "Имя занято"}), 400

    user = User(username=username, email=email, role=role, is_deaf=is_deaf)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Пользователь создан", "user_id": user.id}), 201

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"message": "Неверный email или пароль"}), 401
    return jsonify({"message": "Вход выполнен", "token": generate_token(user), "role": user.role, "user_id": user.id}), 200
=======
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
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
