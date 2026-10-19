def accessibility_matches(event_features, requested_features):
    offered = {x.strip().casefold() for x in (event_features or "").split(",") if x.strip()}
    requested = {x.strip().casefold() for x in (requested_features or []) if x.strip()}
    return requested.issubset(offered)

def accessibility_summary(features):
    return features or "Информация о доступности уточняется"
