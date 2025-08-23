// static/script.js
const mainMenu = document.getElementById('main-menu');
const loadGameSection = document.getElementById('load-game-section');
const storyWindow = document.getElementById('story-window');
const inputArea = document.getElementById('input-area');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const startGameButton = document.getElementById('start-game-button');
const loadGameButton = document.getElementById('load-game-button');
const deleteGameButton = document.getElementById('delete-game-button');
const genreSelect = document.getElementById('genre-select');
const savedGamesSelect = document.getElementById('saved-games-select');
const headerButtons = document.getElementById('header-buttons');
const backButton = document.getElementById('back-button');
const helpButton = document.getElementById('help-button');
const helpModal = document.getElementById('help-modal');
const closeHelpButton = document.getElementById('close-help-button');

const genres = ["Fantasy", "Sci-Fi", "Horror", "Thriller", "Romance", "Drama", "Comedy", "Mystery", "Adventure", "Slice of Life", "Western", "Historical Fiction", "Post-Apocalyptic"];
genres.forEach(genre => {
    const option = document.createElement('option');
    option.value = genre;
    option.textContent = genre;
    genreSelect.appendChild(option);
});

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = text.replace(/\n/g, '<br>');
    storyWindow.appendChild(messageDiv);
    storyWindow.scrollTop = storyWindow.scrollHeight;
}

function showThinkingIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'thinking';
    indicator.className = 'message chimera-message thinking-indicator';
    indicator.innerHTML = '<span>.</span><span>.</span><span>.</span>';
    const style = document.createElement('style');
    style.id = 'blinker-style';
    style.innerHTML = `.thinking-indicator span { animation: blink 1.4s infinite both; font-size: 1.5rem; } .thinking-indicator span:nth-child(2) { animation-delay: .2s; } .thinking-indicator span:nth-child(3) { animation-delay: .4s; } @keyframes blink { 0% { opacity: .2; } 20% { opacity: 1; } 100% { opacity: .2; } }`;
    document.head.appendChild(style);
    storyWindow.appendChild(indicator);
    storyWindow.scrollTop = storyWindow.scrollHeight;
}

function hideThinkingIndicator() {
    const indicator = document.getElementById('thinking');
    const blinkerStyle = document.getElementById('blinker-style');
    if (indicator) indicator.remove();
    if (blinkerStyle) blinkerStyle.remove();
}

function showGameView() {
    mainMenu.style.display = 'none';
    inputArea.style.display = 'flex';
    headerButtons.style.display = 'flex';
    userInput.focus();
}

async function fetchSavedGames() {
    try {
        const response = await fetch('/api/get_saved_games');
        const data = await response.json();
        if (data.saved_games && data.saved_games.length > 0) {
            loadGameSection.style.display = 'block';
            savedGamesSelect.innerHTML = '';
            data.saved_games.forEach(gameName => {
                const option = document.createElement('option');
                option.value = gameName;
                option.textContent = gameName;
                savedGamesSelect.appendChild(option);
            });
        } else {
            loadGameSection.style.display = 'none';
        }
    } catch (error) {
        console.error("Could not fetch saved games:", error);
    }
}

window.addEventListener('DOMContentLoaded', fetchSavedGames);

startGameButton.addEventListener('click', async () => {
    const selectedGenre = genreSelect.value;
    const userVision = document.getElementById('user-vision-input').value;
    const storyTitle = document.getElementById('story-title-input').value;
    if (!userVision.trim() || !storyTitle.trim()) {
        alert('Please fill out all fields.');
        return;
    }
    mainMenu.innerHTML = '<h2>Generating your universe...</h2>';
    try {
        const response = await fetch('/api/start_new_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                genre: selectedGenre,
                user_vision: userVision,
                story_title: storyTitle
            })
        });
        const data = await response.json();
        if (response.ok) {
            showGameView();
            addMessage(data.initial_response, 'chimera');
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (error) {
        mainMenu.innerHTML = `<h2>Error: ${error.message}</h2>`;
    }
});

loadGameButton.addEventListener('click', async () => {
    const storyTitle = savedGamesSelect.value;
    if (!storyTitle) {
        alert("Please select a story.");
        return;
    }
    mainMenu.innerHTML = '<h2>Loading your universe...</h2>';
    try {
        const response = await fetch('/api/load_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ story_title: storyTitle })
        });
        const data = await response.json();
        if (response.ok) {
            showGameView();
            storyWindow.innerHTML = '';
            if (data.history && Array.isArray(data.history)) {
                data.history.forEach(message => {
                    if (message.role === 'user') {
                        addMessage(message.content, 'user');
                    } else if (message.role === 'assistant') {
                        addMessage(message.content, 'chimera');
                    }
                });
            }
        } else {
            throw new Error(data.error || 'Failed to load');
        }
    } catch (error) {
        mainMenu.innerHTML = `<h2>Error: ${error.message}</h2>`;
    }
});

deleteGameButton.addEventListener('click', async () => {
    const storyTitle = savedGamesSelect.value;
    if (!storyTitle) {
        alert("Please select a story to delete.");
        return;
    }
    if (!confirm(`Are you sure you want to permanently delete "${storyTitle}"?\nThis cannot be undone.`)) {
        return;
    }
    try {
        const response = await fetch('/api/delete_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ story_title: storyTitle })
        });
        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            fetchSavedGames(); // Refresh the list
        } else {
            throw new Error(data.error || 'Could not delete the file.');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    addMessage(message, 'user');
    userInput.value = '';
    sendButton.disabled = true;
    userInput.disabled = true;
    showThinkingIndicator();
    try {
        const response = await fetch('/api/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        hideThinkingIndicator();
        if (response.ok) {
            addMessage(data.response, 'chimera');
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (error) {
        hideThinkingIndicator();
        addMessage(`Error: ${error.message}. Please try again.`, 'chimera');
    } finally {
        sendButton.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

helpButton.addEventListener('click', () => {
    helpModal.style.display = 'flex';
});
closeHelpButton.addEventListener('click', () => {
    helpModal.style.display = 'none';
});
helpModal.addEventListener('click', (event) => {
    if (event.target === helpModal) {
        helpModal.style.display = 'none';
    }
});

backButton.addEventListener('click', async () => {
    if (!confirm("Are you sure you want to exit to the main menu? Your progress is saved automatically.")) {
        return;
    }
    window.location.reload();
});