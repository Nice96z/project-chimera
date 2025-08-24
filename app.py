# app.py
# (The Definitive, Corrected Version with Server-Side State Management)

import os
import json 
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from groq import Groq 

import config
from chimera_brain import get_validated_story_response

# --- Initialization ---
load_dotenv()
app = Flask(__name__) 
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key: raise ValueError("No FLASK_SECRET_KEY set for Flask application.")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Local Game Management Functions ---
# These helper functions are already well-written for server-side storage. No changes needed.
def save_game_local(filename, game_state):
    if not os.path.exists(config.SAVE_FOLDER): os.makedirs(config.SAVE_FOLDER)
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    with open(filepath, 'w') as f: json.dump(game_state, f, indent=4) 
    print(f"\n[Game state saved to server file: {filename}]")

def load_game_local(filename):
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    try:
        with open(filepath, 'r') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return None

def get_saved_games_with_details():
    if not os.path.exists(config.SAVE_FOLDER): return []
    saved_stories = []
    for f in os.listdir(config.SAVE_FOLDER):
        if f.endswith('.json'):
            data = load_game_local(f)
            if data and isinstance(data, dict):
                title = data.get('story_title', f.replace('.json', ''))
                genre = data.get('genre', 'Story')
                saved_stories.append({'title': title, 'genre': genre})
    return saved_stories

def delete_game_local(filename):
    filepath = os.path.join(config.SAVE_FOLDER, filename)
    if os.path.exists(filepath):
        try: os.remove(filepath); return True
        except Exception: return False
    return False

def get_safe_filename(title):
    return "".join(x for x in title if x.isalnum() or x in " _-").rstrip() + ".json"

# --- Frontend & API Routes ---
@app.route("/")
def home():
    session.clear() 
    return render_template("index.html", 
                           genres=config.GENRES, 
                           genre_examples=config.GENRE_EXAMPLES,
                           genre_titles=config.GENRE_TITLES)

@app.route("/api/get_saved_games", methods=["GET"])
def api_get_saved_games():
    return jsonify({"saved_games": get_saved_games_with_details()})

@app.route("/api/delete_game", methods=["POST"])
def api_delete_game():
    if not request.is_json: return jsonify({"error": "Invalid request: body must be JSON."}), 400
    data = request.get_json()
    story_title = data.get("story_title")
    if not story_title: return jsonify({"error": "Story title required."}), 400
    if delete_game_local(get_safe_filename(story_title)): return jsonify({"message": "Deleted."}), 200
    else: return jsonify({"error": "Failed to delete story."}), 404
        
@app.route("/api/load_game", methods=["POST"])
def api_load_game():
    if not request.is_json: return jsonify({"error": "Invalid request: body must be JSON."}), 400
    data = request.get_json()
    story_title = data.get("story_title")
    if not story_title: return jsonify({"error": "Story title required."}), 400
    
    filename = get_safe_filename(story_title)
    game_state = load_game_local(filename)
    
    if game_state:
        ### FIX ###
        # Instead of storing the massive game_state in the session cookie,
        # we store ONLY a tiny, unique identifier (the filename).
        session['current_game_id'] = filename
        return jsonify({"history": game_state.get("history")})
    else:
        return jsonify({"error": "Failed to load game file."}), 404

@app.route("/api/start_new_game", methods=["POST"])
def start_new_game():
    if not request.is_json: return jsonify({"error": "Invalid request: body must be JSON."}), 400
    data = request.get_json()
    genre, user_vision, story_title = data.get("genre"), data.get("user_vision"), data.get("story_title")
    if not all([genre, user_vision, story_title]): return jsonify({"error": "Missing fields."}), 400

    world_memories = {"notes": "No significant world events have been recorded."}
    player_psych_profile = {"profile": "Not yet analyzed."}
    unseen_engine_updates = {
        "npc_updates": "No off-screen NPC activity to report.", 
        "world_updates": "No major world events have occurred."
    }

    system_prompt = config.create_system_prompt(
        genre, user_vision, story_title, 
        world_memories, player_psych_profile, unseen_engine_updates
    )
    conversation_history = [{"role": "system", "content": system_prompt}]
    
    ai_response = get_validated_story_response(conversation_history, groq_client)
    
    if "Error:" not in ai_response:
        conversation_history.append({"role": "assistant", "content": ai_response})
        filename = get_safe_filename(story_title)
        
        # This large dictionary is the full state of the world.
        game_state = {
            "history": conversation_history, "filename": filename, "genre": genre,
            "story_title": story_title, "user_vision": user_vision,
            "world_memories": world_memories,
            "player_psych_profile": player_psych_profile,
            "unseen_engine_updates": unseen_engine_updates
        }
        
        ### FIX ###
        # 1. Save the full game_state to a file on the server.
        save_game_local(filename, game_state)
        # 2. Save ONLY the reference ID to the session cookie.
        session['current_game_id'] = filename
        
        return jsonify({"initial_response": ai_response})
    else:
        return jsonify({"error": ai_response}), 500

@app.route("/api/send_message", methods=["POST"])
def send_message():
    if not request.is_json: return jsonify({"error": "Invalid request: body must be JSON."}), 400
    data = request.get_json()
    user_input = data.get("message")
    if not user_input: return jsonify({"error": "Message is empty."}), 400
    
    ### FIX ###
    # This is the most critical change. The entire logic is now server-side.
    
    # 1. Get the small game ID from the session cookie.
    game_id = session.get('current_game_id')
    if not game_id:
        return jsonify({"error": "No active game session found. Your session may have expired."}), 404
    
    # 2. Load the full game state from the server's file system using the ID.
    game_state = load_game_local(game_id)
    if not game_state:
        return jsonify({"error": "Could not load game state from server. File may be missing or corrupt."}), 404
    
    conversation_history = game_state["history"]
    conversation_history.append({"role": "user", "content": user_input})

    # (In the future, your advanced AI modules like the Chronicler & Psychologist would run here,
    # updating the game_state dictionary directly before the next step.)

    updated_system_prompt = config.create_system_prompt(
        game_state["genre"], game_state["user_vision"], game_state["story_title"],
        game_state["world_memories"], game_state["player_psych_profile"], game_state["unseen_engine_updates"]
    )
    conversation_history[0] = {"role": "system", "content": updated_system_prompt}
    
    ai_response = get_validated_story_response(conversation_history, groq_client)
    
    if "Error:" not in ai_response:
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        # 3. Update the history within the main game_state dictionary.
        game_state["history"] = conversation_history
        
        # 4. Save the fully updated game state back to the server file.
        # The session cookie is untouched, as it still correctly holds the game_id.
        save_game_local(game_id, game_state)
        
        return jsonify({"response": ai_response})
    else:
        # If there's an error, we don't save the failed turn.
        return jsonify({"error": ai_response}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)