import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Add the src directory to the Python path
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from src.views.splash_screen import SplashScreen
from src.viewmodels.splash_screen_viewmodel import SplashScreenViewModel

def main():
    app = QApplication(sys.argv)
    
    # Create and show splash screen
    splash_vm = SplashScreenViewModel()
    splash = SplashScreen(splash_vm)
    splash.show()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
