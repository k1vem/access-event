from datetime import datetime

from flask import Blueprint, jsonify, request, g
from models import db, Event
from utils.auth_helpers import role_required

events_bp = Blueprint("events", __name__, url_prefix="/api/events")


@events_bp.get("")
def list_events():
    query = Event.query
    search = request.args.get("q", "").strip()
    if search:
        query = query.filter(Event.title.ilike(f"%{search}%"))
    accessibility = request.args.get("accessibility", "").strip()
    if accessibility:
        query = query.filter(Event.accessibility.ilike(f"%{accessibility}%"))
    return jsonify([event.to_dict() for event in query.order_by(Event.event_date.asc()).all()])


@events_bp.get("/<int:event_id>")
def get_event(event_id):
    event = db.session.get(Event, event_id)
    return (jsonify(event.to_dict()), 200) if event else (jsonify({"error": "Мероприятие не найдено"}), 404)


@events_bp.post("")
@role_required("organizer", "admin")
def create_event():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify({"error": "Название мероприятия обязательно"}), 400
    try:
        event_date = datetime.fromisoformat(data["event_date"]) if data.get("event_date") else datetime.utcnow()
    except (TypeError, ValueError):
        return jsonify({"error": "Неверный формат event_date; используйте ISO 8601"}), 400

    event = Event(
        title=title,
        description=str(data.get("description", "")),
        location=str(data.get("location", "")),
        event_date=event_date,
        accessibility=str(data.get("accessibility", "")),
        is_inclusive=bool(data.get("is_inclusive", True)),
        sign_language=bool(data.get("sign_language", False)),
        visual_alerts=bool(data.get("visual_alerts", False)),
        organizer_id=g.current_user_id,
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201
