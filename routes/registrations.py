from flask import Blueprint, jsonify, request
from models import db, Registration, Event
from utils.auth_helpers import token_required

registrations_bp = Blueprint("registrations", __name__)

@registrations_bp.route("/api/registrations", methods=["POST"])
@token_required
def register_to_event(user):
    data = request.get_json(silent=True) or {}
    event_id = data.get("event_id")
    if not event_id: return jsonify({"message": "Укажите event_id"}), 400
    if not Event.query.get(event_id): return jsonify({"message": "Мероприятие не найдено"}), 404
    if Registration.query.filter_by(user_id=user.id, event_id=event_id).first():
        return jsonify({"message": "Вы уже зарегистрированы"}), 400
    reg = Registration(user_id=user.id, event_id=event_id, status="pending")
    db.session.add(reg)
    db.session.commit()
    return jsonify({"message": "Регистрация создана", "id": reg.id, "status": reg.status}), 201

@registrations_bp.route("/api/registrations", methods=["GET"])
@token_required
def my_registrations(user):
    regs = Registration.query.filter_by(user_id=user.id).all()
    result = [{"id": r.id, "event_id": r.event_id, "status": r.status} for r in regs]
    return jsonify(result), 200