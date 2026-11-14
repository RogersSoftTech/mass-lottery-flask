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

- **Mass Cash**: 5 numbers from 1-35
- **Powerball**: 5 numbers from 1-69 + 1 Powerball from 1-26
- **Mega Millions**: 5 numbers from 1-70 + 1 Megaball from 1-25

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

**Response:**
```json
{
  "game": "mass_cash",
  "game_name": "Mass Cash",
  "white_numbers": [5, 12, 23, 31, 35]
}
```

### GET /api/games
Get list of available games.

**Response:**
```json
[
  { "id": "mass_cash", "name": "Mass Cash" },
  { "id": "powerball", "name": "Powerball" },
  { "id": "mega_millions", "name": "Mega Millions" }
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
