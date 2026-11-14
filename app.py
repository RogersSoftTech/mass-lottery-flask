from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Lottery configurations
LOTTERY_CONFIGS = {
    'powerball': {
        'name': 'Powerball',
        'white_balls': (1, 69),
        'red_balls': (1, 26),
        'count': 5
    },
    'mega_millions': {
        'name': 'Mega Millions',
        'white_balls': (1, 70),
        'yellow_balls': (1, 25),
        'count': 5
    },
    'mass_cash': {
        'name': 'Mass Cash',
        'white_balls': (1, 35),
        'count': 5
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
        
        # Generate white ball numbers
        white_min, white_max = config['white_balls']
        white_numbers = sorted(random.sample(range(white_min, white_max + 1), config['count']))
        
        result = {
            'game': game_type,
            'game_name': config['name'],
            'white_numbers': white_numbers
        }
        
        # Generate bonus ball if applicable
        if game_type == 'powerball':
            red_min, red_max = config['red_balls']
            result['powerball'] = random.randint(red_min, red_max)
        elif game_type == 'mega_millions':
            yellow_min, yellow_max = config['yellow_balls']
            result['megaball'] = random.randint(yellow_min, yellow_max)
        
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
