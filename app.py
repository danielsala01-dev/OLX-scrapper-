"""
Główna aplikacja Flask
Inicjalizuje Flask, bazę danych, JWT, i rejestruje API blueprinty
"""

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import config
from database.models import db
from database.db import init_db
from api.auth import auth_bp
from api.preferences import prefs_bp
from api.listings import listings_bp
from utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

def create_app():
    """Stwórz i skonfiguruj Flask aplikację"""
    
    # Inicjalizuj Flask
    app = Flask(__name__)
    
    # Załaduj konfigurację
    app.config.from_object(config)
    logger.info("✅ Konfiguracja załadowana")
    
    # Inicjalizuj SQLAlchemy
    db.init_app(app)
    logger.info("✅ SQLAlchemy zainicjalizowana")
    
    # Inicjalizuj JWT
    jwt = JWTManager(app)
    logger.info("✅ JWT zainicjalizowany")
    
    # Stwórz tabele bazy danych
    with app.app_context():
        db.create_all()
        logger.info("✅ Baza danych zainicjalizowana")
    
    # Rejestruj API blueprinty
    app.register_blueprint(auth_bp)
    app.register_blueprint(prefs_bp)
    app.register_blueprint(listings_bp)
    logger.info("✅ API blueprinty zarejestrowane")
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'OK'}), 200
    
    # Error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    logger.info("✅ Aplikacja Flask gotowa!")
    
    return app

if __name__ == '__main__':
    # Stwórz app i uruchom serwer
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
