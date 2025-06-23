from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

# Add the src directory to the Python path
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from src.models.player_model import Player
from src.models.database_model import DatabaseModel

class PlayerEntryViewModel(QObject):
    MAX_PLAYERS_PER_TEAM = 15
    
    player_added = pyqtSignal(Player, str)  # Player object and team
    error_occurred = pyqtSignal(str)  # Error message
    start_game = pyqtSignal(list, list)  # Signal to start game with red_team and green_team
    
    def __init__(self):
        super().__init__()
        self.database = DatabaseModel()
        self.red_team = []
        self.green_team = []
    
    def get_player_by_id(self, player_id: int) -> tuple:
        """Query the database for a player by ID"""
        try:
            return self.database.get_player(player_id)
        except Exception as e:
            self.error_occurred.emit(f"Database error: {str(e)}")
            return None
    
    def add_player(self, player_id: int, code_name: str, team: str, equipment_id: int) -> tuple[bool, str]:
        """
        Add a new player to the specified team
        Returns (success: bool, message: str)
        """
        try:
            # Validate team
            team = team.lower()
            if team not in ['red', 'green']:
                return False, "Invalid team. Must be 'Red' or 'Green'"
            
            # Check team capacity
            if team == 'red' and len(self.red_team) >= self.MAX_PLAYERS_PER_TEAM:
                return False, f"Red team is full (max {self.MAX_PLAYERS_PER_TEAM} players)"
            if team == 'green' and len(self.green_team) >= self.MAX_PLAYERS_PER_TEAM:
                return False, f"Green team is full (max {self.MAX_PLAYERS_PER_TEAM} players)"
            
            # Check if player already exists in either team
            if any(p.player_id == player_id for p in self.red_team + self.green_team):
                return False, "Player ID already in use"
            
            # Create new player
            player = Player(player_id, code_name, equipment_id, team)
            
            # Add to the appropriate team
            if team == 'red':
                self.red_team.append(player)
            else:
                self.green_team.append(player)
            
            # Emit signal that player was added
            self.player_added.emit(player, team)
            return True, f"{code_name} added to {team.capitalize()} team"
            
        except Exception as e:
            return False, f"Error adding player: {str(e)}"
    
    def clear_all_players(self):
        """Clear all players from both teams"""
        self.red_team.clear()
        self.green_team.clear()
        return "All players cleared"
    
    def get_team_players(self, team: str) -> list[Player]:
        """Get all players from the specified team"""
        team = team.lower()
        if team == 'red':
            return self.red_team
        elif team == 'green':
            return self.green_team
        return []
    
    def get_all_players(self) -> list[Player]:
        """Get all players from both teams"""
        return self.red_team + self.green_team
        
    def can_start_game(self):
        """Check if we can start the game"""
        total_players = len(self.red_team) + len(self.green_team)
        if total_players < 2:
            return False, "Need at least 2 players to start"
        return True, "Starting game"
        
    def start_game_clicked(self):
        """Handle start game button click"""
        can_start, message = self.can_start_game()
        if can_start:
            # Emit signal to start game with current teams
            self.start_game.emit(self.red_team.copy(), self.green_team.copy())
        return can_start, message
