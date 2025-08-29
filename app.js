// HabbitZ Kids Vocabulary App - Main JavaScript
class VocabularyApp {
    constructor() {
        this.vocabulary = [];
        this.currentGame = null;
        this.gameState = {
            currentQuestion: 0,
            score: 0,
            streak: 0,
            maxStreak: 0,
            totalScore: 0,
            level: 1,
            wordsLearned: new Set(),
            gamesPlayed: 0
        };
        
        this.badges = [
            { id: 'first_game', name: 'First Steps', icon: '👶', description: 'Played your first game!' },
            { id: 'streak_5', name: 'On Fire!', icon: '🔥', description: 'Got 5 in a row correct!' },
            { id: 'words_10', name: 'Word Collector', icon: '📚', description: 'Learned 10 words!' },
            { id: 'words_25', name: 'Vocabulary Star', icon: '⭐', description: 'Learned 25 words!' },
            { id: 'words_50', name: 'Word Master', icon: '🏆', description: 'Learned 50 words!' },
            { id: 'perfect_game', name: 'Perfect!', icon: '💯', description: 'Got 100% in a game!' },
            { id: 'games_10', name: 'Dedicated Learner', icon: '🎯', description: 'Played 10 games!' },
            { id: 'level_up', name: 'Level Up!', icon: '🚀', description: 'Reached level 5!' }
        ];
        
        this.earnedBadges = new Set();
        this.currentWords = [];
        
        this.init();
    }

    async init() {
        try {
            // Load vocabulary data
            this.vocabulary = VOCABULARY_DATA.vocabulary || [];
            console.log(`Loaded ${this.vocabulary.length} words`);
            
            // Load saved progress
            this.loadProgress();
            
            // Initialize UI
            this.setupEventListeners();
            this.updateUI();
            this.setDailyWord();
            
            // Hide loading screen and show app
            setTimeout(() => {
                document.getElementById('loading-screen').style.display = 'none';
                document.getElementById('app').style.display = 'block';
            }, 2000);
            
        } catch (error) {
            console.error('Failed to initialize app:', error);
            this.showError('Failed to load vocabulary data. Please refresh the page.');
        }
    }

    setupEventListeners() {
        // Game button listeners
        document.querySelectorAll('.game-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const game = e.currentTarget.dataset.game;
                this.startGame(game);
            });
        });

        // Definition Match Game
        document.getElementById('dm-next-btn').addEventListener('click', () => {
            this.nextDefinitionMatchQuestion();
        });

        // Memory Helper Game
        document.getElementById('mh-check-btn').addEventListener('click', () => {
            this.checkMemoryHelperAnswer();
        });

        document.getElementById('mh-word-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.checkMemoryHelperAnswer();
            }
        });

        document.getElementById('mh-next-btn').addEventListener('click', () => {
            this.nextMemoryHelperQuestion();
        });

        // Word Builder Game
        document.getElementById('wb-clear-btn').addEventListener('click', () => {
            this.clearWordBuilder();
        });

        document.getElementById('wb-next-btn').addEventListener('click', () => {
            this.nextWordBuilderQuestion();
        });

        // Story Mode Game
        document.getElementById('sm-next-btn').addEventListener('click', () => {
            this.nextStoryQuestion();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.showMainMenu();
            }
        });
    }

    loadProgress() {
        const saved = localStorage.getItem('habbitZ_progress');
        if (saved) {
            try {
                const progress = JSON.parse(saved);
                this.gameState = { ...this.gameState, ...progress };
                this.gameState.wordsLearned = new Set(progress.wordsLearned || []);
                this.earnedBadges = new Set(progress.earnedBadges || []);
            } catch (error) {
                console.error('Failed to load progress:', error);
            }
        }
    }

    saveProgress() {
        try {
            const progress = {
                ...this.gameState,
                wordsLearned: Array.from(this.gameState.wordsLearned),
                earnedBadges: Array.from(this.earnedBadges)
            };
            localStorage.setItem('habbitZ_progress', JSON.stringify(progress));
        } catch (error) {
            console.error('Failed to save progress:', error);
        }
    }

    updateUI() {
        // Update header stats
        document.getElementById('total-score').textContent = this.gameState.totalScore;
        document.getElementById('streak').textContent = this.gameState.streak;
        document.getElementById('level').textContent = this.gameState.level;

        // Update progress screen
        document.getElementById('total-words-learned').textContent = this.gameState.wordsLearned.size;
        document.getElementById('best-streak').textContent = this.gameState.maxStreak;
        document.getElementById('total-points').textContent = this.gameState.totalScore;
        document.getElementById('games-played').textContent = this.gameState.gamesPlayed;

        // Update progress bar
        const progressPercentage = Math.min(100, (this.gameState.wordsLearned.size / 50) * 100);
        document.getElementById('overall-progress').style.width = `${progressPercentage}%`;
        document.getElementById('progress-percentage').textContent = `${Math.round(progressPercentage)}%`;

        // Update badges
        this.updateBadges();
    }

    updateBadges() {
        const badgesGrid = document.getElementById('badges-grid');
        badgesGrid.innerHTML = '';

        this.badges.forEach(badge => {
            const badgeElement = document.createElement('div');
            badgeElement.className = `badge ${this.earnedBadges.has(badge.id) ? 'earned' : 'locked'}`;
            badgeElement.innerHTML = `
                <div class="badge-icon">${this.earnedBadges.has(badge.id) ? badge.icon : '🔒'}</div>
                <div class="badge-name">${badge.name}</div>
            `;
            badgeElement.title = badge.description;
            badgesGrid.appendChild(badgeElement);
        });
    }

    setDailyWord() {
        if (this.vocabulary.length === 0) return;
        
        // Use date to get consistent daily word
        const today = new Date();
        const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
        const wordIndex = dayOfYear % this.vocabulary.length;
        const dailyWord = this.vocabulary[wordIndex];

        document.getElementById('daily-word').textContent = dailyWord.word;
        document.getElementById('daily-definition').textContent = dailyWord.definition;
        document.getElementById('daily-memory').textContent = dailyWord.mnemonic || 'No memory aid available';
    }

    showMainMenu() {
        // Hide all game screens
        document.querySelectorAll('.game-screen').forEach(screen => {
            screen.style.display = 'none';
        });
        
        // Show main menu
        document.getElementById('main-menu').style.display = 'block';
        document.getElementById('results-modal').style.display = 'none';
        
        this.currentGame = null;
    }

    startGame(gameType) {
        this.currentGame = gameType;
        this.gameState.currentQuestion = 0;
        this.gameState.score = 0;
        this.gameState.streak = 0;

        // Hide main menu
        document.getElementById('main-menu').style.display = 'none';

        switch (gameType) {
            case 'definition-match':
                this.startDefinitionMatch();
                break;
            case 'memory-helper':
                this.startMemoryHelper();
                break;
            case 'word-builder':
                this.startWordBuilder();
                break;
            case 'story-mode':
                this.startStoryMode();
                break;
            case 'progress':
                this.showProgress();
                break;
        }
    }

    // Definition Match Game
    startDefinitionMatch() {
        document.getElementById('definition-match-game').style.display = 'block';
        this.currentWords = this.getRandomWords(10);
        this.showDefinitionMatchQuestion();
    }

    showDefinitionMatchQuestion() {
        const questionNum = this.gameState.currentQuestion + 1;
        document.getElementById('dm-question-count').textContent = `Question ${questionNum}/10`;

        if (this.gameState.currentQuestion >= this.currentWords.length) {
            this.endGame();
            return;
        }

        const currentWord = this.currentWords[this.gameState.currentQuestion];
        document.getElementById('dm-target-word').textContent = currentWord.word;

        // Create choices (1 correct + 3 wrong)
        const choices = [currentWord];
        const otherWords = this.vocabulary.filter(w => w !== currentWord);
        
        for (let i = 0; i < 3; i++) {
            const randomWord = otherWords[Math.floor(Math.random() * otherWords.length)];
            if (!choices.includes(randomWord)) {
                choices.push(randomWord);
            }
        }

        // Shuffle choices
        this.shuffleArray(choices);

        // Create choice buttons
        const choicesContainer = document.getElementById('dm-choices');
        choicesContainer.innerHTML = '';

        choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.innerHTML = `<strong>${String.fromCharCode(65 + index)}.</strong> ${choice.definition}`;
            button.addEventListener('click', () => this.checkDefinitionMatch(choice, currentWord, button));
            choicesContainer.appendChild(button);
        });

        // Hide feedback and next button
        document.getElementById('dm-feedback').innerHTML = '';
        document.getElementById('dm-next-btn').style.display = 'none';
    }

    checkDefinitionMatch(selectedWord, correctWord, buttonElement) {
        // Disable all buttons
        document.querySelectorAll('.choice-btn').forEach(btn => {
            btn.classList.add('disabled');
        });

        const feedbackArea = document.getElementById('dm-feedback');
        
        if (selectedWord === correctWord) {
            // Correct answer
            buttonElement.classList.add('correct');
            this.gameState.score++;
            this.gameState.streak++;
            this.gameState.maxStreak = Math.max(this.gameState.maxStreak, this.gameState.streak);
            this.gameState.wordsLearned.add(correctWord.word);

            feedbackArea.innerHTML = `
                <div class="feedback-message feedback-correct">
                    🎉 Excellent! "${correctWord.word}" means "${correctWord.definition}"
                    ${correctWord.mnemonic ? `<br><small>💡 Memory aid: ${correctWord.mnemonic}</small>` : ''}
                </div>
            `;

            this.checkBadges();
        } else {
            // Incorrect answer
            buttonElement.classList.add('incorrect');
            this.gameState.streak = 0;

            // Highlight correct answer
            document.querySelectorAll('.choice-btn').forEach(btn => {
                if (btn.textContent.includes(correctWord.definition)) {
                    btn.classList.add('correct');
                }
            });

            feedbackArea.innerHTML = `
                <div class="feedback-message feedback-incorrect">
                    Not quite! The correct answer is "${correctWord.definition}"
                    ${correctWord.mnemonic ? `<br><small>💡 Memory aid: ${correctWord.mnemonic}</small>` : ''}
                </div>
            `;
        }

        document.getElementById('dm-next-btn').style.display = 'inline-block';
    }

    nextDefinitionMatchQuestion() {
        this.gameState.currentQuestion++;
        this.showDefinitionMatchQuestion();
    }

    // Memory Helper Game
    startMemoryHelper() {
        document.getElementById('memory-helper-game').style.display = 'block';
        this.currentWords = this.getRandomWords(10).filter(w => w.mnemonic);
        if (this.currentWords.length < 10) {
            // Fill with words that have mnemonics
            const mnemonicWords = this.vocabulary.filter(w => w.mnemonic);
            while (this.currentWords.length < 10 && mnemonicWords.length > 0) {
                const randomWord = mnemonicWords[Math.floor(Math.random() * mnemonicWords.length)];
                if (!this.currentWords.includes(randomWord)) {
                    this.currentWords.push(randomWord);
                }
            }
        }
        this.showMemoryHelperQuestion();
    }

    showMemoryHelperQuestion() {
        const questionNum = this.gameState.currentQuestion + 1;
        document.getElementById('mh-question-count').textContent = `Question ${questionNum}/10`;

        if (this.gameState.currentQuestion >= this.currentWords.length) {
            this.endGame();
            return;
        }

        const currentWord = this.currentWords[this.gameState.currentQuestion];
        document.getElementById('mh-memory-text').textContent = currentWord.mnemonic || 'No memory aid available';
        document.getElementById('mh-definition').textContent = `Hint: ${currentWord.definition}`;
        document.getElementById('mh-word-input').value = '';
        document.getElementById('mh-word-input').focus();

        // Hide feedback and next button
        document.getElementById('mh-feedback').innerHTML = '';
        document.getElementById('mh-next-btn').style.display = 'none';
    }

    checkMemoryHelperAnswer() {
        const userInput = document.getElementById('mh-word-input').value.trim().toLowerCase();
        const currentWord = this.currentWords[this.gameState.currentQuestion];
        const correctAnswers = [currentWord.word.toLowerCase(), currentWord.lemma.toLowerCase()];
        
        const feedbackArea = document.getElementById('mh-feedback');
        
        if (correctAnswers.some(answer => answer === userInput)) {
            // Correct answer
            this.gameState.score++;
            this.gameState.streak++;
            this.gameState.maxStreak = Math.max(this.gameState.maxStreak, this.gameState.streak);
            this.gameState.wordsLearned.add(currentWord.word);

            feedbackArea.innerHTML = `
                <div class="feedback-message feedback-correct">
                    🌟 Perfect! The word is "${currentWord.word}"!
                </div>
            `;

            this.checkBadges();
        } else {
            // Incorrect answer
            this.gameState.streak = 0;

            feedbackArea.innerHTML = `
                <div class="feedback-message feedback-incorrect">
                    Close, but the word is "${currentWord.word}". Try to connect the memory aid with the word!
                </div>
            `;
        }

        document.getElementById('mh-next-btn').style.display = 'inline-block';
    }

    nextMemoryHelperQuestion() {
        this.gameState.currentQuestion++;
        this.showMemoryHelperQuestion();
    }

    // Word Builder Game
    startWordBuilder() {
        document.getElementById('word-builder-game').style.display = 'block';
        this.currentWords = this.getRandomWords(10);
        this.showWordBuilderQuestion();
    }

    showWordBuilderQuestion() {
        const questionNum = this.gameState.currentQuestion + 1;
        document.getElementById('wb-question-count').textContent = `Word ${questionNum}/10`;

        if (this.gameState.currentQuestion >= this.currentWords.length) {
            this.endGame();
            return;
        }

        const currentWord = this.currentWords[this.gameState.currentQuestion];
        document.getElementById('wb-definition').textContent = currentWord.definition;

        // Create letter slots
        const slotsContainer = document.getElementById('wb-letter-slots');
        slotsContainer.innerHTML = '';
        
        for (let i = 0; i < currentWord.word.length; i++) {
            const slot = document.createElement('div');
            slot.className = 'letter-slot';
            slot.dataset.index = i;
            slotsContainer.appendChild(slot);
        }

        // Create scrambled letters
        const letters = currentWord.word.toUpperCase().split('');
        // Add some extra letters to make it challenging
        const extraLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').filter(l => !letters.includes(l));
        for (let i = 0; i < Math.min(4, extraLetters.length); i++) {
            letters.push(extraLetters[Math.floor(Math.random() * extraLetters.length)]);
        }
        
        this.shuffleArray(letters);

        // Create letter buttons
        const lettersContainer = document.getElementById('wb-available-letters');
        lettersContainer.innerHTML = '';

        letters.forEach(letter => {
            const button = document.createElement('button');
            button.className = 'letter-btn';
            button.textContent = letter;
            button.addEventListener('click', () => this.selectLetter(letter, button));
            lettersContainer.appendChild(button);
        });

        // Hide feedback and next button
        document.getElementById('wb-feedback').innerHTML = '';
        document.getElementById('wb-next-btn').style.display = 'none';
    }

    selectLetter(letter, buttonElement) {
        if (buttonElement.classList.contains('used')) return;

        const slots = document.querySelectorAll('.letter-slot:not(.filled)');
        if (slots.length === 0) return;

        // Add letter to first empty slot
        const slot = slots[0];
        slot.textContent = letter;
        slot.classList.add('filled');
        slot.dataset.letter = letter;
        buttonElement.classList.add('used');

        // Check if word is complete
        const allSlots = document.querySelectorAll('.letter-slot');
        const isComplete = Array.from(allSlots).every(slot => slot.classList.contains('filled'));
        
        if (isComplete) {
            this.checkWordBuilder();
        }
    }

    checkWordBuilder() {
        const currentWord = this.currentWords[this.gameState.currentQuestion];
        const slots = document.querySelectorAll('.letter-slot');
        const builtWord = Array.from(slots).map(slot => slot.textContent).join('');
        
        const feedbackArea = document.getElementById('wb-feedback');
        
        if (builtWord.toLowerCase() === currentWord.word.toLowerCase()) {
            // Correct answer
            this.gameState.score++;
            this.gameState.streak++;
            this.gameState.maxStreak = Math.max(this.gameState.maxStreak, this.gameState.streak);
            this.gameState.wordsLearned.add(currentWord.word);

            slots.forEach(slot => slot.style.background = 'linear-gradient(135deg, #d4edda, #a3d977)');

            feedbackArea.innerHTML = `
                <div class="feedback-message feedback-correct">
                    🎉 Amazing! You built "${currentWord.word}" correctly!
                    ${currentWord.mnemonic ? `<br><small>💡 ${currentWord.mnemonic}</small>` : ''}
                </div>
            `;

            this.checkBadges();
        } else {
            // Incorrect answer
            this.gameState.streak = 0;
            slots.forEach(slot => slot.style.background = 'linear-gradient(135deg, #f8d7da, #f5a3a3)');

            feedbackArea.innerHTML = `
                <div class="feedback-message feedback-incorrect">
                    Not quite! The correct word is "${currentWord.word}". Try again!
                </div>
            `;
        }

        document.getElementById('wb-next-btn').style.display = 'inline-block';
    }

    clearWordBuilder() {
        // Clear all slots
        document.querySelectorAll('.letter-slot').forEach(slot => {
            slot.textContent = '';
            slot.classList.remove('filled');
            slot.style.background = '';
        });

        // Reset letter buttons
        document.querySelectorAll('.letter-btn').forEach(btn => {
            btn.classList.remove('used');
        });
    }

    nextWordBuilderQuestion() {
        this.gameState.currentQuestion++;
        this.showWordBuilderQuestion();
    }

    // Story Mode Game
    startStoryMode() {
        document.getElementById('story-mode-game').style.display = 'block';
        this.currentWords = this.getRandomWords(5);
        this.showStoryQuestion();
    }

    showStoryQuestion() {
        const questionNum = this.gameState.currentQuestion + 1;
        document.getElementById('sm-progress').textContent = `Story ${questionNum}/5`;

        if (this.gameState.currentQuestion >= this.currentWords.length) {
            this.endGame();
            return;
        }

        const currentWord = this.currentWords[this.gameState.currentQuestion];
        
        // Generate a simple story with the word
        const stories = [
            `Once upon a time, there was a young explorer who needed to <span class="story-word">${currentWord.word}</span> in order to complete their quest. The word means something very specific in this context.`,
            `In a magical kingdom, the princess had to understand what it meant to <span class="story-word">${currentWord.word}</span>. This action would determine the fate of her realm.`,
            `The wise teacher explained to her students that to <span class="story-word">${currentWord.word}</span> was an important skill they needed to learn for their future adventures.`,
            `During the great adventure, our hero discovered that the ancient scroll mentioned the need to <span class="story-word">${currentWord.word}</span> at the crucial moment.`
        ];

        const selectedStory = stories[Math.floor(Math.random() * stories.length)];
        document.getElementById('sm-story-text').innerHTML = selectedStory;

        // Create choices
        const choices = [currentWord];
        const otherWords = this.vocabulary.filter(w => w !== currentWord);
        
        for (let i = 0; i < 3; i++) {
            const randomWord = otherWords[Math.floor(Math.random() * otherWords.length)];
            if (!choices.find(c => c.word === randomWord.word)) {
                choices.push(randomWord);
            }
        }

        this.shuffleArray(choices);

        // Create choice buttons
        const choicesContainer = document.getElementById('sm-choices');
        choicesContainer.innerHTML = '';

        choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.textContent = choice.definition;
            button.addEventListener('click', () => this.checkStoryAnswer(choice, currentWord, button));
            choicesContainer.appendChild(button);
        });

        // Hide feedback and next button
        document.getElementById('sm-feedback').innerHTML = '';
        document.getElementById('sm-next-btn').style.display = 'none';
    }

    checkStoryAnswer(selectedWord, correctWord, buttonElement) {
        // Disable all buttons
        document.querySelectorAll('#sm-choices .choice-btn').forEach(btn => {
            btn.classList.add('disabled');
        });

        const feedbackArea = document.getElementById('sm-feedback');
        
        if (selectedWord.word === correctWord.word) {
            // Correct answer
            buttonElement.classList.add('correct');
            this.gameState.score++;
            this.gameState.streak++;
            this.gameState.maxStreak = Math.max(this.gameState.maxStreak, this.gameState.streak);
            this.gameState.wordsLearned.add(correctWord.word);

            feedbackArea.innerHTML = `
                <div class="feedback-message feedback-correct">
                    📚 Wonderful! "${correctWord.word}" fits perfectly in the story!
                    ${correctWord.mnemonic ? `<br><small>💡 ${correctWord.mnemonic}</small>` : ''}
                </div>
            `;

            this.checkBadges();
        } else {
            // Incorrect answer
            buttonElement.classList.add('incorrect');
            this.gameState.streak = 0;

            // Highlight correct answer
            document.querySelectorAll('#sm-choices .choice-btn').forEach(btn => {
                if (btn.textContent === correctWord.definition) {
                    btn.classList.add('correct');
                }
            });

            feedbackArea.innerHTML = `
                <div class="feedback-message feedback-incorrect">
                    The word "${correctWord.word}" means "${correctWord.definition}" in this story context.
                    ${correctWord.mnemonic ? `<br><small>💡 ${correctWord.mnemonic}</small>` : ''}
                </div>
            `;
        }

        document.getElementById('sm-next-btn').style.display = 'inline-block';
    }

    nextStoryQuestion() {
        this.gameState.currentQuestion++;
        this.showStoryQuestion();
    }

    // Progress Screen
    showProgress() {
        document.getElementById('progress-screen').style.display = 'block';
        this.updateUI();
    }

    // Game Management
    endGame() {
        this.gameState.gamesPlayed++;
        
        // Calculate points based on performance
        const accuracy = this.gameState.score / this.currentWords.length;
        let points = this.gameState.score * 10;
        
        if (accuracy === 1.0) points += 50; // Perfect bonus
        if (this.gameState.streak >= 5) points += 25; // Streak bonus
        
        this.gameState.totalScore += points;
        
        // Update level based on total score
        this.gameState.level = Math.floor(this.gameState.totalScore / 500) + 1;
        
        this.checkBadges();
        this.saveProgress();
        this.updateUI();
        
        this.showResults(points, accuracy);
    }

    showResults(points, accuracy) {
        const modal = document.getElementById('results-modal');
        const totalQuestions = this.currentWords.length;
        
        document.getElementById('final-score').textContent = `${this.gameState.score}/${totalQuestions}`;
        document.getElementById('points-earned').textContent = `+${points}`;
        
        // Calculate stars (1-3 based on performance)
        let stars = 1;
        if (accuracy >= 0.7) stars = 2;
        if (accuracy >= 0.9) stars = 3;
        
        document.getElementById('stars-earned').textContent = '⭐'.repeat(stars);
        
        // Encouraging messages
        const messages = [
            'Great job! Keep learning! 🌟',
            'You\'re doing amazing! 🎉',
            'Fantastic work! 🏆',
            'Keep it up, superstar! ⭐',
            'You\'re getting smarter every day! 🧠',
            'Wonderful progress! 🚀'
        ];
        
        if (accuracy === 1.0) {
            document.getElementById('encouragement-message').textContent = 'Perfect score! You\'re incredible! 💯';
        } else {
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            document.getElementById('encouragement-message').textContent = randomMessage;
        }
        
        modal.style.display = 'flex';
    }

    checkBadges() {
        // Check various badge conditions
        if (this.gameState.gamesPlayed >= 1 && !this.earnedBadges.has('first_game')) {
            this.earnBadge('first_game');
        }
        
        if (this.gameState.streak >= 5 && !this.earnedBadges.has('streak_5')) {
            this.earnBadge('streak_5');
        }
        
        if (this.gameState.wordsLearned.size >= 10 && !this.earnedBadges.has('words_10')) {
            this.earnBadge('words_10');
        }
        
        if (this.gameState.wordsLearned.size >= 25 && !this.earnedBadges.has('words_25')) {
            this.earnBadge('words_25');
        }
        
        if (this.gameState.wordsLearned.size >= 50 && !this.earnedBadges.has('words_50')) {
            this.earnBadge('words_50');
        }
        
        if (this.gameState.gamesPlayed >= 10 && !this.earnedBadges.has('games_10')) {
            this.earnBadge('games_10');
        }
        
        if (this.gameState.level >= 5 && !this.earnedBadges.has('level_up')) {
            this.earnBadge('level_up');
        }
        
        // Perfect game badge
        if (this.gameState.score === this.currentWords.length && this.currentWords.length >= 5 && !this.earnedBadges.has('perfect_game')) {
            this.earnBadge('perfect_game');
        }
    }

    earnBadge(badgeId) {
        this.earnedBadges.add(badgeId);
        
        // Show badge notification (simple alert for now)
        const badge = this.badges.find(b => b.id === badgeId);
        if (badge) {
            setTimeout(() => {
                alert(`🎉 New Badge Earned! ${badge.icon} ${badge.name}\n${badge.description}`);
            }, 1000);
        }
    }

    // Utility Methods
    getRandomWords(count) {
        const shuffled = [...this.vocabulary];
        this.shuffleArray(shuffled);
        return shuffled.slice(0, Math.min(count, shuffled.length));
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    showError(message) {
        alert(`Error: ${message}`);
    }
}

// Global functions for button events
function showMainMenu() {
    if (window.app) {
        window.app.showMainMenu();
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new VocabularyApp();
});

// Prevent zoom on double tap (mobile)
let lastTouchEnd = 0;
document.addEventListener('touchend', function (event) {
    const now = (new Date()).getTime();
    if (now - lastTouchEnd <= 300) {
        event.preventDefault();
    }
    lastTouchEnd = now;
}, false);