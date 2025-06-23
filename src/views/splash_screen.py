from PyQt6.QtWidgets import QSplashScreen, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont

# Add the src directory to the Python path
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

class SplashScreen(QSplashScreen):
    def __init__(self, viewmodel):
        # Create a simple splash screen with a white background and text
        pixmap = QPixmap(400, 300)
        pixmap.fill(Qt.GlobalColor.white)
        super().__init__(pixmap)
        
        self.viewmodel = viewmodel
        self.setWindowTitle("Laser Tag System")
        
        # Set up the splash screen text
        self.setFont(QFont("Arial", 16))
        self.showMessage("Loading Laser Tag System...", 
                        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 
                        Qt.GlobalColor.black)
        
        # Close splash after 3 seconds
        QTimer.singleShot(3000, self.close_splash)
    
    def close_splash(self):
        self.close()
        self.viewmodel.splash_complete()
