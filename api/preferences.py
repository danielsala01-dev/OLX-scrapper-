"""
API endpoints dla preferencji użytkownika
- POST /api/preferences - dodaj preferencję
- GET /api/preferences - pobierz preferencje
- DELETE /api/preferences/<id> - usuń preferencję
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import add_user_preference, get_user_preferences, delete_preference, get_user_by_id

# Stwórz blueprint
prefs_bp = Blueprint('preferences', __name__, url_prefix='/api/preferences')

@prefs_bp.route('', methods=['POST'])
@jwt_required()  # Wymaga JWT token
def create_preference():
    """
    Dodaj nową preferencję wyszukiwania
    Oczekuje: {"category": "electronics", "keywords": "iPhone 14"}
    """
    try:
        user_id = get_jwt_identity()  # Pobierz ID usera z tokena
        data = request.get_json()
        
        # Walidacja
        if not data or not data.get('category') or not data.get('keywords'):
            return jsonify({'error': 'category i keywords wymagane'}), 400
        
        # Dodaj preferencję
        pref = add_user_preference(
            user_id=user_id,
            category=data.get('category'),
            keywords=data.get('keywords')
        )
        
        return jsonify({
            'message': 'Preferencja dodana',
            'preference': pref.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@prefs_bp.route('', methods=['GET'])
@jwt_required()
def get_preferences():
    """Pobierz wszystkie preferencje dla zalogowanego usera"""
    try:
        user_id = get_jwt_identity()
        
        # Sprawdź czy user istnieje
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User nie znaleziony'}), 404
        
        # Pobierz preferencje
        prefs = get_user_preferences(user_id)
        
        return jsonify({
            'preferences': [p.to_dict() for p in prefs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@prefs_bp.route('/<int:pref_id>', methods=['DELETE'])
@jwt_required()
def delete_pref(pref_id):
    """Usuń preferencję"""
    try:
        user_id = get_jwt_identity()
        
        # Usuń preferencję
        success = delete_preference(pref_id)
        
        if not success:
            return jsonify({'error': 'Preferencja nie znaleziona'}), 404
        
        return jsonify({
            'message': 'Preferencja usunięta'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
