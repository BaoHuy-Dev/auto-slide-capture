# Auto Slide Capture

A Windows desktop application that automates taking screenshots of Google Slides presentations.

## Features
- Automatically navigate through a Google Slides presentation
- Capture a user-defined specific region of the screen
- Save each slide as a lossless PNG with the slide number as the filename
- Set a custom delay between slide transitions
- Hotkey support to Start (F8), Pause/Resume (F9), and Stop (F10)

## Installation

### Prerequisites
- Python 3.12+
- Windows 10 or 11

### Setup
1. Clone this repository or download the source code.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Run the application from source:
   ```bash
   python app.py
   ```

## Usage

1. Open your Google Slides presentation in your browser. Ensure the browser window title contains "Google Slides".
2. Open the **Auto Slide Capture** application.
3. Click **Change Capture Region**. A full-screen overlay will appear. Click and drag to draw a rectangle over the slide area, then press `Enter` to confirm.
4. Click **Choose Folder** to select where the screenshots will be saved.
5. Enter the **Start Slide** and **End Slide** numbers.
6. (Optional) Adjust the **Delay** (in seconds) between slides.
7. Click **Start** (or press F8).
8. The application will automatically bring the Google Slides window to the foreground, navigate to the starting slide, and begin capturing. Do not interact with your mouse or keyboard while capturing is in progress.

### Hotkeys
- **F8**: Start capture
- **F9**: Pause / Resume capture
- **F10**: Stop capture immediately

## Troubleshooting
- **"Could not find Google Slides window"**: The application looks for a window containing "Google Slides" in its title. Ensure the presentation tab is active and visible.
- **Hotkeys not working**: The `keyboard` module may require administrator privileges depending on your Windows configuration. If hotkeys fail to register, try running the application as Administrator.
- **Screenshots are out of sync**: If your internet connection or browser is slow, increase the **Delay** setting.

## Building the Executable

To package the application into a standalone Windows executable (`.exe`), you can use `PyInstaller`.

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the application:
   ```bash
   pyinstaller --noconsole --onefile --name "Auto Slide Capture" app.py
   ```
3. The executable will be generated in the `dist/` directory. You can distribute this `.exe` file; it doesn't require Python to be installed on the target machine.
