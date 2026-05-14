"""
VanguardPrime — caller.py
Outbound AI voice call engine.
Stack: LiveKit Agents + Twilio SIP + OpenAI Realtime API
"""

import os
import asyncio
import logging
from script import get_prompt
from logger import log_call

log = logging.getLogger("VanguardCaller")

# ── Keys (loaded from .env) ──────────────────────────────────────────────────
LIVEKIT_URL      = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY  = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")   # e.g. +12395550100
OPENAI_API_KEY     = os.getenv("OPENAI_API_KEY")

async def make_call(lead: dict):
    """
    Places an outbound AI voice call to a lead using LiveKit + Twilio.
    lead = {name, company, phone, type, ...}
    """
    from livekit import api
    from livekit.agents import AgentSession, Agent, RoomInputOptions
    from livekit.agents.llm import ChatContext
    from livekit.plugins import openai, silero, deepgram

    if not lead.get("phone"):
        log.warning(f"No phone number for {lead['name']} — skipping")
        return

    log.info(f"🎙️ Calling {lead['name']} at {lead['phone']}...")

    # Build LiveKit room token for the call
    lk_api = api.LiveKitAPI(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)

    # Create SIP outbound call via Twilio trunk
    # (Twilio SIP trunk must be configured in LiveKit Cloud dashboard)
    room_name = f"vanguard-{lead['name'].lower().replace(' ', '-')}"

    try:
        # Dispatch outbound call
        await lk_api.sip.create_sip_outbound_trunk({
            "name": "twilio-trunk",
            "address": f"sip:{lead['phone'].replace('+', '')}@sip.twilio.com",
            "numbers": [TWILIO_FROM_NUMBER],
        })

        # Agent session with PropPilot pitch prompt
        system_prompt = get_prompt(lead["type"]).replace("[NAME]", lead["name"]).replace("[COMPANY]", lead["company"])

        session = AgentSession(
            stt=deepgram.STT(),
            llm=openai.realtime.RealtimeModel(
                model="gpt-4o-realtime-preview",
                voice="alloy",
                system=system_prompt,
                temperature=0.7,
            ),
            tts=openai.TTS(voice="alloy"),
            vad=silero.VAD.load(),
        )

        # Run the session — agent speaks, listens, responds
        result = await session.run(
            room_name=room_name,
            input_options=RoomInputOptions(auto_subscribe=True)
        )

        # Log outcome
        log_call(
            lead_name=lead["name"],
            company=lead["company"],
            phone=lead["phone"],
            outcome=result.get("outcome", "answered"),
            notes=result.get("summary", ""),
            email_captured=result.get("email_captured")
        )

    except Exception as e:
        log.error(f"Call failed for {lead['name']}: {e}")
        log_call(
            lead_name=lead["name"],
            company=lead["company"],
            phone=lead["phone"],
            outcome="error",
            notes=str(e)
        )
    finally:
        await lk_api.aclose()


async def run_campaign(leads: list):
    """Run calls sequentially with a 30-second gap between each."""
    log.info(f"🔱 VanguardPrime campaign starting — {len(leads)} targets")
    for lead in leads:
        await make_call(lead)
        await asyncio.sleep(30)  # Pause between calls
    log.info("🔱 Campaign complete.")
