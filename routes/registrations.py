<<<<<<< HEAD
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
=======
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
    db.session.add(Notification(user_id=g.current_user_id, event_id=event_id,
                                type="registration_pending", message="Заявка отправлена и ожидает подтверждения.", is_read=False))
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
    db.session.add(Notification(user_id=item.user_id, event_id=item.event_id,
                                type="registration_" + status, message="Статус заявки изменён: " + status, is_read=False))
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
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
