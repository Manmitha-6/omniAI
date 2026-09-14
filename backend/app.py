# ============================================================
# OMNIAI - FLASK BACKEND
# ============================================================

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)

from flask_cors import CORS

from agent import understand_request
from shopping import search_products

import os


# ------------------------------------------------------------
# FRONTEND LOCATION
# ------------------------------------------------------------

FRONTEND_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend"
    )
)


# ------------------------------------------------------------
# FLASK APP
# ------------------------------------------------------------

app = Flask(
    __name__,
    static_folder=FRONTEND_FOLDER
)

CORS(app)


# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


# ------------------------------------------------------------
# STATIC FILES
# ------------------------------------------------------------

@app.route("/<path:path>")
def static_files(path):

    return send_from_directory(
        FRONTEND_FOLDER,
        path
    )


# ------------------------------------------------------------
# OMNIAI RECOMMENDATION API
# ------------------------------------------------------------

@app.route(
    "/api/recommend",
    methods=["POST"]
)
def recommend():

    try:

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({

                "error":
                "Invalid request. JSON data is required."

            }), 400


        user_request = data.get(
            "request",
            ""
        )


        if not isinstance(
            user_request,
            str
        ):

            return jsonify({

                "error":
                "Request must be text."

            }), 400


        user_request = user_request.strip()


        if not user_request:

            return jsonify({

                "error":
                "Please enter a product request."

            }), 400


        print("\n")
        print("=" * 60)
        print("OMNIAI REQUEST")
        print("=" * 60)

        print(
            "User:",
            user_request
        )


        # ----------------------------------------------------
        # STEP 1 - UNDERSTAND REQUEST
        # ----------------------------------------------------

        print(
            "\n[1] Understanding user request..."
        )


        info = understand_request(
            user_request
        )


        print(
            "\nFINAL AI UNDERSTANDING:"
        )

        print(info)


        # ----------------------------------------------------
        # STEP 2 - REAL SEARCH
        # ----------------------------------------------------

        print(
            "\n[2] Searching real data..."
        )


        products = search_products(
            info
        )


        if products is None:

            products = []


        print(
            f"\n[3] Real results found: {len(products)}"
        )


        # ----------------------------------------------------
        # NO RESULTS
        # ----------------------------------------------------

        if len(products) == 0:

            print(
                "No real results were found."
            )

            print("=" * 60)


            return jsonify({

                "message":
                "No real results were found. "
                "Try another product, budget, "
                "brand or preference.",

                "understanding":
                info,

                "count":
                0,

                "products":
                []

            }), 200


        # ----------------------------------------------------
        # LIMIT RESULTS
        # ----------------------------------------------------

        products = products[:20]


        print(
            f"Returning {len(products)} recommendations."
        )

        print("=" * 60)


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "understanding":
            info,

            "count":
            len(products),

            "products":
            products

        }), 200


    # --------------------------------------------------------
    # ERROR
    # --------------------------------------------------------

    except Exception as error:

        print("\n")
        print("=" * 60)
        print("OMNIAI SERVER ERROR")
        print("=" * 60)

        print(
            "Error:",
            str(error)
        )

        print("=" * 60)


        return jsonify({

            "error":
            "Something went wrong while processing your request.",

            "details":
            str(error)

        }), 500


# ------------------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------------------

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "status":
        "online",

        "agent":
        "OmniAI",

        "message":
        "OmniAI backend is running successfully."

    })


# ------------------------------------------------------------
# RUN SERVER
# ------------------------------------------------------------

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print(
        "        OMNIAI INTELLIGENT RECOMMENDATION AGENT"
    )
    print("=" * 60)

    print(
        "Frontend:",
        FRONTEND_FOLDER
    )

    print(
        "API:",
        "http://127.0.0.1:5000/api/recommend"
    )

    print(
        "Health:",
        "http://127.0.0.1:5000/api/health"
    )

    print("=" * 60)

    print(
        "Starting Flask server..."
    )

    print("=" * 60)
    print("\n")


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True
    )