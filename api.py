#!/usr/bin/env python3
"""
Simple Flask API for OLX Scraper - Testing only
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Dummy data
