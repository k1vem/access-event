import datetime
from flask import Blueprint, jsonify, request
from models import db, Event
from utils.auth_helpers import token_required, role_required
from utils.accessibility import format_event_response

events_bp = Blueprint("events", __name__)

def _parse_datetime(value):
    if value is None: return None
    if isinstance(value, datetime.datetime): return value
    if isinstance(value, str):
        cleaned = value.replace("T", " ").strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try: return datetime.datetime.strptime(cleaned, fmt)
            except ValueError: continue
    raise ValueError(f"Некорректная дата: {value}")

@events_bp.route("/api/events", methods=["GET"])
def list_events():
    query = Event.query
    if request.args.get("inclusive") in ("1", "true"):
        query = query.filter_by(is_inclusive=True)
    events = query.order_by(Event.event_date).all()
    return jsonify([format_event_response(e) for e in events]), 200

@events_bp.route("/api/events", methods=["POST"])
@token_required
@role_required("organizer", "admin")
def create_event(user):
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title or len(title) > 100:
        return jsonify({"message": "Название обязательно, до 100 символов"}), 400
    try: event_date = _parse_datetime(data.get("event_date"))
    except ValueError as e: return jsonify({"message": str(e)}), 400
    if not event_date: return jsonify({"message": "Укажите дату и время"}), 400

    event = Event(
        title=title, description=data.get("description"), event_date=event_date,
        location=data.get("location"), organizer_id=user.id,
        is_inclusive=bool(data.get("is_inclusive", False)),
        sign_language=bool(data.get("sign_language", False)),
        visual_alerts=bool(data.get("visual_alerts", False)),
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "Мероприятие создано", "id": event.id}), 201