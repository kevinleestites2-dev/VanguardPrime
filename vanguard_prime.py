#!/usr/bin/env python3
"""
VanguardPrime v2.0 — The Liaison
The Voice of the Pantheon. External Influence. Real Conversations.

Stack: LiveKit Agents + Twilio SIP + OpenAI Realtime API
Mission: Call realtors and cash buyers in Lee County FL.
         Pitch PropPilot AI. Capture emails. Log to MidasPrime.

Author: The Forgemaster + ZapiaPrime
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from leads import get_pending_leads, LEADS
from caller import run_campaign
from logger import get_summary

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [VANGUARD] %(message)s"
)
log = logging.getLogger("VanguardPrime")

def check_keys():
    required = [
        "LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET",
        "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER",
        "OPENAI_API_KEY"
    ]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        log.error(f"❌ Missing keys: {', '.join(missing)}")
        log.error("Add them to .env and restart.")
        return False
    return True

async def main():
    log.info("🔱 VanguardPrime v2.0 Online.")
    log.info("The Voice of the Pantheon is active.")

    if not check_keys():
        return

    # Get leads with phone numbers
    pending = get_pending_leads()

    if not pending:
        log.warning("⚠️  No leads with phone numbers found.")
        log.warning("Add phone numbers to leads.py and restart.")
        log.info("Current leads awaiting phone numbers:")
        for lead in LEADS:
            log.info(f"  → {lead['name']} ({lead['company']}) — {lead['status']}")
        return

    log.info(f"📋 {len(pending)} leads ready to call:")
    for lead in pending:
        log.info(f"  → {lead['name']} | {lead['company']} | {lead['phone']}")

    # Launch campaign
    await run_campaign(pending)

    # Report summary
    summary = get_summary()
    log.info("═══════════════════════════════════")
    log.info(f"🔱 CAMPAIGN COMPLETE")
    log.info(f"Total calls: {summary['total']}")
    for outcome, count in summary['outcomes'].items():
        log.info(f"  {outcome}: {count}")
    log.info("═══════════════════════════════════")

if __name__ == "__main__":
    asyncio.run(main())
