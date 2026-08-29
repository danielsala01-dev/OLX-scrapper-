"""
API endpoints dla ogłoszeń
- GET /api/listings - pobierz ogłoszenia usera
- POST /api/listings/refresh - scrapa nowe ogłoszenia
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import get_user_listings, get_user_by_id, get_user_preferences
from scraper.olx_scraper import get_listings_for_preferences

# Stwórz blueprint
listings_bp = Blueprint('listings', __name__, url_prefix='/api/listings')

@listings_bp.route('', methods=['GET'])
@jwt_required()
def get_listings():
    """Pobierz ogłoszenia dla zalogowanego usera"""
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)
        
        # Pobierz ogłoszenia
        listings = get_user_listings(user_id, limit=limit)
        
        return jsonify({
            'listings': [l.to_dict() for l in listings]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@listings_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_listings():
    """
    Scrapa nowe ogłoszenia dla preferencji usera
    """
    try:
        user_id = get_jwt_identity()
        
        # Sprawdź czy user istnieje
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User nie znaleziony'}), 404
        
        # Pobierz preferencje usera
        preferences = get_user_preferences(user_id)
        if not preferences:
            return jsonify({'error': 'Brak preferencji. Dodaj preferencje najpierw'}), 400
        
        # Scrapa ogłoszenia
        new_listings = get_listings_for_preferences(user_id, preferences)
        
        return jsonify({
            'message': f'Znaleziono {len(new_listings)} nowych ogłoszeń',
            'listings': [l.to_dict() for l in new_listings]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
