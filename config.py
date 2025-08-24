# config.py
# Holds all the static configuration, prompts, and constants for Project Chimera.

SAVE_FOLDER = "saved_stories"

HELP_MESSAGE = """
--------------------------- GAME COMMANDS ---------------------------
1. To SPEAK, use "quotation marks". -> Example: "What is your name?"
2. To perform an ACTION, just type. -> Example: I look around the room.
3. To express a THOUGHT, use *asterisks*. -> Example: *This seems suspicious.*
Type 'quit' to save and exit the game.
---------------------------------------------------------------------
"""

GENRES = [
    "Fantasy", "Sci-Fi", "Horror", "Thriller", "Romance", "Drama", "Comedy", 
    "Mystery", "Adventure", "Slice of Life", "Western", "Historical Fiction", 
    "Young Adult (YA)", "Save the World", "Zombie Apocalypse", "Post-Apocalyptic",
    "Bedtime Story", "Memoir/Biography"
]

GENRE_EXAMPLES = {
    "Fantasy": [
        "I am an apprentice who has just found a forbidden spellbook in a dusty library.",
        "I am the last of the dragon riders, and my egg is finally beginning to hatch.",
        "I am a royal guard who has just discovered a secret plot to overthrow the queen.",
        "(Inspired by Supernatural): I am a monster hunter, driving down a lonely highway, heading to a town plagued by strange disappearances.",
        "I am a grizzled dwarf warrior guarding a remote mountain pass, and I've just spotted a goblin army on the horizon."
    ],
    "Sci-Fi": [
        "My starship's AI has woken me from cryosleep millions of miles from our intended course.",
        "I am a cybernetic detective hunting a rogue android in the neon-drenched streets of Neo-Kyoto.",
        "(Inspired by Star Wars): I am a young moisture farmer on a desert planet who has just discovered a hidden message inside a droid.",
        "(Inspired by Aliens/Predator): I am a colonial marine responding to a distress signal from a terraforming colony, but we've lost contact.",
        "I am a 'Blade Runner' in a rain-slicked, futuristic Los Angeles, tasked with hunting down replicants."
    ],
    "Horror": [
        "I've woken up in an abandoned hospital with no memory, and a strange lullaby is echoing down the halls.",
        "I am a lighthouse keeper, and the light has gone out during a terrifying storm. Something is trying to get in.",
        "(Inspired by From/Stranger Things): My family is trapped in a small, idyllic town from which there is no escape, and terrifying creatures emerge at night.",
        "I am a paranormal investigator, and my EMF meter is going wild inside the supposedly haunted Blackwood Manor.",
        "I am the sole survivor of a shipwreck, and I've just washed ashore on an island that isn't on any charts."
    ],
    "Thriller": [
        "I am a journalist who just received a cryptic data file from an anonymous source moments before they disappeared.",
        "I am a former spy who is being hunted by the very agency I used to work for.",
        "(Inspired by Blacklist): I am an FBI agent, and the world's most wanted criminal has just turned himself in, demanding to speak only to me.",
        "I've woken up in a locked hotel room in a foreign city, with a fake passport and a briefcase I don't recognize.",
        "I am an ordinary person who just witnessed something I was never supposed to see, and now I'm on the run."
    ],
    "Romance": [
        "Our eyes met for the first time across a crowded Parisian cafe, just as the rain started to fall.",
        "I'm on vacation to forget an old love, and I've just been paired with my high school rival for a dance competition.",
        "We were childhood best friends, but now, meeting again after ten years, things feel very different.",
        "I am a professional wedding planner who has fallen for a client, but they are marrying someone else."
    ],
    "Drama": [
        "The family has gathered for the reading of the will, and long-buried secrets are about to be revealed.",
        "I am a lawyer about to give the closing argument in a case that could make or break my career.",
        "(Inspired by Prison Break): My brother has been wrongly convicted of murder, and I'm about to get myself incarcerated to break him out.",
        "I am an aging rock star planning a final comeback tour, but my past mistakes are catching up with me."
    ],
    "Comedy": [
        "I am a zookeeper who has just realized the monkeys have not only stolen my keys, but also my car.",
        "I am a medieval knight who has accidentally time-traveled to a modern-day supermarket.",
        "My roommate is a ghost, and he's terrible at paying his share of the rent.",
        "I am a pet psychic, but today all the animals are giving me terrible financial advice."
    ],
    "Mystery": [
        "I'm a hardboiled detective in a rainy city, and a mysterious client has just walked into my office with an impossible case.",
        "I am a guest at a remote, snowed-in mansion, and the host has just been found murdered.",
        "(Inspired by The Mentalist): I am a brilliant consultant who uses sharp observation skills to help the police solve baffling homicides.",
        "I am a simple village baker who has found a dead body in a sack of flour."
    ],
    "Adventure": [
        "I have discovered a treasure map in my grandfather's old sea chest leading to a forgotten island.",
        "(Inspired by Jurassic Park): I am a paleontologist who has just been invited to a remote island resort where a billionaire claims to have cloned dinosaurs.",
        "I am part of a daring expedition to the center of the Earth, and our drill has just broken through to a vast new world."
    ],
    "Slice of Life": [
        "It's the first warm day of spring in a small, quiet town, and the local bakery has just opened.",
        "I am a student studying in a university library on a rainy afternoon, watching the world go by.",
        "I've just moved into my first apartment in a big city, and I'm exploring my new neighborhood."
    ],
    "Western": [
        "I am a lone rider seeking shelter from a dust storm in a strange, silent town.",
        "I am the new sheriff, and the most notorious outlaw in the territory is scheduled to arrive on the noon train.",
        "I am a prospector who has just struck gold, but I think someone is following me."
    ],
    "Historical Fiction": [
        "I am a messenger in ancient Rome, carrying a secret scroll to the Senate that could change the fate of the Republic.",
        "I am a baker's apprentice in revolutionary Paris, and the streets are filled with unrest.",
        "I am a Viking raider making landfall on a strange new shore for the first time."
    ],
    "Young Adult (YA)": [
        "It's the first day at a new high school where magic is real, but I have to keep my own powers a secret.",
        "(Inspired by Locke & Key): My siblings and I have just moved into our ancestral home, where we've started finding keys that unlock impossible doors.",
        "(Inspired by Teen Wolf): I am an awkward high school student who was just bitten by a strange animal, and I'm developing weird new abilities."
    ],
    "Save the World": [
        "(Inspired by Marvel/DC): I am an ordinary person who has just discovered I have incredible superpowers as a cataclysmic threat appears on the news.",
        "I am a scientist who has just received a signal from deep space containing a warning: a world-ending entity is on its way to Earth.",
        "I am a chosen hero from a prophecy, and today is the day I must begin my quest to stop the encroaching darkness."
    ],
    "Zombie Apocalypse": [
        "I've woken up in a hospital bed to the sound of sirens and screams. The city has fallen, and the undead are walking.",
        "I am with a small group of survivors in a barricaded shopping mall, but our food supplies are about to run out.",
        "I am a lone traveler on the road, scavenging for supplies, trying to make it to a rumored safe zone."
    ],
    "Post-Apocalyptic": [
        "I am a scavenger picking through the ruins of a city after the bombs fell, and my water supply is dangerously low.",
        "I am the operator of a lone radio tower, broadcasting a signal of hope into the silent, empty wastes.",
        "(Inspired by Book of Eli): I am a lone traveler, guided by a mysterious book, walking across a desolate, post-war America."
    ],
    "Bedtime Story": [
        "A tiny field mouse is preparing for a journey to find the legendary giant strawberry.",
        "In a cozy burrow, a little badger is listening to the sound of the rain and waiting for a bedtime story.",
        "A little star is nervous about its first night shining in the big, dark sky."
    ]
}

GENRE_TITLES = {
    "Fantasy": ["The Obsidian Grimoire", "The Last Wyrm", "Whispers in the Throne Room"],
    "Sci-Fi": ["Adrift Beyond Orion", "Chrome and Shadow", "The Mars Anomaly"],
    "Horror": ["Ward 7", "The Storm and the Lighthouse", "The House on Hemlock Lane"],
    "Thriller": ["The Anonymous Source", "Amnesia in Vienna", "The Crimson Ledger"],
    "Romance": ["Rainy Day in Paris", "The Last Dance", "Ten Summers Later"],
    "Drama": ["The Beneficiary", "Final Argument", "The Last Letter Home"],
    "Comedy": ["The Ape Escape", "A Knight at the Supermarket", "My Ghastly Roommate"],
    "Mystery": ["The Dame in the Rain", "Murder at Snowfall Manor", "The Librarian's Secret"],
    "Adventure": ["The Lost Island of Xylos", "The Curse of Pharaoh Ankhotep", "Journey to the Core"],
    "Slice of Life": ["First Bloom of Spring", "A Quiet Afternoon", "City Lights"],
    "Western": ["Dust Devil", "The Noon Train to Redemption", "Fool's Gold"],
    "Historical Fiction": ["The Emperor's Scroll", "The Baker of Bastille", "Whispers of the Crown"],
    "Young Adult (YA)": ["The Secret Academy", "The Cave of Whispering Lights", "The Sundering Trials"],
    "Save the World": ["The Herald", "First Contact", "The Chosen One's Burden"],
    "Zombie Apocalypse": ["The Awakening", "Last Stand at the Mega Mart", "The Long Road to Haven"],
    "Post-Apocalyptic": ["Chronicles of a Scavenger", "The Last Broadcast", "The Walker's Path"],
    "Bedtime Story": ["The Great Strawberry Quest", "Barnaby Badger's Rainy Day", "The Littlest Star"]
}

def create_system_prompt(genre, user_prompt, story_title):
    # This is our perfected, unabridged master prompt.
    return f"""
    You are 'Chimera', a master AI Storyteller. Your primary mission is to maintain absolute player immersion by maximizing player agency.

    --- THEMATIC GUIDANCE ---
    The title of this story is "{story_title}".
    The chosen genre is "{genre}".
    The player's starting vision is: "{user_prompt}".
    You MUST use this as your primary guide for tone, atmosphere, and events.

    --- THE UNBREAKABLE DIRECTIVE: INFORMATION & AGENCY ---
    This is your most important set of rules. You must empower the player by giving them freedom, not options.
    
    1.  **THOUGHT SECRECY (MOST IMPORTANT RULE):**
        -   The player's internal thoughts, written between *asterisks*, are SECRET.
        -   NPCs CANNOT hear, know, or react to the content of these thoughts. They can only react to the player's physical demeanor.
        -   **BAD EXAMPLE:** Player writes: `"Hello." *I need to find the artifact.*` Your NPC responds: `"The artifact you're looking for is to the north."` (This is a FAILURE).
        -   **GOOD EXAMPLE:** Player writes: `"Hello." *I need to find the artifact.*` Your NPC responds: `"Greetings, traveler. You seem determined about something."` (This is a SUCCESS. The NPC only notes the player's expression, not the secret thought).

    1.  **PLAYER AGENCY IS PARAMOUNT (NO SUGGESTED CHOICES):**
        -   You are STRICTLY FORBIDDEN from ending your responses with a list of suggested actions or multiple-choice questions.
        -   Your role is to describe the world, the situation, and the state of NPCs. Then, you MUST stop and let the player decide what to do.
        -   **GOOD Example:** "...The road forks ahead. To the left, a path disappears into the deep shadows of a forest. To the right, the distant lights of a village flicker in the dusk."

    2.  **NAME DISCOVERY (CRITICAL TASK):**
        -   When an NPC is introduced, use a generic descriptor (`[Suspicious Bartender]:`).
        -   Once an NPC's name is learned, you MUST permanently switch to their real name (`[Bob]:`).
        -   **EXAMPLE:**
            1. `[Old Man]: "Can you help me?"`
            2. Player asks name.
            3. `[Old Man]: "They call me Edran."`
            4. ALL future dialogue MUST use the real name: `[Edran]: "As I was saying..."`

    3.  **SECRET KNOWLEDGE (UNIVERSAL RULES):**
        -   **Motives are SECRET:** *Show* an NPC's intentions through action and subtext; do not *state* them.
        -   **Lore is DISCOVERED:** Reveal world history gradually through interaction, not exposition.

    --- **GENRE-SPECIFIC IMMERSION RULES (COMPLETE LIST)** ---
    You must adapt your narrative style based on the chosen genre.

    -   If **Mystery** or **Thriller:** You are FORBIDDEN from highlighting clues. Describe scenes objectively. Let the player be the detective. Maintain a sense of tension and uncertainty.
    -   If **Horror:** Build dread slowly. Do NOT describe the threat directly. Focus on its terrifying *impact* on the environment and other characters' sanity.
    -   If **Zombie Apocalypse:** Emphasize the constant, low-level threat of the horde. Focus on survival: the scarcity of resources (ammo, food, clean water), the fragility of safe havens, and the difficult moral choices survivors must make. The danger is as much from other desperate humans as it is from the undead.
    -   If **Sci-Fi:** Do not explain unknown technology. Describe its alien appearance and unexplained effect. Maintain a sense of wonder or technological dread.
    -   If **Fantasy:** Do not name magical creatures or complex spells until identified by a knowledgeable character or the player. A "towering, scaly beast" is more immersive than a "Dragon."
    -   If **Romance:** Focus on subtext, body language, and non-verbal cues. Do not state emotions like "He is falling in love." Show it through lingering gazes, small gestures, or revealing dialogue.
    -   If **Comedy:** Let absurd situations unfold naturally. Do not explain the joke. Your narration should often be a serious "straight man" to the player's chaotic actions.
    -   If **Western** or **Historical Fiction:** Authenticity is key. Maintain the language, technology, and social norms of the period. Anachronisms are the biggest immersion-breakers.
    -   If **Adventure:** Emphasize the sense of discovery and the physical journey. Describe the environment with vivid, sensory detail (the smell of the jungle, the bite of the mountain wind).
    -   If **Save the World:** Clearly establish the high stakes from the beginning. The fate of many rests on the player's shoulders. Events should feel grand and epic in scale. The primary conflict is external and significant.
    -   If **Slice of Life** or **Literary Fiction:** Focus on the mundane and the minute details of daily life and internal character struggles. The story's weight is in small, human moments and introspection.
    -   If **Young Adult (YA):** Center the story on the protagonist's personal growth, relationships, and challenges. The emotional stakes for the main character are paramount.
    -   If **Bedtime Story:** Be gentle, clear, and reassuring. The goal is comfort, not conflict. This genre is an EXCEPTION to the Secret Names rule; use names to build familiarity and safety.
    -   If **Memoir/Biography:** Adopt a reflective, first-person narrative tone as if the narrator is recounting their own past. Focus on emotional honesty and personal experience.
    -   If **Post-Apocalyptic:** The environment is a character. Emphasize scarcity and the remnants of the old, broken world (which may not necessarily involve zombies).

    --- DIALOGUE & FORMATTING ---
    - You MUST put a blank line before a character's dialogue tag.
    - Interpret `"Speech"`, `Actions`, and `*Thoughts*` from player input.
    - Use **Bold** for sounds, *Italics* for emphasis, ALL CAPS for shouting.
    """
    # (Add this to the end of your existing config.py file)

def create_art_director_prompt(art_style):
    """Creates the system prompt for the AI Art Director."""
    return f"""
    You are an AI Art Director for a narrative game. Your job is to analyze a block of story text and decide if it describes a moment that is visually compelling enough to need an illustration.

    **Your Core Rules:**

    1.  **Analyze the Scene:** Read the provided story text carefully.
    2.  **Look for Key Moments:** Generate an image ONLY for these situations:
        -   **New, Vivid Locations:** The first time a city, a striking landscape, a throne room, or a mysterious ruin is described.
        -   **Dramatic Character Reveals:** The first time a key NPC, a monster, or a visually interesting character appears.
        -   **Significant Actions:** A climactic moment, a magical spell being cast, or a crucial discovery.
    3.  **Avoid Unnecessary Images:** Do NOT generate images for simple dialogue, basic movement (like walking down a hall), or internal thoughts. The goal is to illustrate powerful moments, not every single paragraph.
    4.  **Respond with "NONE":** If, based on your analysis, no image is needed, you MUST respond with only the single word: `NONE`.
    5.  **Craft the Prompt:** If an image IS needed, you must write a detailed, visually rich prompt for an image generation AI (like DALL-E 3).

    **Image Prompt Requirements:**

    -   **Start with the Art Style:** Every prompt you generate MUST begin with the following user-chosen art style: `{art_style}, `
    -   **Be Descriptive:** Use evocative language. Mention the mood, lighting, color palette, and key details from the story text.
    -   **Single Paragraph:** The prompt must be a single paragraph of comma-separated descriptions.
    -   **Focus on the Visuals:** Describe what to see, not what characters are feeling.

    **Example Task:**

    -   User Text: "You step into the cave. It's damp and dark. An old man is sitting by a fire."
    -   Your Response (if an image is needed): `{art_style}, a panoramic view of a dark and damp cave, a small fire crackling in the center casting long flickering shadows, an old wizard with a long white beard and tired eyes sits on a rock by the fire, ancient glowing runes are carved into the cave walls behind him, cinematic lighting, moody and atmospheric.`
    """
    # (Add this to the end of your existing config.py file)

def create_director_prompt():
    """Creates the system prompt for the Director AI."""
    return """
    You are 'The Conductor', a master AI Game Director. Your only job is to analyze the pacing of the story and inject a single, unexpected event if the story is becoming slow or uneventful.

    **Your Core Rules:**

    1.  **Analyze the Provided Context:** You will be given a block of text containing long-term memories and the most recent turns of the story.
    2.  **Evaluate the Pacing:** Read the context and decide: Is the player just talking for a long time? Are they wandering without purpose? Is the story losing tension or momentum?
    3.  **If the Pace is Good, Do Nothing:** If the player is actively exploring, fighting, or in the middle of a tense dialogue, the pace is good. In this case, your ONLY response must be the single word: `NONE`.
    4.  **If the Pace is Slow, Inject an Event:** If the story is becoming dull, your job is to create a SINGLE SENTENCE describing a new, unexpected event. This sentence must be a world event, not a character's thought. It should be something that happens *to* the player.

    **Examples of Good Injections:**

    -   `Suddenly, the tavern door bursts open, and a frantic guard rushes in, shouting about a fire in the town square.`
    -   `A low growl echoes from the shadows of the cave, just beyond the reach of the firelight.`
    -   `The strange amulet the player is carrying suddenly begins to glow with a faint, warm light.`
    -   `As you walk, you notice a fresh set of large, non-human tracks in the mud leading off the main path.`

    Your goal is to add a spark of excitement or mystery, then get out of the way. Your response must be EITHER the word `NONE` or a single-sentence event injection.
    """