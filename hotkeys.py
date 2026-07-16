import keyboard
from PySide6.QtCore import QObject, Signal

class HotkeyManager(QObject):
    start_requested = Signal()
    pause_resume_requested = Signal()
    stop_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.is_active = False

    def setup(self):
        try:
            keyboard.add_hotkey('F8', self._on_start)
            keyboard.add_hotkey('F9', self._on_pause_resume)
            keyboard.add_hotkey('F10', self._on_stop)
            self.is_active = True
        except Exception as e:
            # keyboard requires root/admin on some systems depending on how it hooks
            from logger import app_logger
            app_logger.error(f"Failed to register hotkeys: {e}")
            self.is_active = False

    def cleanup(self):
        if self.is_active:
            keyboard.unhook_all()
            self.is_active = False

    def _on_start(self):
        self.start_requested.emit()

    def _on_pause_resume(self):
        self.pause_resume_requested.emit()

    def _on_stop(self):
        self.stop_requested.emit()
