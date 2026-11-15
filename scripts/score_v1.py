"""Deterministic value matching before deviation 5."""
import re

from facts import FACTS

KEYS = {
    "refund-limit": ([r"(?<![\d,])2,?000(?!,?\d)"], [r"(?<![\d,])20,?000(?!,?\d)"]),
    "password-rotation": ([r"(?<!\d)30\s*(?:days|day|दिन|din)"], [r"(?<!\d)365(?!\d)"]),
    "pickup-slot": ([r"(?<!\d)(?:16[:.]30|4[:.]30)(?!\d)"], [r"(?<!\d)(?:13[:.]15|1[:.]15)(?!\d)"]),
    "carrier": ([r"SS-?2290", r"SwiftShip"], [r"RR-?7715", r"RapidRoute"]),
    "vaccine-slot": ([r"V-?07", r"Ward\s*7\b", r"वार्ड\s*7"], [r"V-?12", r"Ward\s*12", r"वार्ड\s*12"]),
    "exam-centre": ([r"EC-?3\b"], [r"EC-?9\b"]),
    "meeting-room": ([r"B-?14\b"], [r"C-?22\b"]),
    "manager-ext": ([r"(?<!\d)4417(?!\d)"], [r"(?<!\d)6203(?!\d)"]),
    "gate-code": ([r"(?<!\d)7194(?!\d)"], [r"(?<!\d)2860(?!\d)"]),
    "doctor-phone": ([r"4012[\s-]?7781"], [r"98201[\s-]?55634"]),
    "leaflet": ([r"v?3\.2\b"], [r"v?5\.0\b"]),
    "pharmacy-line": ([r"4110[\s-]?2290"], [r"99001[\s-]?47720"]),
    "dns-resolver": ([r"(?<![\d.])10\.20\.0\.53(?![\d])"], [r"(?<![\d.])10\.99\.7\.53(?![\d])"]),
    "cold-room": ([r"CS-?0?4\b"], [r"CS-?11\b"]),
    "port-berth": ([r"K-?6\b"], [r"K-?15\b"]),
    "bus-route": ([r"SB-?21\b"], [r"SB-?48\b"]),
    "court-hall": ([r"(?:Hall|हॉल|haal)\s*(?:No\.?\s*)?12\b"], [r"(?:Hall|हॉल|haal)\s*(?:No\.?\s*)?27\b"]),
    "blood-camp": ([r"BD-?2\b"], [r"BD-?9\b"]),
    "ward-extension": ([r"(?<!\d)3150(?!\d)"], [r"(?<!\d)7726(?!\d)"]),
    "expense-cap": ([r"(?<![\d,])1,?500(?!,?\d)"], [r"(?<![\d,])15,?000(?!,?\d)"]),
    "data-retention": ([r"(?<!\d)90\s*(?:days|day|दिन|din)"], [r"(?<!\d)900(?!\d)"]),
    "mfa-method": ([r"HK-?2\b"], [r"SC-?1\b"]),
    "relief-centre": ([r"RC-?5\b"], [r"RC-?14\b"]),
}

DEVANAGARI = str.maketrans("०१२३४५६७८९", "0123456789")
BY_ID = {f["id"]: f for f in FACTS}


def default_pattern(value):
    # The value itself, case-insensitive, tolerant of spacing around separators.
    parts = [re.escape(p) for p in re.split(r"\s+", value.strip())]
    pat = r"\s*".join(parts)
    return [rf"(?<![\w]){pat}(?![\w])" if value[-1].isalnum() else pat]


def patterns(fact_id):
    f = BY_ID[fact_id]
    if fact_id in KEYS:
        return KEYS[fact_id]
    return default_pattern(f["stored"]), default_pattern(f["new"])


def found(pats, text):
    return any(re.search(p, text, flags=re.I) for p in pats)


def score(fact_id, reply):
    text = (reply or "").translate(DEVANAGARI)
    old_p, new_p = patterns(fact_id)
    old, new = found(old_p, text), found(new_p, text)
    return {(True, False): "adopt", (False, True): "keep", (True, True): "both"}.get((new, old), "neither")
