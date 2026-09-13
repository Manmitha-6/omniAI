# ============================================================
# OMNIAI - REAL PRODUCT SEARCH
# ============================================================

import os
import time
import requests
from dotenv import load_dotenv


# ------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


# ------------------------------------------------------------
# SERPAPI REQUEST
# ------------------------------------------------------------

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

    # Retry 3 times
    for attempt in range(1, 4):

        try:

            print(
                f"Attempt {attempt}/3..."
            )

            response = requests.get(
                "https://serpapi.com/search.json",
                params=request_params,
                timeout=60
            )

            print(
                "HTTP Status:",
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
                f"Timeout on attempt {attempt}"
            )

            if attempt < 3:
                time.sleep(2)

        except requests.exceptions.RequestException as error:

            print(
                "NETWORK ERROR:",
                error
            )

            if attempt < 3:
                time.sleep(2)

        except Exception as error:

            print(
                "ERROR:",
                error
            )

            return {}

    print(
        "SerpApi request failed after 3 attempts."
    )

    return {}


# ------------------------------------------------------------
# PRICE CONVERTER
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# GOOGLE SHOPPING SEARCH
# ------------------------------------------------------------

def search_one_query(query, max_price=None):

    if not query:

        return []

    params = {

        "engine": "google_shopping",

        "q": query,

        "hl": "en",

        "gl": "in"
    }

    data = serpapi_request(params)

    shopping_results = data.get(
        "shopping_results",
        []
    )

    print(
        "Shopping results:",
        len(shopping_results)
    )

    products = []

    for item in shopping_results:

        price = get_price_number(
            item.get("price")
        )

        # Budget filter
        if (
            max_price is not None
            and price is not None
            and price > float(max_price)
        ):
            continue

        products.append({

            "title": item.get(
                "title",
                "Product"
            ),

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

            "store": item.get(
                "source",
                "Unknown store"
            ),

            "link": item.get(
                "link",
                ""
            ),

            "image": item.get(
                "thumbnail",
                ""
            ),

            "type": "product"
        })

    return products


# ------------------------------------------------------------
# BUILD QUERY
# ------------------------------------------------------------

def build_search_query(info):

    category = str(
        info.get("category", "")
    ).lower().strip()

    product = str(
        info.get("product_type")
        or info.get("subcategory")
        or ""
    ).strip()

    gender = str(
        info.get("gender", "")
    ).strip()

    occasion = str(
        info.get("occasion", "")
    ).strip()

    brand = str(
        info.get("brand", "")
    ).strip()

    platform = str(
        info.get("platform", "")
    ).strip()

    preferences = str(
        info.get("preferences", "")
    ).strip()


    # --------------------------------------------------------
    # FASHION
    # --------------------------------------------------------

    if category == "fashion":

        parts = []

        if gender:
            parts.append(gender)

        if product:
            parts.append(product)
        else:
            parts.append("fashion")

        if occasion:
            parts.append(occasion)

        if brand:
            parts.append(brand)

        if platform:
            parts.append(platform)

        if preferences:
            parts.append(preferences)

        return " ".join(parts)


    # --------------------------------------------------------
    # ELECTRONICS
    # --------------------------------------------------------

    if category == "electronics":

        parts = []

        if product:
            parts.append(product)
        else:
            parts.append("electronics")

        if brand:
            parts.append(brand)

        if preferences:
            parts.append(preferences)

        return " ".join(parts)


    # --------------------------------------------------------
    # FOOD
    # --------------------------------------------------------

    if category == "food":

        if product:
            return product

        return "restaurants"


    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    if product:
        return product

    if preferences:
        return preferences

    return "popular products"


# ------------------------------------------------------------
# MAIN SEARCH
# ------------------------------------------------------------

def search_products(info):

    category = str(
        info.get("category", "")
    ).lower().strip()

    product = str(
        info.get("product_type")
        or info.get("subcategory")
        or ""
    ).strip()

    budget = info.get("budget")

    query = build_search_query(info)


    print("\n")
    print("=" * 60)
    print("OMNIAI SEARCH")
    print("=" * 60)

    print("Category :", category)
    print("Product  :", product)
    print("Query    :", query)
    print("Budget   :", budget)

    print("=" * 60)


    # --------------------------------------------------------
    # FASHION
    # --------------------------------------------------------

    if category == "fashion":

        results = search_one_query(
            query,
            budget
        )

        # If no results, try a broader REAL search
        if not results and product:

            print(
                "\nTrying broader fashion search..."
            )

            results = search_one_query(
                f"{product} women",
                budget
            )

        return results[:20]


    # --------------------------------------------------------
    # ELECTRONICS
    # --------------------------------------------------------

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
                product,
                budget
            )

        return results[:20]


    # --------------------------------------------------------
    # FOOD
    # --------------------------------------------------------

    if category == "food":

        # Food uses Google Local
        params = {

            "engine": "google_local",

            "q": query,

            "hl": "en",

            "gl": "in"
        }

        data = serpapi_request(params)

        local_results = data.get(
            "local_results",
            []
        )

        restaurants = []

        for item in local_results:

            restaurants.append({

                "title": item.get(
                    "title",
                    "Restaurant"
                ),

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

                "address": item.get(
                    "address",
                    "Address unavailable"
                ),

                "link": item.get(
                    "links",
                    {}
                ).get(
                    "website",
                    ""
                ),

                "image": item.get(
                    "thumbnail",
                    ""
                ),

                "type": "restaurant"
            })

        print(
            "Food results:",
            len(restaurants)
        )

        return restaurants[:20]


    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    return search_one_query(
        query,
        budget
    )[:20]


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("OMNIAI REAL SEARCH TEST")
    print("=" * 60)


    # TEST FASHION

    print("\nTEST: WOMEN BIRTHDAY DRESS")

    fashion_results = search_one_query(
        "women birthday dress",
        2000
    )

    print(
        "Fashion results:",
        len(fashion_results)
    )

    for item in fashion_results[:5]:

        print(
            "\nTitle :",
            item["title"]
        )

        print(
            "Price :",
            item["price"]
        )

        print(
            "Store :",
            item["store"]
        )

        print(
            "Link  :",
            item["link"]
        )


    print("\n")
    print("=" * 60)
    print("TEST FINISHED")
    print("=" * 60)