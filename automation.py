import time
import os
import pyautogui
from PySide6.QtCore import QThread, Signal
from capture import ScreenCapturer
from utils import bring_window_to_foreground
from logger import app_logger

class AutomationThread(QThread):
    # Signals to update UI
    progress_update = Signal(int, int) # current_slide, total_slides
    status_update = Signal(str)
    finished = Signal()
    error = Signal(str)
    
    def __init__(self, start_slide: int, end_slide: int, delay: float, 
                 output_folder: str, capture_region: dict):
        super().__init__()
        self.start_slide = start_slide
        self.end_slide = end_slide
        self.delay = delay
        self.output_folder = output_folder
        self.capture_region = capture_region
        
        self.capturer = None
        self._is_running = True
        self._is_paused = False
        
    def run(self):
        self.capturer = ScreenCapturer()
        app_logger.info(f"Capture Started: Slides {self.start_slide} to {self.end_slide}")
        total_slides = self.end_slide - self.start_slide + 1
        slides_done = 0
        
        self.status_update.emit("Focusing Google Slides...")
        if not bring_window_to_foreground("Google Slides"):
            self.error.emit("Could not find Google Slides window.")
            app_logger.error("Capture Failed: Google Slides not focused")
            return
            
        time.sleep(1) # Extra wait for UI to settle
        
        # 1. Quay về slide đầu tiên bằng cách bấm PageUp nhiều lần
        self.status_update.emit("Tìm slide bắt đầu...")
        # Bấm PageUp số lần bằng end_slide để đảm bảo chắc chắn về đến slide 1
        pyautogui.press('pageup', presses=self.end_slide + 10, interval=0.02)
        time.sleep(1.0)
        
        # 2. Bấm PageDown để đi đến đúng start_slide
        if self.start_slide > 1:
            pyautogui.press('pagedown', presses=(self.start_slide - 1), interval=0.1)
            time.sleep(1.0)
            
        self.status_update.emit("Bắt đầu chụp...")
        time.sleep(self.delay)

        
        current = self.start_slide
        
        while current <= self.end_slide and self._is_running:
            # Handle pause
            while self._is_paused and self._is_running:
                time.sleep(0.1)
                
            if not self._is_running:
                break
                
            self.status_update.emit(f"Capturing slide {current} / {self.end_slide}")
            app_logger.info(f"Current Slide: {current}")
            
            output_file = os.path.join(self.output_folder, f"{current}.png")
            
            # Ensure window is still in foreground before capture just in case?
            # We assume user hasn't messed with it.
            
            success = self.capturer.capture(self.capture_region, output_file)
            
            if not success:
                self.error.emit(f"Failed to capture slide {current}.")
                app_logger.error(f"Capture Failed: slide {current}")
                # We could break or continue. Let's break.
                break
                
            app_logger.info(f"Capture Success: slide {current}")
            
            slides_done += 1
            self.progress_update.emit(slides_done, total_slides)
            
            current += 1
            if current <= self.end_slide:
                pyautogui.press('pagedown')
                time.sleep(self.delay)
                
        if self._is_running:
            self.status_update.emit("Finished successfully")
            app_logger.info("Capture Finished Successfully")
        else:
            self.status_update.emit("Stopped by user")
            app_logger.info("Capture Stopped by User")
            
        self.finished.emit()
        
    def stop(self):
        self._is_running = False
        
    def pause(self):
        self._is_paused = True
        
    def resume(self):
        self._is_paused = False
