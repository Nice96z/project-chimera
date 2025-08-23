# chimera_brain.py
# (Definitive, Corrected Version)
# Handles all communication with the OpenAI API for story generation.

import openai

def get_ai_response(history, client):
    """
    Sends the conversation history to the AI and gets the next part of the story.
    It now correctly uses the 'client' object passed to it.
    """
    try:
        print("...Chimera is weaving your universe...")
        
        # --- THIS IS THE FIX ---
        # We are calling the 'create' method on the 'client' object,
        # not on the 'openai' module itself.
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
            temperature=0.85,
        )
        content = response.choices[0].message.content
        return content if content else "Error: The AI returned an empty response."
    except openai.AuthenticationError:
        return "Authentication Error: Your OpenAI API key is incorrect."
    except Exception as e:
        return f"An unexpected error occurred with the OpenAI API: {e}"