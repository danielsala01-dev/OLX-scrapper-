# OLX Notification System

A Python-based notification system that monitors OLX listings and alerts you when new items are listed in your selected categories.

## Features

- 🔍 Monitor multiple OLX categories
- 🔔 Real-time notifications (Email, Discord, Slack)
- 💾 Automatic tracking of seen items
- ⏰ Configurable check intervals
- 🎯 Category selection via configuration

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/danielsala01-dev/OLX-scrapper-.git
   cd OLX-scrapper-
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your settings:
   ```bash
   cp config.example.json config.json
   # Edit config.json with your preferences
   ```

5. Run the application:
   ```bash
   python main.py
   ```

## Configuration

Edit `config.json` to set:
- OLX categories to monitor
- Notification preferences (email, Discord, etc.)
- Check interval (in minutes)
- API credentials

## Project Structure

```
.
├── main.py                 # Entry point
├── config.json             # Configuration file
├── requirements.txt        # Python dependencies
├── olx/
│   ├── __init__.py
│   ├── api.py              # OLX API integration
│   └── scraper.py          # Item scraping logic
├── database/
│   ├── __init__.py
│   ├── db.py               # Database management
│   └── models.py           # Database models
├── notifications/
│   ├── __init__.py
│   ├── notifier.py         # Base notifier class
│   ├── email_notifier.py   # Email notifications
│   ├── discord_notifier.py # Discord notifications
│   └── slack_notifier.py   # Slack notifications
└── utils/
    ├── __init__.py
    └── logger.py           # Logging utilities
```

## License

MIT
