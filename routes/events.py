<<<<<<< HEAD
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
=======
from datetime import datetime
from flask import Blueprint, jsonify, request, g
from models import db, Event
from utils.auth_helpers import role_required

events_bp = Blueprint("events", __name__, url_prefix="/api/events")

@events_bp.get("")
def list_events():
    query = Event.query
    q = request.args.get("q", "").strip()
    if q: query = query.filter(Event.title.ilike(f"%{q}%"))
    accessibility = request.args.get("accessibility", "").strip()
    if accessibility: query = query.filter(Event.accessibility.ilike(f"%{accessibility}%"))
    return jsonify([event.to_dict() for event in query.order_by(Event.event_date.asc()).all()])

@events_bp.get("/<int:event_id>")
def get_event(event_id):
    event = db.session.get(Event, event_id)
    return (jsonify(event.to_dict()), 200) if event else (jsonify({"error":"Мероприятие не найдено"}), 404)

@events_bp.post("")
@role_required("organizer", "admin")
def create_event():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title: return jsonify({"error":"Название мероприятия обязательно"}), 400
    try: event_date = datetime.fromisoformat(data["event_date"]) if data.get("event_date") else datetime.utcnow()
    except (TypeError, ValueError): return jsonify({"error":"Неверный формат event_date; используйте ISO 8601"}), 400
    event = Event(title=title, description=str(data.get("description", "")), location=str(data.get("location", "")),
                  event_date=event_date, accessibility=str(data.get("accessibility", "")), organizer_id=g.current_user_id)
    db.session.add(event); db.session.commit()
    return jsonify(event.to_dict()), 201
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
