// static/script.js
// The Definitive, Polished JavaScript for Project Chimera

// --- DATA INJECTION FROM FLASK ---
// These global constants are injected by the Flask template engine in index.html
// and are available to this script.
// const genres, genreExamples, genreTitles; 

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM ELEMENT SELECTION ---
    const mainTitle = document.querySelector('header h1');
    const mainMenu = document.getElementById('main-menu-view');
    const gameView = document.getElementById('game-view');
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
    const inputArea = document.getElementById('input-area');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const headerButtons = document.getElementById('header-buttons');
    const backButton = document.getElementById('back-button');
    const helpButton = document.getElementById('help-button');
    const helpModal = document.getElementById('help-modal');
    const closeHelpButton = document.getElementById('close-help-button');

    // --- INITIAL SETUP ---
    mainTitle.setAttribute('data-text', mainTitle.textContent);
    genres.forEach(genre => {
        const option = document.createElement('option');
        option.value = genre; option.textContent = genre;
        genreSelect.appendChild(option);
    });
    fetchSavedGames();
    updatePlaceholders();

    // --- UI & API FUNCTIONS ---
    function showGameView() {
        mainMenu.classList.add('hidden');
        gameView.classList.remove('hidden');
        headerButtons.classList.remove('hidden');
        inputArea.style.display = 'flex'; // This must be set to flex
        userInput.focus();
    }
    
    function addMessage(text, sender, isTyping = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        storyWindow.appendChild(messageDiv);

        if (!isTyping || sender === 'user') {
            messageDiv.innerHTML = text.replace(/\n/g, '<br>'); // Instantly add for user or loaded history
            storyWindow.scrollTop = storyWindow.scrollHeight;
        } else { // Apply typewriter effect for new AI messages
            let i = 0;
            const speed = 25; // Milliseconds per character
            function typeWriter() {
                if (i < text.length) {
                    messageDiv.innerHTML += text.charAt(i);
                    i++;
                    storyWindow.scrollTop = storyWindow.scrollHeight;
                    setTimeout(typeWriter, speed);
                }
            }
            typeWriter();
        }
    }

    async function fetchSavedGames() {
        try {
            const response = await fetch('/api/get_saved_games');
            if (!response.ok) throw new Error(`HTTP error!`);
            const data = await response.json();
            if (data.saved_games && data.saved_games.length > 0) {
                loadGameSection.classList.remove('hidden');
                savedGamesSelect.innerHTML = '';
                data.saved_games.forEach(game => {
                    const option = document.createElement('option');
                    option.value = game.title;
                    option.textContent = `${game.title} (${game.genre})`;
                    savedGamesSelect.appendChild(option);
                });
            } else {
                loadGameSection.classList.add('hidden');
            }
        } catch (error) {
            console.error("Could not fetch saved games:", error);
            loadGameSection.classList.add('hidden');
        }
    }

    function updatePlaceholders() {
        const selectedGenre = genreSelect.value;
        const examples = genreExamples[selectedGenre] || [];
        const titles = genreTitles[selectedGenre] || [];
        userVisionInput.placeholder = (examples.length > 0) ? `e.g., ${examples[Math.floor(Math.random() * examples.length)]}` : "e.g., A traveler arrives...";
        storyTitleInput.placeholder = (titles.length > 0) ? `e.g., ${titles[Math.floor(Math.random() * titles.length)]}` : "e.g., The Journey Begins";
        // Reveal the Begin button only after a genre is chosen
        if (selectedGenre) { startGameButton.classList.remove('hidden'); } 
        else { startGameButton.classList.add('hidden'); }
    }
    
    // --- EVENT HANDLERS ---
    async function handleLoadGame() {
        const selectedStory = savedGamesSelect.value;
        if (!selectedStory) return;
        mainMenu.innerHTML = '<h2>Loading your universe...</h2>';
        try {
            const response = await fetch('/api/load_game', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ story_title: selectedStory }) });
            if (!response.ok) throw new Error((await response.json()).error);
            const data = await response.json();
            showGameView();
            storyWindow.innerHTML = '';
            // Load history instantly, without typewriter effect
            data.history.forEach(message => {
                if (message.role === 'user') { addMessage(message.content, 'user', false); }
                else if (message.role === 'assistant') { addMessage(message.content, 'chimera', false); }
            });
        } catch (error) { alert(`Error: ${error.message}`); }
    }

    async function handleDeleteGame() {
        const selectedStory = savedGamesSelect.value;
        if (!selectedStory) return;
        if (confirm(`Are you sure you want to permanently delete "${selectedStory}"?`)) {
            try {
                const response = await fetch('/api/delete_game', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ story_title: selectedStory }) });
                if (!response.ok) throw new Error((await response.json()).error);
                const data = await response.json();
                alert(data.message);
                fetchSavedGames();
            } catch (error) { alert(`Error: ${error.message}`); }
        }
    }
    
    async function handleStartNewGame(event) {
        event.preventDefault();
        if (!genreSelect.value) { alert("Please choose a genre."); return; }
        if (!userVisionInput.value.trim() || !storyTitleInput.value.trim()) { alert('Please fill out all fields.'); return; }
        mainMenu.innerHTML = '<h2>Generating your universe...</h2>';
        try {
            const response = await fetch('/api/start_new_game', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ genre: genreSelect.value, user_vision: userVisionInput.value, story_title: storyTitleInput.value }) });
            if (!response.ok) throw new Error((await response.json()).error);
            const data = await response.json();
            showGameView();
            storyWindow.innerHTML = '';
            addMessage(data.initial_response, 'chimera', true);
        } catch (error) { alert(`Error: ${error.message}`); mainMenu.innerHTML = `<h2>Error starting game. Please try again.</h2>`;}
    }

    async function handleSendMessage() {
        const messageText = userInput.value.trim();
        if (!messageText) return;
        addMessage(messageText, 'user', false);
        userInput.value = '';
        sendButton.disabled = true;
        try {
            const response = await fetch('/api/send_message', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: messageText }) });
            if (!response.ok) throw new Error((await response.json()).error);
            const data = await response.json();
            addMessage(data.response, 'chimera', true);
        } catch (error) {
            addMessage(`*Error: ${error.message}*`, 'chimera', false);
        } finally {
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    // --- EVENT LISTENERS ---
    genreSelect.addEventListener('change', updatePlaceholders);
    loadGameButton.addEventListener('click', handleLoadGame);
    deleteGameButton.addEventListener('click', handleDeleteGame);
    creationForm.addEventListener('submit', handleStartNewGame);
    sendButton.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keydown', (event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); handleSendMessage(); } });
    helpButton.addEventListener('click', () => { helpModal.classList.remove('hidden'); });
    closeHelpButton.addEventListener('click', () => { helpModal.classList.add('hidden'); });
    helpModal.addEventListener('click', (event) => { if (event.target === helpModal) { helpModal.classList.add('hidden'); } });
    backButton.addEventListener('click', () => { if (confirm("Are you sure? Your progress is saved.")) { window.location.reload(); } });
});