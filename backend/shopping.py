# ============================================================
# OMNIAI - REAL PRODUCT & FOOD SEARCH
# ============================================================

import os
import requests
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# API URLS
# ============================================================

SERPAPI_URL = "https://serpapi.com/search.json"

SERPER_SEARCH_URL = "https://google.serper.dev/search"

# IMPORTANT:
# Serper Shopping endpoint
SERPER_SHOPPING_URL = "https://google.serper.dev/shopping"


# ============================================================
# SERPAPI REQUEST
# ============================================================

def serpapi_request(params):

    if not SERPAPI_KEY:
        print("ERROR: SERPAPI_KEY is missing.")
        return {}

    request_params = params.copy()
    request_params["api_key"] = SERPAPI_KEY

    print("\n----------------------------------------")
    print("SERPAPI SEARCH")
    print("----------------------------------------")
    print("Engine   :", request_params.get("engine"))
    print("Query    :", request_params.get("q"))
    print("Location :", request_params.get("location"))

    try:

        response = requests.get(
            SERPAPI_URL,
            params=request_params,
            timeout=12
        )

        print(
            "SerpApi HTTP Status:",
            response.status_code
        )

        response.raise_for_status()

        data = response.json()

        if data.get("error"):

            print(
                "SERPAPI ERROR:",
                data.get("error")
            )

            return {}

        return data

    except requests.exceptions.Timeout:

        print(
            "SerpApi timed out after 12 seconds."
        )

        return {}

    except requests.exceptions.RequestException as error:

        print(
            "SERPAPI NETWORK ERROR:",
            error
        )

        return {}

    except Exception as error:

        print(
            "SERPAPI ERROR:",
            error
        )

        return {}


# ============================================================
# SERPER SHOPPING REQUEST
# ============================================================

def serper_shopping_request(query):

    if not SERPER_API_KEY:

        print(
            "SERPER_API_KEY is missing."
        )

        return {}

    if not query:

        return {}

    print("\n----------------------------------------")
    print("SERPER SHOPPING SEARCH")
    print("----------------------------------------")
    print("Query:", query)

    headers = {

        "X-API-KEY": SERPER_API_KEY,

        "Content-Type": "application/json"

    }

    payload = {

        "q": query,

        "gl": "in",

        "hl": "en",

        "num": 20

    }

    try:

        response = requests.post(

            SERPER_SHOPPING_URL,

            headers=headers,

            json=payload,

            timeout=8

        )

        print(
            "Serper Shopping HTTP Status:",
            response.status_code
        )

        response.raise_for_status()

        data = response.json()

        return data

    except requests.exceptions.Timeout:

        print(
            "Serper Shopping timed out after 8 seconds."
        )

        return {}

    except requests.exceptions.RequestException as error:

        print(
            "SERPER SHOPPING ERROR:",
            error
        )

        return {}

    except Exception as error:

        print(
            "SERPER SHOPPING ERROR:",
            error
        )

        return {}


# ============================================================
# SERPER NORMAL SEARCH
# ============================================================

def serper_request(query):

    if not SERPER_API_KEY:

        print(
            "SERPER_API_KEY is missing."
        )

        return {}

    if not query:

        return {}

    headers = {

        "X-API-KEY": SERPER_API_KEY,

        "Content-Type": "application/json"

    }

    payload = {

        "q": query,

        "gl": "in",

        "hl": "en",

        "num": 20

    }

    try:

        response = requests.post(

            SERPER_SEARCH_URL,

            headers=headers,

            json=payload,

            timeout=6

        )

        response.raise_for_status()

        return response.json()

    except Exception as error:

        print(
            "SERPER SEARCH ERROR:",
            error
        )

        return {}


# ============================================================
# PRICE CONVERSION
# ============================================================

def get_price_number(price):

    if price is None:

        return None

    try:

        value = str(price)

        value = (

            value
            .replace("₹", "")
            .replace("Rs.", "")
            .replace("Rs", "")
            .replace(",", "")
            .replace("$", "")
            .strip()

        )

        if "-" in value:

            value = value.split("-")[0].strip()

        return float(value)

    except Exception:

        return None


# ============================================================
# PRODUCT LINK
# ============================================================

def get_product_link(item):

    link = item.get("link")

    if link:

        return link

    product_link = item.get("product_link")

    if product_link:

        return product_link

    return ""


# ============================================================
# SERPER SHOPPING → OMNIAI PRODUCT
# ============================================================

def convert_serper_shopping_product(item):

    title = item.get(
        "title",
        "Product"
    )

    price = item.get(
        "price",
        "Price unavailable"
    )

    rating = item.get(
        "rating",
        "N/A"
    )

    rating_count = item.get(
        "ratingCount",
        item.get(
            "reviews",
            "N/A"
        )
    )

    source = item.get(
        "source",
        "Unknown store"
    )

    link = item.get(
        "link",
        ""
    )

    image = item.get(
        "imageUrl",
        ""
    )

    return {

        "title": title,

        "price": price,

        "rating": rating,

        "reviews": rating_count,

        "store": source,

        "link": link,

        "image": image,

        "type": "product"

    }


# ============================================================
# SERPAPI SHOPPING → OMNIAI PRODUCT
# ============================================================

def convert_serpapi_product(item):

    title = item.get(
        "title",
        "Product"
    )

    price = item.get(
        "price",
        "Price unavailable"
    )

    rating = item.get(
        "rating",
        "N/A"
    )

    reviews = item.get(
        "reviews",
        "N/A"
    )

    store = item.get(
        "source",
        "Unknown store"
    )

    link = item.get(
        "link",
        item.get(
            "product_link",
            ""
        )
    )

    image = item.get(
        "thumbnail",
        ""
    )

    return {

        "title": title,

        "price": price,

        "rating": rating,

        "reviews": reviews,

        "store": store,

        "link": link,

        "image": image,

        "type": "product"

    }


# ============================================================
# GOOGLE SHOPPING SEARCH
# ============================================================

def search_one_query(
    query,
    max_price=None
):

    if not query:

        return []

    print("\n")
    print("=" * 60)
    print("PRODUCT SEARCH")
    print("=" * 60)

    print(
        "Query:",
        query
    )

    # ========================================================
    # 1. SERPAPI SHOPPING
    # ========================================================

    products = []

    if SERPAPI_KEY:

        params = {

            "engine": "google_shopping",

            "q": query,

            "hl": "en",

            "gl": "in"

        }

        data = serpapi_request(
            params
        )

        shopping_results = data.get(
            "shopping_results",
            []
        )

        print(
            "SerpApi Shopping results:",
            len(shopping_results)
        )

        for item in shopping_results:

            product = convert_serpapi_product(
                item
            )

            price_number = get_price_number(
                product.get("price")
            )

            if (

                max_price is not None

                and price_number is not None

                and price_number > float(max_price)

            ):

                continue

            products.append(
                product
            )

    # ========================================================
    # 2. SERPER SHOPPING FALLBACK
    # ========================================================

    if not products and SERPER_API_KEY:

        print("\n")
        print(
            "SerpApi returned no products."
        )

        print(
            "Trying Serper Shopping..."
        )

        data = serper_shopping_request(
            query
        )

        shopping_results = data.get(
            "shopping",
            []
        )

        print(
            "Serper Shopping results:",
            len(shopping_results)
        )

        for item in shopping_results:

            product = convert_serper_shopping_product(
                item
            )

            price_number = get_price_number(
                product.get("price")
            )

            if (

                max_price is not None

                and price_number is not None

                and price_number > float(max_price)

            ):

                continue

            products.append(
                product
            )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique_products = []

    seen_links = set()

    seen_titles = set()

    for product in products:

        link = product.get(
            "link",
            ""
        )

        title = product.get(
            "title",
            ""
        ).strip().lower()

        if link and link in seen_links:

            continue

        if title and title in seen_titles:

            continue

        if link:

            seen_links.add(link)

        if title:

            seen_titles.add(title)

        unique_products.append(
            product
        )

    print(
        "Final product results:",
        len(unique_products)
    )

    return unique_products[:20]


# ============================================================
# SEARCH QUERY BUILDER
# ============================================================

def build_search_query(info):

    category = str(
        info.get(
            "category",
            ""
        )
    ).lower().strip()

    product = str(
        info.get(
            "product_type"
        )
        or info.get(
            "subcategory"
        )
        or ""
    ).strip()

    gender = str(
        info.get(
            "gender",
            ""
        )
    ).strip()

    occasion = str(
        info.get(
            "occasion",
            ""
        )
    ).strip()

    brand = str(
        info.get(
            "brand",
            ""
        )
    ).strip()

    platform = str(
        info.get(
            "platform",
            ""
        )
    ).strip()

    preferences = str(
        info.get(
            "preferences",
            ""
        )
    ).strip()

    location = str(
        info.get(
            "location",
            ""
        )
    ).strip()

    # ========================================================
    # FASHION
    # ========================================================

    if category == "fashion":

        parts = []

        if gender:

            parts.append(
                gender
            )

        if product:

            parts.append(
                product
            )

        else:

            parts.append(
                "fashion"
            )

        if occasion:

            parts.append(
                occasion
            )

        if brand:

            parts.append(
                brand
            )

        if platform:

            parts.append(
                platform
            )

        if preferences:

            parts.append(
                preferences
            )

        return " ".join(parts)


    # ========================================================
    # ELECTRONICS
    # ========================================================

    if category == "electronics":

        parts = []

        if product:

            parts.append(
                product
            )

        else:

            parts.append(
                "electronics"
            )

        if brand:

            parts.append(
                brand
            )

        if preferences:

            parts.append(
                preferences
            )

        return " ".join(parts)


    # ========================================================
    # FOOD
    # ========================================================

    if category == "food":

        if product:

            return product

        return "restaurants food"


    # ========================================================
    # GENERAL
    # ========================================================

    if product:

        return product

    if preferences:

        return preferences

    return "popular products"


# ============================================================
# SERPER FOOD SEARCH
# ============================================================

def search_food_with_serper(
    query,
    location=""
):

    if not SERPER_API_KEY:

        print(
            "SERPER_API_KEY is missing."
        )

        return []

    food_query = query

    if location:

        food_query = (
            f"{query} restaurants in {location}"
        )

    print("\n")
    print("=" * 60)
    print("SERPER FOOD SEARCH")
    print("=" * 60)

    print(
        "Query:",
        food_query
    )

    headers = {

        "X-API-KEY": SERPER_API_KEY,

        "Content-Type": "application/json"

    }

    payload = {

        "q": food_query,

        "gl": "in",

        "hl": "en",

        "num": 20

    }

    try:

        response = requests.post(

            SERPER_SEARCH_URL,

            headers=headers,

            json=payload,

            timeout=6

        )

        response.raise_for_status()

        data = response.json()

        organic_results = data.get(
            "organic",
            []
        )

        restaurants = []

        for item in organic_results:

            restaurant_name = item.get(
                "title",
                "Restaurant"
            )

            snippet = item.get(
                "snippet",
                ""
            )

            link = item.get(
                "link",
                ""
            )

            maps_query = (

                f"{restaurant_name} "
                f"{location}"

            ).strip()

            maps_link = (

                "https://www.google.com/maps/search/?api=1&query="

                + requests.utils.quote(
                    maps_query
                )

            )

            restaurant = {

                "title": restaurant_name,

                "price": "Price unavailable",

                "rating": "N/A",

                "reviews": "N/A",

                "store": "Google Search",

                "address": (

                    snippet

                    if snippet

                    else "Address unavailable"

                ),

                "link": link,

                "maps_link": maps_link,

                "image": "",

                "type": "restaurant"

            }

            restaurants.append(
                restaurant
            )

        return restaurants[:20]

    except Exception as error:

        print(
            "SERPER FOOD ERROR:",
            error
        )

        return []


# ============================================================
# PRODUCT SEARCH
# ============================================================

def search_products(info):

    category = str(
        info.get(
            "category",
            ""
        )
    ).lower().strip()

    product = str(
        info.get(
            "product_type"
        )
        or info.get(
            "subcategory"
        )
        or ""
    ).strip()

    budget = info.get(
        "budget"
    )

    location = str(
        info.get(
            "location",
            ""
        )
    ).strip()

    query = build_search_query(
        info
    )

    print("\n")
    print("=" * 60)
    print("OMNIAI SEARCH")
    print("=" * 60)

    print(
        "Category :",
        category
    )

    print(
        "Product  :",
        product
    )

    print(
        "Query    :",
        query
    )

    print(
        "Budget   :",
        budget
    )

    print(
        "Location :",
        location
    )

    print("=" * 60)


    # ========================================================
    # FASHION
    # ========================================================

    if category == "fashion":

        results = search_one_query(
            query,
            budget
        )

        if not results and product:

            print(
                "\nTrying broader fashion search..."
            )

            results = search_one_query(
                f"{product} fashion",
                budget
            )

        if not results:

            print(
                "\nTrying general fashion search..."
            )

            results = search_one_query(
                "fashion products",
                budget
            )

        print(
            "Final fashion results:",
            len(results)
        )

        return results[:20]


    # ========================================================
    # ELECTRONICS
    # ========================================================

    if category == "electronics":

        results = search_one_query(
            query,
            budget
        )

        if not results and product:

            print(
                "\nTrying broader electronics search..."
            )

            results = search_one_query(
                f"{product} electronics",
                budget
            )

        if not results:

            print(
                "\nTrying general electronics search..."
            )

            results = search_one_query(
                "electronics products",
                budget
            )

        print(
            "Final electronics results:",
            len(results)
        )

        return results[:20]


    # ========================================================
    # FOOD
    # ========================================================

    if category == "food":

        food_query = query

        if location:

            food_query = (
                f"{query} in {location}"
            )

        # ----------------------------------------------------
        # FIRST: SERPAPI GOOGLE LOCAL
        # ----------------------------------------------------

        restaurants = []

        params = {

            "engine": "google_local",

            "q": food_query,

            "hl": "en",

            "gl": "in"

        }

        if location:

            params["location"] = location

        data = serpapi_request(
            params
        )

        local_results = data.get(
            "local_results",
            []
        )

        print(
            "SerpApi local results:",
            len(local_results)
        )

        for item in local_results:

            restaurant_name = item.get(
                "title",
                "Restaurant"
            )

            address = item.get(
                "address",
                "Address unavailable"
            )

            maps_query = (

                f"{restaurant_name} "
                f"{address}"

            ).strip()

            maps_link = (

                "https://www.google.com/maps/search/?api=1&query="

                + requests.utils.quote(
                    maps_query
                )

            )

            links = item.get(
                "links",
                {}
            )

            website = ""

            if isinstance(
                links,
                dict
            ):

                website = links.get(
                    "website",
                    ""
                )

            restaurant = {

                "title": restaurant_name,

                "price": item.get(
                    "price",
                    "Price unavailable"
                ),

                "rating": item.get(
                    "rating",
                    "N/A"
                ),

                "reviews": item.get(
                    "reviews",
                    "N/A"
                ),

                "store": "Google Local",

                "address": address,

                "link": website,

                "maps_link": maps_link,

                # THIS IS THE IMPORTANT IMAGE
                "image": item.get(
                    "thumbnail",
                    ""
                ),

                "type": "restaurant"

            }

            restaurants.append(
                restaurant
            )

        # ----------------------------------------------------
        # SECOND: SERPER FOOD FALLBACK
        # ----------------------------------------------------

        if not restaurants:

            print(
                "\nNo SerpApi food results."
            )

            print(
                "Trying Serper food fallback..."
            )

            restaurants = search_food_with_serper(
                query,
                location
            )

        # ----------------------------------------------------
        # THIRD: BROADER FOOD SEARCH
        # ----------------------------------------------------

        if not restaurants:

            print(
                "\nTrying broader food search..."
            )

            restaurants = search_food_with_serper(
                "best food restaurants",
                location
            )

        print(
            "Final food results:",
            len(restaurants)
        )

        return restaurants[:20]


    # ========================================================
    # GENERAL SEARCH
    # ========================================================

    results = search_one_query(
        query,
        budget
    )

    return results[:20]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("OMNIAI REAL SEARCH TEST")
    print("=" * 60)


    # ========================================================
    # TEST 1 - FASHION
    # ========================================================

    print("\n")
    print("=" * 60)
    print("TEST: WOMEN BIRTHDAY DRESS")
    print("=" * 60)

    fashion_results = search_one_query(
        "women birthday dress",
        2000
    )

    print(
        "Fashion results:",
        len(fashion_results)
    )

    for item in fashion_results[:5]:

        print("\nTitle :",
              item["title"])

        print("Price :",
              item["price"])

        print("Store :",
              item["store"])

        print("Rating:",
              item["rating"])

        print("Reviews:",
              item["reviews"])

        print("Image :",
              item["image"])

        print("Link  :",
              item["link"])


    # ========================================================
    # TEST 2 - ELECTRONICS
    # ========================================================

    print("\n")
    print("=" * 60)
    print("TEST: WIRELESS HEADPHONES")
    print("=" * 60)

    electronics_results = search_one_query(
        "wireless headphones",
        3000
    )

    print(
        "Electronics results:",
        len(electronics_results)
    )

    for item in electronics_results[:5]:

        print("\nTitle :",
              item["title"])

        print("Price :",
              item["price"])

        print("Store :",
              item["store"])

        print("Rating:",
              item["rating"])

        print("Image :",
              item["image"])

        print("Link  :",
              item["link"])


    # ========================================================
    # TEST 3 - FOOD
    # ========================================================

    print("\n")
    print("=" * 60)
    print("TEST: BIRYANI")
    print("=" * 60)

    food_results = search_food_with_serper(
        "biryani",
        "Hyderabad, Telangana, India"
    )

    print(
        "Food results:",
        len(food_results)
    )

    for item in food_results[:5]:

        print("\nRestaurant:",
              item["title"])

        print("Rating:",
              item["rating"])

        print("Address:",
              item["address"])

        print("Image:",
              item["image"])

        print("Maps:",
              item["maps_link"])


    # ========================================================
    # FINISHED
    # ========================================================

    print("\n")
    print("=" * 60)
    print("TEST FINISHED")
    print("=" * 60)