#!/usr/bin/env python3
"""
Notification system for OLX items
"""

import logging
from typing import List, Dict
from abc import ABC, abstractmethod
from notifications.email_notifier import EmailNotifier
from notifications.discord_notifier import DiscordNotifier
from notifications.slack_notifier import SlackNotifier

logger = logging.getLogger(__name__)

class BaseNotifier(ABC):
    """
    Abstract base class for notifiers
    """
    
    @abstractmethod
    def send(self, items: List[Dict]) -> bool:
        """
        Send notification
        
        Args:
            items: List of items to notify about
            
        Returns:
            True if successful, False otherwise
        """
        pass

class NotificationManager:
    """
    Manages multiple notification channels
    """
    
    def __init__(self, config: Dict):
        """
        Initialize notification manager
        
        Args:
            config: Notification configuration dictionary
        """
        self.config = config
        self.notifiers = []
        self._initialize_notifiers()
    
    def _initialize_notifiers(self):
        """
        Initialize active notifiers based on configuration
        """
        # Email notifier
        if self.config.get('email', {}).get('enabled', False):
            self.notifiers.append(EmailNotifier(self.config['email']))
            logger.info("Email notifier initialized")
        
        # Discord notifier
        if self.config.get('discord', {}).get('enabled', False):
            self.notifiers.append(DiscordNotifier(self.config['discord']))
            logger.info("Discord notifier initialized")
        
        # Slack notifier
        if self.config.get('slack', {}).get('enabled', False):
            self.notifiers.append(SlackNotifier(self.config['slack']))
            logger.info("Slack notifier initialized")
        
        if not self.notifiers:
            logger.warning("No notifiers configured")
    
    def notify_items(self, items: List[Dict]):
        """
        Send notifications through all active channels
        
        Args:
            items: List of items to notify about
        """
        if not items:
            logger.info("No items to notify about")
            return
        
        logger.info(f"Sending notifications for {len(items)} items through {len(self.notifiers)} channels")
        
        for notifier in self.notifiers:
            try:
                success = notifier.send(items)
                if success:
                    logger.info(f"Notification sent successfully via {notifier.__class__.__name__}")
                else:
                    logger.warning(f"Failed to send notification via {notifier.__class__.__name__}")
            except Exception as e:
                logger.error(f"Error sending notification via {notifier.__class__.__name__}: {str(e)}")
