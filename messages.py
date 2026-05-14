"""
VanguardPrime — messages.py
All outreach copy. Tuned per channel and target type.
Golden Rule: Lead with THEIR earn, never OUR value.
"""

# ── LinkedIn DMs — Realtors ───────────────────────────────────────────────────

LINKEDIN_REALTOR_CONNECTION = """
Hey {first_name} — noticed you're active in the Lee County investor space.
I source off-market distressed properties (tax deeds, pre-foreclosure) before they hit auction.
Looking for one solid local agent to work these deals with. Worth a quick chat?
"""

LINKEDIN_REALTOR_FOLLOWUP = """
Hey {first_name} — just following up on my last message.
We're pulling live inventory from Lee County Clerk records daily — pre-auction,
$40K–$400K range, most before anyone else sees them.
If you have buyers looking for distressed deals, I'd love to send you a sample list.
No commitment — just want to see if it's a fit. 🤝
"""

LINKEDIN_REALTOR_LAST = """
{first_name} — last one from me, I promise.
I have 3 active Lee County tax deed properties I'm trying to move this week.
If you have a cash buyer for any of these, there's a finder's fee in it for you.
Just say the word and I'll send the addresses.
"""

# ── LinkedIn DMs — Cash Buyers ────────────────────────────────────────────────

LINKEDIN_BUYER_CONNECTION = """
Hey {first_name} — I source off-market distressed deals in Lee County FL
(tax deeds, pre-foreclosures, pre-auction). Pulling live from county clerk records daily.
If you're still buying in that market, I'd love to put deals in front of you.
What's your buy box look like?
"""

# ── Facebook Group Posts ──────────────────────────────────────────────────────

FACEBOOK_POST_DEAL = """
🏚️ OFF-MARKET LEE COUNTY — PRE-AUCTION INVENTORY

Just pulled today's tax deed + foreclosure filings from Lee County Clerk.
Several properties in Fort Myers, Cape Coral, and Lehigh Acres range.
Price range: $45K – $280K. Most need work. All pre-auction.

If you're a cash buyer or have a buyer looking for distressed inventory in SWFL,
drop a comment or DM me — I'll send you the details directly.

Finder's fee model. Nothing upfront. 🔱
"""

FACEBOOK_BUYER_INTRO = """
👋 New here — I'm Kevin, based in Fort Myers.

I pull off-market distressed properties from Lee County public records daily —
tax deed filings, lis pendens, pre-foreclosure notices — before they go to auction.

Looking to connect with serious cash buyers in the area.
If you want to be on my daily deal list, drop your info below or DM me.

No spam. Just deals. 💰
"""

# ── Email — Cold Outreach ─────────────────────────────────────────────────────

EMAIL_SUBJECT_REALTOR = "Off-market Lee County deals — pre-auction inventory for your buyers"

EMAIL_BODY_REALTOR = """Hi {first_name},

My name is Kevin — I source off-market distressed properties in Lee County
directly from county clerk records (tax deeds, pre-foreclosures, lis pendens)
before they go to auction.

I'm looking for one investor-friendly agent in the area to work these deals with.
The model is simple: I bring the deals, you bring the buyers, we split the finder's fee.

I have active inventory in Fort Myers, Cape Coral, and Lehigh Acres right now —
properties in the $45K–$280K range that most people won't see for weeks.

Would it make sense to send you a sample list this week?

— Kevin
PropPilot AI | Fort Myers, FL
"""

EMAIL_SUBJECT_BUYER = "Pre-auction Lee County distressed inventory — daily deal list"

EMAIL_BODY_BUYER = """Hi {first_name},

My name is Kevin. I pull off-market properties in Lee County from public records
every day — tax deed filings, foreclosures, pre-auction — before they hit any
marketplace.

I'm looking to build a short list of serious cash buyers to send deals to directly.
Finder's fee at closing. Nothing upfront.

Current inventory includes Fort Myers, Cape Coral, and Lehigh Acres.
Most properties in the $45K–$280K range, varying condition.

If you want to see what I'm working with, I can send the current list today.

— Kevin
PropPilot AI | Fort Myers, FL
"""

# ── Google Voice SMS ──────────────────────────────────────────────────────────

SMS_REALTOR = """Hi {first_name}, this is Kevin in Fort Myers — I source off-market tax deed + foreclosure properties in Lee County before auction. Looking for a local agent to work these deals with. Have buyers for distressed inventory? Happy to send a sample list. -Kevin"""

SMS_BUYER = """Hi {first_name}, Kevin here — Fort Myers. I pull pre-auction distressed deals in Lee County daily from public records. Looking for serious cash buyers. Want to see the current list? -Kevin"""


def get_message(channel, target_type, variant="primary", context={}):
    """
    Returns the right message for channel + target_type.
    channel: linkedin | facebook | email | sms
    target_type: realtor | cash_buyer
    variant: primary | followup | last
    context: dict with name fields
    """
    first_name = context.get("first_name", "there")

    if channel == "linkedin":
        if target_type == "realtor":
            templates = {
                "primary": LINKEDIN_REALTOR_CONNECTION,
                "followup": LINKEDIN_REALTOR_FOLLOWUP,
                "last": LINKEDIN_REALTOR_LAST,
            }
            return templates.get(variant, LINKEDIN_REALTOR_CONNECTION).format(first_name=first_name)
        elif target_type == "cash_buyer":
            return LINKEDIN_BUYER_CONNECTION.format(first_name=first_name)

    elif channel == "facebook":
        if variant == "intro":
            return FACEBOOK_BUYER_INTRO
        return FACEBOOK_POST_DEAL

    elif channel == "email":
        if target_type == "realtor":
            return {"subject": EMAIL_SUBJECT_REALTOR, "body": EMAIL_BODY_REALTOR.format(first_name=first_name)}
        elif target_type == "cash_buyer":
            return {"subject": EMAIL_SUBJECT_BUYER, "body": EMAIL_BODY_BUYER.format(first_name=first_name)}

    elif channel == "sms":
        if target_type == "realtor":
            return SMS_REALTOR.format(first_name=first_name)
        elif target_type == "cash_buyer":
            return SMS_BUYER.format(first_name=first_name)

    return None
