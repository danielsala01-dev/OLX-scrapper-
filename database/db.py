#!/usr/bin/env python3
"""
Database management module
"""

import logging
from typing import List, Dict, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, OLXItem

logger = logging.getLogger(__name__)

class Database:
    """
    Database manager for OLX items
    """
    
    def __init__(self, config: Dict):
        """
        Initialize database connection
        
        Args:
            config: Database configuration dictionary
        """
        self.config = config
        self.db_type = config.get('type', 'sqlite')
        
        if self.db_type == 'sqlite':
            db_path = config.get('path', 'olx_items.db')
            self.connection_string = f'sqlite:///{db_path}'
        else:
            # Add support for other databases as needed
            raise ValueError(f"Unsupported database type: {self.db_type}")
        
        self.engine = create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)
    
    def initialize(self):
        """
        Initialize database tables
        """
        try:
            Base.metadata.create_all(self.engine)
            logger.info(f"Database initialized at {self.config.get('path', 'olx_items.db')}")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def item_exists(self, item_id: str) -> bool:
        """
        Check if an item already exists in the database
        
        Args:
            item_id: ID of the item to check
            
        Returns:
            True if item exists, False otherwise
        """
        try:
            session = self.Session()
            item = session.query(OLXItem).filter(OLXItem.id == item_id).first()
            session.close()
            return item is not None
        except Exception as e:
            logger.error(f"Error checking if item exists: {str(e)}")
            return False
    
    def store_items(self, items: List[Dict]):
        """
        Store new items in database
        
        Args:
            items: List of item dictionaries to store
        """
        try:
            session = self.Session()
            
            for item in items:
                # Check if item already exists
                existing = session.query(OLXItem).filter(OLXItem.id == item.get('id')).first()
                
                if not existing:
                    db_item = OLXItem(
                        id=item.get('id'),
                        title=item.get('title'),
                        description=item.get('description'),
                        category=item.get('category'),
                        price=item.get('price'),
                        location=item.get('location'),
                        seller_name=item.get('seller_name'),
                        seller_rating=item.get('seller_rating'),
                        url=item.get('url'),
                        image_url=item.get('image_url'),
                        notification_sent=item.get('notification_sent', False)
                    )
                    session.add(db_item)
            
            session.commit()
            logger.info(f"Stored {len(items)} items in database")
            
        except Exception as e:
            logger.error(f"Error storing items: {str(e)}")
            session.rollback()
        finally:
            session.close()
    
    def get_recent_items(self, limit: int = 10) -> List[Dict]:
        """
        Get recently discovered items
        
        Args:
            limit: Maximum number of items to return
            
        Returns:
            List of recent items
        """
        try:
            session = self.Session()
            items = session.query(OLXItem).order_by(OLXItem.discovered_at.desc()).limit(limit).all()
            session.close()
            return [item.to_dict() for item in items]
        except Exception as e:
            logger.error(f"Error retrieving recent items: {str(e)}")
            return []
    
    def get_items_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """
        Get items by category
        
        Args:
            category: Category to filter by
            limit: Maximum number of items to return
            
        Returns:
            List of items in the category
        """
        try:
            session = self.Session()
            items = session.query(OLXItem).filter(OLXItem.category == category).order_by(
                OLXItem.discovered_at.desc()
            ).limit(limit).all()
            session.close()
            return [item.to_dict() for item in items]
        except Exception as e:
            logger.error(f"Error retrieving items by category: {str(e)}")
            return []
