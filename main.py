# main.py
# (The Definitive, Corrected Version with Groq - Final Build)
# The main entry point and game loop for Project Chimera.

import os
import json 
import random
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from groq import Groq 

# Import our custom modules
import config
from chimera_brain import get_ai_response

# --- Initialization ---
load_dotenv()
app = Flask(__name__) 
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise ValueError("No FLASK_SECRET_KEY set for Flask application.")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# --- Local Game Management Functions ---
def save_game_local(history, genre, filename):
    """Saves the story history and genre to a JSON file."""
    if not os.path.exists(config.SAVE_FOLDER):
        os.makedirs(config.SAVE_FOLDER)
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    save_data = {"history": history, "genre": genre}
    with open(filepath, 'w') as f:
        json.dump(save_data, f, indent=4) 
    print(f"\n[Game saved to {filename}]")

def load_game_local(filename):
    """Loads a story history and genre from a JSON file."""
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            history, genre = None, "Story" # Safe defaults
            if isinstance(data, dict):
                history = data.get("history")
                genre = data.get("genre", "Story")
            elif isinstance(data, list):
                history = data # Backward compatibility
            return history, genre
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

def get_saved_games_with_details():
    """Reads all save files and extracts their title and genre."""
    if not os.path.exists(config.SAVE_FOLDER):
        return []
    
    saved_stories = []
    for filename in os.listdir(config.SAVE_FOLDER):
        if filename.endswith('.json'):
            filepath = os.path.join(config.SAVE_FOLDER, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    title = filename.replace('.json', '')
                    genre = "Story" 
                    if isinstance(data, dict):
                        genre = data.get('genre', 'Story')
                    saved_stories.append({'title': title, 'genre': genre})
            except Exception as e:
                print(f"Error reading save file {filename}: {e}")
                saved_stories.append({'title': filename.replace('.json', ''), 'genre': 'Unknown'})
    return saved_stories

def delete_game_local(filename):
    """Securely deletes a specified save game file."""
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath); return True
        except Exception: return False
    return False


# --- Frontend Routes ---
@app.route("/")
def home():
    """Serves the main HTML page for the game."""
    session.clear() 
    return render_template("index.html")


# --- API Routes ---
@app.route("/api/get_saved_games", methods=["GET"])
def api_get_saved_games():
    """API endpoint to get the rich list of saved games for the Library View."""
    return jsonify({"saved_games": get_saved_games_with_details()})

@app.route("/api/delete_game", methods=["POST"])
def api_delete_game():
    data = request.json
    # --- SAFETY CHECK ---
    if not data: return jsonify({"error": "Invalid request."}), 400
    story_title = data.get("story_title")
    if not story_title: return jsonify({"error": "Story title required."}), 400
    filename = story_title + ".json"
    if delete_game_local(filename):
        return jsonify({"message": f"'{story_title}' deleted."}), 200
    else:
        return jsonify({"error": "Failed to delete story."}), 404
        
@app.route("/api/load_game", methods=["POST"])
def api_load_game():
    data = request.json
    # --- SAFETY CHECK ---
    if not data: return jsonify({"error": "Invalid request."}), 400
    story_title = data.get("story_title")
    if not story_title: return jsonify({"error": "Story title is required."}), 400
    filename = story_title + ".json"
    history, genre = load_game_local(filename)
    if history:
        session['game_state'] = {"history": history, "filename": filename, "genre": genre}
        return jsonify({"history": history})
    else:
        return jsonify({"error": "Failed to load game file."}), 404

@app.route("/api/start_new_game", methods=["POST"])
def start_new_game():
    data = request.json
    # --- SAFETY CHECK ---
    if not data: return jsonify({"error": "Invalid request."}), 400
    genre, user_vision, story_title = data.get("genre"), data.get("user_vision"), data.get("story_title")
    if not all([genre, user_vision, story_title]): return jsonify({"error": "Missing fields."}), 400

    system_prompt = config.create_system_prompt(genre, user_vision, story_title)
    conversation_history = [{"role": "system", "content": system_prompt}]
    
    ai_response = get_ai_response(conversation_history, groq_client)
    
    if ai_response and "Error:" not in ai_response:
        conversation_history.append({"role": "assistant", "content": ai_response})
        filename = "".join(x for x in story_title if x.isalnum() or x in " _-").rstrip() + ".json"
        session['game_state'] = {"history": conversation_history, "filename": filename, "genre": genre}
        save_game_local(conversation_history, genre, filename)
        return jsonify({"initial_response": ai_response})
    else:
        return jsonify({"error": "Failed to initialize story."}), 500

@app.route("/api/send_message", methods=["POST"])
def send_message():
    data = request.json
    # --- SAFETY CHECK ---
    if not data: return jsonify({"error": "Invalid request."}), 400
    user_input = data.get("message")
    if not user_input: return jsonify({"error": "Message is empty."}), 400
    
    game_state = session.get('game_state')
    if not game_state: return jsonify({"error": "No active session."}), 404
    
    conversation_history, filename, genre = game_state["history"], game_state["filename"], game_state["genre"]
    conversation_history.append({"role": "user", "content": user_input})
    
    ai_response = get_ai_response(conversation_history, groq_client)
    
    if ai_response and "Error:" not in ai_response:
        conversation_history.append({"role": "assistant", "content": ai_response})
        game_state["history"] = conversation_history
        session['game_state'] = game_state
        save_game_local(conversation_history, genre, filename)
        return jsonify({"response": ai_response})
    else:
        conversation_history.pop()
        error_message = ai_response or "The AI failed to respond."
        return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)