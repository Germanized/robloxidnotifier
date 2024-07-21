# Roblox Item Monitor

This project is a Python-based GUI application that monitors the sale status of specified Roblox items. It checks the status of the items every 10 seconds and sends a Windows notification when any item's sale status changes (e.g., goes on sale or off sale). The application uses a modern, dark-themed PyQt5 interface with rounded edges and can be minimized to the system tray to continue monitoring in the background.

## Purpose

The purpose of this application is to provide a convenient way for Roblox users to track the sale status of items they are interested in. Users can input the URLs of the items they want to monitor, and the application will periodically check the status of these items, sending notifications when their status changes.

## How to Use

### Installation

1. **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd roblox-item-monitor
    ```

2. **Install the Required Packages**:
    Create a file named `requirements.txt` with the following content:
    ```plaintext
    PyQt5
    selenium
    webdriver-manager
    plyer
    playsound==1.2.2
    ```

    Then, install the dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure Required Files Are Present**:
    - `notif.mp3`: A sound file that will be played when a notification is sent.
    - `icon.png`: An icon file for the application window.
    - `icon.ico`: An icon file for the system tray.

### Running the Application

1. **Navigate to the Directory**:
    ```bash
    cd path/to/roblox-item-monitor
    ```

2. **Run the Application**:
    ```bash
    python roblox_monitor.py
    ```

### Using the Application

1. **Enter Roblox Item URLs**:
    - Enter the URLs of the Roblox items you want to monitor in the text box, one URL per line.

2. **Start Monitoring**:
    - Click the "Start Monitoring" button to begin monitoring the entered URLs.

3. **Test Notification**:
    - Click the "Test Notification" button to send a test notification and ensure the notification system is working.

4. **Minimize to System Tray**:
    - Click the "Minimize to Tray" button to hide the application window and continue monitoring in the background. You can restore the application by clicking the system tray icon.

5. **Exit**:
    - Click the "Exit" button to close the application.

## Features

- **Modern Dark-Themed GUI**: The application features a sleek, dark-themed interface with rounded edges.
- **Real-Time Monitoring**: The application checks the status of Roblox items every 10 seconds.
- **Windows Notifications**: Users receive notifications when an item's sale status changes.
- **System Tray Integration**: The application can be minimized to the system tray and continue monitoring in the background.
- **Sound Alerts**: Plays a sound notification (`notif.mp3`) when a status change is detected.

## Credits

This application was created by Marcelo.

---

Feel free to reach out if you have any questions or need further assistance. Enjoy using the Roblox Item Monitor!
