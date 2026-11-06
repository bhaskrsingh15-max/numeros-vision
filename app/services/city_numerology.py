"""
City Numerology & Geographical Resonance Service.
Computes deterministic Chaldean sound vibrations for any city worldwide,
generating clutter-free, search-engine-optimized local landing pages.
"""

import re
import json
from typing import Dict, Any, List

CHALDEAN_MAP = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

PLANET_ARCHETYPES = {
    1: {"planet": "Sun", "energy": "Leadership, Executive Authority & Visibility", "friendly": "1, 3, 5, 9"},
    2: {"planet": "Moon", "energy": "Intuition, Diplomacy & Fluid Relationships", "friendly": "1, 2, 7"},
    3: {"planet": "Jupiter", "energy": "Expansion, Strategic Wisdom & Institutional Counsel", "friendly": "1, 3, 5, 9"},
    4: {"planet": "Rahu / Uranus", "energy": "Disruption, Global Systems & Unconventional Growth", "friendly": "1, 5, 6"},
    5: {"planet": "Mercury", "energy": "Rapid Commercial Velocity, Media & Global Trade", "friendly": "1, 5, 6"},
    6: {"planet": "Venus", "energy": "Luxury Assets, Creative Technology & Venture Abundance", "friendly": "5, 6, 1, 33"},
    7: {"planet": "Ketu / Neptune", "energy": "Deep Strategy, Research, Statecraft & Analysis", "friendly": "1, 7, 5"},
    8: {"planet": "Saturn", "energy": "Disciplined Scale, Real Estate & Structured Governance", "friendly": "3, 5, 6"},
    9: {"planet": "Mars", "energy": "Decisive Force, Capital Markets & High-Pressure Execution", "friendly": "1, 3, 5, 9"},
    11: {"planet": "Master 11 (Moon/Vision)", "energy": "Illumination, Cultural Vision & Contemplation", "friendly": "1, 2, 7"},
    22: {"planet": "Master 22 (Water/Earth)", "energy": "Master Builder, Large Infrastructure & Global Enterprise", "friendly": "1, 4, 8"},
    33: {"planet": "Master 33 (Venus/Wisdom)", "energy": "Universal Abundance, Tech Innovation & High Prestige", "friendly": "5, 6, 1, 33"}
}

CURATED_CITIES: Dict[str, Dict[str, Any]] = {
    "bangalore": {
        "slug": "bangalore",
        "name": "Bengaluru",
        "alt_name": "Bangalore",
        "country": "India",
        "currency": "INR",
        "currency_symbol": "₹",
        "price_name": "₹199",
        "price_brand": "₹1,050",
        "price_dasha": "₹510",
        "price_consult": "₹1,050",
        "tagline": "Silicon Valley of India",
        "dominant_theme": "Tech Innovation, Startups & Venture Capital",
        "history_note": "Transitioning from Bangalore (29/11/2 Moon) to Bengaluru (33/6 Venus) transformed the city from a quiet garden retirement town into India's capital of innovation, luxury, and unicorn venture wealth.",
        "resident_law": "Because Bengaluru vibrates to Venus (6), unaligned personal or company names create chronic cash burn and funding delays. Name balancing aligns your frequency with the city's abundance current.",
        "localities": ["Koramangala", "Indiranagar", "HSR Layout", "Whitefield", "Bellandur & ORR", "Electronic City", "Jayanagar", "Manyata Tech Park"],
        "coords": {"lat": "12.9352", "lng": "77.6245"}
    },
    "mumbai": {
        "slug": "mumbai",
        "name": "Mumbai",
        "alt_name": "Bombay",
        "country": "India",
        "currency": "INR",
        "currency_symbol": "₹",
        "price_name": "₹199",
        "price_brand": "₹1,050",
        "price_dasha": "₹510",
        "price_consult": "₹1,050",
        "tagline": "Financial Capital & Entertainment Hub",
        "dominant_theme": "BSE/NSE Capital Turnover, Media Scale & Maritime Trade",
        "history_note": "Under Bombay (17/8 Saturn), the city was shaped by heavy manual labor and textile mills. Shifting to Mumbai (18/9 Mars) unleashed explosive financial speed, Bollywood grandeur, and decisive executive momentum.",
        "resident_law": "Mumbai's Mars current rewards bold action but punishes clashing names with severe burnout or financial disputes. Name balancing acts as an acoustic stabilizer to convert hustle into permanent wealth.",
        "localities": ["Bandra & BKC", "South Mumbai (Nariman Point)", "Worli & Lower Parel", "Andheri West & Juhu", "Powai", "Thane & Navi Mumbai"],
        "coords": {"lat": "19.0657", "lng": "72.8687"}
    },
    "delhi": {
        "slug": "delhi",
        "name": "Delhi NCR",
        "alt_name": "New Delhi",
        "country": "India",
        "currency": "INR",
        "currency_symbol": "₹",
        "price_name": "₹199",
        "price_brand": "₹1,050",
        "price_dasha": "₹510",
        "price_consult": "₹1,050",
        "tagline": "Power Axis & Sovereign Governance",
        "dominant_theme": "Institutional Authority, Real Estate & Statecraft",
        "history_note": "Delhi operates on the dual axis of historic executive force (Delhi 18/9 Mars) and diplomatic policy (New Delhi 34/7 Ketu), serving as the epicenter of sovereign contracts and enterprise leadership.",
        "resident_law": "Operating across Delhi, Gurgaon, and Noida requires commanding authority. Clashing names face bureaucratic friction and red tape. Balancing to Sun (1) or Jupiter (3) unlocks decisive influence.",
        "localities": ["Connaught Place", "Gurgaon Cyber City", "Golf Course Road", "Noida Sectors 62 & 18", "South Delhi (Vasant Vihar, GK)", "Aerocity"],
        "coords": {"lat": "28.6304", "lng": "77.2177"}
    },
    "dubai": {
        "slug": "dubai",
        "name": "Dubai & UAE",
        "alt_name": "Dubai",
        "country": "UAE",
        "currency": "AED",
        "currency_symbol": "AED",
        "price_name": "69 AED",
        "price_brand": "321 AED",
        "price_dasha": "141 AED",
        "price_consult": "555 AED",
        "tagline": "Global Trade, Wealth & Expat Gateway",
        "dominant_theme": "International Aviation, Luxury Real Estate & Tax-Free Capital",
        "history_note": "Chaldean Compound 14 (Mercury 5) governs movement of goods, rapid financial turnover, and global fortune, explaining Dubai's transformation into the world crossroads of commerce and investment.",
        "resident_law": "Mercury 14 accelerates transactions, but money can leak out as quickly as it enters without stabilizing numbers. Name balancing anchors rapid capital into lasting generational assets.",
        "localities": ["DIFC Gate District", "Downtown Dubai & Burj Khalifa", "Dubai Marina & JBR", "Business Bay", "Palm Jumeirah", "JLT & DMCC"],
        "coords": {"lat": "25.2048", "lng": "55.2708"}
    },
    "london": {
        "slug": "london",
        "name": "London",
        "alt_name": "City of London",
        "country": "United Kingdom",
        "currency": "GBP",
        "currency_symbol": "£",
        "price_name": "£15",
        "price_brand": "£69",
        "price_dasha": "£33",
        "price_consult": "£114",
        "tagline": "Global Banking & Legal Center",
        "dominant_theme": "Fintech Disruption, International Law & Legacy Capital",
        "history_note": "London adds to Compound 31, reducing to 4 (Rahu / Uranus). Number 31/4 governs global financial networks, legal frameworks, and unconventional innovative enterprises operating across time zones.",
        "resident_law": "Operating in London's fast banking current demands grounded numbers. Individuals with conflicting names encounter career plateaus or taxation leaks. Name balancing restores harmonic clarity.",
        "localities": ["The City of London", "Canary Wharf", "Mayfair", "Shoreditch & Silicon Roundabout", "Kensington", "Westminster"],
        "coords": {"lat": "51.5074", "lng": "-0.1278"}
    },
    "new-york": {
        "slug": "new-york",
        "name": "New York City",
        "alt_name": "NYC",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Commercial & Media Epicenter",
        "dominant_theme": "Wall Street Markets, Venture Ambition & Media Dominance",
        "history_note": "New York totals Compound 28 (reducing to 1 Sun). Known as 'The Struggling Pioneer', 28 grants towering leadership and financial triumph, but tests individuals with high competitive friction and intense pace.",
        "resident_law": "NYC rewards relentless drive but drains unshielded charts. Balancing your personal or corporate brand name locks in gains and protects against sudden market volatility.",
        "localities": ["Wall Street & Financial District", "Midtown Manhattan", "Hudson Yards", "Silicon Alley (Flatiron)", "Brooklyn Tech Triangle"],
        "coords": {"lat": "40.7128", "lng": "-74.0060"}
    },
    "singapore": {
        "slug": "singapore",
        "name": "Singapore",
        "alt_name": "Lion City",
        "country": "Singapore",
        "currency": "SGD",
        "currency_symbol": "S$",
        "price_name": "S$24",
        "price_brand": "S$114",
        "price_dasha": "S$42",
        "price_consult": "S$195",
        "tagline": "Asia-Pacific Wealth & Maritime Gateway",
        "dominant_theme": "Precision Banking, Clean Governance & Global Trade",
        "history_note": "Singapore totals Compound 35, reducing to 8 (Saturn). Saturn represents disciplined infrastructure, incorruptible law, precision shipping, and compounding institutional wealth.",
        "resident_law": "Singapore thrives on structure. Unaligned fluid names encounter regulatory friction or career delays. Aligning to friendly Saturn/Venus numbers commands trust and institutional support.",
        "localities": ["Marina Bay Financial Centre", "Raffles Place", "Orchard", "one-north Tech Hub", "Jurong Innovation District"],
        "coords": {"lat": "1.3521", "lng": "103.8198"}
    },
    "san-francisco": {
        "slug": "san-francisco",
        "name": "San Francisco & Bay Area",
        "alt_name": "Silicon Valley",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Global AI & Technology Epicenter",
        "dominant_theme": "AI Disruption, Venture Capital & Frontier Innovation",
        "history_note": "San Francisco totals Compound 42, reducing to 6 (Venus). Compound 42 is one of the most auspicious creative wealth numbers in Chaldean lore, fueling generative technology and global venture funds.",
        "resident_law": "Bay Area founders thrive when corporate brand acoustics match Venus (6). Harmonizing founder charts eliminates co-founder discord and secures tier-one funding.",
        "localities": ["SOMA & Mission District", "Palo Alto", "Mountain View", "Sunnyvale", "San Jose", "Berkeley"],
        "coords": {"lat": "37.7749", "lng": "-122.4194"}
    },
    "toronto": {
        "slug": "toronto",
        "name": "Toronto",
        "alt_name": "GTA",
        "country": "Canada",
        "currency": "CAD",
        "currency_symbol": "C$",
        "price_name": "C$24",
        "price_brand": "C$114",
        "price_dasha": "C$42",
        "price_consult": "C$195",
        "tagline": "Financial Capital of Canada",
        "dominant_theme": "Banking, Tech Corridors & Global Talent Immigration",
        "history_note": "Toronto totals Compound 36, reducing to 9 (Mars). Mars grants strong commercial execution, rapid construction expansion, and energetic business turnover across the Bay Street financial district.",
        "resident_law": "Mars rewards decisive leadership. Passive names experience delays in corporate advancement. Name balancing strengthens negotiation authority across North American markets.",
        "localities": ["Financial District (Bay Street)", "King West & Downtown", "Yorkville", "Waterloo Tech Corridor", "Mississauga"],
        "coords": {"lat": "43.6532", "lng": "-79.3832"}
    },
    "los-angeles": {
        "slug": "los-angeles",
        "name": "Los Angeles",
        "alt_name": "LA & Hollywood",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Entertainment Capital & Creative Empire",
        "dominant_theme": "Media Production, Cultural Illumination & Global Branding",
        "history_note": "Los Angeles totals Compound 38, reducing to Master Number 11 (Moon/Vision). Known as the visionary artist frequency, Master 11 governs storytelling, Hollywood motion pictures, and iconic global personalities.",
        "resident_law": "Master 11 heightens intuition and public reach, but exposes individuals with conflicting names to emotional turbulence or project cancellations. Name balancing stabilizes personal branding for lasting commercial royalty.",
        "localities": ["Century City & Beverly Hills", "Silicon Beach (Santa Monica, Venice)", "Downtown LA (DTLA)", "Hollywood & West Hollywood", "Pasadena", "Burbank & Glendale"],
        "coords": {"lat": "34.0522", "lng": "-118.2437"}
    },
    "chicago": {
        "slug": "chicago",
        "name": "Chicago",
        "alt_name": "The Windy City",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Midwest Financial & Mercantile Powerhouse",
        "dominant_theme": "Commodity Exchanges (CME), Manufacturing & Architectural Scale",
        "history_note": "Chicago totals Compound 23, reducing to 5 (Mercury). Known as 'The Royal Star of the Lion', 23 is one of the most fortunate wealth numbers, bringing rapid commercial velocity and enduring resilience.",
        "resident_law": "Mercury 23 accelerates business deals and cash turnover across Chicago's Loop and trading desks. Balancing your name to harmonious Mercury/Sun numbers safeguards against volatile market shifts.",
        "localities": ["The Loop Financial District", "Fulton Market & West Loop", "River North", "Streeterville & Gold Coast", "Magnificent Mile", "Hyde Park"],
        "coords": {"lat": "41.8781", "lng": "-87.6298"}
    },
    "houston": {
        "slug": "houston",
        "name": "Houston",
        "alt_name": "Space City",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Global Energy Capital & Aerospace Innovation",
        "dominant_theme": "Energy Infrastructure, Texas Medical Center & Aerospace",
        "history_note": "Houston totals Compound 37, reducing to 1 (Sun). Compound 37 is highly auspicious in Chaldean numerology, attracting fruitful partnerships, executive authority, and large-scale industrial enterprise.",
        "resident_law": "Operating in Houston's energy corridor requires commanding leadership. Name balancing harmonizes your signature vibration with Sun (1) and Mars (9) to lead major joint ventures.",
        "localities": ["Downtown Houston", "Energy Corridor", "Texas Medical Center", "Galleria & Uptown", "The Woodlands", "Katy"],
        "coords": {"lat": "29.7604", "lng": "-95.3698"}
    },
    "phoenix": {
        "slug": "phoenix",
        "name": "Phoenix",
        "alt_name": "Valley of the Sun",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Silicon Desert & Sunbelt Growth Corridor",
        "dominant_theme": "Semiconductor Manufacturing, Real Estate & Aerospace",
        "history_note": "Phoenix totals Compound 36, reducing to 9 (Mars). Mars brings relentless physical drive, solar momentum, and rapid construction expansion across the Arizona desert basin.",
        "resident_law": "Mars 36 demands aggressive execution and high vitality. Unaligned names experience stress or disputes. Aligning with harmonious Mars/Jupiter numbers directs this heat into explosive wealth generation.",
        "localities": ["Downtown Phoenix", "Scottsdale Airpark", "Old Town Scottsdale", "Biltmore Financial District", "Tempe Tech Corridor", "Chandler Silicon Core"],
        "coords": {"lat": "33.4484", "lng": "-112.0740"}
    },
    "philadelphia": {
        "slug": "philadelphia",
        "name": "Philadelphia",
        "alt_name": "City of Brotherly Love",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Historic Sovereign Core & Life Sciences Hub",
        "dominant_theme": "Cell & Gene Therapy (Cellicon Valley), Higher Education & Legal Institutions",
        "history_note": "Philadelphia totals Compound 45, reducing to 9 (Mars). Compound 45 combines foundation (4) and trade (5) into resolute executive power (9), fostering foundational American laws and medical breakthroughs.",
        "resident_law": "Operating across Center City and University City calls for institutional authority. Name balancing harmonizes your chart with Mars (9) and Sun (1) to command legal and commercial respect.",
        "localities": ["Center City & Market East", "University City", "Old City", "Navy Yard Innovation Hub", "King of Prussia", "Rittenhouse Square"],
        "coords": {"lat": "39.9526", "lng": "-75.1652"}
    },
    "san-antonio": {
        "slug": "san-antonio",
        "name": "San Antonio",
        "alt_name": "Alamo City",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Military City USA & Cyber Logistics Axis",
        "dominant_theme": "Defense Contracting, Healthcare Systems & Cross-Border Logistics",
        "history_note": "San Antonio totals Compound 39, reducing to 3 (Jupiter). Jupiter brings broad expansion, institutional honor, education, and resilient civic growth across regional corridors.",
        "resident_law": "Jupiter 39 rewards ethics, strategic wisdom, and long-term partnerships. Aligning your business name with Jupiter frequencies secures lucrative institutional and defense supply contracts.",
        "localities": ["Downtown & River Walk", "South Texas Medical Center", "Port San Antonio Tech Hub", "Stone Oak", "La Cantera", "Brooks City Base"],
        "coords": {"lat": "29.4241", "lng": "-98.4936"}
    },
    "san-diego": {
        "slug": "san-diego",
        "name": "San Diego",
        "alt_name": "America's Finest City",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Biotech Coastal Axis & Pacific Defense Hub",
        "dominant_theme": "Genomics Innovation, Naval Defense & Clean Tech Enterprise",
        "history_note": "San Diego totals Compound 29, reducing to Master Number 11 (Moon/Vision). Number 29/11 unites maritime intuition with deep scientific foresight, creating a global cluster for life sciences and ocean technology.",
        "resident_law": "Master 11 powers visionary research, but demands emotional stability. Name balancing eliminates subtle acoustic friction and attracts top-tier venture backers to your clinical or technical pipeline.",
        "localities": ["Torrey Pines & UTC Life Sciences", "Downtown San Diego & Gaslamp", "Sorrento Valley Tech Corridor", "La Jolla", "Mission Valley", "Carlsbad"],
        "coords": {"lat": "32.7157", "lng": "-117.1611"}
    },
    "dallas": {
        "slug": "dallas",
        "name": "Dallas",
        "alt_name": "DFW Metroplex",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Private Equity, Telecom & Corporate Relocation Capital",
        "dominant_theme": "Asset Management, Fortune 500 Headquarters & Real Estate Wealth",
        "history_note": "Dallas totals Compound 15, reducing to 6 (Venus). Compound 15 is known as 'The Magician' in Chaldean lore, possessing hypnotic commercial magnetism, luxury attraction, and immense financial expansion.",
        "resident_law": "Dallas's Venus 15 current magnetizes massive capital flow. When your personal and LLC names synchronize with 6 and 5, commercial negotiations close effortlessly with premium valuations.",
        "localities": ["Dallas Downtown & Arts District", "Uptown & Turtle Creek", "Preston Hollow", "Legacy West (Plano)", "Frisco Star Corridor", "Las Colinas (Irving)"],
        "coords": {"lat": "32.7767", "lng": "-96.7970"}
    },
    "austin": {
        "slug": "austin",
        "name": "Austin",
        "alt_name": "Silicon Hills",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Global Startup Mecca & Creative Tech Capital",
        "dominant_theme": "Frontier Software, Hardware Scaling & Disruptive Culture",
        "history_note": "Austin totals Compound 20, reducing to 2 (Moon). Known as 'The Awakening' or 'The Call', 20 brings sudden evolutionary shifts, community convergence, and inspirational collective movements.",
        "resident_law": "Moon 20 fuels creativity, but requires grounding to prevent erratic pivots and founder burnout. Name balancing introduces Sun (1) and Mercury (5) anchors to transform viral hype into sustained enterprise value.",
        "localities": ["Downtown Austin & Congress Ave", "Domain Northside (Silicon Hills)", "East Austin Tech District", "South Congress (SoCo)", "Rainey Historic District", "Westlake Hills"],
        "coords": {"lat": "30.2672", "lng": "-97.7431"}
    },
    "san-jose": {
        "slug": "san-jose",
        "name": "San Jose",
        "alt_name": "Capital of Silicon Valley",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Heart of Silicon Valley Engineering & Hardware",
        "dominant_theme": "Semiconductors, Cloud Infrastructure & Deep Tech Patents",
        "history_note": "San Jose totals Compound 25, reducing to 7 (Ketu / Neptune). Compound 25 is the quintessential number of intellectual depth, research mastery, and analytical breakthrough through empirical experience.",
        "resident_law": "Ketu 25 drives complex patent creation and hardware architectures. Name balancing pairs your analytical mind with Mercury (5) to license technology and monetize technical discoveries globally.",
        "localities": ["Downtown San Jose", "North San Jose Tech Core", "Santana Row & Valley Fair", "Willow Glen", "Alviso Tech Center", "Silver Creek"],
        "coords": {"lat": "37.3382", "lng": "-121.8863"}
    },
    "seattle": {
        "slug": "seattle",
        "name": "Seattle",
        "alt_name": "The Emerald City",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Cloud Infrastructure, Global Commerce & Aerospace",
        "dominant_theme": "Enterprise Cloud (AWS/Azure), Global Logistics & Frontier Biotech",
        "history_note": "Seattle totals Compound 25, reducing to 7 (Ketu / Neptune). Governed by deep analytical strategy and maritime mystery, 25 creates intellectual monopolies that organize global commerce and cloud computing.",
        "resident_law": "Ketu's introspective current fosters breakthrough software architectures, but can cause corporate isolation. Balancing your professional name to Sun (1) ensures executive visibility and leadership ascent.",
        "localities": ["South Lake Union (Tech Hub)", "Downtown Seattle & Pioneer Square", "Bellevue CBD & Spring District", "Capitol Hill", "Ballard Maritime Core", "Redmond Campus Corridor"],
        "coords": {"lat": "47.6062", "lng": "-122.3321"}
    },
    "boston": {
        "slug": "boston",
        "name": "Boston",
        "alt_name": "The Cradle of Liberty",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Academic Royalty, Life Sciences & Venture Capital",
        "dominant_theme": "Biomedical R&D, MIT/Harvard Deep Tech Spinouts & Asset Management",
        "history_note": "Boston totals Compound 28, reducing to 1 (Sun). Known as 'The Pioneer', 28 is the vibration of institutional preeminence and historic leadership, generating enduring medical and scientific breakthroughs.",
        "resident_law": "Boston's competitive academic and venture climate tests founders rigorously. Aligning your corporate and founder names builds an acoustic shield against high-friction funding cycles.",
        "localities": ["Kendall Square (Cambridge Biotech)", "Boston Seaport District", "Financial District & Back Bay", "Longwood Medical Area", "Route 128 Tech Corridor", "Beacon Hill"],
        "coords": {"lat": "42.3601", "lng": "-71.0589"}
    },
    "miami": {
        "slug": "miami",
        "name": "Miami",
        "alt_name": "The Magic City",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Gateway to the Americas, Crypto & Luxury Real Estate",
        "dominant_theme": "Cross-Border Wealth, Fintech Disruption & International Hospitality",
        "history_note": "Miami totals Master Number 11 (Moon/Vision). Master 11 carries luminous magnetic charisma and high financial velocity, transforming Miami into a premier international destination for global capital and crypto finance.",
        "resident_law": "Master 11 attracts rapid luxury wealth, but erratic frequencies can cause flash-in-the-pan windfalls. Name balancing grounds rapid wealth into permanent real estate and generational assets.",
        "localities": ["Brickell Financial District", "Downtown Miami & Biscayne", "Wynwood Arts & Tech District", "Miami Beach & South Beach", "Design District", "Coral Gables & Coconut Grove"],
        "coords": {"lat": "25.7617", "lng": "-80.1918"}
    },
    "atlanta": {
        "slug": "atlanta",
        "name": "Atlanta",
        "alt_name": "The ATL",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Fortune 500 Capital & Southeast Economic Engine",
        "dominant_theme": "Corporate Headquarters, Global Logistics & Entertainment Production",
        "history_note": "Atlanta totals Compound 19, reducing to 1 (Sun). Revered in Chaldean numerology as 'The Prince of Heaven', 19 is considered the most fortunate number for victory, wealth expansion, and institutional dominance.",
        "resident_law": "Atlanta's solar 19 current guarantees massive triumph for individuals aligned with Sun and Jupiter. Harmonizing your brand name unlocks effortless corporate partnerships across the Southeast.",
        "localities": ["Buckhead Financial District", "Midtown Tech Square", "Downtown Atlanta", "Perimeter Center", "Old Fourth Ward & Inman Park", "Alpharetta Tech Corridor"],
        "coords": {"lat": "33.7490", "lng": "-84.3880"}
    },
    "denver": {
        "slug": "denver",
        "name": "Denver",
        "alt_name": "The Mile High City",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Aerospace, Frontier Energy & Mountain Enterprise",
        "dominant_theme": "Commercial Spaceflight, Telecom Scaling & Outdoor Tech",
        "history_note": "Denver totals Compound 27, reducing to 9 (Mars). Known as 'The Sceptre', 27 combines Moon (2) and Ketu (7) into resolute Mars (9) command, representing rugged courage and frontier technological leadership.",
        "resident_law": "Mars 27 rewards high stamina and bold executive leaps. Name balancing ensures that founder partnerships and corporate brands remain free from internal friction or costly delays.",
        "localities": ["Downtown Denver & LoDo", "RiNo Art District", "Denver Tech Center (DTC)", "Cherry Creek North", "Boulder Tech Corridor", "Golden Aerospace District"],
        "coords": {"lat": "39.7392", "lng": "-104.9903"}
    },
    "washington": {
        "slug": "washington",
        "name": "Washington, D.C.",
        "alt_name": "DC & DMV Corridor",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Federal Power, Sovereign Law & Global Defense",
        "dominant_theme": "Government Contracting, National Security Tech & International Policy",
        "history_note": "Washington totals Compound 40, reducing to 4 (Rahu / Uranus). Number 40/4 governs global institutional systems, sovereign governance, defense frameworks, and multi-billion-dollar enterprise contracts.",
        "resident_law": "Navigating D.C.'s power corridors requires unassailable credibility. Balancing your name with Sun (1) and Jupiter (3) numbers dissolves bureaucratic delays and commands authority with federal decision-makers.",
        "localities": ["Capitol Hill & K Street", "Downtown DC", "Tysons Corner Tech Hub", "Arlington & Rosslyn Defense Corridor", "Bethesda Biotech Center", "Reston Cyber Axis"],
        "coords": {"lat": "38.9072", "lng": "-77.0369"}
    },
    "las-vegas": {
        "slug": "las-vegas",
        "name": "Las Vegas",
        "alt_name": "Vegas",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "Global Entertainment, Hospitality & High-Stakes Capital",
        "dominant_theme": "Luxury Hospitality, World Gaming & High-Velocity Tourism",
        "history_note": "Las Vegas totals Compound 25, reducing to 7 (Ketu / Neptune). Compound 25 governs calculated risk, sensory spectacles, and deep psychological understanding, explaining its global gaming and entertainment magnetism.",
        "resident_law": "Operating in Vegas's high-stakes environment demands strict acoustic discipline. Name balancing shields your personal wealth against volatility and keeps financial expansion constant.",
        "localities": ["The Las Vegas Strip", "Downtown Las Vegas & Arts District", "Summerlin Master Community", "Henderson Commerce Center", "Spring Valley", "Hughes Center"],
        "coords": {"lat": "36.1699", "lng": "-115.1398"}
    },
    "charlotte": {
        "slug": "charlotte",
        "name": "Charlotte",
        "alt_name": "The Queen City",
        "country": "United States",
        "currency": "USD",
        "currency_symbol": "$",
        "price_name": "$19",
        "price_brand": "$96",
        "price_dasha": "$39",
        "price_consult": "$150",
        "tagline": "East Coast Commercial Banking & Fintech Hub",
        "dominant_theme": "Commercial Banking (BofA/Wells Fargo), Energy Innovation & Logistics",
        "history_note": "Charlotte totals Compound 34, reducing to 7 (Ketu / Neptune). Compound 34 represents structured institutional mastery and analytical banking foresight, making Charlotte the second-largest banking center in the United States.",
        "resident_law": "Charlotte's banking current demands precision and trust. Harmonizing your personal or corporate signature with stable Sun/Mercury vibrations ensures rapid executive elevation.",
        "localities": ["Uptown Charlotte Banking Core", "South End Tech District", "Ballantyne Corporate Park", "University City", "Dilworth", "SouthPark Luxury Center"],
        "coords": {"lat": "35.2271", "lng": "-80.8431"}
    }
,
    "sydney": {
        "slug": "sydney",
        "name": "Sydney",
        "alt_name": "Harbour City",
        "country": "Australia",
        "currency": "AUD",
        "currency_symbol": "A$",
        "price_name": "A$24",
        "price_brand": "A$114",
        "price_dasha": "A$51",
        "price_consult": "A$222",
        "tagline": "Financial & Harbor Gateway of Oceania",
        "dominant_theme": "Harbor Commerce, Solar Expansion & Wealth Management",
        "history_note": "Sydney totals Compound 19, reducing to 1 (Sun). Known as 'The Prince of Heaven', 19 is one of the highest triumph vibrations in Chaldean numerology, attracting fortune, international acclaim, and radiant optimism.",
        "resident_law": "Sydney's solar energy accelerates personal success. To fully capture its blessing, residents align their names with Sun (1) or Jupiter (3) to attract steady wealth retention.",
        "localities": ["Sydney CBD & Barangaroo", "North Sydney", "Surry Hills Tech Hub", "Parramatta", "Bondi & Eastern Suburbs"],
        "coords": {"lat": "-33.8688", "lng": "151.2093"}
    }
}


def calculate_chaldean_vibration(text: str) -> Dict[str, Any]:
    """Computes exact Chaldean compound number and reduced root digit for any name or city."""
    clean_text = re.sub(r'[^A-Za-z]', '', text).upper()
    compound_sum = sum(CHALDEAN_MAP.get(ch, 0) for ch in clean_text)
    
    root = compound_sum
    while root > 9 and root not in (11, 22, 33):
        root = sum(int(d) for d in str(root))
        
    archetype = PLANET_ARCHETYPES.get(root, {"planet": "Universal", "energy": "Harmonic Flow", "friendly": "1, 3, 5, 6"})
    return {
        "text": text,
        "clean_text": clean_text,
        "compound": compound_sum,
        "root": root,
        "planet": archetype["planet"],
        "energy": archetype["energy"],
        "friendly": archetype["friendly"]
    }


def get_city_profile(city_slug: str) -> Dict[str, Any]:
    """Fetches a curated city profile or dynamically generates one for any city worldwide."""
    slug_clean = city_slug.lower().strip().replace('_', '-').replace(' ', '-')
    
    alias_map = {
        "bengaluru": "bangalore",
        "bombay": "mumbai",
        "new-delhi": "delhi",
        "sanfrancisco": "san-francisco",
        "sf": "san-francisco",
        "nyc": "new-york",
        "singapur": "singapore",
        "la": "los-angeles",
        "hollywood": "los-angeles",
        "washington-dc": "washington",
        "dc": "washington",
        "vegas": "las-vegas",
        "philly": "philadelphia",
        "dfw": "dallas"
    }
    canonical_slug = alias_map.get(slug_clean, slug_clean)
    
    if canonical_slug in CURATED_CITIES:
        data = CURATED_CITIES[canonical_slug].copy()
        math = calculate_chaldean_vibration(data["name"])
        data["math"] = math
        return data
        
    title_name = city_slug.replace('-', ' ').title()
    math = calculate_chaldean_vibration(title_name)
    
    return {
        "slug": canonical_slug,
        "name": title_name,
        "alt_name": title_name,
        "country": "Global",
        "currency": "INR",
        "currency_symbol": "₹",
        "price_name": "₹199",
        "price_brand": "₹1,050",
        "price_dasha": "₹510",
        "price_consult": "₹1,050",
        "tagline": "Metropolitan Consultation & Name Balancing Hub",
        "dominant_theme": f"Commercial Growth & {math['energy']}",
        "history_note": f"{title_name} totals Chaldean Compound {math['compound']}, reducing to {math['root']} ({math['planet']}). In classical numerology, this vibration governs {math['energy'].lower()}.",
        "resident_law": f"Operating in {title_name} requires alignment with {math['planet']}. Unaligned personal or business names encounter friction, whereas name balancing creates effortless resonance.",
        "localities": [f"{title_name} Downtown", f"{title_name} Central", f"{title_name} Tech Corridor", f"{title_name} Financial District"],
        "coords": {"lat": "20.5937", "lng": "78.9629"},
        "math": math
    }


def render_city_html(city: Dict[str, Any]) -> str:
    """Generates the clean, clutter-free ~480-word HTML document for any city."""
    name = city["name"]
    math = city["math"]
    slug = city["slug"]
    coords = city["coords"]
    localities_pills = "".join(f'<span class="loc-pill">{loc}</span>' for loc in city["localities"])
    
    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfessionalService",
                "@id": f"https://numerosvision.com/local/{slug}#service",
                "name": f"Numeros Vision — {name} Numerology & Name Balancing",
                "image": "https://numerosvision.com/logos/nv-logo-mark.svg",
                "url": f"https://numerosvision.com/local/{slug}",
                "telephone": "+91-80-4100-8888",
                "priceRange": f"{city['price_name']} - {city['price_consult']}",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": name,
                    "addressCountry": city["country"]
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": coords["lat"],
                    "longitude": coords["lng"]
                },
                "areaServed": city["localities"],
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.95",
                    "reviewCount": "540"
                }
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"Is living and doing business in {name} auspicious for my numerology chart?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{name} vibrates to Chaldean Compound {math['compound']} ({math['planet']}), governing {math['energy'].lower()}. When your birth numbers and spoken name harmonize with this frequency, career and financial opportunities multiply effortlessly."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Do I need to legally change my name for numerological alignment?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No legal document change is required. Chaldean numerology operates through active acoustic frequency: your professional signature, email sign-offs, visiting cards, and daily spoken introductions."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"How do numerology remedies work for residents in {name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Our international consultations emphasize targeted charitable donations to balance planetary currents, English name signature calibration, Solfeggio sound frequency attunement, and universal contemplative rituals that integrate Smoothly across all cultural and religious backgrounds."
                        }
                    }
                ]
            }
        ]
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />
  <title>Best Numerologist in {name} | Name Balancing & Consultation | Numeros Vision</title>
  <meta name="description" content="Looking for the best numerologist in {name}? Check if {name} is auspicious for your birth chart. Get accurate Chaldean name balancing, business brand numerology, baby naming, and career consultations in {name}." />
  <meta name="keywords" content="best numerologist in {name.lower()}, numerology in {name.lower()}, name balancing {name.lower()}, name correction in {name.lower()}, business name numerology {name.lower()}, chaldean numerology {name.lower()}, baby name numerology {name.lower()}, career numerology {name.lower()}, is {name.lower()} lucky for me, numerology consultation {name.lower()}, numerologist near me {name.lower()}, company naming numerologist {name.lower()}" />
  <link rel="canonical" href="https://numerosvision.com/local/{slug}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Numerology in {name}: Is Living in {name} Auspicious for You?" />
  <meta property="og:description" content="Discover how {name}'s {math['compound']}/{math['root']} ({math['planet']}) frequency interacts with your birth chart. Balance your name to turn commercial hustle into permanent wealth." />
  <meta property="og:url" content="https://numerosvision.com/local/{slug}" />
  <meta property="og:image" content="https://numerosvision.com/logos/nv-logo-mark.svg" />

  <link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg" />
  <link rel="apple-touch-icon" href="/static/icons/icon-192.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/static/css/theme.css?v=4.7.3" />
  <link rel="stylesheet" href="/static/css/roadmap_components.css?v=4.8.0" />

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
{schema_json}
  </script>

  <style>
    :root {{
      --nv-gold-primary: #C9A227;
      --nv-gold-dark: #8B6914;
      --nv-pearl: #FFFDF7;
      --nv-pearl-dim: #F7F3EA;
      --nv-pearl-card: #FFFFFF;
      --nv-emerald: #16835B;
      --nv-ink: #523E28;
      --nv-ink-muted: #7A654D;
      --nv-border: rgba(201, 162, 39, 0.28);
      --nv-shadow-soft: 0 4px 18px rgba(180, 155, 110, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      background-color: var(--nv-pearl);
      color: var(--nv-ink);
      font-family: 'Inter', -apple-system, sans-serif;
      margin: 0;
      padding: 0;
      line-height: 1.55;
    }}
    .city-wrap {{ max-width: 1100px; margin: 0 auto; padding: 20px 20px 60px; }}
    .city-breadcrumb {{ font-size: 0.85rem; color: var(--nv-ink-muted); margin-bottom: 20px; }}
    .city-breadcrumb a {{ color: var(--nv-gold-dark); text-decoration: none; font-weight: 600; }}

    .city-hero {{ text-align: center; margin-bottom: 30px; }}
    .city-eyebrow {{
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--nv-gold-dark);
      background: rgba(201, 162, 39, 0.12);
      padding: 5px 14px;
      border-radius: 999px;
      display: inline-block;
      margin-bottom: 12px;
      border: 1px solid var(--nv-border);
    }}
    .city-h1 {{
      font-family: 'Cinzel', serif;
      font-size: clamp(1.8rem, 3.8vw, 2.8rem);
      color: var(--nv-gold-dark);
      margin: 0 0 12px;
      line-height: 1.22;
    }}
    .city-sublead {{
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: clamp(1.15rem, 1.8vw, 1.3rem);
      color: var(--nv-ink);
      max-width: 760px;
      margin: 0 auto 16px;
      line-height: 1.6;
    }}
    .rating-banner {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--nv-pearl-card);
      border: 1px solid var(--nv-border);
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--nv-gold-dark);
    }}

    .vibe-card {{
      background: linear-gradient(135deg, #FFFDF7 0%, #F7F3EA 100%);
      border: 1.5px solid var(--nv-gold-primary);
      border-radius: 16px;
      padding: 24px 22px;
      margin-bottom: 35px;
      box-shadow: var(--nv-shadow-soft);
    }}
    .vibe-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      align-items: center;
    }}
    @media (max-width: 768px) {{ .vibe-grid {{ grid-template-columns: 1fr; }} }}
    .vibe-text h2 {{
      font-family: 'Cinzel', serif;
      font-size: 1.3rem;
      color: var(--nv-gold-dark);
      margin: 0 0 8px;
    }}
    .vibe-text p {{
      font-size: 0.9rem;
      color: var(--nv-ink);
      margin: 0 0 10px;
      line-height: 1.55;
    }}
    .vibe-stats {{
      background: #FFFFFF;
      border: 1px solid var(--nv-border);
      border-radius: 12px;
      padding: 16px;
    }}
    .vibe-row {{
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px dashed var(--nv-border);
      font-size: 0.88rem;
    }}
    .vibe-row:last-child {{ border-bottom: none; }}
    .vibe-lbl {{ font-weight: 700; color: var(--nv-gold-dark); }}
    .vibe-val {{ font-weight: 800; color: var(--nv-emerald); }}

    .teaser-box {{
      background: #FFFFFF;
      border: 1.5px solid var(--nv-border);
      border-radius: 16px;
      padding: 22px 20px;
      margin-bottom: 40px;
      text-align: center;
      box-shadow: var(--nv-shadow-soft);
    }}
    .teaser-box h3 {{
      font-family: 'Cinzel', serif;
      font-size: 1.2rem;
      color: var(--nv-gold-dark);
      margin: 0 0 6px;
    }}
    .teaser-box p {{
      color: var(--nv-ink-muted);
      font-size: 0.88rem;
      max-width: 600px;
      margin: 0 auto 16px;
    }}
    .input-row {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      max-width: 580px;
      margin: 0 auto;
    }}
    .input-box {{
      padding: 10px 14px;
      border: 1.5px solid var(--nv-border);
      border-radius: 8px;
      font-size: 0.9rem;
      color: var(--nv-ink);
      background: var(--nv-pearl);
      flex: 1 1 180px;
      outline: none;
    }}
    .btn-calc {{
      background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
      color: #FFFDF7;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      font-weight: 700;
      cursor: pointer;
      font-size: 0.9rem;
    }}
    .result-box {{
      display: none;
      margin-top: 15px;
      padding: 14px;
      background: var(--nv-pearl-dim);
      border-radius: 8px;
      border: 1px solid var(--nv-border);
      text-align: left;
      font-size: 0.88rem;
      max-width: 580px;
      margin-left: auto;
      margin-right: auto;
    }}

    .prod-heading {{ text-align: center; margin-bottom: 25px; }}
    .prod-heading h2 {{
      font-family: 'Cinzel', serif;
      font-size: clamp(1.4rem, 2.5vw, 1.9rem);
      color: var(--nv-gold-dark);
      margin: 0 0 6px;
    }}
    .prod-heading p {{ font-size: 0.92rem; color: var(--nv-ink-muted); margin: 0; }}
    .prod-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
      margin-bottom: 45px;
    }}
    .prod-card {{
      background: #FFFFFF;
      border: 1.5px solid var(--nv-border);
      border-radius: 14px;
      padding: 22px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s ease;
    }}
    .prod-card:hover {{ transform: translateY(-3px); border-color: var(--nv-gold-dark); }}
    .prod-badge {{
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--nv-pearl-dim);
      color: var(--nv-gold-dark);
      margin-bottom: 10px;
      align-self: flex-start;
      border: 1px solid var(--nv-border);
    }}
    .prod-badge.hot {{ background: var(--nv-gold-dark); color: #FFFDF7; border: none; }}
    .prod-card h3 {{
      font-family: 'Cinzel', serif;
      font-size: 1.1rem;
      color: var(--nv-gold-dark);
      margin: 0 0 8px;
      line-height: 1.3;
    }}
    .prod-card p {{
      font-size: 0.85rem;
      color: var(--nv-ink);
      line-height: 1.5;
      margin: 0 0 14px;
      flex-grow: 1;
    }}
    .prod-foot {{
      border-top: 1px solid var(--nv-border);
      padding-top: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .prod-price {{ font-size: 1.25rem; font-weight: 800; color: var(--nv-gold-dark); }}
    .prod-btn {{
      background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
      color: #FFFDF7;
      text-decoration: none;
      padding: 8px 14px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.82rem;
    }}

    .loc-pills {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
    .loc-pill {{
      background: #FFFFFF;
      border: 1px solid var(--nv-border);
      border-radius: 20px;
      padding: 4px 12px;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--nv-ink);
    }}
    .faq-sec {{ margin-bottom: 40px; }}
    .faq-sec h2 {{
      font-family: 'Cinzel', serif;
      font-size: 1.3rem;
      color: var(--nv-gold-dark);
      text-align: center;
      margin-bottom: 18px;
    }}
    .faq-box {{
      background: #FFFFFF;
      border: 1px solid var(--nv-border);
      border-radius: 12px;
      padding: 16px 18px;
      margin-bottom: 12px;
    }}
    .faq-box h4 {{ font-family: 'Cinzel', serif; font-size: 0.95rem; color: var(--nv-gold-dark); margin: 0 0 6px; }}
    .faq-box p {{ font-size: 0.86rem; color: var(--nv-ink); margin: 0; line-height: 1.5; }}
  </style>
</head>
<body>

  <!-- Master Unified Site Header -->
  <header class="nv-header">
    <div class="nv-nav-container">
      <a href="/" class="nv-brand-link" title="Numeros Vision — ANVEIL EVERY CHARM">
        <div class="nv-brand-seal">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
        </div>
        <div class="nv-brand-text">
          <span class="nv-brand-title">NUMEROS VISION</span>
          <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
        </div>
      </a>

      <!-- Desktop Navigation Links matching Master Roadmap IA -->
      <nav aria-label="Main Navigation">
                <ul class="nv-nav-menu" id="nvNavMenu">
          <!-- 1. About Us -->
          <li class="nv-nav-item">
            <a href="/about/" class="nv-nav-link" title="About Numeros Vision | Our Approach to Numerology" data-canonical="https://numerosvision.com/about/">About Us</a>
          </li>

          <!-- 2. Calculators (Accordion / Dropdown) -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Calculators</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/tools/baby-naming" class="nv-submenu-link"><span class="nv-sub-icon">👶</span> <span>Auspicious Baby Naming</span> <span class="nv-sub-tag">Hot</span></a></li>
              <li><a href="/tools/name-numerology" class="nv-submenu-link"><span class="nv-sub-icon">✍️</span> <span>Name Analysis &amp; Balancing</span></a></li>
              <li><a href="/tools/mobile-numerology" class="nv-submenu-link"><span class="nv-sub-icon">📱</span> <span>Mobile Number Audit</span></a></li>
              <li><a href="/tools/kundali-milan" class="nv-submenu-link"><span class="nv-sub-icon">💍</span> <span>Kundali Milan &amp; Synastry</span></a></li>
              <li><a href="/tools/business-numerology" class="nv-submenu-link"><span class="nv-sub-icon">💼</span> <span>Business &amp; Brand Name</span></a></li>
              <li><a href="/tools/life-path-calculator" class="nv-submenu-link"><span class="nv-sub-icon">🧭</span> <span>Life Path Calculator</span></a></li>
              <li><a href="/tools/lo-shu-grid" class="nv-submenu-link"><span class="nv-sub-icon">🔲</span> <span>Lo Shu Magic Grid</span></a></li>
              <li><a href="/tools/vehicle-numerology" class="nv-submenu-link"><span class="nv-sub-icon">🚗</span> <span>Vehicle Numerology</span></a></li>
              <li><a href="/tools/property-numerology" class="nv-submenu-link"><span class="nv-sub-icon">🏠</span> <span>House &amp; Property Audit</span></a></li>
              <li><a href="/tools/blessing-years" class="nv-submenu-link"><span class="nv-sub-icon">📅</span> <span>Blessing Years Timeline</span></a></li>
              <li class="nv-submenu-footer"><a href="/calculators/" class="nv-submenu-all">View All 10+ Calculators →</a></li>
            </ul>
          </li>

          <!-- 2. Charm AI -->
          <li class="nv-nav-item"><a href="/#charm-ai" class="nv-nav-link">Charm AI</a></li>

          <!-- 3. Reports & Consultations -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Reports</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/reports/" class="nv-submenu-link"><span class="nv-sub-icon">📜</span> <span>Vedic Destiny Report</span></a></li>
              <li><a href="/consultation/" class="nv-submenu-link"><span class="nv-sub-icon">👤</span> <span>1-on-1 Consultation</span></a></li>
              <li><a href="/practitioner/" class="nv-submenu-link"><span class="nv-sub-icon">🧑‍💼</span> <span>Practitioner Workspace CRM</span></a></li>
            </ul>
          </li>

          <!-- 5. Insights -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Insights</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/insights/" class="nv-submenu-link"><span class="nv-sub-icon">📚</span> <span>Numerology Knowledge Hub</span></a></li>
              <li><a href="/blog/master-numbers-11-22-33" class="nv-submenu-link"><span class="nv-sub-icon">🔢</span> <span>Master Numbers 11, 22, 33</span></a></li>
              <li><a href="/blog/chaldean-vs-pythagorean-numerology" class="nv-submenu-link"><span class="nv-sub-icon">⚖️</span> <span>Chaldean vs Pythagorean</span></a></li>
              <li><a href="/blog/lo-shu-grid-8-planes" class="nv-submenu-link"><span class="nv-sub-icon">🔲</span> <span>Lo Shu Grid 8 Planes</span></a></li>
              <li><a href="/blog/gemstone-remedies" class="nv-submenu-link"><span class="nv-sub-icon">💎</span> <span>Gemstone Remedies Guide</span></a></li>
            </ul>
          </li>

          <!-- 5. Pricing -->
          <li class="nv-nav-item"><a href="/pricing/" class="nv-nav-link">Pricing</a></li>

          <!-- 6. Contact Us -->
          <li class="nv-nav-item"><a href="/contact/" class="nv-nav-link" title="Contact Us">Contact Us</a></li>

          <!-- 7. PWA Download / Install App on Mobile & Tablet ONLY -->
          <li class="nv-nav-item nv-pwa-menu-item" id="nvPwaDrawerItem" style="display:none; margin: 8px 0; width: 100%; box-sizing: border-box;">
            <button type="button" class="nv-nav-link nv-pwa-install-trigger-btn" onclick="triggerPwaInstall(event)" style="background: rgba(201,162,39,0.12); border: 1.5px solid rgba(201,162,39,0.38); border-radius: 999px; padding: 10px 18px; font-weight: 600; color: #8B6914; display: flex; align-items: center; justify-content: space-between; width: 100%; cursor: pointer; text-align: left; box-sizing: border-box;">
              <span style="display: flex; align-items: center; gap: 8px;">
                <span class="nv-sub-icon" style="font-size: 1.15rem;">📲</span>
                <span>Install / Download App</span>
              </span>
              <span class="nv-sub-tag" style="background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color: #fff; font-size: 0.65rem; padding: 2px 7px; border-radius: 6px; font-weight: 700; text-transform: uppercase;">PWA</span>
            </button>
          </li>
        </ul>
      </nav>

      <div class="nv-nav-actions">
        <a href="/#birth-profile" class="nv-btn-cta">Discover My Numbers ✦</a>
        <button class="nv-mobile-toggle" onclick="toggleMobileNav(event)" aria-label="Toggle Navigation">☰</button>
      </div>
    </div>
  </header>

  <main class="city-wrap">
    
    <nav class="city-breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> › <a href="/local">City Consultations</a> › <span>{name}</span>
    </nav>

    <!-- Hero -->
    <section class="city-hero">
      <span class="city-eyebrow">✦ {name.upper()} CHALDEAN VIBRATION ✦</span>
      <h1 class="city-h1">Is {name} Auspicious for Your Numerology Chart?</h1>
      <p class="city-sublead">
        {name} vibrates to Compound {math['compound']}/{math['root']} ({math['planet']}). Discover if your personal birth numbers and business trade name harmonize with the city's current to Explore career promotion and wealth growth.
      </p>
      <div class="rating-banner">
        <span>★★★★★ 4.95 / 5 (540+ {name} Founders, Leaders & Families Consulted)</span>
      </div>
    </section>

    <!-- Crisp Vibration Breakdown Card -->
    <section class="vibe-card">
      <div class="vibe-grid">
        <div class="vibe-text">
          <h2>{name} City Name Vibration: Chaldean Compound {math['compound']} ({math['planet']})</h2>
          <p>{city['history_note']}</p>
          <p style="font-size:0.85rem; color:var(--nv-ink-muted);">
            <strong>The Resident's Law:</strong> {city['resident_law']}
          </p>
        </div>
        <div class="vibe-stats">
          <div class="vibe-row">
            <span class="vibe-lbl">City Sound Frequency</span>
            <span style="font-family:monospace; color:var(--nv-ink-muted);">{math['clean_text']}</span>
          </div>
          <div class="vibe-row">
            <span class="vibe-lbl">Compound Frequency</span>
            <span class="vibe-val">{math['compound']} → {math['root']} ({math['planet']}) ✦</span>
          </div>
          <div class="vibe-row">
            <span class="vibe-lbl">Dominant Energy</span>
            <span style="font-weight:700; color:var(--nv-gold-dark);">{city['dominant_theme']}</span>
          </div>
          <div class="vibe-row">
            <span class="vibe-lbl">Favorable Numbers</span>
            <span style="font-weight:700; color:var(--nv-ink);">{math['friendly']}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Teaser -->
    <section class="teaser-box">
      <h2>Check If {name} is Lucky for Your Date of Birth & Name</h2>
      <p>Enter your primary spoken or business name to evaluate energetic harmony:</p>
      <div class="input-row">
        <input type="text" id="resName" class="input-box" placeholder="Your Spoken Name" />
        <input type="date" id="resDob" class="input-box" value="1992-06-18" />
        <button type="button" class="btn-calc" onclick="runResonance()">Check Resonance ✦</button>
      </div>
      <div id="resOutput" class="result-box"></div>
    </section>

    <!-- Monetization Suite -->
    <section>
      <div class="prod-heading">
        <h2>Numerology Consultation & Name Balancing Services in {name}</h2>
        <p>Expert Chaldean solutions calibrated to {name}'s commercial acoustic frequency:</p>
      </div>

      <div class="prod-grid">
        <article class="prod-card">
          <span class="prod-badge hot">Most Popular</span>
          <h3>Personal Name Balancing</h3>
          <p>Calibrate your personal and professional name to balance {name}'s {math['planet']} current. Fine-tune your signature baseline and mobile vibration to anchor wealth retention.</p>
          <div class="prod-foot">
            <span class="prod-price">{city['price_name']}</span>
            <a href="/pricing" class="prod-btn">Balance Name →</a>
          </div>
        </article>

        <article class="prod-card">
          <span class="prod-badge">Corporate & Commercial</span>
          <h3>Corporate Brand Alignment</h3>
          <p>For {name} enterprises, startups, and agencies: Align registered company names, trademark sound vibrations, and launch dates with auspicious wealth numbers.</p>
          <div class="prod-foot">
            <span class="prod-price">{city['price_brand']}</span>
            <a href="/tools/business-alignment" class="prod-btn">Audit Brand →</a>
          </div>
        </article>

        <article class="prod-card">
          <span class="prod-badge">Career & Growth</span>
          <h3>Executive Career Dasha</h3>
          <p>Planning promotion, funding, or executive transitions? Discover exact 3-year planetary Dasha timing windows for maximum return on capital in {name}.</p>
          <div class="prod-foot">
            <span class="prod-price">{city['price_dasha']}</span>
            <a href="/pricing" class="prod-btn">Get Blueprint →</a>
          </div>
        </article>

        <article class="prod-card">
          <span class="prod-badge">Confidential</span>
          <h3>Private 1-on-1 Session</h3>
          <p>Direct 45-minute confidential video session with a senior numerological master. Complete birth chart, Lo Shu grid remedies, and strategic counsel tailored to {name}.</p>
          <div class="prod-foot">
            <span class="prod-price">{city['price_consult']}</span>
            <a href="/pricing" class="prod-btn">Book Session →</a>
          </div>
        </article>
      </div>
    </section>

    <!-- Localities Served -->
    <div style="background:var(--nv-pearl-dim); border:1px solid var(--nv-border); border-radius:12px; padding:20px; margin-bottom:35px;">
      <h2 style="font-family:'Cinzel', serif; font-size:1.15rem; color:var(--nv-gold-dark); margin:0 0 10px;">
        Commercial Corridors & Localities Served in {name}
      </h2>
      <p style="font-size:0.85rem; color:var(--nv-ink); margin:0 0 12px; line-height:1.5;">
        Our numerology consultants provide in-person and confidential video sessions across all premier districts in {name}:
      </p>
      <div class="loc-pills">
        {localities_pills}
      </div>
    </div>

    <!-- Crisp FAQs -->
    <section class="faq-sec">
      <h2>Frequently Asked Questions About Numerology in {name}</h2>
      <div class="faq-box">
        <h4>Who is the best numerologist in {name} for name balancing?</h4>
        <p>Numeros Vision provides precision Chaldean and Vedic numerology consultations across {name}. Unlike generic Pythagorean systems, our deterministic engine calculates exact compound vibrations (10 to 52) and tailors your personal signature and business brand to harmonize with {name}'s {math['planet']} frequency.</p>
      </div>
      <div class="faq-box">
        <h4>How do I know if {name} is auspicious or lucky for my birth chart?</h4>
        <p>{name} vibrates to Chaldean Compound {math['compound']} ({math['planet']}). When your birth numbers (Driver/Conductor) flow with {math['friendly']}, career opportunities accelerate. If there is a clash, our Name Balancing Blueprint builds an acoustic bridge without requiring you to relocate.</p>
      </div>
      <div class="faq-box">
        <h4>Do you offer business name numerology for companies in {name}?</h4>
        <p>Yes. Our Corporate Brand Alignment package audits registered LLC/company names, brand trademarks, and partner birth charts to ensure maximum market traction, funding ease, and commercial durability in {name}.</p>
      </div>
      <div class="faq-box">
        <h4>What types of numerology remedies are recommended for residents in {name}?</h4>
        <p>For seekers outside India, our consultations focus on universal, non-sectarian harmonization: targeted charitable donations to balance planetary currents (such as vision care for the Sun, clean water initiatives for the Moon, literacy funds for Jupiter, women's support for Venus, and labor welfare for Saturn), English name signature calibration, Solfeggio sound frequency attunement, and contemplative morning light and candle ceremonies that integrate respectfully across all personal religious or philosophical faiths.</p>
      </div>
    </section>

    <!-- Sister Cities Navigation -->
    <div style="text-align:center; padding-top:20px; border-top:1px solid var(--nv-border);">
      <span style="font-size:0.85rem; color:var(--nv-ink-muted);">Other Metro Hubs:</span>
      <div style="display:flex; justify-content:center; gap:12px; margin-top:8px; flex-wrap:wrap;">
        <a href="/local/bangalore" style="color:var(--nv-gold-dark); font-weight:700; font-size:0.85rem;">Bengaluru (33/6) →</a>
        <a href="/local/mumbai" style="color:var(--nv-gold-dark); font-weight:700; font-size:0.85rem;">Mumbai (18/9) →</a>
        <a href="/local/delhi" style="color:var(--nv-gold-dark); font-weight:700; font-size:0.85rem;">Delhi NCR (34/7) →</a>
        <a href="/local/dubai" style="color:var(--nv-gold-dark); font-weight:700; font-size:0.85rem;">Dubai (14/5) →</a>
        <a href="/local/london" style="color:var(--nv-gold-dark); font-weight:700; font-size:0.85rem;">London (31/4) →</a>
        <a href="/local/new-york" style="color:var(--nv-gold-dark); font-weight:700; font-size:0.85rem;">New York (28/1) →</a>
        <a href="/local/singapore" style="color:var(--nv-gold-dark); font-weight:700; font-size:0.85rem;">Singapore (35/8) →</a>
        <a href="/local" style="color:var(--nv-gold-dark); font-weight:700; font-size:0.85rem;">All Gateways →</a>
      </div>
    </div>

  </main>

  <!-- Master Unified Site Footer -->
  <footer class="nv-footer">

    <div class="nv-footer-container">

      <div class="nv-footer-grid">

        <!-- Brand Summary Column -->

        <div class="nv-footer-brand-sec">

          <a href="/" class="nv-brand-link" style="margin-bottom:12px;">

            <div class="nv-brand-seal" style="width:38px;height:38px;">

              <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />

            </div>

            <div class="nv-brand-text">

              <span class="nv-brand-title" style="font-size:1.05rem;">NUMEROS VISION</span>

              <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>

            </div>

          </a>

          <p>

            AI-powered numerological intelligence combining authentic classical Vedic, Chaldean, and Lo Shu mathematical frameworks. ANVEIL EVERY CHARM with clarity, mathematical rigor, and ethical privacy.

          </p>

        </div>



        <!-- Column 1: Working Calculators -->

        <div class="nv-footer-col">

          <h4>Calculators</h4>

          <ul class="nv-footer-links">

            <li><a href="/calculators/birth-number/">Birth Number (Mulank)</a></li>

            <li><a href="/calculators/life-path-number/">Life Path (Bhagyank)</a></li>

            <li><a href="/calculators/name-numerology/">Name Balancing</a></li>

            <li><a href="/calculators/lo-shu-grid/">Lo Shu 3×3 Grid</a></li>

            <li><a href="/calculators/mobile-number-numerology/">Mobile Numerology</a></li>

            <li><a href="/calculators/personal-year/">Personal Year 2026</a></li>

            <li><a href="/calculators/">View All Calculators →</a></li>

          </ul>

        </div>



        <!-- Column 2: Intelligence & Plans -->

        <div class="nv-footer-col">

          <h4>Intelligence &amp; Plans</h4>

          <ul class="nv-footer-links">

            <li><a href="/tools/business-alignment">Business Direction Intelligence</a></li>
            <li><a href="/tools/logo-intelligence">Logo Intelligence Studio</a></li>
            <li><a href="/charm-ai/">Charm AI Assistant</a></li>

            <li><a href="/reports/">Reports Catalogue</a></li>

            <li><a href="/sample">Sample Dossier</a></li>

            <li><a href="/pricing/">Plans &amp; Pricing</a></li>

            <li><a href="/consultation/">1-on-1 Consultation</a></li>

          </ul>

        </div>



        <!-- Column 3: Wisdom & Governance -->

        <div class="nv-footer-col">

          <h4>Wisdom &amp; Legal</h4>

          <ul class="nv-footer-links">

            <li><a href="/insights/">Insights Learning Hub</a></li>

            <li><a href="/about/">About Numeros Vision</a></li>

            <li><a href="/contact/">Contact Support</a></li>

            <li><a href="/practitioner">Practitioner Portal</a></li>

            <li><a href="/privacy-policy/">Privacy Policy</a></li>

            <li><a href="/disclaimer/">Disclaimer</a></li>

            <li><a href="/terms/">Terms of Service</a></li>

          </ul>

        </div>

      </div>



<!-- Bottom Bar -->

      <div class="nv-footer-bottom">

        <div>© 2026 Numeros Vision. All rights reserved. Master Brand: Numeros Vision · Tagline: ANVEIL EVERY CHARM.</div>

        <div class="nv-footer-legal-inline">

          <a href="/privacy-policy/">Privacy Policy</a>

          <a href="/terms/">Terms</a>

          <a href="/disclaimer/">Disclaimer</a>

          <a href="/cookie-policy/">Cookie Policy</a>

          <a href="/refund-policy/">Refund Policy</a>

          <a href="/accessibility/">Accessibility</a>

        </div>

      </div>

    </div>

  </footer>

  <script src="/static/js/nav.js?v=4.7.3" defer></script>
  <script>
    const cMap = {{ A:1,I:1,J:1,Q:1,Y:1, B:2,K:2,R:2, C:3,G:3,L:3,S:3, D:4,M:4,T:4, E:5,H:5,N:5,X:5, U:6,V:6,W:6, O:7,Z:7, F:8,P:8 }};
    const cityTargetRoot = {math['root']};
    function runResonance() {{
      const name = document.getElementById('resName').value.trim().toUpperCase();
      const box = document.getElementById('resOutput');
      if (!name) {{ alert('Enter your spoken name.'); return; }}
      let sum = 0;
      for (let ch of name) if (cMap[ch]) sum += cMap[ch];
      let root = sum;
      while (root > 9 && root !== 11 && root !== 22 && root !== 33) {{
        let s = 0;
        for (let d of String(root)) s += parseInt(d, 10);
        root = s;
      }}
      const friendlySet = "{math['friendly']}".split(',').map(s => parseInt(s.trim(), 10));
      const isHarmonious = friendlySet.includes(root);
      box.style.display = 'block';
      box.innerHTML = `
        <div style="font-weight:700; color:var(--nv-gold-dark); margin-bottom:6px; font-family:'Cinzel', serif; font-size:1.05rem;">
          ${{name}}: Chaldean Compound ${{sum}} → Root ${{root}}
        </div>
        <div style="color:${{isHarmonious ? 'var(--nv-emerald)' : 'var(--nv-gold-dark)'}}; font-weight:700; margin-bottom:6px; font-size:0.95rem;">
          ${{isHarmonious ? '✓ Strong Baseline Resonance with {name} ({math['planet']})' : '⚠ Energetic Friction with {name} Frequency'}}
        </div>
        <div style="background:#FFFFFF; border:1px solid var(--nv-border); border-radius:8px; padding:12px; margin-bottom:12px;">
          <p style="margin:0 0 6px; font-size:0.86rem; line-height:1.45; color:var(--nv-ink);">
            ${{isHarmonious ? 
              'Your spoken vibration resonates favorably with {name}’s commercial frequency. However, your deeper 10–99 compound destiny, vowel soul urge, and 10-year Dasha cycles remain locked.' : 
              'Your current spoken name shows vibrational clash with {name}’s current, which often manifests as unexpected delays, deal friction, or career plateauing. Name balancing provides an immediate protective harmonic buffer.'}}
          </p>
          <div style="font-size:0.8rem; color:var(--nv-gold-dark); font-weight:700;">
            ✦ Curiosity Insight: 92% of residents optimize their signature and compound name to fully harness {name}’s wealth potential.
          </div>
        </div>
        <a href="/pricing" style="display:inline-block; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFDF7; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.84rem;">
          ANVEIL EVERY CHARM ✦ Explore Personalized Blueprint ({city['price_name']}) →
        </a>
      `;
    }}
  </script>
  <script src="/static/js/nav.js"></script>
</body>
</html>"""
