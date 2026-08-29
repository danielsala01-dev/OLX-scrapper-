"""
Logika scrapowania OLX
Pobiera ogłoszenia na podstawie preferencji usera
"""

from database.db import add_listing, listing_exists
import requests
from datetime import datetime

def get_listings_for_preferences(user_id, preferences):
    """
    Pobierz ogłoszenia z OLX dla preferencji usera
    
    Args:
        user_id: ID usera
        preferences: lista UserPreferences
    
    Returns:
        lista nowych Listings
    """
    
    new_listings = []
    
    # TODO: Zaimplementuj prawdziwy scraper OLX
    # Na razie zwracamy mock data
    
    for pref in preferences:
        # Mock data - zastąpi to prawdziwy scraper
        mock_listings = [
            {
                'olx_id': f'mock_{pref.category}_1',
                'title': f'Test {pref.category} 1 - {pref.keywords}',
                'price': 99.99,
                'category': pref.category,
                'url': 'https://olx.com.br/example1',
                'description': 'To jest testowe ogłoszenie'
            },
            {
                'olx_id': f'mock_{pref.category}_2',
                'title': f'Test {pref.category} 2 - {pref.keywords}',
                'price': 199.99,
                'category': pref.category,
                'url': 'https://olx.com.br/example2',
                'description': 'To jest drugie testowe ogłoszenie'
            }
        ]
        
        # Dodaj do bazy (jeśli już nie istnieje)
        for listing_data in mock_listings:
            if not listing_exists(listing_data['olx_id']):
                listing = add_listing(
                    user_id=user_id,
                    olx_id=listing_data['olx_id'],
                    title=listing_data['title'],
                    price=listing_data['price'],
                    category=listing_data['category'],
                    url=listing_data['url'],
                    description=listing_data['description']
                )
                new_listings.append(listing)
    
    return new_listings

# TODO: Funkcje do implementacji
# def scrape_olx_api(category, keywords, location):
#     """Scrapa OLX API dla kategorii i słów kluczowych"""
#     pass
# 
# def filter_listings_by_keywords(listings, keywords):
#     """Filtruje ogłoszenia po słowach kluczowych"""
#     pass
