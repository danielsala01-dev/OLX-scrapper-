#!/usr/bin/env python3
"""
Discord notification sender
"""

import logging
import requests
import json
from typing import List, Dict

logger = logging.getLogger(__name__)

class DiscordNotifier:
    """
    Sends Discord notifications for new OLX items
    """
    
    def __init__(self, config: Dict):
        """
        Initialize Discord notifier
        
        Args:
            config: Discord configuration dictionary
        """
        self.config = config
        self.webhook_url = config.get('webhook_url')
    
    def send(self, items: List[Dict]) -> bool:
        """
        Send Discord notification
        
        Args:
            items: List of items to notify about
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for item in items:
                payload = self._create_payload(item)
                
                response = requests.post(
                    self.webhook_url,
                    json=payload,
                    timeout=10
                )
                response.raise_for_status()
            
            logger.info(f"Discord notifications sent for {len(items)} items")
            return True
            
        except Exception as e:
            logger.error(f"Error sending Discord notification: {str(e)}")
            return False
    
    def _create_payload(self, item: Dict) -> Dict:
        """
        Create Discord webhook payload
        
        Args:
            item: Item to create payload for
            
        Returns:
            Discord webhook payload
        """
        embed = {
            "title": item.get('title', 'New Item'),
            "description": item.get('description', '')[:200],  # Limit description length
            "color": 3447003,  # Blue color
            "fields": [
                {
                    "name": "Category",
                    "value": item.get('category', 'N/A'),
                    "inline": True
                },
                {
                    "name": "Price",
                    "value": str(item.get('price', 'N/A')),
                    "inline": True
                },
                {
                    "name": "Location",
                    "value": item.get('location', 'N/A'),
                    "inline": True
                },
                {
                    "name": "Seller",
                    "value": f"{item.get('seller_name', 'N/A')} (⭐ {item.get('seller_rating', 'N/A')})",
                    "inline": True
                }
            ],
            "thumbnail": {
                "url": item.get('image_url', '')
            }
        }
        
        if item.get('url'):
            embed["url"] = item.get('url')
        
        return {
            "embeds": [embed]
        }
