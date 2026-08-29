"""
Modele bazy danych
- User: użytkownik aplikacji
- UserPreferences: preferencje wyszukiwania (kategorie + słowa)
- Listings: znalezione ogłoszenia z OLX
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Inicjalizacja SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """
    Model użytkownika
    Przechowuje: email, hasło (zaszyfrowane), datę rejestracji
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacje do innych tabel
    preferences = db.relationship('UserPreferences', backref='user', lazy=True, cascade='all, delete-orphan')
    listings = db.relationship('Listings', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Zaszyfruj hasło przed zapisaniem"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Sprawdź czy hasło się zgadza"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Konwertuj model do JSON"""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class UserPreferences(db.Model):
    """
    Model preferencji użytkownika
    Przechowuje: kategorie i słowa kluczowe do wyszukiwania
    Przykład: kategoria="electronics", keywords="iPhone 14, iPhone 15"
    """
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    keywords = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Konwertuj do JSON"""
        return {
            'id': self.id,
            'category': self.category,
            'keywords': self.keywords,
            'created_at': self.created_at.isoformat()
        }

class Listings(db.Model):
    """
    Model ogłoszeń z OLX
    Przechowuje znalezione aukcje dla każdego użytkownika
    """
    __tablename__ = 'listings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    olx_id = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Konwertuj do JSON"""
        return {
            'id': self.id,
            'olx_id': self.olx_id,
            'title': self.title,
            'price': self.price,
            'category': self.category,
            'url': self.url,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }
