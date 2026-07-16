import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QProgressBar, 
    QFileDialog, QMessageBox, QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt, QTimer
from config import ConfigManager
from logger import app_logger
from overlay import OverlayWindow
from automation import AutomationThread
from hotkeys import HotkeyManager
from capture import ScreenCapturer
import time
import os
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Slide Capture")
        self.setMinimumWidth(500)
        
        self.config_manager = ConfigManager()
        self.automation_thread = None
        
        self.init_ui()
        self.load_config()
        self.setup_hotkeys()
        
        self.start_time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Settings Group ---
        settings_group = QGroupBox("Configuration")
        form_layout = QFormLayout(settings_group)
        form_layout.setSpacing(10)
        
        # Start Slide
        self.start_slide_input = QLineEdit()
        self.start_slide_input.setPlaceholderText("e.g. 1")
        form_layout.addRow("Start Slide:", self.start_slide_input)
        
        # End Slide
        self.end_slide_input = QLineEdit()
        self.end_slide_input.setPlaceholderText("e.g. 50")
        form_layout.addRow("End Slide:", self.end_slide_input)
        
        # Delay
        self.delay_input = QLineEdit()
        self.delay_input.setText("0.5")
        form_layout.addRow("Delay (seconds):", self.delay_input)
        
        # Output Folder
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Not selected")
        self.folder_label.setStyleSheet("color: gray;")
        self.folder_btn = QPushButton("Choose Folder")
        self.folder_btn.clicked.connect(self.choose_folder)
        folder_layout.addWidget(self.folder_label, 1)
        folder_layout.addWidget(self.folder_btn)
        form_layout.addRow("Output Folder:", folder_layout)
        
        # Capture Region
        region_layout = QHBoxLayout()
        self.region_label = QLabel("❌ Region Not Saved")
        self.region_label.setStyleSheet("color: red; font-weight: bold;")
        self.region_btn = QPushButton("Change Capture Region")
        self.region_btn.clicked.connect(self.change_capture_region)
        region_layout.addWidget(self.region_label, 1)
        region_layout.addWidget(self.region_btn)
        form_layout.addRow("Capture Region:", region_layout)
        
        main_layout.addWidget(settings_group)
        
        # --- Progress Group ---
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.status_label)
        
        self.time_label = QLabel("Elapsed: 00:00:00 | Remaining: --:--:--")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("color: gray;")
        progress_layout.addWidget(self.time_label)
        
        main_layout.addWidget(progress_group)
        
        # --- Controls Layout ---
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        self.start_btn = QPushButton("Start (F8)")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("font-weight: bold; background-color: #4CAF50; color: white;")
        self.start_btn.clicked.connect(self.start_automation)
        
        self.pause_btn = QPushButton("Pause (F9)")
        self.pause_btn.setMinimumHeight(40)
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.pause_resume_automation)
        
        self.stop_btn = QPushButton("Stop (F10)")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("font-weight: bold; background-color: #F44336; color: white;")
        self.stop_btn.clicked.connect(self.stop_automation)
        
        self.test_btn = QPushButton("Test Capture")
        self.test_btn.setMinimumHeight(40)
        self.test_btn.clicked.connect(self.test_capture)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.pause_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.test_btn)
        
        main_layout.addLayout(controls_layout)
        
    def setup_hotkeys(self):
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.start_requested.connect(self.start_automation)
        self.hotkey_manager.pause_resume_requested.connect(self.pause_resume_automation)
        self.hotkey_manager.stop_requested.connect(self.stop_automation)
        self.hotkey_manager.setup()
        
    def load_config(self):
        folder = self.config_manager.get_output_folder()
        if folder:
            self.folder_label.setText(folder)
            self.folder_label.setStyleSheet("color: black;")
            
        region = self.config_manager.get_capture_region()
        if region:
            self.update_region_label(True)
            
    def update_region_label(self, saved: bool):
        if saved:
            self.region_label.setText("✔ Region Saved")
            self.region_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.region_label.setText("❌ Region Not Saved")
            self.region_label.setStyleSheet("color: red; font-weight: bold;")

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            # Save properly in config
            folder = os.path.normpath(folder)
            self.config_manager.set_output_folder(folder)
            self.folder_label.setText(folder)
            self.folder_label.setStyleSheet("color: black;")

    def change_capture_region(self):
        self.overlay = OverlayWindow()
        self.overlay.region_selected.connect(self.on_region_selected)
        self.overlay.show()
        
    def on_region_selected(self, left: int, top: int, width: int, height: int):
        self.config_manager.set_capture_region(left, top, width, height)
        self.update_region_label(True)
        
    def test_capture(self):
        region = self.config_manager.get_capture_region()
        if not region:
            QMessageBox.warning(self, "Error", "Capture region not selected!")
            return
            
        capturer = ScreenCapturer()
        test_file = os.path.join(os.getcwd(), "test.png")
        success = capturer.capture(region, test_file)
        
        if success:
            app_logger.info("Test capture successful.")
            if os.name == 'nt':
                # Open with default image viewer on Windows
                os.startfile(test_file)
        else:
            QMessageBox.warning(self, "Error", "Failed to take test capture.")

    def start_automation(self):
        if self.automation_thread and self.automation_thread.isRunning():
            return
            
        # Validate inputs
        if not self.config_manager.get_capture_region():
            QMessageBox.warning(self, "Error", "Capture region not selected!")
            return
            
        if not self.config_manager.get_output_folder():
            QMessageBox.warning(self, "Error", "Output folder not selected!")
            return
            
        try:
            start_slide = int(self.start_slide_input.text())
            end_slide = int(self.end_slide_input.text())
            delay = float(self.delay_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid numeric input for slides or delay.")
            return
            
        if start_slide > end_slide:
            QMessageBox.warning(self, "Error", "Start slide must be less than or equal to End slide.")
            return

        # Disable UI
        self.set_ui_enabled(False)
        self.status_label.setText("Starting automation...")
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(end_slide - start_slide + 1)
        
        self.start_time = time.time()
        self.timer.start(1000)
        
        self.automation_thread = AutomationThread(
            start_slide, end_slide, delay,
            self.config_manager.get_output_folder(),
            self.config_manager.get_capture_region()
        )
        self.automation_thread.progress_update.connect(self.on_progress)
        self.automation_thread.status_update.connect(self.on_status)
        self.automation_thread.error.connect(self.on_error)
        self.automation_thread.finished.connect(self.on_finished)
        self.automation_thread.start()
        
    def on_progress(self, current, total):
        self.progress_bar.setValue(current)
        
    def on_status(self, text):
        self.status_label.setText(text)
        
    def on_error(self, text):
        QMessageBox.warning(self, "Error", text)
        
    def on_finished(self):
        self.set_ui_enabled(True)
        self.timer.stop()
        
    def update_time(self):
        if not self.automation_thread or not self.automation_thread.isRunning():
            return
            
        elapsed = int(time.time() - self.start_time)
        
        current_val = self.progress_bar.value()
        total_val = self.progress_bar.maximum()
        
        if current_val > 0:
            time_per_slide = elapsed / current_val
            remaining = int(time_per_slide * (total_val - current_val))
        else:
            remaining = 0
            
        def format_time(seconds):
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            return f"{h:02d}:{m:02d}:{s:02d}"
            
        self.time_label.setText(f"Elapsed: {format_time(elapsed)} | Remaining: {format_time(remaining) if current_val > 0 else '--:--:--'}")
        
    def pause_resume_automation(self):
        if self.automation_thread and self.automation_thread.isRunning():
            if self.automation_thread._is_paused:
                self.automation_thread.resume()
                self.pause_btn.setText("Pause (F9)")
                self.status_label.setText("Resumed...")
            else:
                self.automation_thread.pause()
                self.pause_btn.setText("Resume (F9)")
                self.status_label.setText("Paused")
        
    def stop_automation(self):
        if self.automation_thread and self.automation_thread.isRunning():
            self.automation_thread.stop()
            self.status_label.setText("Stopping...")
            self.stop_btn.setEnabled(False)

    def set_ui_enabled(self, enabled: bool):
        self.start_slide_input.setEnabled(enabled)
        self.end_slide_input.setEnabled(enabled)
        self.delay_input.setEnabled(enabled)
        self.folder_btn.setEnabled(enabled)
        self.region_btn.setEnabled(enabled)
        self.start_btn.setEnabled(enabled)
        self.test_btn.setEnabled(enabled)
        
        self.pause_btn.setEnabled(not enabled)
        self.stop_btn.setEnabled(not enabled)

    def closeEvent(self, event):
        if self.automation_thread and self.automation_thread.isRunning():
            self.automation_thread.stop()
            self.automation_thread.wait()
            
        if self.hotkey_manager:
            self.hotkey_manager.cleanup()
            
        event.accept()
