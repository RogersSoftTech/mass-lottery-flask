from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
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
    Generate lottery numbers with optional consecutive pairs.
    
    :param min_num: Minimum number range
    :param max_num: Maximum number range
    :param count: How many numbers to generate
    :param consecutive_pairs: 0, 1, or 2 - how many consecutive pairs to include
    :param allow_duplicates: Whether duplicates are allowed (for The Numbers Game)
    :return: Sorted list of numbers
    """
    numbers = []
    max_attempts = 1000
    
    if consecutive_pairs > 0:
        # Generate the specified number of consecutive pairs
        pairs_to_generate = min(consecutive_pairs, count // 2)
        
        for _ in range(pairs_to_generate):
            valid_pair_found = False
            attempts = 0
            
            while not valid_pair_found and attempts < 100:
                # Pick a random starting number that allows for a consecutive pair
                start_num = random.randint(min_num, max_num - 1)
                next_num = start_num + 1
                
                # Check if both numbers are valid and not already in the list
                if next_num <= max_num and start_num not in numbers and next_num not in numbers:
                    # Check that adding this pair won't create a chain with existing numbers
                    creates_chain = any(abs(n - start_num) == 1 or abs(n - next_num) == 1 for n in numbers)
                    
                    if not creates_chain:
                        numbers.append(start_num)
                        numbers.append(next_num)
                        valid_pair_found = True
                
                attempts += 1
        
        # Fill remaining slots with random numbers that don't create consecutive pairs
        attempts = 0
        while len(numbers) < count and attempts < max_attempts:
            rn = random.randint(min_num, max_num)
            if rn not in numbers or allow_duplicates:
                # Check if this number would create a consecutive pair
                would_create_pair = any(abs(n - rn) == 1 for n in numbers)
                if not would_create_pair or allow_duplicates:
                    numbers.append(rn)
            attempts += 1
        
        # If we couldn't fill all slots, just fill remaining with any random numbers
        while len(numbers) < count:
            rn = random.randint(min_num, max_num)
            if allow_duplicates or rn not in numbers:
                numbers.append(rn)
    else:
        # Generate numbers with NO consecutive pairs allowed
        attempts = 0
        
        while len(numbers) < count and attempts < max_attempts:
            rn = random.randint(min_num, max_num)
            
            if allow_duplicates:
                # For games that allow duplicates (The Numbers Game)
                would_create_pair = any(abs(n - rn) == 1 for n in numbers)
                if not would_create_pair:
                    numbers.append(rn)
            else:
                # For most games: ensure unique numbers and no consecutive pairs
                if rn not in numbers:
                    would_create_pair = any(abs(n - rn) == 1 for n in numbers)
                    if not would_create_pair:
                        numbers.append(rn)
            attempts += 1
        
        # If we couldn't fill all slots, just fill remaining
        while len(numbers) < count:
            rn = random.randint(min_num, max_num)
            if allow_duplicates or rn not in numbers:
                numbers.append(rn)
    
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
