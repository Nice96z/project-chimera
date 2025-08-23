# game_manager.py
# (Version 3.0 - Text-Only MVP)
# Handles saving and loading the text-based story history.

import os
import json
import config

def save_game(history, filename):
    """Saves the story history to a JSON file."""
    if not os.path.exists(config.SAVE_FOLDER):
        os.makedirs(config.SAVE_FOLDER)
    
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    # The save file is now just the list of conversation history.
    with open(filepath, 'w') as f:
        json.dump(history, f, indent=4)
    print(f"\n[Game saved to {filename}]")

def load_game(filename):
    """Loads a story history from a JSON file."""
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            # This handles both our new saves and ALL previous versions seamlessly.
            # If it's a dictionary with a "history" key, get it.
            if isinstance(data, dict):
                return data.get("history")
            # If it's just a list, return it directly.
            elif isinstance(data, list):
                return data
            else:
                return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def get_saved_games():
    """Returns a list of saved game files."""
    if not os.path.exists(config.SAVE_FOLDER):
        return []
    return [f for f in os.listdir(config.SAVE_FOLDER) if f.endswith('.json')]