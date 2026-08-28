#!/usr/bin/env python3
"""
OLX API integration module

Handles communication with OLX API to fetch listings
"""

import requests
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class OLXAPIClient:
    """
    Client for OLX API interactions
    """
    
    def __init__(self, base_url: str):
        """
        Initialize OLX API client
        
        Args:
            base_url: Base URL for OLX API
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_listings(self, category: str, location: str, limit: int = 50) -> Optional[List[Dict]]:
        """
        Fetch listings from OLX for a specific category
        
        Args:
            category: OLX category to fetch
            location: Location to search in
            limit: Maximum number of listings to fetch
            
        Returns:
            List of listings or None if error occurred
        """
        try:
            # Construct API endpoint
            endpoint = f"{self.base_url}/listings"
            
            params = {
                'category': category,
                'region': location,
                'limit': limit,
                'sort': 'newest'
            }
            
            logger.info(f"Fetching listings for category: {category}, location: {location}")
            
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'listings' in data:
                logger.info(f"Retrieved {len(data['listings'])} listings for {category}")
                return data['listings']
            else:
                logger.warning(f"Unexpected API response format for {category}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error for category {category}: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"JSON parsing error for category {category}: {str(e)}")
            return None
    
    def get_item_details(self, item_id: str) -> Optional[Dict]:
        """
        Fetch detailed information about a specific item
        
        Args:
            item_id: ID of the item to fetch
            
        Returns:
            Item details or None if error occurred
        """
        try:
            endpoint = f"{self.base_url}/listings/{item_id}"
            
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching item {item_id}: {str(e)}")
            return None
    
    def get_categories(self) -> Optional[List[Dict]]:
        """
        Fetch available OLX categories
        
        Returns:
            List of available categories or None if error occurred
        """
        try:
            endpoint = f"{self.base_url}/categories"
            
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Retrieved {len(data.get('categories', []))} categories")
            
            return data.get('categories', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching categories: {str(e)}")
            return None
