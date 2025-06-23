from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QGroupBox, QFormLayout,
    QTabWidget, QListWidget, QListWidgetItem, QFrame, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QIntValidator
from viewmodels.player_entry_viewmodel import PlayerEntryViewModel
from models.player_model import Player

class PlayerEntryScreen(QMainWindow):
    def __init__(self, viewmodel: PlayerEntryViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the player entry screen UI"""
        self.setWindowTitle("Laser Tag - Player Entry")
        self.setMinimumSize(800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Left side - Player entry form
        form_group = QGroupBox("Add Player")
        form_layout = QFormLayout()
        
        # Player ID input
        self.player_id_edit = QLineEdit()
        self.player_id_edit.setPlaceholderText("Enter player ID")
        self.player_id_edit.setValidator(QIntValidator(1, 9999))  # Only allow numbers
        form_layout.addRow("Player ID:", self.player_id_edit)
        
        # Code name input
        self.code_name_edit = QLineEdit()
        self.code_name_edit.setPlaceholderText("Enter code name")
        form_layout.addRow("Code Name:", self.code_name_edit)
        
        # Equipment ID input
        self.equipment_id_edit = QLineEdit()
        self.equipment_id_edit.setPlaceholderText("Enter equipment ID")
        self.equipment_id_edit.setValidator(QIntValidator(1, 9999))
        form_layout.addRow("Equipment ID:", self.equipment_id_edit)
        
        # Team selection
        self.team_combo = QComboBox()
        self.team_combo.addItems(["Red", "Green"])
        form_layout.addRow("Team:", self.team_combo)
        
        # Add player button
        self.add_button = QPushButton("Add Player")
        form_layout.addRow(self.add_button)
        
        # Clear all button
        self.clear_button = QPushButton("Clear All Players (F12)")
        form_layout.addRow(self.clear_button)
        
        # Start game button
        self.start_button = QPushButton("Start Game (F5)")
        form_layout.addRow(self.start_button)
        
        form_group.setLayout(form_layout)
        
        # Right side - Team lists
        teams_group = QGroupBox("Teams")
        teams_layout = QHBoxLayout()
        
        # Red team list
        self.red_team_list = QListWidget()
        self.red_team_list.setMinimumWidth(250)
        red_team_group = QGroupBox("Red Team (0/15)")
        red_layout = QVBoxLayout()
        red_layout.addWidget(self.red_team_list)
        red_team_group.setLayout(red_layout)
        
        # Green team list
        self.green_team_list = QListWidget()
        self.green_team_list.setMinimumWidth(250)
        green_team_group = QGroupBox("Green Team (0/15)")
        green_layout = QVBoxLayout()
        green_layout.addWidget(self.green_team_list)
        green_team_group.setLayout(green_layout)
        
        teams_layout.addWidget(red_team_group)
        teams_layout.addWidget(green_team_group)
        teams_group.setLayout(teams_layout)
        
        # Add widgets to main layout
        main_layout.addWidget(form_group, 1)
        main_layout.addWidget(teams_group, 2)
        
        # Set up keyboard shortcuts
        self.start_button.setShortcut("F5")
        self.clear_button.setShortcut("F12")
    
    def connect_signals(self):
        """Connect UI signals to viewmodel and slots"""
        self.add_button.clicked.connect(self.add_player)
        self.clear_button.clicked.connect(self.clear_players)
        self.start_button.clicked.connect(self.start_game)
        self.viewmodel.player_added.connect(self.on_player_added)
        self.viewmodel.error_occurred.connect(self.show_error)
        self.viewmodel.start_game.connect(self.on_start_game)
    
    def add_player(self):
        """Handle the add player button click"""
        try:
            player_id = int(self.player_id_edit.text().strip())
            code_name = self.code_name_edit.text().strip()
            equipment_id = int(self.equipment_id_edit.text().strip())
            team = self.team_combo.currentText()
            
            if not code_name:
                QMessageBox.warning(self, "Error", "Please enter a code name")
                return
            
            success, message = self.viewmodel.add_player(player_id, code_name, team, equipment_id)
            if success:
                self.clear_form()
                self.update_team_lists()
            QMessageBox.information(self, "Success" if success else "Error", message)
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers for ID and Equipment ID")
    
    def clear_form(self):
        """Clear the input form"""
        self.player_id_edit.clear()
        self.code_name_edit.clear()
        self.equipment_id_edit.clear()
        self.player_id_edit.setFocus()
    
    def clear_players(self):
        """Clear all players from both teams"""
        reply = QMessageBox.question(
            self, 'Clear All Players', 
            'Are you sure you want to clear all players?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.viewmodel.clear_all_players()
            self.update_team_lists()
    
    def start_game(self):
        """Handle start game button click"""
        success, message = self.viewmodel.start_game_clicked()
        if not success:
            QMessageBox.warning(self, "Cannot Start Game", message)
    
    @pyqtSlot(Player, str)
    def on_player_added(self, player, team):
        """Handle when a new player is added"""
        self.update_team_lists()
    
    def update_team_lists(self):
        """Update the team list widgets"""
        # Update red team list
        self.red_team_list.clear()
        for player in self.viewmodel.red_team:
            item = QListWidgetItem(f"{player.code_name} (ID: {player.player_id}, Equip: {player.equipment_id})")
            self.red_team_list.addItem(item)
        
        # Update green team list
        self.green_team_list.clear()
        for player in self.viewmodel.green_team:
            item = QListWidgetItem(f"{player.code_name} (ID: {player.player_id}, Equip: {player.equipment_id})")
            self.green_team_list.addItem(item)
        
        # Update team headers with counts
        self.red_team_list.parent().setTitle(f"Red Team ({len(self.viewmodel.red_team)}/15)")
        self.green_team_list.parent().setTitle(f"Green Team ({len(self.viewmodel.green_team)}/15)")
    
    def show_error(self, message):
        """Show an error message"""
        QMessageBox.critical(self, "Error", message)
    
    def on_start_game(self, red_team, green_team):
        """Handle game start signal"""
        from src.views.play_action_screen import PlayActionScreen
        from src.viewmodels.play_action_viewmodel import PlayActionViewModel
        
        # Create and show the play action screen
        play_action_vm = PlayActionViewModel(red_team, green_team)
        self.play_action_screen = PlayActionScreen(play_action_vm)
        self.play_action_screen.show()
        
        # Hide the player entry screen
        self.hide()
