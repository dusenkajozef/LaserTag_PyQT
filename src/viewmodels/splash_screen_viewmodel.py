from PyQt6.QtCore import QObject, pyqtSignal

# Add the src directory to the Python path
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from src.views.player_entry_screen import PlayerEntryScreen
from src.viewmodels.player_entry_viewmodel import PlayerEntryViewModel

class SplashScreenViewModel(QObject):
    def __init__(self):
        super().__init__()
        self.player_entry_vm = None
        self.player_entry_screen = None
    
    def splash_complete(self):
        # This method is called when the splash screen is done
        # Initialize and show the player entry screen
        self.player_entry_vm = PlayerEntryViewModel()
        self.player_entry_screen = PlayerEntryScreen(self.player_entry_vm)
        self.player_entry_screen.show()
