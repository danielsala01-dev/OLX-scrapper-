#!/usr/bin/env python3
"""
Email notification sender
"""

import logging
import smtplib
from typing import List, Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class EmailNotifier:
    """
    Sends email notifications for new OLX items
    """
    
    def __init__(self, config: Dict):
        """
        Initialize email notifier
        
        Args:
            config: Email configuration dictionary
        """
        self.config = config
        self.smtp_server = config.get('smtp_server')
        self.smtp_port = config.get('smtp_port', 587)
        self.sender_email = config.get('sender_email')
        self.sender_password = config.get('sender_password')
        self.recipient_email = config.get('recipient_email')
    
    def send(self, items: List[Dict]) -> bool:
        """
        Send email notification
        
        Args:
            items: List of items to notify about
            
        Returns:
            True if successful, False otherwise
        """
        try:
            message = self._create_message(items)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info(f"Email sent to {self.recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def _create_message(self, items: List[Dict]) -> MIMEMultipart:
        """
        Create email message
        
        Args:
            items: List of items to include in message
            
        Returns:
            Email message object
        """
        message = MIMEMultipart('alternative')
        message['Subject'] = f"🔔 OLX Alert: {len(items)} new item(s) found"
        message['From'] = self.sender_email
        message['To'] = self.recipient_email
        
        # Create HTML content
        html = self._create_html_content(items)
        
        # Attach HTML content
        message.attach(MIMEText(html, 'html'))
        
        return message
    
    def _create_html_content(self, items: List[Dict]) -> str:
        """
        Create HTML email content
        
        Args:
            items: List of items to include
            
        Returns:
            HTML content string
        """
        html = "<html><body>"
        html += "<h2>🔔 New OLX Items Alert</h2>"
        html += f"<p>Found {len(items)} new item(s):</p>"
        html += "<hr>"
        
        for item in items:
            html += "<div style='margin: 20px 0; padding: 10px; border: 1px solid #ccc;'>"
            html += f"<h3>{item.get('title', 'N/A')}</h3>"
            html += f"<p><strong>Category:</strong> {item.get('category', 'N/A')}</p>"
            html += f"<p><strong>Price:</strong> {item.get('price', 'N/A')}</p>"
            html += f"<p><strong>Location:</strong> {item.get('location', 'N/A')}</p>"
            html += f"<p><strong>Seller:</strong> {item.get('seller_name', 'N/A')} (Rating: {item.get('seller_rating', 'N/A')})</p>"
            
            if item.get('url'):
                html += f"<p><a href='{item.get('url')}'>View Item</a></p>"
            
            if item.get('image_url'):
                html += f"<img src='{item.get('image_url')}' style='max-width: 200px;'><br>"
            
            html += f"<p><em>Found at: {item.get('discovered_at', 'N/A')}</em></p>"
            html += "</div>"
        
        html += "</body></html>"
        return html
