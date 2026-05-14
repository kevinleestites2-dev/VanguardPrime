#!/usr/bin/env python3
"""
VanguardPrime v3.0 — The Ghost Operator
The Voice of the Pantheon. Zero cost. Zero calls. Maximum reach.

Channels: LinkedIn DM | Facebook Groups | Email | SMS (Google Voice)
Mission:  Reach realtors + cash buyers in Lee County FL.
          Pitch PropPilot AI deals. Capture emails. Close finder's fees.

Author: The Forgemaster + ZapiaPrime
"""

import os
import sys
from messages import get_message
from targets import REALTORS, CASH_BUYERS
from tracker import log_touch, print_dashboard, get_pipeline

# ── DAILY OPERATIONS PLAYBOOK ─────────────────────────────────────────────────

PLAYBOOK = """
╔══════════════════════════════════════════════════════════════╗
║         🔱 VANGUARDPRIME v3.0 — GHOST OPERATOR              ║
║         Zero cost. Maximum reach. Daily grind.               ║
╚══════════════════════════════════════════════════════════════╝

MISSION: Close first finder's fee. Fund the War Chest.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAILY SEQUENCE — Run this every morning (30 min total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1 — FACEBOOK GROUPS (10 min) 🆓
  Open each group below. Post the DEAL POST or INTRO.
  Check comments/DMs from yesterday. Reply to everyone.
  
  Groups:
  → Southwest FL Real Estate Investors:
    https://www.facebook.com/groups/swflrei/
  → Florida Cash Buyer Network:
    https://www.facebook.com/groups/1690473611174670/
  → Cape Coral & Fort Myers Homebuyers:
    https://www.facebook.com/groups/961127484599630/
  → Fort Myers Real Estate:
    https://www.facebook.com/groups/118678668834600/

  Post script: run  python3 vanguard_prime.py post facebook
  Copy the output → paste into each group.

STEP 2 — LINKEDIN (15 min) 🆓
  Search: "realtor Lee County Florida" or "real estate agent Fort Myers"
  Send connection requests + opening DM to 5 new profiles/day.
  Follow up with anyone who connected but didn't reply (Day 3+).
  
  Message scripts: run  python3 vanguard_prime.py msg linkedin realtor
  
  LinkedIn limits: ~20 connections/day on free account — stay under.

STEP 3 — FOLLOW UP (5 min)
  Check tracker for anyone in "replied" or "interested" status.
  Those get priority. Deal list goes out TODAY.
  
  Dashboard: run  python3 vanguard_prime.py dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHEN SOMEONE RESPONDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  → "Send me your list" / "What do you have?"
    Ask for their email → add to EmailOctopus → send deal list PDF
    Log: python3 vanguard_prime.py update [name] interested

  → "What's the fee?"
    "$500–$2,000 at closing. Nothing upfront."

  → "Are you an agent?"
    "No — I'm a deal sourcer. I pull from public records daily.
    You bring the buyer, I bring the deal, we split the fee."

  → "Send me the addresses"
    Pull from ScoutPrime (lee.realtaxdeed.com / lee.realforeclose.com)
    Send 2-3 specific deals. Keep it concrete.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE SEQUENCE (per lead)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Day 1:  First contact (LinkedIn connect + DM, or FB post)
  Day 3:  Follow up if no reply
  Day 7:  Final touch ("last one from me")
  Day 8+: Mark dead → move to next target

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
METRICS — What success looks like
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Week 1:  5+ leads contacted. 1-2 replies.
  Week 2:  1 email captured. Deal list sent.
  Week 3:  First deal in pipeline.
  Week 4:  First fee. War Chest gets its first deposit. 🔱
"""

def print_message(channel, target_type, variant="primary", name=""):
    context = {"first_name": name.split()[0] if name else "there"}
    msg = get_message(channel, target_type, variant, context)
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📨 {channel.upper()} — {target_type.upper()} — {variant.upper()}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if isinstance(msg, dict):
        print(f"SUBJECT: {msg['subject']}\n")
        print(msg['body'])
    else:
        print(msg)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "help":
        print(PLAYBOOK)

    elif args[0] == "dashboard":
        print_dashboard()

    elif args[0] == "post" and len(args) >= 2:
        channel = args[1]
        variant = args[2] if len(args) > 2 else "primary"
        print_message(channel, "cash_buyer", variant)

    elif args[0] == "msg" and len(args) >= 3:
        channel = args[1]
        target_type = args[2]
        variant = args[3] if len(args) > 3 else "primary"
        name = args[4] if len(args) > 4 else ""
        print_message(channel, target_type, variant, name)

    elif args[0] == "update" and len(args) >= 3:
        name = args[1]
        status = args[2]
        notes = " ".join(args[3:]) if len(args) > 3 else ""
        from tracker import update_status
        update_status(name, status, notes=notes)
        print(f"✅ {name} → {status}")

    elif args[0] == "touch" and len(args) >= 4:
        name = args[1]
        channel = args[2]
        variant = args[3]
        from tracker import log_touch
        log_touch(name, channel, variant)
        print(f"✅ Logged: {name} — {channel} — {variant}")

    else:
        print(PLAYBOOK)
