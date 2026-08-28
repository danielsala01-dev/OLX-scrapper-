#!/usr/bin/env python3
"""
Slack notification sender
"""

import logging
import requests
import json
from typing import List, Dict

logger = logging.getLogger(__name__)

class SlackNotifier:
    """
    Sends Slack notifications for new OLX items
    """
    
    def __init__(self, config: Dict):
        """
        Initialize Slack notifier
        
        Args:
            config: Slack configuration dictionary
        """
        self.config = config
        self.webhook_url = config.get('webhook_url')
    
    def send(self, items: List[Dict]) -> bool:
        """
        Send Slack notification
        
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
            
            logger.info(f"Slack notifications sent for {len(items)} items")
            return True
            
        except Exception as e:
            logger.error(f"Error sending Slack notification: {str(e)}")
            return False
    
    def _create_payload(self, item: Dict) -> Dict:
        """
        Create Slack webhook payload
        
        Args:
            item: Item to create payload for
            
        Returns:
            Slack webhook payload
        """
        return {
            "text": f"🔔 New OLX Item: {item.get('title', 'New Item')}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🔔 New OLX Listing",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{item.get('title', 'New Item')}*\n{item.get('description', '')[:150]}"
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": item.get('image_url', ''),
                        "alt_text": "Item image"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Category:*\n{item.get('category', 'N/A')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Price:*\n{item.get('price', 'N/A')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Location:*\n{item.get('location', 'N/A')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Seller:*\n{item.get('seller_name', 'N/A')} ⭐ {item.get('seller_rating', 'N/A')}"
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View Item",
                                "emoji": True
                            },
                            "url": item.get('url', ''),
                            "style": "primary"
                        }
                    ]
                }
            ]
        }
