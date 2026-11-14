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
        
        if game_type not in LOTTERY_CONFIGS:
            return jsonify({'error': 'Invalid game type'}), 400
        
        config = LOTTERY_CONFIGS[game_type]
        
        # Generate main numbers
        num_min, num_max = config['numbers']
        main_numbers = sorted(random.sample(range(num_min, num_max + 1), config['count']))
        
        result = {
            'game': game_type,
            'game_name': config['name'],
            'numbers': main_numbers,
            'bonus_color': config['bonus_color']
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
