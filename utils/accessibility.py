def accessibility_matches(event_features, requested_features):
    offered = {
        item.strip().casefold()
        for item in (event_features or "").split(",")
        if item.strip()
    }
    requested = {
        str(item).strip().casefold()
        for item in (requested_features or [])
        if str(item).strip()
    }
    return requested.issubset(offered)


def accessibility_summary(features):
    return features or "Информация о доступности уточняется"


def format_event_response(event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description or "",
        "event_date": event.event_date.isoformat() if event.event_date else None,
        "location": event.location or "",
        "organizer_id": event.organizer_id,
        "accessibility": event.accessibility or "",
        "is_inclusive": bool(event.is_inclusive),
        "sign_language": bool(event.sign_language),
        "visual_alerts": bool(event.visual_alerts),
    }
