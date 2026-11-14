document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const gameSelect = document.getElementById('game-select');
    const resultContainer = document.getElementById('result-container');
    const numbersDisplay = document.getElementById('numbers-display');
    const gameName = document.getElementById('game-name');
    const bonusSection = document.getElementById('bonus-section');
    const bonusBall = document.getElementById('bonus-ball');
    const errorMessage = document.getElementById('error-message');
    const loading = document.getElementById('loading');
    const copyBtn = document.getElementById('copy-btn');
    const newBtn = document.getElementById('new-btn');

    let lastResult = null;

    generateBtn.addEventListener('click', generateNumbers);
    copyBtn.addEventListener('click', copyNumbers);
    newBtn.addEventListener('click', generateNumbers);

    async function generateNumbers() {
        try {
            // Show loading state
            generateBtn.disabled = true;
            loading.classList.remove('hidden');
            errorMessage.classList.add('hidden');
            resultContainer.classList.add('hidden');

            const game = gameSelect.value;
            const response = await fetch('/api/lottery', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ game })
            });

            if (!response.ok) {
                throw new Error('Failed to generate numbers');
            }

            const data = await response.json();
            lastResult = data;

            displayResults(data);

            loading.classList.add('hidden');
            resultContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = 'Error generating numbers: ' + error.message;
            errorMessage.classList.remove('hidden');
            loading.classList.add('hidden');
        } finally {
            generateBtn.disabled = false;
        }
    }

    function displayResults(data) {
        // Update game name
        gameName.textContent = data.game_name;

        // Clear and display white numbers
        numbersDisplay.innerHTML = '';
        data.white_numbers.forEach(number => {
            const ball = document.createElement('div');
            ball.className = 'number-ball';
            ball.textContent = number;
            numbersDisplay.appendChild(ball);
        });

        // Hide bonus section by default
        bonusSection.classList.add('hidden');

        // Display powerball or megaball if present
        if (data.powerball !== undefined) {
            bonusBall.textContent = data.powerball;
            bonusBall.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
            bonusSection.classList.remove('hidden');
        } else if (data.megaball !== undefined) {
            bonusBall.textContent = data.megaball;
            bonusBall.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
            bonusSection.classList.remove('hidden');
        }
    }

    function copyNumbers() {
        if (!lastResult) return;

        let text = `${lastResult.game_name}: ${lastResult.white_numbers.join(', ')}`;

        if (lastResult.powerball !== undefined) {
            text += ` + Powerball: ${lastResult.powerball}`;
        } else if (lastResult.megaball !== undefined) {
            text += ` + Megaball: ${lastResult.megaball}`;
        }

        navigator.clipboard.writeText(text).then(() => {
            // Show feedback
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '✓ Copied!';
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
            alert('Failed to copy to clipboard');
        });
    }

    // Generate numbers on Enter key
    gameSelect.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            generateNumbers();
        }
    });
});
