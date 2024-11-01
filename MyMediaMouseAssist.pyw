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
        # Timer to handle idle timeout for media state
        self.idle_timer = None
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
        elif state == "inactive":
            self.icon.icon = self.create_image("M", "#F44336")
        elif state == "media":
            # Trigger volume bar
            self.change_volume(0xAF) # Virtual-Key code for Volume Up
            self.change_volume(0xAE) # Virtual-Key code for Volume Down
            self.icon.icon = self.create_image("M", "#2196F3")
            self.start_idle_timer()
        self.icon.visible = True

    def toggle_state(self, icon, item):
        if self.state == "active":
            self.set_state("inactive")
        else:
            self.set_state("active")

    def media_state(self):
        if self.state == "active":  # Only activate media state if in active state
            self.set_state("media")
            self.start_idle_timer()

    def exit_app(self, icon, item):
        self.icon.stop()
        terminate_event.set()  # Signal to terminate

    def on_clicked(self, x, y, button, pressed):
        if button == mouse.Button.middle and pressed:
            self.media_state()

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

    def start_idle_timer(self):
        self.cancel_idle_timer()
        self.idle_timer = Timer(2.0, self.return_to_active)  # Updated timeout to 2 seconds
        self.idle_timer.start()

    def cancel_idle_timer(self):
        if self.idle_timer:
            self.idle_timer.cancel()
            self.idle_timer = None

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
