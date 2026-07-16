import sys
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # PROCESS_PER_MONITOR_DPI_AWARE
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from logger import app_logger

def main():
    app_logger.info("Application Start")
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    exit_code = app.exec()
    app_logger.info("Application Exit")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
