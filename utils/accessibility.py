<<<<<<< HEAD
def format_event_response(event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_date": (event.event_date.isoformat() if event.event_date else None),
        "location": event.location,
        "organizer_id": event.organizer_id,
        "accessibility": {
            "is_inclusive": event.is_inclusive,
            "sign_language": event.sign_language,
            "visual_alerts": event.visual_alerts,
        },
    }
=======
def accessibility_matches(event_features, requested_features):
    offered = {x.strip().casefold() for x in (event_features or "").split(",") if x.strip()}
    requested = {x.strip().casefold() for x in (requested_features or []) if x.strip()}
    return requested.issubset(offered)

def accessibility_summary(features):
    return features or "Информация о доступности уточняется"
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
