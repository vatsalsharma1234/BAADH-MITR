from app.models import Alert, ElevationBand, Household, Severity

_ELEVATION_WEIGHT = {
    ElevationBand.riverbank: 40,
    ElevationBand.low_lying: 30,
    ElevationBand.mid_slope: 10,
    ElevationBand.high_ground: 0,
}

_SEVERITY_MULTIPLIER = {
    Severity.watch: 0.4,
    Severity.moderate: 0.7,
    Severity.severe: 1.0,
    Severity.extreme: 1.3,
}

ELDERLY_WEIGHT = 25
NO_SMARTPHONE_WEIGHT = 20
MOBILITY_WEIGHT = 20
HOUSEHOLD_SIZE_WEIGHT = 2


def score_household(household: Household, alert: Alert) -> tuple[float, str]:
    reasons = []
    base = _ELEVATION_WEIGHT[household.elevation_band]
    if base:
        reasons.append(household.elevation_band.value.replace("_", " "))

    score = float(base)

    if household.elderly_only:
        score += ELDERLY_WEIGHT
        reasons.append("elderly-only household")

    if not household.has_smartphone:
        score += NO_SMARTPHONE_WEIGHT
        reasons.append("no resident smartphone")

    if household.mobility_limited:
        score += MOBILITY_WEIGHT
        reasons.append("limited mobility / can't self-evacuate quickly")

    size_bonus = min(household.resident_count, 6) * HOUSEHOLD_SIZE_WEIGHT
    score += size_bonus
    if household.resident_count >= 4:
        reasons.append(f"{household.resident_count} residents")

    score *= _SEVERITY_MULTIPLIER[alert.severity]

    reason = ", ".join(reasons) if reasons else "standard priority"
    return round(score, 2), reason


def build_checklist(households: list[Household], alert: Alert):
    scored = []
    for h in households:
        score, reason = score_household(h, alert)
        scored.append({"household": h, "priority_score": score, "reason": reason})

    scored.sort(key=lambda row: row["priority_score"], reverse=True)
    for i, row in enumerate(scored, start=1):
        row["rank"] = i
    return scored
