from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import secrets
import random

app = Flask(__name__)
CORS(app)

# Lottery configurations - all Massachusetts lottery games
LOTTERY_CONFIGS = {
    'mega_millions': {
        'name': 'Mega Millions',
        'numbers': (1, 70),
        'bonus': (1, 25),
        'bonus_name': 'Megaball',
        'count': 5,
        'bonus_color': '#24408F'
    },
    'powerball': {
        'name': 'Powerball',
        'numbers': (1, 69),
        'bonus': (1, 26),
        'bonus_name': 'Powerball',
        'count': 5,
        'bonus_color': '#EB1414'
    },
    'megabucks': {
        'name': 'Megabucks',
        'numbers': (1, 44),
        'count': 6,
        'bonus_color': '#000000'
    },
    'mass_cash': {
        'name': 'Mass Cash',
        'numbers': (1, 35),
        'count': 5,
        'bonus_color': '#FDB913'
    },
    'lucky_for_life': {
        'name': 'Lucky For Life',
        'numbers': (1, 48),
        'bonus': (1, 18),
        'bonus_name': 'Lucky Ball',
        'count': 5,
        'bonus_color': '#047841'
    },
    'the_numbers_game': {
        'name': 'The Numbers Game',
        'numbers': (0, 9),
        'count': 4,
        'bonus_color': '#FF6600'
    }
}

def generate_numbers(min_num, max_num, count, consecutive_pairs=0, allow_duplicates=False):
    """
    Generate lottery numbers with optional consecutive pairs using improved randomness.
    
    Uses Fisher-Yates shuffle algorithm for better distribution.
    
    :param min_num: Minimum number range
    :param max_num: Maximum number range
    :param count: How many numbers to generate
    :param consecutive_pairs: 0, 1, or 2 - how many consecutive pairs to include
    :param allow_duplicates: Whether duplicates are allowed (for The Numbers Game)
    :return: Sorted list of numbers
    """
    
    if consecutive_pairs == 0 or not consecutive_pairs:
        # No consecutive pairs - use Fisher-Yates shuffle for better randomness
        if allow_duplicates:
            # For The Numbers Game: allow duplicates, but no consecutive numbers
            numbers = []
            available = list(range(min_num, max_num + 1))
            
            for _ in range(count):
                idx = secrets.randbelow(len(available))
                num = available[idx]
                numbers.append(num)
                
                # Remove the selected number and its neighbors to avoid consecutive
                new_available = []
                for n in available:
                    if abs(n - num) > 1:
                        new_available.append(n)
                
                # Add back some numbers if we removed too many
                if len(new_available) == 0 and len(available) > 1:
                    new_available = [n for n in available if n != num]
                
                available = new_available if new_available else available
            
            return sorted(numbers)
        else:
            # Standard case: unique numbers, no consecutive
            available = list(range(min_num, max_num + 1))
            random.shuffle(available)
            
            # Filter out consecutive numbers efficiently
            selected = []
            for num in available:
                if not selected or all(abs(num - s) > 1 for s in selected):
                    selected.append(num)
                    if len(selected) == count:
                        break
            
            # If we can't get enough without consecutive, relax the constraint slightly
            while len(selected) < count:
                candidate = secrets.randbelow(max_num - min_num + 1) + min_num
                if candidate not in selected:
                    selected.append(candidate)
            
            return sorted(selected)
    
    else:
        # With consecutive pairs - generate pairs first, then fill remaining
        pairs_to_generate = min(consecutive_pairs, count // 2)
        numbers = []
        pairs_generated = 0
        
        # Generate exactly the requested number of consecutive pairs
        max_pair_attempts = 300
        pair_attempts = 0
        
        while pairs_generated < pairs_to_generate and pair_attempts < max_pair_attempts:
            # Use secrets for cryptographic randomness
            start_num = min_num + secrets.randbelow(max_num - min_num)
            next_num = start_num + 1
            
            if next_num <= max_num and start_num not in numbers and next_num not in numbers:
                # Check no chains with existing numbers
                creates_chain = any(abs(n - start_num) == 1 or abs(n - next_num) == 1 for n in numbers)
                
                if not creates_chain:
                    numbers.append(start_num)
                    numbers.append(next_num)
                    pairs_generated += 1
            
            pair_attempts += 1
        
        # Fill remaining slots, ensuring NO new consecutive pairs are created
        remaining_needed = count - len(numbers)
        
        if remaining_needed > 0:
            # Generate a pool of valid candidates
            # Must not be in numbers AND must not be adjacent to ANY existing number
            available = []
            for n in range(min_num, max_num + 1):
                if n not in numbers:
                    # Check if this number would create a consecutive pair
                    would_create_pair = any(abs(n - num) == 1 for num in numbers)
                    if not would_create_pair:
                        available.append(n)
            
            # Shuffle the available pool
            random.shuffle(available)
            
            # Select from available, ensuring no consecutive pairs among selections
            selected = []
            for candidate in available:
                # Check if candidate is consecutive to any already selected
                is_consecutive_to_selected = any(abs(candidate - s) == 1 for s in selected)
                if not is_consecutive_to_selected:
                    selected.append(candidate)
                    if len(selected) == remaining_needed:
                        break
            
            # Add selected numbers to our final list
            numbers.extend(selected)
            
            # If we still need more (edge case with very small ranges)
            if len(numbers) < count:
                for n in range(min_num, max_num + 1):
                    if n not in numbers and len(numbers) < count:
                        numbers.append(n)
        
        return sorted(numbers)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/lottery', methods=['POST'])
def generate_lottery():
    """Generate lottery numbers based on game type"""
    try:
        data = request.get_json()
        game_type = data.get('game', 'mass_cash')
        consecutive_pairs = data.get('consecutive_pairs', 0)
        
        if game_type not in LOTTERY_CONFIGS:
            return jsonify({'error': 'Invalid game type'}), 400
        
        # Validate consecutive pairs
        consecutive_pairs = max(0, min(2, int(consecutive_pairs)))
        
        config = LOTTERY_CONFIGS[game_type]
        
        # Generate main numbers with consecutive pair logic
        num_min, num_max = config['numbers']
        allow_dups = game_type == 'the_numbers_game'
        main_numbers = generate_numbers(
            num_min, 
            num_max, 
            config['count'], 
            consecutive_pairs=consecutive_pairs,
            allow_duplicates=allow_dups
        )
        
        result = {
            'game': game_type,
            'game_name': config['name'],
            'numbers': main_numbers,
            'bonus_color': config['bonus_color'],
            'consecutive_pairs': consecutive_pairs
        }
        
        # Generate bonus ball if the game has one
        if 'bonus' in config:
            bonus_min, bonus_max = config['bonus']
            bonus_name = config.get('bonus_name', 'Bonus Ball')
            bonus_value = random.randint(bonus_min, bonus_max)
            result['bonus'] = {
                'name': bonus_name,
                'value': bonus_value
            }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/games', methods=['GET'])
def get_games():
    """Get list of available games"""
    games = []
    for key, config in LOTTERY_CONFIGS.items():
        games.append({
            'id': key,
            'name': config['name']
        })
    return jsonify(games)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
