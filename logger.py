"""
VanguardPrime — logger.py
Logs all call results to MidasPrime war chest.
"""

import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/vanguard_calls.json")

def log_call(lead_name, company, phone, outcome, notes="", email_captured=None):
    """
    Outcomes: answered | voicemail | no_answer | interested | callback_requested | closed
    """
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "lead_name": lead_name,
        "company": company,
        "phone": phone,
        "outcome": outcome,
        "notes": notes,
        "email_captured": email_captured,
    }

    # Load existing log
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[VANGUARD LOG] {lead_name} — {outcome}")

    # If email captured → add to EmailOctopus list
    if email_captured:
        _add_to_email_list(email_captured, lead_name, company)

    return entry

def _add_to_email_list(email, name, company):
    """Push captured email to EmailOctopus PropPilot list."""
    import urllib.request
    import urllib.parse

    API_KEY = os.getenv("EMAILOCTOPUS_API_KEY", "eo_c31f4c1b1d65c2a63fca72914998816255aa47619e76a130444898786e5050f4")
    LIST_ID = os.getenv("EMAILOCTOPUS_LIST_ID", "2f14af34-2a2f-11f1-bfee-4dc30cc37367")

    payload = json.dumps({
        "api_key": API_KEY,
        "email_address": email,
        "fields": {
            "FirstName": name.split()[0] if name else "",
            "LastName": name.split()[-1] if name and len(name.split()) > 1 else "",
            "Company": company
        },
        "tags": ["vanguard-call", "realtor-outreach"],
        "status": "SUBSCRIBED"
    }).encode()

    req = urllib.request.Request(
        f"https://emailoctopus.com/api/1.6/lists/{LIST_ID}/contacts",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as res:
            print(f"[VANGUARD] Email captured → EmailOctopus: {email}")
    except Exception as e:
        print(f"[VANGUARD] EmailOctopus error: {e}")

def get_summary():
    if not os.path.exists(LOG_FILE):
        return {"total": 0, "outcomes": {}}
    with open(LOG_FILE, "r") as f:
        data = json.load(f)
    outcomes = {}
    for entry in data:
        o = entry["outcome"]
        outcomes[o] = outcomes.get(o, 0) + 1
    return {"total": len(data), "outcomes": outcomes}
