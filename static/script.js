let installPrompt = null;

window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    installPrompt = event;
});

document.addEventListener('DOMContentLoaded', () => {
    const installSection = document.getElementById('install-section');
    const installBtn = document.getElementById('install-btn');
    const installInstructions = document.getElementById('install-instructions');
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
    const consecutiveCheckbox = document.getElementById('consecutive-checkbox');
    const radioGroup = document.getElementById('radio-group');
    const radioButtons = document.querySelectorAll('input[name="consecutive-pairs"]');

    let lastResult = null;

    document.querySelectorAll('.logo-ball').forEach(ball => {
        ball.textContent = Math.floor(Math.random() * 69) + 1;
        let bounces = 0;
        ball.addEventListener('animationiteration', () => {
            bounces += 1;
            if (bounces % 3 !== 0) return;
            const previous = Number(ball.textContent);
            ball.textContent = (previous + Math.floor(Math.random() * 68)) % 69 + 1;
        });
    });

    if (window.matchMedia('(display-mode: standalone)').matches || navigator.standalone === true) {
        installSection.hidden = true;
    }

    window.addEventListener('appinstalled', () => {
        installPrompt = null;
        installSection.hidden = true;
    });

    installBtn.addEventListener('click', async () => {
        if (!installPrompt) {
            installInstructions.hidden = !installInstructions.hidden;
            installBtn.setAttribute('aria-expanded', String(!installInstructions.hidden));
            return;
        }

        const prompt = installPrompt;
        installPrompt = null;
        try {
            await prompt.prompt();
        } catch (error) {
            console.error('Unable to open the install prompt:', error);
            installInstructions.hidden = false;
            installBtn.setAttribute('aria-expanded', 'true');
        }
    });

    generateBtn.addEventListener('click', generateNumbers);
    copyBtn.addEventListener('click', copyNumbers);
    newBtn.addEventListener('click', generateNumbers);

    // Toggle radio buttons based on checkbox
    consecutiveCheckbox.addEventListener('change', () => {
        radioButtons.forEach(btn => {
            btn.disabled = !consecutiveCheckbox.checked;
        });
    });

    async function generateNumbers() {
        if (generateBtn.disabled) return;

        const game = gameSelect.value;
        const updateNumbersOnly = lastResult && lastResult.game === game &&
            !resultContainer.classList.contains('hidden');

        try {
            generateBtn.disabled = true;
            newBtn.disabled = true;
            errorMessage.classList.add('hidden');
            if (!updateNumbersOnly) {
                loading.classList.remove('hidden');
                resultContainer.classList.add('hidden');
            }
            
            // Get consecutive pairs value if checkbox is checked, otherwise 0
            let consecutivePairs = 0;
            if (consecutiveCheckbox.checked) {
                const checkedRadio = document.querySelector('input[name="consecutive-pairs"]:checked');
                consecutivePairs = parseInt(checkedRadio.value);
            }

            const response = await fetch('/api/lottery', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    game,
                    consecutive_pairs: consecutivePairs
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate numbers');
            }

            const data = await response.json();

            if (updateNumbersOnly) {
                numbersDisplay.querySelectorAll('.number-ball').forEach((ball, index) => {
                    ball.textContent = data.numbers[index];
                });
                if (data.bonus) {
                    bonusBall.textContent = data.bonus.value;
                }
            } else {
                displayResults(data);
            }
            lastResult = data;

            loading.classList.add('hidden');
            resultContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = 'Error generating numbers: ' + error.message;
            errorMessage.classList.remove('hidden');
            loading.classList.add('hidden');
        } finally {
            generateBtn.disabled = false;
            newBtn.disabled = false;
        }
    }

    function displayResults(data) {
        // Update game name
        gameName.textContent = data.game_name;

        // Clear and display main numbers
        numbersDisplay.innerHTML = '';
        data.numbers.forEach(number => {
            const ball = document.createElement('div');
            ball.className = 'number-ball';
            ball.textContent = number;
            ball.style.background = `linear-gradient(135deg, ${data.bonus_color}, ${adjustColor(data.bonus_color, -20)})`;
            numbersDisplay.appendChild(ball);
        });

        // Hide bonus section by default
        bonusSection.classList.add('hidden');

        // Display bonus ball if present
        if (data.bonus) {
            bonusBall.textContent = data.bonus.value;
            bonusBall.style.background = `linear-gradient(135deg, ${data.bonus_color}, ${adjustColor(data.bonus_color, -20)})`;
            const bonusLabel = document.querySelector('.bonus-label');
            if (bonusLabel) {
                bonusLabel.textContent = `${data.bonus.name}:`;
            }
            bonusSection.classList.remove('hidden');
        }
    }

    function adjustColor(hex, percent) {
        // Simple color adjustment for gradients
        return hex;
    }

    function copyNumbers() {
        if (!lastResult) return;

        let text = `${lastResult.game_name}: ${lastResult.numbers.join(', ')}`;

        if (lastResult.bonus) {
            text += ` + ${lastResult.bonus.name}: ${lastResult.bonus.value}`;
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
