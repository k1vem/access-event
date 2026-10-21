<<<<<<< HEAD
import datetime, functools, jwt
from flask import current_app, jsonify, request
from models import db, User

def generate_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=current_app.config["JWT_EXPIRATION_HOURS"]),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def token_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Токен отсутствует"}), 401
        token = auth_header.split("Bearer ", 1)[1]
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Срок действия токена истёк"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Неверный токен"}), 401
        user = db.session.get(User, data.get("user_id"))
        if user is None:
            return jsonify({"message": "Пользователь не найден"}), 401
        return f(user=user, *args, **kwargs)
    return wrapper

def role_required(*roles):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(user, *args, **kwargs):
            if user.role not in roles:
                return jsonify({"message": "Недостаточно прав"}), 403
            return f(user=user, *args, **kwargs)
        return wrapper
    return decorator
=======
from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import current_app, g, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password): return generate_password_hash(password)
def verify_password(password, password_hash): return check_password_hash(password_hash, password)

def generate_token(user_id, role="user"):
    exp = datetime.utcnow() + timedelta(hours=current_app.config.get("JWT_EXPIRATION_HOURS", 24))
    return jwt.encode({"user_id": int(user_id), "role": role, "exp": exp}, current_app.config["JWT_SECRET"], algorithm="HS256")

def decode_token(token):
    return jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])

def token_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "): return jsonify({"error":"Требуется Bearer-токен"}), 401
        try:
            payload = decode_token(header[7:])
            g.current_user_id = int(payload["user_id"])
            g.current_user_role = payload.get("role", "user")
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            return jsonify({"error":"Недействительный или просроченный токен"}), 401
        return view(*args, **kwargs)
    return wrapped

def role_required(*roles):
    def decorator(view):
        @wraps(view)
        @token_required
        def wrapped(*args, **kwargs):
            if g.current_user_role not in roles: return jsonify({"error":"Недостаточно прав"}), 403
            return view(*args, **kwargs)
        return wrapped
    return decorator
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
