from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import random
import os
from pathlib import Path

@dataclass
class GameSettings:
    game_duration: int = 360  # 6 minutes in seconds
    warning_time: int = 30    # 30 seconds warning before game ends
    points_per_hit: int = 10
    points_per_base: int = 100
    music_dir: str = str(Path(__file__).parent.parent / "assets" / "sounds")

class GameModel:
    def __init__(self, red_team: list, green_team: list):
        self.settings = GameSettings()
        self.red_team = red_team
        self.green_team = green_team
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.is_running: bool = False
        self.game_log: List[str] = []
        self.current_music: Optional[str] = None
        
        # Initialize scores
        self.red_score: int = 0
        self.green_score: int = 0
        
        # Track which players have hit a base
        self.base_hitters = set()
        
        # Track base hits
        self.red_base_hit = False
        self.green_base_hit = False
        
        # Initialize player states
        for player in self.red_team + self.green_team:
            player.hit_base = False
            player.recently_scored = False
    
    def start_game(self):
        """Start a new game"""
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=self.settings.game_duration)
        self.is_running = True
        self.game_log.append(f"Game started at {self.start_time.strftime('%H:%M:%S')}")
        self._select_music()
    
    def end_game(self):
        """End the current game"""
        if self.is_running:
            self.is_running = False
            self.game_log.append(f"Game ended at {datetime.now().strftime('%H:%M:%S')}")
            self.game_log.append(f"Final Score - Red: {self.red_score} | Green: {self.green_score}")
    
    def get_remaining_time(self) -> int:
        """Get remaining game time in seconds"""
        if not self.is_running or not self.end_time:
            return 0
        
        remaining = (self.end_time - datetime.now()).total_seconds()
        return max(0, int(remaining))
    
    def format_time(self, seconds: int) -> str:
        """Format seconds as MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_formatted_remaining_time(self) -> str:
        """Get formatted remaining time (MM:SS)"""
        return self.format_time(self.get_remaining_time())
    
    def is_warning_time(self) -> bool:
        """Check if we're in the warning time period"""
        return self.get_remaining_time() <= self.settings.warning_time
    
    def _select_music(self):
        """Select a random music file from the sounds directory"""
        try:
            music_dir = Path(self.settings.music_dir)
            if music_dir.exists() and music_dir.is_dir():
                # Look for both WAV and MP3 files
                music_files = list(music_dir.glob("*.wav")) + list(music_dir.glob("*.mp3"))
                if music_files:
                    self.current_music = str(random.choice(music_files))
                else:
                    print("No music files found in", music_dir)
        except Exception as e:
            print(f"Error selecting music: {e}")
    
    def register_hit(self, shooter_id: int, target_id: int):
        """Register a hit between players"""
        if not self.is_running:
            return False, "Game is not running"
        
        # Find shooter and target
        shooter = None
        target = None
        
        for player in self.red_team + self.green_team:
            if player.equipment_id == shooter_id:
                shooter = player
            if player.equipment_id == target_id:
                target = player
        
        if not shooter or not target:
            return False, "Invalid player IDs"
        
        # Check if shooter hit themselves
        if shooter_id == target_id:
            return False, "Cannot hit yourself"
        
        # Calculate score change
        if shooter.team == target.team:
            # Friendly fire - deduct points
            shooter.score -= self.settings.points_per_hit
            self.game_log.append(f"Friendly fire! {shooter.code_name} hit {target.code_name} (-{self.settings.points_per_hit})")
        else:
            # Hit opponent - add points
            shooter.score += self.settings.points_per_hit
            self.game_log.append(f"{shooter.code_name} hit {target.code_name} (+{self.settings.points_per_hit})")
        
        # Update team scores
        self._update_team_scores()
        return True, "Hit registered"
    
    def register_base_hit(self, player_id: int):
        """Register a base hit"""
        if not self.is_running:
            return False, "Game is not running"
        
        player = next((p for p in self.red_team + self.green_team if p.equipment_id == player_id), None)
        if not player:
            return False, "Invalid player ID"
        
        # Check if player already hit a base
        if player.equipment_id in self.base_hitters:
            return False, "Already hit a base"
        
        # Award points and mark as base hitter
        player.score += self.settings.points_per_base
        player.base_hit = True
        self.base_hitters.add(player.equipment_id)
        
        # Update team scores
        self._update_team_scores()
        
        self.game_log.append(f"{player.code_name} scored a base hit! (+{self.settings.points_per_base})")
        return True, "Base hit registered"
    
    def _update_team_scores(self):
        """Update team scores based on player scores"""
        self.red_score = sum(player.score for player in self.red_team)
        self.green_score = sum(player.score for player in self.green_team)
    
    def get_team_players_sorted(self, team: str) -> list:
        """Get players from a team, sorted by score (highest first)"""
        team_players = [p for p in (self.red_team if team.lower() == 'red' else self.green_team)]
        return sorted(team_players, key=lambda p: p.score, reverse=True)
    
    def get_recent_events(self, count: int = 5) -> list:
        """Get the most recent game events"""
        return self.game_log[-count:] if self.game_log else []
    
    def get_scores(self) -> dict:
        """Get the current scores and team states
        
        Returns:
            dict: Dictionary containing scores and team states
        """
        return {
            'red_score': self.red_score,
            'green_score': self.green_score,
            **self.get_team_states()
        }
    
    def get_team_states(self) -> dict:
        """Get the current state of both teams
        
        Returns:
            dict: Dictionary containing team states with player information
        """
        def get_player_state(player):
            return {
                'id': player.equipment_id,
                'name': player.code_name,
                'score': player.score,
                'base_hit': player.base_hit,
                'recently_scored': player.recently_scored
            }
            
        return {
            'red_players': [get_player_state(p) for p in self.red_team],
            'green_players': [get_player_state(p) for p in self.green_team],
            'red_base_hit': self.red_base_hit,
            'green_base_hit': self.green_base_hit
        }
