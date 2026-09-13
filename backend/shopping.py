import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_one_query(query, min_price=None, max_price=None):

    params = {
        "engine": "google_shopping_light",
        "q": query,
        "api_key": SERPAPI_KEY,
        "location": "Hyderabad, Telangana, India",
        "hl": "en",
        "gl": "in"
    }

    if min_price is not None:
        params["min_price"] = min_price

    if max_price is not None:
        params["max_price"] = max_price

    try:
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            print("SERPAPI ERROR:", data["error"])
            return []

        results = data.get("shopping_results", [])

        if not results:
            results = data.get("inline_shopping_results", [])

        products = []

        for item in results:

            products.append({
                "title": item.get("title"),
                "price": item.get("price"),
                "store": item.get("source"),
                "rating": item.get("rating"),
                "reviews": item.get("reviews"),
                "link": item.get("product_link") or item.get("link"),
                "image": item.get("thumbnail")
            })

        return products

    except Exception as e:
        print("SEARCH ERROR:", e)
        return []


def search_products(query, min_price=None, max_price=None):

    all_products = []

    # Search the original request
    searches = [
        query,
        "women jeans " + query,
        "women jeans Myntra",
        "women jeans AJIO"
    ]

    for search in searches:

        print("SEARCHING:", search)

        products = search_one_query(
            search,
            min_price,
            max_price
        )

        all_products.extend(products)

    # Remove duplicate products
    unique_products = []
    seen = set()

    for product in all_products:

        key = (
            product.get("title"),
            product.get("store"),
            product.get("price")
        )

        if key not in seen:
            seen.add(key)
            unique_products.append(product)

    print("TOTAL UNIQUE PRODUCTS:", len(unique_products))

    return unique_products