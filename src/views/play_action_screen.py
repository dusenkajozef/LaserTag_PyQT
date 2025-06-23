from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QListWidgetItem, QFrame, QMessageBox, QSlider, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer, QTime
from PyQt6.QtGui import QFont, QColor, QPalette
from src.utils.audio import AudioPlayer
from viewmodels.play_action_viewmodel import PlayActionViewModel

class PlayActionScreen(QMainWindow):
    def __init__(self, viewmodel: PlayActionViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.setup_ui()
        self.connect_signals()
        
        # Start the game when the screen is shown
        self.viewmodel.start_game()
    
    def setup_ui(self):
        """Set up the play action screen UI"""
        self.setWindowTitle("Laser Tag - Game In Progress")
        self.setMinimumSize(1000, 700)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Game info
        game_info_layout = QHBoxLayout()
        
        # Timer
        timer_group = QGroupBox("Game Timer")
        timer_layout = QVBoxLayout()
        self.timer_label = QLabel("06:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        timer_layout.addWidget(self.timer_label)
        timer_group.setLayout(timer_layout)
        
        # Volume control
        volume_group = QGroupBox("Volume")
        volume_layout = QVBoxLayout()
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        volume_layout.addWidget(QLabel("Music Volume:"))
        volume_layout.addWidget(self.volume_slider)
        volume_group.setLayout(volume_layout)
        
        # End game button
        end_game_group = QGroupBox()
        end_game_layout = QVBoxLayout()
        self.end_game_btn = QPushButton("End Game")
        self.end_game_btn.clicked.connect(self.confirm_end_game)
        end_game_layout.addWidget(self.end_game_btn)
        end_game_group.setLayout(end_game_layout)
        
        game_info_layout.addWidget(timer_group, 1)
        game_info_layout.addWidget(volume_group, 1)
        game_info_layout.addWidget(end_game_group, 1)
        
        main_layout.addLayout(game_info_layout)
        
        # Team scores
        self.red_score_label = QLabel("Red: 0")
        self.red_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_score_label.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")
        
        self.green_score_label = QLabel("Green: 0")
        self.green_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_score_label.setStyleSheet("color: green; font-weight: bold; font-size: 16px;")
        
        # Add widgets to top bar
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.red_score_label, 1)
        top_layout.addWidget(self.green_score_label, 1)
        
        # Main content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        # Left side - Red team
        red_team_group = QFrame()
        red_team_group.setFrameShape(QFrame.Shape.StyledPanel)
        red_team_layout = QVBoxLayout(red_team_group)
        
        red_team_header = QLabel("Red Team")
        red_team_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        red_team_header.setStyleSheet("font-weight: bold; font-size: 18px; color: red;")
        
        self.red_team_list = QListWidget()
        
        red_team_layout.addWidget(red_team_header)
        red_team_layout.addWidget(self.red_team_list)
        
        # Right side - Green team
        green_team_group = QFrame()
        green_team_group.setFrameShape(QFrame.Shape.StyledPanel)
        green_team_layout = QVBoxLayout(green_team_group)
        
        green_team_header = QLabel("Green Team")
        green_team_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        green_team_header.setStyleSheet("font-weight: bold; font-size: 18px; color: green;")
        
        self.green_team_list = QListWidget()
        
        green_team_layout.addWidget(green_team_header)
        green_team_layout.addWidget(self.green_team_list)
        
        # Bottom - Game log
        log_group = QFrame()
        log_group.setFrameShape(QFrame.Shape.StyledPanel)
        log_layout = QVBoxLayout(log_group)
        
        log_header = QLabel("Game Events")
        log_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        log_header.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        self.log_list = QListWidget()
        self.log_list.setMaximumHeight(150)
        
        log_layout.addWidget(log_header)
        log_layout.addWidget(self.log_list)
        
        # Add widgets to content layout
        content_layout.addWidget(red_team_group, 1)
        content_layout.addWidget(green_team_group, 1)
        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(content_widget, 1)
        main_layout.addWidget(log_group)
        
        # Set styles
        self.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:last-child {
                border-bottom: none;
            }
            QFrame {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        # Initialize audio player
        self.audio_player = AudioPlayer()
        self.audio_player.music_ended.connect(self.on_music_ended)
        
        # Connect viewmodel's play_sound signal
        self.viewmodel.play_sound = self.play_sound_effect
        
        # Start playing background music
        self.audio_player.play_random_track()
    
    def connect_signals(self):
        """Connect viewmodel signals to slots"""
        self.viewmodel.update_timer.connect(self.update_game_timer)
        self.viewmodel.update_scores.connect(self.update_scores)
        self.viewmodel.update_log.connect(self.update_log)
        self.viewmodel.game_ended.connect(self.game_ended)
        self.viewmodel.warning_time.connect(self.on_warning_time)
    
    @pyqtSlot(str)
    def update_game_timer(self, time_remaining_str):
        """Update the game timer display
        
        Args:
            time_remaining_str: Time remaining as a string (e.g., "05:30")
        """
        try:
            # Convert MM:SS string to total seconds
            if ':' in time_remaining_str:
                minutes, seconds = map(int, time_remaining_str.split(':'))
                time_remaining = minutes * 60 + seconds
            else:
                time_remaining = int(time_remaining_str)
                minutes = time_remaining // 60
                seconds = time_remaining % 60
            
            # Update the display
            self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
            
            # Change color and play sound when under 30 seconds
            if time_remaining <= 30:
                if time_remaining == 30:  # Play warning sound once when reaching 30 seconds
                    self.play_sound_effect('warning')
                    
                if time_remaining % 2 == 0:
                    self.timer_label.setStyleSheet("font-size: 24px; font-weight: bold; color: red;")
                    
                    # Play tick sound for last 5 seconds
                    if time_remaining <= 5:
                        self.play_sound_effect('tick')
            else:
                self.timer_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        except (ValueError, TypeError) as e:
            print(f"Error updating timer: {e}")
            # Fallback to just displaying the string as-is
            self.timer_label.setText(str(time_remaining_str))
    
    def on_volume_changed(self, value):
        """Handle volume slider changes"""
        if hasattr(self, 'audio_player'):
            self.audio_player.set_volume(value)
    
    def on_music_ended(self):
        """Handle when the current music track ends"""
        if hasattr(self, 'audio_player'):
            self.audio_player.play_random_track()
    
    def play_sound_effect(self, sound_type: str):
        """Play a sound effect based on type"""
        sound_effects = {
            'hit': 'assets/sounds/hit.wav',
            'base_hit': 'assets/sounds/base_hit.wav',
            'game_over': 'assets/sounds/game_over.wav',
            'warning': 'assets/sounds/warning.wav',
            'tick': 'assets/sounds/tick.wav'
        }
        
        if sound_type in sound_effects:
            self.audio_player.play_sound_effect(sound_effects[sound_type])
    
    @pyqtSlot(dict)
    def update_scores(self, scores):
        """Update the score displays"""
        self.red_score_label.setText(f"Red: {scores['red_score']}")
        self.green_score_label.setText(f"Green: {scores['green_score']}")
        
        # Update red team list
        self.red_team_list.clear()
        for player in scores.get('red_players', []):
            base_indicator = " (B)" if player.get('base_hit') else ""
            item = QListWidgetItem(f"{player['name']}: {player['score']}{base_indicator}")
            
            # Highlight the player if they recently scored
            if player.get('recently_scored'):
                item.setBackground(QColor(255, 230, 230))  # Light red
                player['recently_scored'] = False
                
            self.red_team_list.addItem(item)
        
        # Update green team list
        self.green_team_list.clear()
        for player in scores.get('green_players', []):
            base_indicator = " (B)" if player.get('base_hit') else ""
            item = QListWidgetItem(f"{player['name']}: {player['score']}{base_indicator}")
            
            # Highlight the player if they recently scored
            if player.get('recently_scored'):
                item.setBackground(QColor(230, 255, 230))  # Light green
                player['recently_scored'] = False
                
            self.green_team_list.addItem(item)
    
    @pyqtSlot(list)
    def update_log(self, log_entries):
        """Update the game log"""
        self.log_list.clear()
        for entry in log_entries:
            self.log_list.addItem(entry)
        
        # Auto-scroll to bottom
        self.log_list.scrollToBottom()
    
    @pyqtSlot()
    def on_warning_time(self):
        """Handle warning time (last 30 seconds)"""
        # Flash the timer
        if hasattr(self, 'flash_timer'):
            self.flash_timer.stop()
        
        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self.flash_timer_label)
        self.flash_timer.start(500)  # Flash every 500ms
        
        # Play warning sound through the sound system
        self.play_sound_effect('warning')
    
    def flash_timer_label(self):
        """Toggle timer flash effect"""
        if self.timer_label.styleSheet():
            self.timer_label.setStyleSheet("")
        else:
            self.timer_label.setStyleSheet("color: red; font-weight: bold; font-size: 24px;")
    
    @pyqtSlot()
    def game_ended(self):
        """Handle game end"""
        if hasattr(self, 'viewmodel') and hasattr(self.viewmodel, 'timer'):
            self.viewmodel.timer.stop()
            
        # Play game over sound
        if hasattr(self, 'audio_player'):
            self.audio_player.play_sound_effect("game_over")
            
        # Determine winner and show message
        winner = self.viewmodel.get_winning_team()
        if winner == 'Tie':
            message = "Game Over! It's a tie!"
        else:
            message = f"Game Over! {winner} team wins!"
            
        message += f"\n\nFinal Score - Red: {self.red_score} | Green: {self.green_score}"
        
        # Show game over dialog
        QMessageBox.information(self, "Game Over", message)
        
        # Clean up
        if hasattr(self, 'audio_player'):
            self.audio_player.stop()
            
        if hasattr(self, 'viewmodel') and hasattr(self.viewmodel, 'cleanup'):
            self.viewmodel.cleanup()
            
        self.close()
    
    def confirm_end_game(self):
        """Show confirmation dialog before ending the game"""
        reply = QMessageBox.question(
            self, 'End Game', 
            'Are you sure you want to end the game?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.viewmodel.end_game()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if hasattr(self, 'viewmodel') and hasattr(self.viewmodel, 'cleanup'):
            self.viewmodel.cleanup()
        event.accept()
