# shared_utils.py
import os
import random
import logging
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_naive
from datetime import datetime

logger = logging.getLogger(__name__)

def ensure_datetime(value):
    if isinstance(value, str):
        value = parse_datetime(value)
    return value

def datetime_to_str(dt):
    if isinstance(dt, str):
        dt = parse_datetime(dt)
    if dt:
        if is_aware(dt):
            dt = make_naive(dt)
        return dt.strftime('%Y-%m-%d %H:%M')
    return None

def safe_make_naive(dt):
    dt = ensure_datetime(dt)
    if dt is None:
        return None
    return make_naive(dt) if is_aware(dt) else dt

def get_random_saying(file_path):
    if not os.path.exists(file_path):
        logger.error(f"Failed to read sayings file: [Errno 2] No such file or directory: '{file_path}'")
        return "No sayings available."
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sayings = [line.strip() for line in file if line.strip()]
        
        if not sayings:
            logger.error("Sayings file is empty.")
            return "No sayings available."
        
        return random.choice(sayings)
    except Exception as e:
        logger.error(f"Error reading sayings file: {e}")
        return "No sayings available."
