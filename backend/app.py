from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from agent import understand_request
from shopping import search_products

app = Flask(__name__)
CORS(app)

FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def frontend_files(path):
    return send_from_directory(FRONTEND_DIR, path)


@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    user_request = data.get("request", "").strip()

    if not user_request:
        return jsonify({
            "error": "Please enter your requirement."
        }), 400

    try:

        ai_result = understand_request(user_request)

    except Exception as e:

        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

            return jsonify({
                "error": "OmniAI has temporarily reached the Gemini AI request limit. Please try again later."
            }), 429

        return jsonify({
            "error": error_message
        }), 500

    try:

        products = search_products(user_request)

        if not products:

            return jsonify({
                "error": "No real products were found. Please try a different search."
            }), 404

        return jsonify({
            "understanding": ai_result,
            "products": products[:20]
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)