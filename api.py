#!/usr/bin/env python3
"""
Simple Flask API for OLX Scraper - Testing only
"""
import json
from urllib.parse import quote_plus
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
with open("config.marketplaces.json", "r", encoding="utf-8") as f:
    MARKETPLACES = json.load(f)

# In-memory listings store (no dummy entries)
DUMMY_LISTINGS = []


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "olx-scrapper-api",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/api/listings", methods=["GET"])
def get_listings():
    return jsonify({
        "count": len(DUMMY_LISTINGS),
        "results": DUMMY_LISTINGS
    }), 200


@app.route("/api/listings/<int:item_id>", methods=["GET"])
def get_listing(item_id):
    for item in DUMMY_LISTINGS:
        if item.get("id") == item_id:
            return jsonify(item), 200
    return jsonify({"error": "Listing not found"}), 404


@app.route("/api/search", methods=["GET"])
def search_listings():
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify({
            "count": len(DUMMY_LISTINGS),
            "results": DUMMY_LISTINGS
        }), 200

    filtered = [
        item for item in DUMMY_LISTINGS
        if q in str(item.get("title", "")).lower()
        or q in str(item.get("description", "")).lower()
        or q in str(item.get("category", "")).lower()
    ]
    return jsonify({
        "count": len(filtered),
        "results": filtered
    }), 200


@app.route("/api/listings", methods=["POST"])
def create_listing():
    payload = request.get_json(silent=True) or {}

    required_fields = ["title", "price", "category"]
    missing = [f for f in required_fields if f not in payload]
    if missing:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing
        }), 400

    new_id = (max([x.get("id", 0) for x in DUMMY_LISTINGS], default=0) + 1)
    new_item = {
        "id": new_id,
        "title": payload.get("title"),
        "price": payload.get("price"),
        "category": payload.get("category"),
        "description": payload.get("description", ""),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    DUMMY_LISTINGS.append(new_item)

    return jsonify(new_item), 201
@app.route("/api/marketplaces", methods=["GET"])
def get_marketplaces():
    result = [{"key": k, "name": v["name"]} for k, v in MARKETPLACES.items()]
    return jsonify({"count": len(result), "results": result}), 200


@app.route("/api/categories", methods=["GET"])
def get_categories():
    marketplace = request.args.get("marketplace", "").strip().lower()
    if not marketplace or marketplace not in MARKETPLACES:
        return jsonify({"error": "Invalid marketplace"}), 400

    categories = MARKETPLACES[marketplace]["categories"]
    return jsonify({"count": len(categories), "results": categories}), 200


@app.route("/api/search-url", methods=["GET"])
def build_search_url():
    marketplace = request.args.get("marketplace", "").strip().lower()
    category_key = request.args.get("category_key", "").strip().lower()
    query = request.args.get("q", "").strip()

    if marketplace not in MARKETPLACES:
        return jsonify({"error": "Invalid marketplace"}), 400

    category = next(
        (c for c in MARKETPLACES[marketplace]["categories"] if c["key"] == category_key),
        None
    )
    if not category:
        return jsonify({"error": "Invalid category_key"}), 400

    base_url = MARKETPLACES[marketplace]["base_url"]
    path = category["path"]
    full = f"{base_url}{path}"

    if query:
        full = f"{full}?q={quote_plus(query)}"

    return jsonify({
        "marketplace": marketplace,
        "category_key": category_key,
        "url": full
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
