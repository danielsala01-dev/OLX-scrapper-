#!/usr/bin/env python3
"""
Database models for OLX items
"""

from sqlalchemy import Column, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class OLXItem(Base):
    """
    Model for OLX items stored in database
    """
    __tablename__ = 'olx_items'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)
    price = Column(Float)
    location = Column(String)
    seller_name = Column(String)
    seller_rating = Column(Float)
    url = Column(String)
    image_url = Column(String)
    discovered_at = Column(DateTime, default=datetime.now)
    notification_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<OLXItem(id={self.id}, title={self.title}, category={self.category})>"
    
    def to_dict(self):
        """
        Convert model to dictionary
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'location': self.location,
            'seller_name': self.seller_name,
            'seller_rating': self.seller_rating,
            'url': self.url,
            'image_url': self.image_url,
            'discovered_at': self.discovered_at.isoformat() if self.discovered_at else None,
        }
