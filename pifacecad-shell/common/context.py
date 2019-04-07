from common.buttons import ButtonController
from common.display import DisplayRenderer
from common.input import InputController
from common.process import ProcessController
from common.settings import AppSettings
from common.telegram import TelegramController
from pifacecad import PiFaceCAD

SETTINGS_PATH = 'settings.json'


class AppContext:
    VERSION = '1.0.0'

    ACTIVITY_ID_START = 0
    ACTIVITY_ID_HELLO = 1
    ACTIVITY_ID_WIFI = 2
    ACTIVITY_ID_CAMERA = 3

    def __init__(self, cad: PiFaceCAD):
        self.settings = AppSettings.from_file(SETTINGS_PATH)
        self.display_renderer = DisplayRenderer(cad)
        self.button_controller = ButtonController(cad)
        self.input_controller = InputController(self.display_renderer, self.button_controller)
        self.process_controller = ProcessController(self.display_renderer, self.button_controller,
                                                    self.input_controller)
        self.telegram_controller = TelegramController(self.settings)
