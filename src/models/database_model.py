import os
import sqlite3
from typing import Optional, Tuple

class DatabaseModel:
    def __init__(self, db_path: str = 'data/laser_tag.db'):
        """Initialize the database connection and create tables if they don't exist"""
        self.db_path = db_path
        self._create_tables()
    
    def _get_connection(self):
        """Create a database connection and return the connection object"""
        # Create the data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        """Create the players table if it doesn't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    code_name TEXT NOT NULL,
                    team TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def get_player(self, player_id: int) -> Optional[Tuple[int, str]]:
        """Get a player by ID. Returns (player_id, code_name) or None if not found"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, code_name FROM players WHERE id = ?', (player_id,))
            return cursor.fetchone()
    
    def add_player(self, player_id: int, code_name: str, team: str = None) -> bool:
        """Add a new player to the database. Returns True if successful, False if player ID already exists"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO players (id, code_name, team) VALUES (?, ?, ?)',
                    (player_id, code_name, team)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Player ID already exists
            return False
    
    def update_player_team(self, player_id: int, team: str) -> bool:
        """Update a player's team. Returns True if successful, False if player not found"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE players SET team = ? WHERE id = ?',
                (team, player_id)
            )
            conn.commit()
            return cursor.rowcount > 0
