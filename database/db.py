"""
Funkcje pomocnicze do pracy z bazą danych
- inicjalizacja bazy
- operacje CRUD (Create, Read, Update, Delete)
"""

from .models import db, User, UserPreferences, Listings
from datetime import datetime

def init_db(app):
    """Inicjalizuj bazę danych - stwórz wszystkie tabele"""
    with app.app_context():
        db.create_all()
        print("✅ Baza danych zainicjalizowana")

def create_user(email, password):
    """Stwórz nowego użytkownika"""
    # Sprawdź czy user już istnieje
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "User już istnieje"
    
    # Stwórz nowego usera
    user = User(email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    return user, "OK"

def get_user_by_email(email):
    """Pobierz usera po emailu"""
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    """Pobierz usera po ID"""
    return User.query.get(user_id)

def add_user_preference(user_id, category, keywords):
    """Dodaj preferencję wyszukiwania dla usera"""
    pref = UserPreferences(user_id=user_id, category=category, keywords=keywords)
    db.session.add(pref)
    db.session.commit()
    return pref

def get_user_preferences(user_id):
    """Pobierz wszystkie preferencje usera"""
    return UserPreferences.query.filter_by(user_id=user_id).all()

def delete_preference(pref_id):
    """Usuń preferencję"""
    pref = UserPreferences.query.get(pref_id)
    if pref:
        db.session.delete(pref)
        db.session.commit()
        return True
    return False

def add_listing(user_id, olx_id, title, price, category, url, description=None):
    """Dodaj znalezione ogłoszenie"""
    listing = Listings(
        user_id=user_id,
        olx_id=olx_id,
        title=title,
        price=price,
        category=category,
        url=url,
        description=description
    )
    db.session.add(listing)
    db.session.commit()
    return listing

def get_user_listings(user_id, limit=50):
    """Pobierz ogłoszenia dla usera"""
    return Listings.query.filter_by(user_id=user_id).order_by(Listings.created_at.desc()).limit(limit).all()

def listing_exists(olx_id):
    """Sprawdź czy ogłoszenie już istnieje w bazie"""
    return Listings.query.filter_by(olx_id=olx_id).first() is not None
