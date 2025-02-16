import keyboard
import sys
from controller import ToyController

class KeyboardController(ToyController):
    def __init__(self, host="192.168.4.1", port=8080):
        super().__init__(host, port)

    def run_keyboard_mode(self):
        print("Keyboard Control Mode")
        print("Commands:")
        print("  Right Arrow - Toggle Toy 1 Trigger 1 (90⇄145 degrees)")
        print("  Left Arrow  - Toggle Toy 1 Trigger 2 (90⇄145 degrees)")
        print("  ESC        - Exit program")

        try:
            keyboard.on_press_key("right", lambda _: self.weave_right())
            keyboard.on_press_key("left", lambda _: self.weave_left())
            keyboard.on_press_key("up", lambda _: self.guard())
            keyboard.on_press_key("E", lambda _: self.toggle_trigger1())
            keyboard.on_press_key("Q", lambda _: self.toggle_trigger2())
            keyboard.on_press_key("esc", lambda _: sys.exit(0))

            keyboard.wait("esc")

        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.close()