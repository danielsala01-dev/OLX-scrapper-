#!/usr/bin/env python3
"""
OLX Scraper module

Handles scraping and processing of OLX listings
"""

import logging
from typing import List, Dict
from datetime import datetime
from olx.api import OLXAPIClient
from database.db import Database

logger = logging.getLogger(__name__)

class OLXScraper:
    """
    Scraper for OLX listings
    """
    
    def __init__(self, config: Dict):
        """
        Initialize OLX scraper
        
        Args:
            config: Configuration dictionary with OLX settings
        """
        self.config = config
        self.api_client = OLXAPIClient(config['base_url'])
        self.location = config.get('location', '')
    
    def get_new_listings(self, db: Database, categories: List[str]) -> List[Dict]:
        """
        Fetch new listings from OLX that haven't been seen before
        
        Args:
            db: Database instance for checking seen items
            categories: List of categories to check
            
        Returns:
            List of new items
        """
        new_items = []
        
        for category in categories:
            logger.info(f"Checking category: {category}")
            
            listings = self.api_client.get_listings(category, self.location)
            
            if listings is None:
                logger.warning(f"Failed to fetch listings for {category}")
                continue
            
            for item in listings:
                # Check if item already exists in database
                if not db.item_exists(item.get('id')):
                    # Enrich item data
                    enriched_item = self._enrich_item(item, category)
                    new_items.append(enriched_item)
                    logger.info(f"New item found: {enriched_item.get('title')} (ID: {enriched_item.get('id')})")
        
        return new_items
    
    def _enrich_item(self, item: Dict, category: str) -> Dict:
        """
        Add additional information to an item
        
        Args:
            item: Item data from API
            category: Category the item belongs to
            
        Returns:
            Enriched item data
        """
        enriched = item.copy()
        enriched['category'] = category
        enriched['discovered_at'] = datetime.now().isoformat()
        enriched['notification_sent'] = False
        
        return enriched
