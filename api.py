#!/usr/bin/env python3
"""
Simple Flask API for OLX Scraper - Testing only
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Dummy data
DUMMY_LISTINGS = [
    {
        "id": 1,
        "title": "iPhone 13 Pro",
        "price": 3500,
        "category": "electronics",
        "description": "Used iPhone 13 Pro, mint condition",
        "image": "https://via.placeholder.com/300x300?text=iPhone+13"
    },
    {
        "id": 2,
        "title": "MacBook Pro 14",
        "price": 5000,
        "category": "electronics",
        "description": "MacBook Pro 14 inch, 2021",
        "image": "https://via.placeholder.com/300x300?text=MacBook"
    },
    {
        "id": 3,
        "title": "Bikepack",
        "price": 150,
        "category": "sports",
        "description": "Mountain bike backpack, new",
        "image": "https://via.placeholder.com/300x300?text=Bikepack"
    },
    {
        "id": 4,
        "title": "Gaming Laptop",
        "price": 4200,
        "category": "electronics",
        "description": "ASUS ROG gaming laptop",
        "image": "https://via.placeholder.com/300x300?text=Gaming+Laptop"
    },
    {
        "id": 5,
        "title": "Office Chair",
        "price": 500,
        "category": "furniture",
        "description": "Comfortable office chair",
        "image": "https://via.placeholder.com/300x300?text=Office+Chair"
    }
]


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "message": "OLX API is running"
    }), 200


@app.route('/api/listings', methods=['GET'])
def get_listings():
    """Get all listings"""
    return jsonify({
        "status": "success",
        "data": DUMMY_LISTINGS
    }), 200


@app.route('/api/listings/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    """Get single listing by ID"""
    listing = next((l for l in DUMMY_LISTINGS if l["id"] == listing_id), None)
    
    if not listing:
        return jsonify({
            "status": "error",
            "message": f"Listing {listing_id} not found"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": listing
    }), 200


@app.route('/api/search', methods=['GET'])
def search():
    """Search listings by query"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({
            "status": "error",
            "message": "Query parameter 'q' is required"
        }), 400
    
    results = [l for l in DUMMY_LISTINGS if query in l["title"].lower() or query in l["description"].lower()]
    
    return jsonify({
        "status": "success",
        "query": query,
        "data": results
    }), 200


@app.route('/api/listings', methods=['POST'])
def create_listing():
    """Create new listing (dummy)"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'price' not in data:
        return jsonify({
            "status": "error",
            "message": "title and price are required"
        }), 400
    
    new_listing = {
        "id": max([l["id"] for l in DUMMY_LISTINGS]) + 1,
        "title": data.get("title"),
        "price": data.get("price"),
        "category": data.get("category", "other"),
        "description": data.get("description", ""),
        "image": data.get("image", "https://via.placeholder.com/300x300?text=No+Image")
    }
    
    DUMMY_LISTINGS.append(new_listing)
    
    return jsonify({
        "status": "success",
        "data": new_listing
    }), 201


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("OLX API Server Starting...")
    print("=" * 50)
    print("Host: 0.0.0.0")
    print("Port: 5000")
    print("=" * 50)
    print("Endpoints:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/listings - Get all listings")
    print("  GET  /api/listings/<id> - Get listing by ID")
    print("  GET  /api/search?q=<query> - Search listings")
    print("  POST /api/listings - Create new listing")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
