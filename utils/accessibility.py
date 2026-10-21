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