#!/usr/bin/env python3
"""
Main entry point for OLX Notification System
"""

import json
import logging
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from olx.scraper import OLXScraper
from notifications.notifier import NotificationManager
from database.db import Database
from utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

def load_config(config_path="config.json"):
    """
    Load configuration from JSON file
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file '{config_path}' not found.")
        logger.error("Please copy config.example.json to config.json and configure it.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in '{config_path}'")
        raise

def cleanup_expired_listings():
    """
    Scheduled task to remove expired listings from the database.
    """
    try:
        logger.info("Running expired listings cleanup...")
        config = load_config()
        db = Database(config['database'])
        deleted = db.delete_expired_items()
        logger.info(f"Cleanup complete: {deleted} expired listing(s) removed")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}", exc_info=True)


def check_listings():
    """
    Scheduled task to check for new OLX listings
    """
    try:
        logger.info("Starting OLX listings check...")
        
        # Load configuration
        config = load_config()
        
        # Initialize database
        db = Database(config['database'])
        
        # Initialize scraper
        scraper = OLXScraper(config['olx'])
        
        # Get new listings
        new_items = scraper.get_new_listings(db, config['olx']['categories'])
        
        if new_items:
            logger.info(f"Found {len(new_items)} new items")
            
            # Send notifications
            notifier = NotificationManager(config['notifications'])
            notifier.notify_items(new_items)
            
            # Store items in database
            db.store_items(new_items)
        else:
            logger.info("No new items found")
            
    except Exception as e:
        logger.error(f"Error during listings check: {str(e)}", exc_info=True)

def main():
    """
    Main function to start the OLX monitoring system
    """
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Initialize database
        db = Database(config['database'])
        db.initialize()
        logger.info("Database initialized")
        
        # Setup scheduler
        scheduler = BackgroundScheduler()
        check_interval = config['olx'].get('check_interval_minutes', 15)
        
        # Add the check_listings job
        scheduler.add_job(
            check_listings,
            'interval',
            minutes=check_interval,
            id='olx_check',
            name='OLX Listings Check'
        )

        # Add cleanup job every 30 minutes
        scheduler.add_job(
            cleanup_expired_listings,
            'interval',
            minutes=30,
            id='cleanup_expired',
            name='Expired Listings Cleanup'
        )
        
        logger.info(f"Scheduler configured to check every {check_interval} minutes")
        
        # Start scheduler
        scheduler.start()
        logger.info("OLX Notification System started successfully")
        logger.info("Press Ctrl+C to stop")
        
        # Keep the application running
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
            scheduler.shutdown()
            logger.info("OLX Notification System stopped")
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
