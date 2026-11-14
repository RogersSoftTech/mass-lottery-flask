# Mass Lottery - Python Flask Edition

A simple, modern lottery number generator web application built with Python Flask.

## Features

- 🎰 Multiple lottery games (Mass Cash, Powerball, Mega Millions)
- 🎲 Random number generation
- 📋 Copy numbers to clipboard
- 📱 Fully responsive design
- 🚀 Fast and lightweight
- 🛡️ CORS enabled for flexibility

## Games Supported

- **Mega Millions**: 5 numbers from 1-70 + 1 Megaball from 1-25
- **Powerball**: 5 numbers from 1-69 + 1 Powerball from 1-26
- **Megabucks**: 6 numbers from 1-44
- **Mass Cash**: 5 numbers from 1-35
- **Lucky For Life**: 5 numbers from 1-48 + 1 Lucky Ball from 1-18
- **The Numbers Game**: 4 numbers from 0-9

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn (production)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RogersSoftTech/mass-lottery-flask.git
   cd mass-lottery-flask
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

### Install as an app

Open the site over HTTPS (or localhost) and select **Install App**. If your browser
does not show an install prompt, use its menu to install the app or add it to your
home screen. On iPhone and iPad, use Safari's Share menu and select **Add to Home
Screen**. Number generation requires a connection to the server.

## API Endpoints

### GET /
Serves the main HTML page.

### POST /api/lottery
Generate lottery numbers for a specific game.

**Request:**
```json
{
  "game": "mass_cash"
}
```

**Response (no bonus):**
```json
{
  "game": "mass_cash",
  "game_name": "Mass Cash",
  "numbers": [5, 12, 23, 31, 35],
  "bonus_color": "#FDB913"
}
```

**Response (with bonus):**
```json
{
  "game": "powerball",
  "game_name": "Powerball",
  "numbers": [5, 12, 23, 31, 35],
  "bonus": {
    "name": "Powerball",
    "value": 21
  },
  "bonus_color": "#EB1414"
}
```

### GET /api/games
Get list of available games.

**Response:**
```json
[
  { "id": "mega_millions", "name": "Mega Millions" },
  { "id": "powerball", "name": "Powerball" },
  { "id": "megabucks", "name": "Megabucks" },
  { "id": "mass_cash", "name": "Mass Cash" },
  { "id": "lucky_for_life", "name": "Lucky For Life" },
  { "id": "the_numbers_game", "name": "The Numbers Game" }
]
```

## Project Structure

```
mass-lottery-flask/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML page
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend logic
```

## Development

### Running Tests

(Tests coming soon)

### Code Style

This project follows PEP 8 guidelines for Python code.

## Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker (Coming Soon)

## Environment Variables

Create a `.env` file in the root directory (optional):

```env
FLASK_ENV=development
FLASK_DEBUG=true
```

## License

This project is open source and available under the MIT License.

## Author

Created by Rogers Soft Tech

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
