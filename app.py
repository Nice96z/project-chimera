# app.py
# The Flask Web Application Backend for Project Chimera (MVP - Definitive, Final Corrected)

import os
import json 
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
    raise ValueError("No FLASK_SECRET_KEY set for Flask application")

client = Groq(api_key=os.getenv("OPENAI_API_KEY"))

# --- Local Game Management Functions (Pulled from game_manager.py for stability) ---
def save_game_local(history, filename):
    if not os.path.exists(config.SAVE_FOLDER): os.makedirs(config.SAVE_FOLDER)
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    with open(filepath, 'w') as f: json.dump(history, f, indent=4) 
    print(f"\n[Game saved to {filename}]")

def load_game_local(filename):
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'history' in data: return data['history']
            elif isinstance(data, list): return data
            return None
    except (FileNotFoundError, json.JSONDecodeError): return None

def get_saved_games_local():
    if not os.path.exists(config.SAVE_FOLDER): return []
    return [f for f in os.listdir(config.SAVE_FOLDER) if f.endswith('.json')]

def delete_game_local(filename):
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            print(f"[Game file deleted: {filename}]")
            return True
        except Exception as e:
            print(f"[Error deleting file {filename}: {e}]")
            return False
    else:
        print(f"[Deletion failed: File not found {filename}]")
        return False


# --- Frontend Routes ---
@app.route("/")
def home():
    session.clear() 
    return render_template("index.html",genres=config.GENRES, 
                           genre_examples=config.GENRE_EXAMPLES, 
                           genre_titles=config.GENRE_TITLES)

# --- API Routes ---
@app.route("/api/delete_game", methods=["POST"])
def api_delete_game():
    data = request.json
    if not data or "story_title" not in data: return jsonify({"error": "Story title is required for deletion."}), 400
    story_title = data["story_title"]
    filename = story_title + ".json"
    if ".." in filename or "/" in filename or "\\" in filename: return jsonify({"error": "Invalid filename."}), 400
    if delete_game_local(filename):
        return jsonify({"message": f"'{story_title}' was successfully deleted."}), 200
    else:
        return jsonify({"error": f"Could not find or delete the story '{story_title}'."}), 404
        
@app.route("/api/get_saved_games", methods=["GET"])
def api_get_saved_games():
    saved_games = get_saved_games_local()
    display_names = [game.replace('.json', '') for game in saved_games]
    return jsonify({"saved_games": display_names})

@app.route("/api/load_game", methods=["POST"])
def api_load_game():
    data = request.json
    if not data or "story_title" not in data: return jsonify({"error": "Story title is required."}), 400
    story_title = data["story_title"]
    filename = story_title + ".json"
    history = load_game_local(filename)
    if history:
        session['game_state'] = {"history": history, "filename": filename}
        return jsonify({"history": history})
    else:
        return jsonify({"error": "Failed to load game file."}), 404

@app.route("/api/start_new_game", methods=["POST"])
def start_new_game():
    data = request.json
    if not data: return jsonify({"error": "Invalid request."}), 400
    genre, user_vision, story_title = data.get("genre"), data.get("user_vision"), data.get("story_title")
    if not all([genre, user_vision, story_title]): return jsonify({"error": "Missing fields."}), 400
    system_prompt = config.create_system_prompt(genre, user_vision, story_title)
    conversation_history = [{"role": "system", "content": system_prompt}]
    
    # We now correctly pass the client object to our get_ai_response function
    ai_response = get_ai_response(conversation_history, client)
    
    if ai_response and "Error:" not in ai_response:
        conversation_history.append({"role": "assistant", "content": ai_response})
        filename = "".join(x for x in story_title if x.isalnum() or x in " _-").rstrip() + ".json"
        session['game_state'] = {"history": conversation_history, "filename": filename}
        save_game_local(conversation_history, filename)
        return jsonify({"initial_response": ai_response})
    else:
        return jsonify({"error": "Failed to initialize story."}), 500

@app.route("/api/send_message", methods=["POST"])
def send_message():
    data = request.json
    if not data: return jsonify({"error": "Invalid request."}), 400
    user_input = data.get("message")
    if not user_input: return jsonify({"error": "Message is empty."}), 400
    
    game_state = session.get('game_state')
    if not game_state: return jsonify({"error": "No active game session."}), 404
    
    conversation_history, filename = game_state["history"], game_state["filename"]
    conversation_history.append({"role": "user", "content": user_input})
    
    # We now correctly pass the client object
    ai_response = get_ai_response(conversation_history, client)
    
    if ai_response and "Error:" not in ai_response:
        conversation_history.append({"role": "assistant", "content": ai_response})
        game_state["history"] = conversation_history
        session['game_state'] = game_state
        save_game_local(conversation_history, filename)
        return jsonify({"response": ai_response})
    else:
        conversation_history.pop()
        error_message = ai_response or "The AI failed to respond."
        return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)