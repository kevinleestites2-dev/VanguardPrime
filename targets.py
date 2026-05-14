"""
VanguardPrime — targets.py
Ghost Operator target list.
Realtors + Cash Buyers in Lee County / Fort Myers FL.
"""

REALTORS = [
    {
        "name": "Larry Johnson",
        "company": "Valor Residential & Commercial Real Estate",
        "type": "realtor",
        "linkedin": "search",  # Search: "Larry Johnson Valor Residential Fort Myers"
        "email": None,
        "facebook": None,
        "status": "pending",
    },
    {
        "name": "Patty Walker",
        "company": "RE/MAX Gulf Coast Living",
        "type": "realtor",
        "linkedin": "search",
        "email": None,
        "facebook": None,
        "status": "pending",
    },
    {
        "name": "William Ward",
        "company": "A-Ward Winning Realty",
        "type": "realtor",
        "linkedin": "search",
        "email": None,
        "facebook": None,
        "status": "pending",
    },
]

CASH_BUYERS = [
    {
        "name": "Southwest Florida Real Estate Investors Group",
        "type": "facebook_group",
        "url": "https://www.facebook.com/groups/swflrei/",
        "focus": "Fort Myers, Cape Coral, Lehigh Acres — cash buyers actively posting",
        "action": "post_deal",
        "status": "pending",
    },
    {
        "name": "Florida Cash Buyer Network",
        "type": "facebook_group",
        "url": "https://www.facebook.com/groups/1690473611174670/",
        "focus": "Statewide cash buyers, active Florida deals",
        "action": "post_deal",
        "status": "pending",
    },
    {
        "name": "Cape Coral & Fort Myers Homebuyers",
        "type": "facebook_group",
        "url": "https://www.facebook.com/groups/961127484599630/",
        "focus": "Buyers + sellers + realtors in Cape Coral / Fort Myers",
        "action": "post_deal",
        "status": "pending",
    },
    {
        "name": "Fort Myers Real Estate",
        "type": "facebook_group",
        "url": "https://www.facebook.com/groups/118678668834600/",
        "focus": "Local real estate portal — listings and buyers",
        "action": "post_deal",
        "status": "pending",
    },
]

ALL_TARGETS = REALTORS + CASH_BUYERS
