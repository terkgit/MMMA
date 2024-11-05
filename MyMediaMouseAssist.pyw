# MyMediaMouseAssist v1.1.0
#      _____     ____
#    /      \  |  o | 
#   | Terkel |/ ___\| 
#   |_________/     
#   |_|_| |_|_|

import pystray
from PIL import Image, ImageDraw, ImageFont
from threading import Thread, Event, Timer
import time
from pynput import mouse
import ctypes

# Event to signal termination
terminate_event = Event()

class TrayStateMachine:
    def __init__(self):
        # Initial state
        self.state = "active"
        self.press_time = None  # To track the press time for middle click
        # Timer to handle idle timeout for media state
        self.idle_timer = None
        # Timer for triggering the volume bar in pre_media state
        self.pre_media_timer = None
        # Create the tray icon
        self.icon = pystray.Icon("Tray Application")
        self.icon.icon = self.create_image("M", "#4CAF50")  # Initial state set to active with "M"
        self.icon.menu = pystray.Menu(
            pystray.MenuItem('Toggle State', self.toggle_state),
            pystray.MenuItem('Exit', self.exit_app)
        )
        # Set the global mouse listener
        self.listener = mouse.Listener(on_click=self.on_clicked, on_scroll=self.on_scroll)
        self.listener.start()

    def create_image(self, text, color):
        # Create an image with the specified text and background color
        image = Image.new('RGB', (64, 64), color)
        dc = ImageDraw.Draw(image)
        font_size = 32
        try:
            font = ImageFont.truetype("arial", font_size)
        except IOError:
            font = ImageFont.load_default()
        text_bbox = dc.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        position = ((64 - text_width) // 2, (64 - text_height) // 2)
        dc.text(position, text, fill="black", font=font)
        return image

    def set_state(self, state):
        self.state = state
        if state == "active":
            self.icon.icon = self.create_image("M", "#4CAF50")
            self.cancel_idle_timer()
            self.cancel_pre_media_timer()
        elif state == "inactive":
            self.icon.icon = self.create_image("M", "#F44336")
        elif state == "pre_media":
            self.icon.icon = self.create_image("M", "#4CAF50")  # Same color as idle
            self.start_pre_media_timer()
        elif state == "media":
            self.icon.icon = self.create_image("M", "#2196F3")
            self.start_idle_timer()
        self.icon.visible = True

    def toggle_state(self, icon, item):
        if self.state == "active":
            self.set_state("inactive")
        else:
            self.set_state("active")

    def media_state(self):
        if self.state == "pre_media":  # Transition from pre_media to media
            self.set_state("media")

    def exit_app(self, icon, item):
        self.icon.stop()
        terminate_event.set()  # Signal to terminate

    def on_clicked(self, x, y, button, pressed):
        if button == mouse.Button.middle:
            if pressed:
                self.press_time = time.time()
                self.set_state("pre_media")  # Transition to pre_media on middle press
            else:
                if self.state == "pre_media":
                    hold_time = time.time() - self.press_time
                    if hold_time >= 0.5:  # If held for 0.5 seconds or more
                        self.media_state()
                    else:
                        self.set_state("active")  # Return to active if held for less than 0.5 seconds
                self.press_time = None

    def on_scroll(self, x, y, dx, dy):
        # Only control volume in media state
        if self.state == "media":
            if dy > 0:
                self.change_volume(0xAF) # Virtual-Key code for Volume Up
            elif dy < 0:
                self.change_volume(0xAE) # Virtual-Key code for Volume Down

    def change_volume(self, key_code):
        # Simulate key press
        ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
        # Simulate key release
        ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)
        self.start_idle_timer()

    def trigger_volume_bar(self):
        # Simulate volume up and then volume down to trigger the system volume bar
        self.change_volume(0xAF)  # Volume Up
        self.change_volume(0xAE)  # Volume Down

    def start_idle_timer(self):
        self.cancel_idle_timer()
        self.idle_timer = Timer(2.0, self.return_to_active)  # Updated timeout to 2 seconds
        self.idle_timer.start()

    def cancel_idle_timer(self):
        if self.idle_timer:
            self.idle_timer.cancel()
            self.idle_timer = None

    def start_pre_media_timer(self):
        self.cancel_pre_media_timer()
        self.pre_media_timer = Timer(0.5, self.trigger_volume_bar)
        self.pre_media_timer.start()

    def cancel_pre_media_timer(self):
        if self.pre_media_timer:
            self.pre_media_timer.cancel()
            self.pre_media_timer = None

    def return_to_active(self):
        if self.state == "media":
            self.set_state("active")

    def run_tray(self):
        self.icon.run()

# Instantiate the state machine
state_machine = TrayStateMachine()

# Running the tray icon
Thread(target=state_machine.run_tray).start()

# Keeping the main thread alive until termination is signaled
while not terminate_event.is_set():
    time.sleep(1)

print("Application terminated.")
