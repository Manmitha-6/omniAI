import os
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


# ============================================================
# CATEGORY DEFINITIONS
# ============================================================

FASHION_PRODUCTS = [
    "dress", "dresses",
    "shirt", "shirts",
    "tshirt", "t-shirt", "t-shirts",
    "jeans",
    "trousers", "pants",
    "kurti", "kurtis",
    "saree", "sarees",
    "lehenga", "lehengas",
    "top", "tops",
    "skirt", "skirts",
    "jacket", "jackets",
    "hoodie", "hoodies",
    "sweater", "sweaters",
    "coat", "coats",
    "blazer", "blazers",
    "shorts",
    "shoes",
    "sneakers",
    "running shoes",
    "sandals",
    "heels",
    "boots",
    "slippers",
    "watch", "watches",
    "bag", "bags",
    "handbag", "handbags",
    "backpack", "backpacks",
    "wallet", "wallets",
    "belt", "belts",
    "sunglasses",
    "jewellery", "jewelry",
    "necklace", "necklaces",
    "earrings",
    "bracelet", "bracelets",
    "ring", "rings"
]


ELECTRONICS_PRODUCTS = [
    "phone", "phones",
    "smartphone", "smartphones",
    "mobile", "mobiles",
    "iphone",
    "android",
    "laptop", "laptops",
    "computer", "computers",
    "tablet", "tablets",
    "ipad",
    "smartwatch", "smartwatches",
    "headphones",
    "earphones",
    "earbuds",
    "airpods",
    "speaker", "speakers",
    "television", "televisions",
    "tv",
    "smart tv",
    "monitor", "monitors",
    "keyboard", "keyboards",
    "mouse",
    "printer", "printers",
    "camera", "cameras",
    "dslr",
    "mirrorless camera",
    "power bank", "power banks",
    "charger", "chargers",
    "router", "routers",
    "gaming console",
    "playstation",
    "xbox",
    "refrigerator",
    "fridge",
    "washing machine",
    "air conditioner",
    "ac",
    "microwave",
    "air fryer",
    "vacuum cleaner"
]


FOOD_PRODUCTS = [
    "biryani",
    "pizza",
    "burger",
    "ice cream",
    "icecream",
    "cake",
    "cakes",
    "chocolate",
    "sandwich",
    "sandwiches",
    "pasta",
    "noodles",
    "momos",
    "dosa",
    "idli",
    "vada",
    "fried rice",
    "shawarma",
    "rolls",
    "chicken",
    "fried chicken",
    "meals",
    "thali",
    "dessert",
    "desserts",
    "coffee",
    "tea",
    "juice",
    "milkshake",
    "restaurant",
    "restaurants",
    "cafe",
    "cafes",
    "hotel",
    "hotels",
    "food",
    "groceries",
    "snacks"
]


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):
    if not text:
        return ""

    text = text.lower().strip()

    # Telugu punctuation / common variations
    text = text.replace("లో", " in ")
    text = text.replace("లోని", " in ")

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    return text


# ============================================================
# PRODUCT DETECTION
# ============================================================

def detect_product(text):

    text_lower = text.lower()

    all_products = (
        sorted(FASHION_PRODUCTS, key=len, reverse=True),
        sorted(ELECTRONICS_PRODUCTS, key=len, reverse=True),
        sorted(FOOD_PRODUCTS, key=len, reverse=True)
    )

    for product_list in all_products:
        for product in product_list:

            if product in text_lower:

                if product in FASHION_PRODUCTS:
                    return "fashion", product

                if product in ELECTRONICS_PRODUCTS:
                    return "electronics", product

                if product in FOOD_PRODUCTS:
                    return "food", product

    return None, ""


# ============================================================
# TELUGU FOOD WORDS
# ============================================================

TELUGU_FOOD = [
    "బిర్యానీ",
    "బిర్యాని",
    "ఐస్ క్రీమ్",
    "ఐస్క్రీమ్",
    "పిజ్జా",
    "బర్గర్",
    "కేక్",
    "చాక్లెట్",
    "దోస",
    "ఇడ్లీ",
    "మోమోస్",
    "నూడుల్స్",
    "రెస్టారెంట్",
    "హోటల్",
    "ఫుడ్"
]


TELUGU_ELECTRONICS = [
    "మొబైల్",
    "ఫోన్",
    "ల్యాప్‌టాప్",
    "ల్యాప్టాప్",
    "టీవీ",
    "కెమెరా",
    "హెడ్‌ఫోన్స్",
    "ఇయర్‌ఫోన్స్",
    "స్పీకర్",
    "టాబ్లెట్"
]


TELUGU_FASHION = [
    "డ్రెస్",
    "చొక్కా",
    "షర్ట్",
    "జీన్స్",
    "చీర",
    "కుర్తీ",
    "షూస్",
    "చెప్పులు",
    "బ్యాగ్",
    "వాచ్",
    "నెక్లెస్",
    "చెవిపోగులు"
]


# ============================================================
# TELUGU PRODUCT DETECTION
# ============================================================

def detect_telugu_product(text):

    for word in TELUGU_FOOD:
        if word in text:
            return "food", word

    for word in TELUGU_ELECTRONICS:
        if word in text:
            return "electronics", word

    for word in TELUGU_FASHION:
        if word in text:
            return "fashion", word

    return None, ""


# ============================================================
# LOCATION DETECTION
# ============================================================

LOCATIONS = {
    "hyderabad": "Hyderabad",
    "హైదరాబాద్": "Hyderabad",

    "bangalore": "Bangalore",
    "bengaluru": "Bangalore",

    "chennai": "Chennai",

    "mumbai": "Mumbai",

    "delhi": "Delhi",
    "new delhi": "Delhi",

    "pune": "Pune",

    "kolkata": "Kolkata",

    "goa": "Goa",

    "vizag": "Visakhapatnam",
    "visakhapatnam": "Visakhapatnam",

    "vijayawada": "Vijayawada",

    "tirupati": "Tirupati"
}


def detect_location(text):

    text_lower = text.lower()

    for key, value in LOCATIONS.items():

        if key in text_lower:
            return value

    return ""


# ============================================================
# BUDGET DETECTION
# ============================================================

def detect_budget(text):

    patterns = [

        r"(?:under|below|less than|within|upto|up to)\s*[₹rs.]?\s*([\d,]+)",

        r"[₹]\s*([\d,]+)",

        r"(?:rs|inr)\s*([\d,]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text.lower()
        )

        if match:

            try:
                return int(
                    match.group(1).replace(",", "")
                )
            except:
                pass

    return None


# ============================================================
# GENDER
# ============================================================

def detect_gender(text):

    text = text.lower()

    if "women" in text or "woman" in text or "female" in text:
        return "women"

    if "men" in text or "man" in text or "male" in text:
        return "men"

    if "boys" in text or "boy" in text:
        return "boys"

    if "girls" in text or "girl" in text:
        return "girls"

    return ""


# ============================================================
# OCCASION
# ============================================================

def detect_occasion(text):

    text = text.lower()

    occasions = [
        "birthday",
        "wedding",
        "party",
        "college",
        "office",
        "work",
        "casual",
        "gym",
        "running",
        "travel",
        "festival",
        "dinner",
        "family"
    ]

    for occasion in occasions:

        if occasion in text:
            return occasion

    return ""


# ============================================================
# PLATFORM
# ============================================================

def detect_platform(text):

    text = text.lower()

    platforms = [
        "myntra",
        "ajio",
        "amazon",
        "flipkart",
        "meesho",
        "nykaa",
        "croma",
        "reliance digital"
    ]

    for platform in platforms:

        if platform in text:
            return platform

    return ""


# ============================================================
# FALLBACK UNDERSTANDING
# ============================================================

def fallback_understand_request(user_text):

    text = normalize(user_text)

    # First try English products
    category, product = detect_product(text)

    # Then Telugu
    if not category:
        category, product = detect_telugu_product(
            user_text
        )

    location = detect_location(user_text)

    budget = detect_budget(text)

    gender = detect_gender(text)

    occasion = detect_occasion(text)

    platform = detect_platform(text)

    # If only location + food words
    if not category:

        if any(word in user_text for word in TELUGU_FOOD):
            category = "food"

        elif any(word in user_text for word in TELUGU_ELECTRONICS):
            category = "electronics"

        elif any(word in user_text for word in TELUGU_FASHION):
            category = "fashion"

    return {
        "category": category or "general",
        "subcategory": product,
        "product_type": product,
        "gender": gender,
        "occasion": occasion,
        "style": "",
        "color": "",
        "brand": "",
        "platform": platform,
        "budget": budget,
        "location": location,
        "preferences": user_text
    }


# ============================================================
# GEMINI UNDERSTANDING
# ============================================================

def understand_with_gemini(user_text):

    if not client:
        return None

    prompt = f"""
You are the classification engine of OmniAI.

The user can ask for products or places from:

1. FASHION
2. ELECTRONICS
3. FOOD

IMPORTANT:
Return ONLY valid JSON.

Do NOT invent products.
Do NOT change the user's requested product.
Do NOT confuse food with fashion or electronics.

User request:
{user_text}

Return:

{{
  "category": "",
  "subcategory": "",
  "product_type": "",
  "gender": "",
  "occasion": "",
  "style": "",
  "color": "",
  "brand": "",
  "platform": "",
  "budget": null,
  "location": "",
  "preferences": ""
}}

Rules:

FASHION examples:
dress, shirt, t-shirt, jeans, saree, kurti,
shoes, sneakers, sandals, watch, bag,
jewellery, necklace, earrings.

ELECTRONICS examples:
phone, smartphone, iPhone, laptop,
tablet, TV, camera, headphones,
earbuds, speaker, smartwatch,
monitor, keyboard, mouse, printer.

FOOD examples:
biryani, pizza, burger, ice cream,
cake, chocolate, dosa, idli, noodles,
momos, restaurant, cafe, food.

If the user says:
"I want ice cream"

category must be:
food

product_type must be:
ice cream

If the user says:
"I want a laptop"

category must be:
electronics

product_type must be:
laptop

If the user says:
"I want a dress"

category must be:
fashion

product_type must be:
dress

If location is Hyderabad, return:
"Hyderabad"

If budget is ₹500 or under 500, return:
500
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        raw = response.text.strip()

        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")
        raw = raw.strip()

        data = json.loads(raw)

        return data

    except Exception as error:

        print(
            "Gemini failed, using local parser:",
            error
        )

        return None


# ============================================================
# FINAL UNDERSTANDING
# ============================================================

def understand_request(user_text):

    print("\n==============================")
    print("USER REQUEST:")
    print(user_text)

    # Always run local detection first
    local = fallback_understand_request(
        user_text
    )

    # Gemini may improve attributes
    gemini = understand_with_gemini(
        user_text
    )

    if gemini:

        # IMPORTANT:
        # Local product/category has priority.
        # This prevents Gemini from changing
        # "ice cream" into something else.

        if local["category"] != "general":
            gemini["category"] = local["category"]

        if local["product_type"]:
            gemini["product_type"] = local[
                "product_type"
            ]

            gemini["subcategory"] = local[
                "product_type"
            ]

        if local["location"]:
            gemini["location"] = local[
                "location"
            ]

        if local["budget"] is not None:
            gemini["budget"] = local[
                "budget"
            ]

        if local["platform"]:
            gemini["platform"] = local[
                "platform"
            ]

        result = gemini

    else:
        result = local

    print("\nUNDERSTOOD:")
    print(json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ))

    return result