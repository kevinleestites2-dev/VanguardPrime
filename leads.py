"""
VanguardPrime — leads.py
Target list manager. Realtors + Cash Buyers in Lee County FL.
"""

LEADS = [
    {
        "name": "Larry Johnson",
        "company": "Valor Residential & Commercial Real Estate",
        "type": "realtor",
        "market": "Lee County FL",
        "phone": None,  # Pull from PropertyOnion profile
        "status": "pending",
        "notes": "Investor-focused agent. Listed on PropertyOnion."
    },
    {
        "name": "Patty Walker",
        "company": "RE/MAX Gulf Coast Living",
        "type": "realtor",
        "market": "Lee County FL",
        "phone": None,
        "status": "pending",
        "notes": "Deep local roots. Post-Ian distressed inventory specialist."
    },
    {
        "name": "William Ward",
        "company": "A-Ward Winning Realty",
        "type": "realtor",
        "market": "Lee County FL",
        "phone": None,
        "status": "pending",
        "notes": "Investor-friendly. PropertyOnion listed."
    },
    {
        "name": "Florida Cash Home Buyers",
        "company": "FL Cash Home Buyers LLC",
        "type": "cash_buyer",
        "market": "Lee County FL",
        "phone": None,
        "website": "floridacashhomebuyers.com/lee-county",
        "status": "pending",
        "notes": "Active buyer, renovates and resells. Looking for distressed inventory."
    },
    {
        "name": "House Heroes",
        "company": "House Heroes LLC",
        "type": "cash_buyer",
        "market": "Fort Myers FL",
        "phone": None,
        "status": "pending",
        "notes": "Active Fort Myers cash buyer. Top rated."
    },
    {
        "name": "123SoldCash",
        "company": "123SoldCash.com",
        "type": "cash_buyer",
        "market": "Fort Myers FL",
        "phone": None,
        "status": "pending",
        "notes": "Top rated Fort Myers cash investor."
    },
]

def get_pending_leads():
    return [l for l in LEADS if l["status"] == "pending" and l["phone"]]

def mark_lead(name, status, notes=""):
    for lead in LEADS:
        if lead["name"] == name:
            lead["status"] = status
            if notes:
                lead["notes"] += f" | {notes}"
            return lead
    return None

def add_lead(name, company, lead_type, phone, market="Lee County FL", notes=""):
    LEADS.append({
        "name": name,
        "company": company,
        "type": lead_type,
        "market": market,
        "phone": phone,
        "status": "pending",
        "notes": notes
    })
