import os
import mss
from logger import app_logger

class ScreenCapturer:
    def __init__(self):
        self.sct = mss.mss()

    def capture(self, region: dict, output_path: str) -> bool:
        """
        Captures a region of the screen and saves it.
        region must have 'left', 'top', 'width', 'height'.
        Returns True if successful, False otherwise.
        """
        try:
            # mss uses 'left', 'top', 'width', 'height' as keys
            monitor = {
                "left": region["left"],
                "top": region["top"],
                "width": region["width"],
                "height": region["height"]
            }
            
            output = self.sct.grab(monitor)
            mss.tools.to_png(output.rgb, output.size, output=output_path)
            app_logger.info(f"Captured screen to {output_path}")
            return True
            
        except Exception as e:
            app_logger.error(f"Failed to capture screen: {e}")
            return False
