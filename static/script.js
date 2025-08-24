document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Element Selection ---
    const mainTitle = document.querySelector('header h1');
    const mainMenu = document.getElementById('main-menu-view');
    const gameView = document.getElementById('game-view');
    const headerButtons = document.getElementById('header-buttons');
    const backButton = document.getElementById('back-button');
    const helpButton = document.getElementById('help-button');
    const helpModal = document.getElementById('help-modal');
    const closeHelpButton = document.getElementById('close-help-button');
    const creationForm = document.getElementById('creation-form');
    const genreSelect = document.getElementById('genre-select');
    const userVisionInput = document.getElementById('user-vision-input');
    const storyTitleInput = document.getElementById('story-title-input');
    const startGameButton = document.getElementById('start-game-button');
    const loadGameSection = document.getElementById('load-game-section');
    const savedGamesSelect = document.getElementById('saved-games-select');
    const loadGameButton = document.getElementById('load-game-button');
    const deleteGameButton = document.getElementById('delete-game-button');
    const storyWindow = document.getElementById('story-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // --- Initial Setup ---
    mainTitle.setAttribute('data-text', mainTitle.textContent); // For glitch effect
    const genres = ["Fantasy", "Sci-Fi", "Horror", "Thriller", "Romance", "Drama", "Comedy", 
    "Mystery", "Adventure", "Slice of Life", "Western", "Historical Fiction", 
    "Young Adult (YA)", "Save the World", "Zombie Apocalypse", "Post-Apocalyptic",
    "Bedtime Story", "Memoir/Biography"];
    const placeholderOption = document.createElement('option');
    placeholderOption.value = ""; placeholderOption.textContent = "Select a genre...";
    placeholderOption.disabled = true; placeholderOption.selected = true;
    genreSelect.appendChild(placeholderOption);
    genres.forEach(genre => { const option = document.createElement('option'); option.value = genre; option.textContent = genre; genreSelect.appendChild(option); });
    fetchSavedGames();

    // --- UI Management ---
    function showGameView() { mainMenu.classList.add('hidden'); gameView.classList.remove('hidden'); headerButtons.classList.remove('hidden'); userInput.focus(); }

    // --- NEW: TYPEWRITER EFFECT FUNCTION ---
    function addMessageToStory(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        storyWindow.appendChild(messageDiv);

        if (sender === 'user') {
            messageDiv.innerHTML = text; // User messages appear instantly
            storyWindow.scrollTop = storyWindow.scrollHeight;
        } else {
            let i = 0;
            const speed = 20; // Lower is faster
            function typeWriter() {
                if (i < text.length) {
                    // Check for <br> tag
                    if (text.substring(i, i + 4) === '<br>') {
                        messageDiv.innerHTML += '<br>';
                        i += 4;
                    } else {
                        messageDiv.innerHTML += text.charAt(i);
                        i++;
                    }
                    storyWindow.scrollTop = storyWindow.scrollHeight;
                    setTimeout(typeWriter, speed);
                }
            }
            typeWriter();
        }
    }

    // --- API & Core Logic ---
    async function fetchSavedGames() { try { const response = await fetch('/api/get_saved_games'); if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`); const data = await response.json(); if (data.saved_games && data.saved_games.length > 0) { loadGameSection.classList.remove('hidden'); savedGamesSelect.innerHTML = ''; data.saved_games.forEach(gameName => { const option = document.createElement('option'); option.value = gameName; option.textContent = gameName; savedGamesSelect.appendChild(option); }); } else { loadGameSection.classList.add('hidden'); } } catch (error) { console.error("Could not fetch saved games:", error); loadGameSection.classList.add('hidden'); } }

    // --- Event Handler Functions with View Switching ---
    async function handleLoadGame() {
        const selectedStory = savedGamesSelect.value;
        if (!selectedStory) return;
        try {
            const response = await fetch('/api/load_game', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ story_title: selectedStory }) });
            if (!response.ok) throw new Error((await response.json()).error);
            const data = await response.json();
            showGameView();
            storyWindow.innerHTML = '';
            data.history.forEach(message => {
                const formattedText = message.content.replace(/\n/g, '<br>'); // MODIFIED
                if (message.role === 'user') { addMessageToStory(formattedText, 'user'); }
                else if (message.role === 'assistant') { addMessageToStory(formattedText, 'chimera'); }
            });
        } catch (error) { alert(`Error: ${error.message}`); }
    }
    
    async function handleDeleteGame() {
        const selectedStory = savedGamesSelect.value;
        if (!selectedStory) return;
        if (confirm(`Are you sure you want to permanently delete "${selectedStory}"?`)) {
            try {
                const response = await fetch('/api/delete_game', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ story_title: selectedStory }) });
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || 'Failed to delete story.');
                alert(data.message);
                fetchSavedGames();
            } catch (error) { alert(`Error: ${error.message}`); }
        }
    }

    async function handleStartNewGame(event) {
        event.preventDefault();
        try {
            const response = await fetch('/api/start_new_game', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ genre: genreSelect.value, user_vision: userVisionInput.value, story_title: storyTitleInput.value }) });
            if (!response.ok) throw new Error((await response.json()).error);
            const data = await response.json();
            showGameView();
            storyWindow.innerHTML = '';
            addMessageToStory(data.initial_response.replace(/\n/g, '<br>'), 'chimera'); // MODIFIED
        } catch (error) { alert(`Error: ${error.message}`); }
    }

    async function handleSendMessage() {
        const messageText = userInput.value.trim();
        if (!messageText) return;
        addMessageToStory(messageText, 'user'); // MODIFIED
        userInput.value = '';
        sendButton.disabled = true;
        try {
            const response = await fetch('/api/send_message', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: messageText }) });
            if (!response.ok) throw new Error((await response.json()).error);
            const data = await response.json();
            addMessageToStory(data.response.replace(/\n/g, '<br>'), 'chimera'); // MODIFIED
        } catch (error) {
            addMessageToStory(`*Error: ${error.message}*`, 'chimera'); // MODIFIED
        } finally {
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    // --- Event Listeners ---
    loadGameButton.addEventListener('click', handleLoadGame);
    deleteGameButton.addEventListener('click', handleDeleteGame);
    creationForm.addEventListener('submit', handleStartNewGame);
    sendButton.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keydown', (event) => { if (event.key === 'Enter') { event.preventDefault(); handleSendMessage(); } });
    backButton.addEventListener('click', () => { if(confirm("Are you sure you want to exit to the main menu? Your progress is saved.")) { window.location.reload(); } });
    helpButton.addEventListener('click', () => { helpModal.classList.remove('hidden'); });
    closeHelpButton.addEventListener('click', () => { helpModal.classList.add('hidden'); });
    helpModal.addEventListener('click', (event) => { if (event.target === helpModal) { helpModal.classList.add('hidden'); } });

    // --- Smart Button Logic ---
    function checkFormValidity() { const allFieldsFilled = genreSelect.value && userVisionInput.value.trim() !== '' && storyTitleInput.value.trim() !== ''; startGameButton.classList.toggle('hidden', !allFieldsFilled); }
    genreSelect.addEventListener('change', checkFormValidity);
    userVisionInput.addEventListener('input', checkFormValidity);
    storyTitleInput.addEventListener('input', checkFormValidity);
    checkFormValidity();
});