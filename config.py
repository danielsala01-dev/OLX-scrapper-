"""
Konfiguracja aplikacji Flask
Ustawienia bazy danych, JWT, zmienne środowiskowe
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Załaduj zmienne z pliku .env
load_dotenv()

class Config:
    """Bazowa konfiguracja aplikacji"""
    
    # Flask secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-zmien-to-w-produkcji')
    
    # Baza danych SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///olx_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-zmien-to')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    # OLX Scraper settings
    OLX_CHECK_INTERVAL_MINUTES = 15

class DevelopmentConfig(Config):
    """Ustawienia dla trybu development"""
    DEBUG = True

class ProductionConfig(Config):
    """Ustawienia dla produkcji"""
    DEBUG = False

# Aktywna konfiguracja
config = DevelopmentConfig()
