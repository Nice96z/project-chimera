# main.py
# (Version MVP 1.0 - The Text Engine)
# The main entry point and game loop for Project Chimera.

import os
from dotenv import load_dotenv
from openai import OpenAI

# Import our custom modules, now simplified
import config
from chimera_brain import get_ai_response
from game_manager import save_game, load_game, get_saved_games

def main():
    """Main function to run the game."""
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY not set in .env file.")
        return

    client = OpenAI(api_key=OPENAI_API_KEY)

    def start_game(game_history, save_filename):
        """The main, simplified game loop."""
        while True:
            user_input = input("YOU: ")
            
            if user_input.lower() == 'quit':
                save_game(game_history, save_filename)
                print("\nYour tale ends here... for now. Thanks for playing!")
                break
            elif user_input.lower() == 'help':
                print(config.HELP_MESSAGE)
                continue
            
            game_history.append({"role": "user", "content": user_input})
            ai_response = get_ai_response(game_history, client)
            game_history.append({"role": "assistant", "content": ai_response})
            
            # The output is now a simple, clean print statement.
            print(f"\nCHIMERA:\n{ai_response}\n")

    def run_prologue():
        """Handles the creation of a new game."""
        print("\n--- Let's Build Your Universe ---")
        
        print("First, choose a genre for your story:")
        for i, genre in enumerate(config.GENRES):
            print(f"[{i+1}] {genre}")
        
        try:
            genre_choice = int(input("> ")) - 1
            chosen_genre = config.GENRES[genre_choice]
        except (ValueError, IndexError):
            print("Invalid choice. Defaulting to Adventure."); chosen_genre = "Adventure"

        print(f"\nGenre: {chosen_genre}")
        
        default_example = "A traveler arrives in a new and interesting place."
        example_sentence = config.GENRE_EXAMPLES.get(chosen_genre, default_example)
        
        print("\nNow, describe your starting situation in a single sentence.")
        print(f"Example: '{example_sentence}'")
        user_vision = input("> ")
        if not user_vision: print("A description is required. Exiting."); return
        
        story_title = input("\nFinally, give your story a title: ")
        if not story_title: print("A title is required. Exiting."); return
        
        filename = "".join(x for x in story_title if x.isalnum() or x in " _-").rstrip() + ".json"
        
        system_prompt = config.create_system_prompt(chosen_genre, user_vision, story_title)
        current_history = [{"role": "system", "content": system_prompt}]
        
        print("\nExcellent. Your universe is being generated...")
        ai_response = get_ai_response(current_history, client)
        current_history.append({"role": "assistant", "content": ai_response})
        
        print(f"\nCHIMERA:\n{ai_response}\n")
        
        start_game(current_history, filename)

    def main_menu():
        """The initial startup menu for the game."""
        print("--- Welcome to Chimera: The Text Engine ---")
        saved_games = get_saved_games()
        
        if not saved_games:
            print("A new story awaits...")
            run_prologue()
            return

        print("Type 'help' at any time for a list of commands.")
        print("\n[1] Create a New Story")
        print("[2] Continue a Saved Story")
        
        choice = input("> ")

        if choice == '1':
            run_prologue()
        elif choice == '2':
            print("\nWhich story would you like to continue?")
            for i, game in enumerate(saved_games):
                print(f"[{i+1}] {game.replace('.json', '')}")
            try:
                load_choice = int(input("> ")) - 1
                filename = saved_games[load_choice]
                
                current_history = load_game(filename)
                
                if current_history:
                    print("\n--- Story Continued ---")
                    print(f"\nCHIMERA:\n{current_history[-1]['content']}\n")
                    start_game(current_history, filename)
                else:
                    print(f"\nError: Could not load the story file '{filename}'.")
            except (ValueError, IndexError):
                print("Invalid choice.")
        else:
            print("Invalid choice.")

    main_menu()

# Standard Python entry point
if __name__ == "__main__":
    main()