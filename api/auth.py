"""
API endpoints dla autentykacji
- POST /api/auth/register - rejestracja
- POST /api/auth/login - logowanie
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database.db import create_user, get_user_by_email

# Stwórz blueprint (grupa endpointów)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Rejestracja nowego użytkownika
    Oczekuje: {"email": "user@example.com", "password": "haslo123"}
    """
    try:
        data = request.get_json()
        
        # Walidacja
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email i password wymagane'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Stwórz usera
        user, message = create_user(email, password)
        
        if not user:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': 'Rejestracja udana',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Logowanie użytkownika
    Oczekuje: {"email": "user@example.com", "password": "haslo123"}
    Zwraca: JWT token
    """
    try:
        data = request.get_json()
        
        # Walidacja
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email i password wymagane'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Sprawdź usera
        user = get_user_by_email(email)
        if not user or not user.check_password(password):
            return jsonify({'error': 'Nieprawidłowy email lub hasło'}), 401
        
        # Stwórz JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Logowanie udane',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
