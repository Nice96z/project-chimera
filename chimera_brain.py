# chimera_brain.py
# (Definitive, Corrected Version)

import config

STORYTELLER_MODEL = "llama3-70b-8192"
EDITOR_MODEL = "llama3-8b-8192"
MAX_RETRIES = 2

def _call_groq_model(client, conversation_history, model_to_use):
    """Private helper to call the Groq API and handle errors."""
    try:
        chat_completion = client.chat.completions.create(
            messages=conversation_history, model=model_to_use,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API ({model_to_use}): {e}")
        return f"Error: The AI model could not be reached. Please try again later."

def get_validated_story_response(conversation_history, groq_client):
    """
    Implements the Editor Loop: gets a response from Chimera, checks it with a
    faster model, and retries on failure to ensure high quality.
    """
    original_system_prompt_content = conversation_history[0]['content']
    current_retries = 0
    
    ### FIX: Initialize story_response to prevent the 'possibly unbound' error.
    story_response = "" 

    while current_retries <= MAX_RETRIES:
        print(f"[Brain]: Calling Storyteller (Attempt {current_retries + 1})...")
        story_response = _call_groq_model(groq_client, conversation_history, STORYTELLER_MODEL)
        if "Error:" in story_response: return story_response 

        print("[Brain]: Calling Editor for validation...")
        editor_prompt_text = config.create_editor_prompt(story_response)
        editor_conversation = [{"role": "user", "content": editor_prompt_text}]
        validation_result = _call_groq_model(groq_client, editor_conversation, EDITOR_MODEL)

        if "PASS" in validation_result:
            print("[Brain]: Editor check: PASS.")
            # Restore the original, clean prompt before returning
            conversation_history[0]['content'] = original_system_prompt_content
            return story_response
        else:
            print(f"[Brain]: Editor check: FAIL. Regenerating...")
            current_retries += 1
            # Add a correction message for the next attempt
            correction_message = (
                "\n\n--- URGENT CORRECTION ---\nYour previous response failed a quality check. "
                "Regenerate your response, paying strict attention to every rule in your system prompt."
            )
            conversation_history[0]['content'] = original_system_prompt_content + correction_message
    
    # Restore the original prompt even if we fall through
    conversation_history[0]['content'] = original_system_prompt_content
    print("[Brain]: Warning! Max retries reached. Returning last response.")
    return story_response + "\n\n[System Warning: This response may have quality issues.]"