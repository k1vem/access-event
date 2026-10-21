from flask import Blueprint, jsonify, g, request

from models import db, Event, Registration, Notification
from utils.auth_helpers import token_required

registrations_bp = Blueprint("registrations", __name__, url_prefix="/api")


@registrations_bp.post("/events/<int:event_id>/register")
@token_required
def register_for_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({"error": "Мероприятие не найдено"}), 404
    existing = Registration.query.filter_by(user_id=g.current_user_id, event_id=event_id).first()
    if existing and existing.status != "cancelled":
        return jsonify({"error": "Вы уже зарегистрированы"}), 409
    if existing:
        existing.status = "pending"
        item = existing
    else:
        item = Registration(user_id=g.current_user_id, event_id=event_id, status="pending")
        db.session.add(item)
    db.session.add(Notification(
        user_id=g.current_user_id,
        event_id=event_id,
        type="registration_pending",
        message="Заявка отправлена и ожидает подтверждения.",
        is_read=False,
    ))
    db.session.commit()
    return jsonify(item.to_dict()), 201


@registrations_bp.patch("/registrations/<int:registration_id>")
@token_required
def review_registration(registration_id):
    item = db.session.get(Registration, registration_id)
    if not item:
        return jsonify({"error": "Заявка не найдена"}), 404
    if g.current_user_role not in ("organizer", "admin"):
        return jsonify({"error": "Недостаточно прав"}), 403
    if g.current_user_role == "organizer" and item.event.organizer_id != g.current_user_id:
        return jsonify({"error": "Можно менять заявки только на свои мероприятия"}), 403
    status = (request.get_json(silent=True) or {}).get("status")
    if status not in ("confirmed", "cancelled", "pending"):
        return jsonify({"error": "Недопустимый статус"}), 400
    item.status = status
    db.session.add(Notification(
        user_id=item.user_id,
        event_id=item.event_id,
        type="registration_" + status,
        message="Статус заявки изменён: " + status,
        is_read=False,
    ))
    db.session.commit()
    return jsonify(item.to_dict())


@registrations_bp.delete("/events/<int:event_id>/register")
@token_required
def cancel_registration(event_id):
    item = Registration.query.filter_by(user_id=g.current_user_id, event_id=event_id).first()
    if not item:
        return jsonify({"error": "Регистрация не найдена"}), 404
    item.status = "cancelled"
    db.session.commit()
    return jsonify(item.to_dict())


@registrations_bp.get("/me/registrations")
@registrations_bp.get("/my/registrations")
@token_required
def my_registrations():
    items = Registration.query.filter_by(user_id=g.current_user_id).all()
    return jsonify([item.to_dict() for item in items])
