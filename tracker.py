"""
VanguardPrime — tracker.py
CRM-lite. Tracks every outreach touch, response, and status.
Logs deals closed → war_chest.json
"""

import json
import os
from datetime import datetime

TRACKER_FILE = os.path.join(os.path.dirname(__file__), "../logs/vanguard_tracker.json")
WAR_CHEST_FILE = os.path.join(os.path.dirname(__file__), "../logs/war_chest.json")

STATUSES = [
    "pending",       # Not yet contacted
    "contacted",     # Message sent, no reply
    "replied",       # They responded
    "interested",    # Actively engaged, want deal list
    "email_captured", # Got their email → on PropPilot list
    "deal_sent",     # Sent them an actual deal
    "closed",        # Deal closed — fee earned 🔱
    "dead",          # No response after 3 touches
    "not_interested",
]

def _load():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return {}

def _save(data):
    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_touch(name, channel, message_variant, status="contacted", notes=""):
    data = _load()
    if name not in data:
        data[name] = {"touches": [], "status": "pending", "email": None}

    data[name]["touches"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "channel": channel,
        "variant": message_variant,
        "status": status,
        "notes": notes,
    })
    data[name]["status"] = status
    _save(data)
    print(f"[VANGUARD TRACKER] {name} — {channel} — {status}")

def update_status(name, status, email=None, notes=""):
    data = _load()
    if name not in data:
        data[name] = {"touches": [], "status": status, "email": None}
    data[name]["status"] = status
    if email:
        data[name]["email"] = email
    if notes:
        data[name].setdefault("notes", []).append(notes)
    _save(data)

def log_deal_closed(name, fee_amount, deal_notes=""):
    """Called when a deal closes. Writes to war chest."""
    update_status(name, "closed", notes=f"CLOSED — ${fee_amount}")

    # Write to war chest
    os.makedirs(os.path.dirname(WAR_CHEST_FILE), exist_ok=True)
    if os.path.exists(WAR_CHEST_FILE):
        with open(WAR_CHEST_FILE, "r") as f:
            chest = json.load(f)
    else:
        chest = {"total": 0, "entries": []}

    chest["total"] += fee_amount
    chest["entries"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "source": "VanguardPrime",
        "contact": name,
        "amount": fee_amount,
        "notes": deal_notes,
    })

    with open(WAR_CHEST_FILE, "w") as f:
        json.dump(chest, f, indent=2)

    print(f"[WAR CHEST] +${fee_amount} from {name}. Total: ${chest['total']}")

def get_pipeline():
    data = _load()
    pipeline = {}
    for name, info in data.items():
        s = info.get("status", "pending")
        pipeline.setdefault(s, []).append(name)
    return pipeline

def print_dashboard():
    pipeline = get_pipeline()
    print("\n═══════════════════════════════════")
    print("🔱 VANGUARDPRIME — PIPELINE STATUS")
    print("═══════════════════════════════════")
    for status in STATUSES:
        leads = pipeline.get(status, [])
        if leads:
            print(f"  {status.upper()} ({len(leads)}): {', '.join(leads)}")
    print("═══════════════════════════════════\n")
