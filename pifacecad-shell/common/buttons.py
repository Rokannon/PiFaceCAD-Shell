import collections
import time

from pifacecad import PiFaceCAD


class ButtonController:
    BUTTON_1 = 0
    BUTTON_2 = 1
    BUTTON_3 = 2
    BUTTON_4 = 3
    BUTTON_5 = 4
    BUTTON_ENTER = 5
    BUTTON_LEFT = 6
    BUTTON_RIGHT = 7

    PRESS_DELAY = 0.2

    def __init__(self, cad: PiFaceCAD):
        self.cad = cad
        self.time_pressed_by_id = collections.defaultdict(float)

    def wait_button_press(self):
        while True:
            for button_id, switch in enumerate(self.cad.switches):
                current_time = time.time()
                if switch.value and current_time - self.time_pressed_by_id[button_id] > self.PRESS_DELAY:
                    self.time_pressed_by_id[button_id] = current_time
                    return button_id
            time.sleep(0.01)

    def is_button_pressed(self, button_id):
        return self.cad.switches[button_id].value
