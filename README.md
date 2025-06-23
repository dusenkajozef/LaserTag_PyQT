# Laser Tag System

A laser tag game management system built with Python and PyQt6, following the MVVM architecture pattern.

## Features

- Player registration and team management
- Real-time score tracking
- Game timer with countdown
- Network communication for hit detection
- Database persistence for player information
- Play-by-play action log

## Requirements

- Python 3.8+
- PyQt6
- SQLite3 (included in Python standard library)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Laser_Tag
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Running the Application

To start the Laser Tag system:

```bash
python -m src.main
```

## Usage

1. **Player Entry Screen**
   - Add players by entering their ID, code name, and equipment ID
   - Assign players to Red or Green teams
   - Start the game when ready (minimum 2 players required)

2. **Play Action Screen**
   - View real-time scores and team standings
   - Monitor the game timer
   - Track game events in the action log
   - End the game manually if needed

## Project Structure

```
src/
├── __init__.py
├── main.py                 # Application entry point
├── models/                # Data models and business logic
│   ├── __init__.py
│   ├── player_model.py    # Player data model
│   ├── game_model.py      # Game logic and state
│   ├── database_model.py  # Database operations
│   └── network_model.py   # Network communication
├── views/                 # UI components
│   ├── __init__.py
│   ├── splash_screen.py   # Splash screen
│   ├── player_entry_screen.py  # Player registration
│   └── play_action_screen.py   # Game interface
└── viewmodels/            # View models for MVVM
    ├── __init__.py
    ├── splash_screen_viewmodel.py
    ├── player_entry_viewmodel.py
    └── play_action_viewmodel.py
```

## Configuration

Network settings can be configured in the `config.py` file:
- Host address
- Port numbers for sending/receiving data
