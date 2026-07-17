import sys
import ctypes
import os
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QPixmap
from PySide6.QtCore import QRect, Qt
from main_window import MainWindow

def main():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:
        pass
        
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    os.makedirs("screenshots", exist_ok=True)
    
    # --- Step 1: Main Window Configuration ---
    main_win = MainWindow()
    main_win.start_slide_input.setText("2")
    main_win.end_slide_input.setText("9")
    main_win.delay_input.setText("0.5")
    main_win.folder_label.setText("Output Folder: C:\\Users\\Admin\\Downloads\\autotest")
    main_win.region_label.setText("✔ Region Saved")
    main_win.region_label.setStyleSheet("color: green; font-weight: bold;")
    
    main_win.resize(450, 250)
    # Grab without showing
    pixmap1 = main_win.grab()
    pixmap1.save("screenshots/step1.png")
    
    # --- Step 4: Progress Simulation ---
    main_win.progress_bar.setValue(50)
    main_win.status_label.setText("Capturing slide 5 / 9")
    main_win.start_btn.setEnabled(False)
    main_win.pause_btn.setEnabled(True)
    main_win.stop_btn.setEnabled(True)
    
    pixmap4 = main_win.grab()
    pixmap4.save("screenshots/step4.png")
    
    # --- Step 3: Overlay Simulation ---
    # Create a dummy pixmap simulating a screen
    pixmap3 = QPixmap(800, 600)
    pixmap3.fill(QColor(255, 255, 255)) # White background
    
    painter = QPainter(pixmap3)
    # Dark semi-transparent overlay
    painter.fillRect(pixmap3.rect(), QColor(0, 0, 0, 100))
    
    # The cleared selected region
    rect = QRect(100, 100, 600, 400)
    painter.setCompositionMode(QPainter.CompositionMode_Clear)
    painter.fillRect(rect, Qt.transparent)
    
    # Red border
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
    painter.setPen(QPen(QColor(255, 0, 0), 2))
    painter.drawRect(rect)
    painter.end()
    
    pixmap3.save("screenshots/step3.png")

if __name__ == "__main__":
    main()
