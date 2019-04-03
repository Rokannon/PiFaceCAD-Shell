from pifacecad import PiFaceCAD

from common.buttons import ButtonController
from common.display import DisplayRenderer
from common.input import InputController
from common.process import ProcessController


class AppContext:
    ACTIVITY_ID_START = 0
    ACTIVITY_ID_HELLO = 1
    ACTIVITY_ID_WIFI_MAIN = 2
    ACTIVITY_ID_WIFI_SELECT = 3

    def __init__(self, cad: PiFaceCAD):
        self.display_renderer = DisplayRenderer(cad)
        self.button_controller = ButtonController(cad)
        self.input_controller = InputController(cad, self.display_renderer, self.button_controller)
        self.process_controller = ProcessController(self.display_renderer, self.button_controller,
                                                    self.input_controller)
