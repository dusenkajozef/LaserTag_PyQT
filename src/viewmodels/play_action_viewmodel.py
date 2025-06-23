from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QTime
from models.game_model import GameModel
from models.network_model import NetworkModel

class PlayActionViewModel(QObject):
    """View model for the Play Action Screen"""
    
    # Signals for UI updates
    update_timer = pyqtSignal(str)  # Current time remaining
    update_scores = pyqtSignal(dict)  # Team and player scores
    update_log = pyqtSignal(list)  # Game events log
    game_ended = pyqtSignal()  # When the game ends
    warning_time = pyqtSignal()  # When warning time is reached
    
    def __init__(self, red_team: list, green_team: list):
        super().__init__()
        self.game_model = GameModel(red_team, green_team)
        # Use the same port (7501) for both receiving and transmitting
        self.network = NetworkModel(host='127.0.0.1', tx_port=7501, rx_port=7501)
        
        # Set up timer for game updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game_state)
        self.timer.setInterval(1000)  # Update every second
        
        # Connect network signals
        self.network.data_received.connect(self.handle_network_data)
        self.network.error_occurred.connect(self.handle_network_error)
        
        # Sound signals
        self.play_sound = None  # Will be connected by the view
    
    def start_game(self):
        """Start the game and network service"""
        self.game_model.start_game()
        self.network.start()
        self.timer.start()
        
        # Broadcast game start
        self.network.broadcast_game_start()
        
        # Initial update
        self.update_game_state()
    
    def end_game(self):
        """End the game and clean up"""
        self.timer.stop()
        self.game_model.end_game()
        self.network.broadcast_game_end()
        self.game_ended.emit()
    
    def update_game_state(self):
        """Update the game state and emit signals"""
        if not self.game_model.is_running:
            return
            
        # Update timer
        remaining = self.game_model.get_remaining_time()
        minutes = remaining // 60
        seconds = remaining % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.update_timer.emit(time_str)
        
        # Check for warning time (last 30 seconds)
        if remaining == 30:
            self.warning_time.emit()
            
        # Check for game end
        if remaining <= 0:
            self.game_model.end_game()
            self.game_ended.emit()
            return
            
        # Update scores and team states
        self.update_scores.emit({
            'red_score': self.game_model.red_score,
            'green_score': self.game_model.green_score,
            **self.game_model.get_team_states()
        })
        
        # Update game log
        self.update_log.emit(self.game_model.get_recent_events(5))
    
    def handle_network_data(self, data):
        """Handle incoming network data
        
        Args:
            data: Either a string (legacy) or a dict with 'type' key
        """
        try:
            # Handle dictionary format from NetworkModel
            if isinstance(data, dict):
                data_type = data.get('type')
                if data_type == 'player_hit':
                    shooter_id = data.get('shooter_id')
                    target_id = data.get('target_id')
                    if shooter_id is not None and target_id is not None:
                        success, message = self.game_model.register_hit(shooter_id, target_id)
                        if success:
                            self.update_scores.emit(self.game_model.get_scores())
                            self.update_log.emit([message])
                            if hasattr(self, 'play_sound'):
                                self.play_sound.emit('hit')
                elif data_type == 'base_hit':
                    base_team = data.get('base_team')
                    if base_team in ['red', 'green']:
                        success, message = self.game_model.register_base_hit(base_team)
                        if success:
                            self.update_scores.emit(self.game_model.get_scores())
                            self.update_log.emit([message])
                            if hasattr(self, 'play_sound'):
                                self.play_sound.emit('base_hit')
                elif data_type == 'game_start' and not self.game_model.is_running:
                    self.game_model.start_game()
                elif data_type == 'game_end' and self.game_model.is_running:
                    self.game_model.end_game()
            # Handle legacy string format (for backward compatibility)
            elif isinstance(data, str):
                # Handle base hits (53 for red base, 43 for green base)
                if data == "53":  # Red base hit
                    success, message = self.game_model.register_base_hit('red')
                    if success:
                        self.update_scores.emit(self.game_model.get_scores())
                        self.update_log.emit([message])
                        if hasattr(self, 'play_sound'):
                            self.play_sound.emit('base_hit')
                elif data == "43":  # Green base hit
                    success, message = self.game_model.register_base_hit('green')
                    if success:
                        self.update_scores.emit(self.game_model.get_scores())
                        self.update_log.emit([message])
                        if hasattr(self, 'play_sound'):
                            self.play_sound.emit('base_hit')
                # Handle hit events (format: "shooter_id:target_id")
                elif ":" in data:
                    shooter_id, target_id = map(int, data.split(":"))
                    success, message = self.game_model.register_hit(shooter_id, target_id)
                    if success:
                        self.update_scores.emit(self.game_model.get_scores())
                        self.update_log.emit([message])
                        if hasattr(self, 'play_sound'):
                            self.play_sound.emit('hit')
                # Handle game control commands
                elif data == "202" and not self.game_model.is_running:  # Start game
                    self.game_model.start_game()
                elif data == "221" and self.game_model.is_running:  # End game
                    self.game_model.end_game()
                    self.game_ended.emit()
        except Exception as e:
            print(f"Error handling network data: {e}")
    
    def handle_network_error(self, message: str):
        """Handle network errors"""
        print(f"Network error: {message}")
    
    def cleanup(self):
        """Clean up resources"""
        self.timer.stop()
        self.network.stop()
        
    def get_winning_team(self) -> str:
        """Get the winning team or 'tie' if scores are equal"""
        if self.game_model.red_score > self.game_model.green_score:
            return 'Red'
        elif self.game_model.green_score > self.game_model.red_score:
            return 'Green'
        return 'Tie'
