import argparse
from pynput import keyboard, mouse
from PIL import ImageGrab
import os

# TODO: Add proper logging rather than print statements.

class Screenshot:
    def __init__(self, dest_folder):
        self.dest_folder = os.path.expanduser(dest_folder) if dest_folder else ""
        self.alt_pressed = False
        self.shift_pressed = False
        self.region_capture = False
        self.start_x, self.start_y = None, None
        self.end_x, self.end_y = None, None

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.mouse_listener.start()

    def update_region_capture(self):
        if self.alt_pressed and self.shift_pressed:
            self.region_capture = True
            self.start_x, self.start_y, self.end_x, self.end_y = None, None, None, None
        else:
            if self.region_capture:
                self.region_capture = False
                self.capture_screenshot()

    def on_press(self, key):
        if key == keyboard.Key.alt:
            self.alt_pressed = True
            self.update_region_capture()
        elif key == keyboard.Key.shift:
            self.shift_pressed = True
            self.update_region_capture()

    def on_release(self, key):
        if key == keyboard.Key.alt:
            self.alt_pressed = False
            self.update_region_capture()
        elif key == keyboard.Key.shift:
            self.shift_pressed = False
            self.update_region_capture()

    def on_move(self, x, y):
        if self.region_capture:
            if not self.start_x or not self.start_y:
                self.start_x, self.start_y = x, y
            else:
                self.end_x, self.end_y = x, y

    def capture_screenshot(self):
        if self.start_x == self.end_x or self.start_y == self.end_y:
            return
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        right = max(self.start_x, self.end_x)
        bottom = max(self.start_y, self.end_y)

        if left != right and top != bottom:
            bbox = (left, top, right, bottom)
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            if self.dest_folder and not os.path.exists(self.dest_folder):
                os.makedirs(self.dest_folder)
            screenshot.save(self.dest_folder + "capture.png")
            print(f"Screenshot saved at {self.dest_folder + 'capture.png'}")

    def run(self):
        print("quickshot running")
        # TODO: Revisit this try/except logic (needed?)
        try:
            while True:
                pass  # Keep the main thread alive
        except KeyboardInterrupt:
            self.listener.stop()
            self.listener.join()
            self.mouse_listener.stop()
            self.mouse_listener.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture screenshots of selected regions.")
    parser.add_argument("--dest_folder", type=str, default="", help="Destination folder path for saved screenshot")
    args = parser.parse_args()
    screenshot_instance = Screenshot(args.dest_folder)
    screenshot_instance.run()