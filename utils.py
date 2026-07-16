import win32gui
import win32con
import time
from logger import app_logger

def bring_window_to_foreground(window_title_substring: str = "Google Slides") -> bool:
    """
    Attempts to find a window with the given substring in its title and bring it to the foreground.
    Returns True if successful, False otherwise.
    """
    found_hwnd = []
    
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if window_title_substring.lower() in title.lower():
                found_hwnd.append(hwnd)
                
    win32gui.EnumWindows(enum_windows_proc, None)
    
    if not found_hwnd:
        # Fallback: try finding common browsers
        fallback_substrings = ["Google Chrome", "Microsoft Edge", "Firefox", "Brave"]
        for fallback in fallback_substrings:
            def enum_fallback_proc(hwnd, lParam):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if fallback.lower() in title.lower():
                        found_hwnd.append(hwnd)
            win32gui.EnumWindows(enum_fallback_proc, None)
            if found_hwnd:
                app_logger.info(f"Fell back to window containing '{fallback}'")
                break
                
    if not found_hwnd:
        app_logger.warning(f"Could not find window containing '{window_title_substring}' or any common browser")
        return False
        
    hwnd = found_hwnd[0] # Just take the first one
    
    try:
        # If minimized, restore it
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            
        # Bring to foreground
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.5) # Wait a bit for the window to actually come to foreground
        return True
    except Exception as e:
        app_logger.error(f"Error bringing window {hwnd} to foreground: {e}")
        return False
