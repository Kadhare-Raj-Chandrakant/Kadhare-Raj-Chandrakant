#!/usr/bin/env python3
"""
Configuration module for GitHub Contribution Snake
"""

import os

def get_github_username():
    username = os.getenv('GITHUB_USERNAME')
    if not username:
        print("Error: GITHUB_USERNAME environment variable is required")
        return None
    return username

def get_github_token():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable is required")
        return None
    return token

def validate_config():
    username = get_github_username()
    token = get_github_token()
    if not username or not token:
        return False
    return True

SNAKE_CONFIG = {
    'cell_size': 11,
    'cell_spacing': 3,
    'snake_length': 6,
    'animation_duration': 120,
    'padding': 30
}

COLORS = {
    'dark': {
        'background': '#0d1117',
        'grid': '#21262d',
        'levels': ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353'],
        'snake': '#f85149',
        'snake_head': '#ff6b6b'
    },
    'light': {
        'background': '#ffffff',
        'grid': '#ebedf0',
        'levels': ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'],
        'snake': '#f85149',
        'snake_head': '#ff6b6b'
    }
}
