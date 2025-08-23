# chimera_brain.py
# (Version 2.0 - Powered by Groq and Llama 3)
# Handles all communication with the Groq API for ultra-fast story generation.

def get_ai_response(history, client):
    """
    Sends the conversation history to the Groq API and gets the next part of the story.
    """
    try:
        print("...Chimera is weaving your universe (at Groq speed)...")
        
        # This is the new Groq API call. It uses the same structure as OpenAI.
        response = client.chat.completions.create(
            # We are now using Llama 3, a powerful and fast open-source model.
            # The model name includes the context size (8192 tokens).
            model="llama3-8b-8192", 
            messages=history,
            temperature=0.8, # A slightly lower temperature can be good for story consistency
        )
        content = response.choices[0].message.content
        return content if content else "Error: The AI returned an empty response."
    except Exception as e:
        # We catch any kind of error from the API call and report it.
        # This is important for debugging deployment issues.
        return f"An unexpected error occurred with the Groq API: {e}"