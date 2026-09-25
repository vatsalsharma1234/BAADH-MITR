import random
from datetime import datetime

from app.models import Severity

_SEVERITY_LADDER = [
    (Severity.watch, (1.5, 2.5), "River rising slowly. Monitor, no action needed yet."),
    (Severity.moderate, (2.5, 3.5), "River level approaching bankfull. Prepare warning routes."),
    (Severity.severe, (3.5, 4.8), "Bankfull expected within 24-48 hours. Begin door-to-door relay."),
    (Severity.extreme, (4.8, 6.0), "Major flooding expected imminently. Evacuate priority households now."),
]


def generate_next_alert(river: str, previous_severity: Severity | None = None) -> dict:
    levels = [s for s, _, _ in _SEVERITY_LADDER]
    if previous_severity is None:
        idx = 0
    else:
        prev_idx = levels.index(previous_severity)
        move = random.choices([1, 0, -1], weights=[0.6, 0.25, 0.15])[0]
        idx = max(0, min(len(levels) - 1, prev_idx + move))

    severity, (lo, hi), note = _SEVERITY_LADDER[idx]
    river_level_m = round(random.uniform(lo, hi), 2)

    return {
        "severity": severity,
        "river_level_m": river_level_m,
        "forecast_note": f"{river}: {note}",
        "issued_at": datetime.utcnow(),
        "source": "simulated_flood_feed",
    }
