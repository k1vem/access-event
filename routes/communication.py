from flask import Blueprint, jsonify, request, g
from models import db, Event, Message, Notification, Review
from utils.auth_helpers import token_required

communication_bp = Blueprint("communication", __name__, url_prefix="/api")

@communication_bp.get("/events/<int:event_id>/messages")
@token_required
def get_messages(event_id):
    if not db.session.get(Event, event_id):
        return jsonify({"error": "Мероприятие не найдено"}), 404
    rows = Message.query.filter_by(event_id=event_id).order_by(Message.sent_at.asc()).all()
    return jsonify([{"id": x.id, "event_id": x.event_id, "user_id": x.sender_id,
                     "message": x.content, "created_at": x.sent_at.isoformat()} for x in rows])

@communication_bp.post("/events/<int:event_id>/messages")
@token_required
def post_message(event_id):
    if not db.session.get(Event, event_id):
        return jsonify({"error": "Мероприятие не найдено"}), 404
    content = str((request.get_json(silent=True) or {}).get("message", "")).strip()
    if not content or len(content) > 2000:
        return jsonify({"error": "Сообщение должно содержать от 1 до 2000 символов"}), 400
    row = Message(event_id=event_id, sender_id=g.current_user_id, content=content)
    db.session.add(row)
    db.session.commit()
    return jsonify({"id": row.id, "event_id": row.event_id, "user_id": row.sender_id,
                    "message": row.content, "created_at": row.sent_at.isoformat()}), 201

@communication_bp.get("/events/<int:event_id>/reviews")
def get_reviews(event_id):
    if not db.session.get(Event, event_id):
        return jsonify({"error": "Мероприятие не найдено"}), 404
    return jsonify([x.to_dict() for x in Review.query.filter_by(event_id=event_id).order_by(Review.created_at.desc()).all()])

@communication_bp.post("/events/<int:event_id>/reviews")
@token_required
def post_review(event_id):
    if not db.session.get(Event, event_id):
        return jsonify({"error": "Мероприятие не найдено"}), 404
    data = request.get_json(silent=True) or {}
    try:
        rating = int(data.get("rating", 0))
    except (TypeError, ValueError):
        rating = 0
    if not 1 <= rating <= 5:
        return jsonify({"error": "Оценка должна быть от 1 до 5"}), 400
    if Review.query.filter_by(event_id=event_id, user_id=g.current_user_id).first():
        return jsonify({"error": "Вы уже оставили отзыв"}), 409
    row = Review(event_id=event_id, user_id=g.current_user_id, rating=rating,
                 comment=str(data.get("comment", ""))[:2000])
    db.session.add(row)
    db.session.commit()
    return jsonify(row.to_dict()), 201

@communication_bp.get("/notifications")
@token_required
def get_notifications():
    rows = Notification.query.filter_by(user_id=g.current_user_id).order_by(Notification.created_at.desc()).all()
    return jsonify([{"id": x.id, "event_id": x.event_id, "type": x.type,
                     "is_read": x.is_read, "created_at": x.created_at.isoformat()} for x in rows])

@communication_bp.patch("/notifications/<int:notification_id>")
@token_required
def mark_notification_read(notification_id):
    row = db.session.get(Notification, notification_id)
    if not row or row.user_id != g.current_user_id:
        return jsonify({"error": "Уведомление не найдено"}), 404
    row.is_read = True
    db.session.commit()
    return jsonify({"id": row.id, "is_read": row.is_read})
