import sys
import time
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, 
                             QLabel, QSystemTrayIcon, QMenu, QAction, QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from plyer import notification
from playsound import playsound

class RobloxMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initTray()
        self.initSelenium()
        
        self.urls = {}

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_statuses)
        self.timer.start(10000)  # Check every 10 seconds

    def initUI(self):
        self.setWindowTitle('Roblox Item Monitor')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window frame for rounded corners

        # Define the stylesheet for the dark theme and rounded corners
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
                color: #FFFFFF;
                border-radius: 10px;
            }
            QTextEdit {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #FFFFFF;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4E4E4E;
                color: #FFFFFF;
                border: 1px solid #FFFFFF;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5E5E5E;
            }
        """)

        widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel('Roblox item Notifier By Marcelo Enter Roblox item URLs (one per line):', self)
        layout.addWidget(self.label)

        self.textEdit = QTextEdit(self)
        layout.addWidget(self.textEdit)

        button_layout = QHBoxLayout()

        self.startButton = QPushButton('Start Monitoring', self)
        self.startButton.clicked.connect(self.start_monitoring)
        button_layout.addWidget(self.startButton)

        self.testButton = QPushButton('Test Notification', self)
        self.testButton.clicked.connect(self.send_test_notification)
        button_layout.addWidget(self.testButton)

        self.trayButton = QPushButton('Minimize to Tray', self)
        self.trayButton.clicked.connect(self.minimize_to_tray)
        button_layout.addWidget(self.trayButton)

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(QApplication.quit)
        button_layout.addWidget(self.exitButton)

        layout.addLayout(button_layout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def initTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.png'))

        tray_menu = QMenu()

        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def initSelenium(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    def start_monitoring(self):
        url_text = self.textEdit.toPlainText().strip()
        if url_text:
            self.urls = {url: None for url in url_text.split('\n')}
            self.check_statuses()

    def check_statuses(self):
        for url in self.urls.keys():
            threading.Thread(target=self.check_status, args=(url,)).start()

    def check_status(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
            buy_button = self.driver.find_elements(By.CLASS_NAME, "shopping-cart-buy-button")
            buy_button_alt = self.driver.find_elements(By.CLASS_NAME, "PurchaseButton")
            item_name = url.split('/')[-1]

            on_sale = bool(buy_button or buy_button_alt)
            previous_status = self.urls[url]
            self.urls[url] = on_sale

            if previous_status is not None and previous_status != on_sale:
                status = "on sale" if on_sale else "off sale"
                notification.notify(
                    title="Roblox Item Status",
                    message=f"{item_name} is now {status}",
                    app_icon="icon.ico",
                    timeout=5
                )
                playsound('notif.mp3')

        except Exception as e:
            print(f"Error checking {url}: {e}")

    def send_test_notification(self):
        notification.notify(
            title="Test Notification",
            message="This is a test notification.",
            app_icon="icon.ico",
            timeout=5
        )
        playsound('notif.mp3')

    def minimize_to_tray(self):
        self.hide()
        self.tray_icon.showMessage("Roblox Item Monitor", "The application is running in the system tray.", QSystemTrayIcon.Information, 2000)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Roblox Item Monitor", "The application is still running in the system tray.", QSystemTrayIcon.Information, 2000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = RobloxMonitor()
    window.show()
    
    sys.exit(app.exec_())
