from common.context import AppContext
from common.display import DisplayRenderer

OPTION_TEST = 'Test'
OPTION_WIFI = 'Setup Wi-Fi'
OPTION_HELLO = 'Say "Hello"'
OPTION_CAMERA = 'Use Camera'


class StartActivity:
    def __init__(self, context: AppContext):
        self.context = context
        self.first_run = True
        self.selected_option = None

    def execute(self):
        if self.first_run:
            self.first_run = False
            self.context.display_renderer.set_line('PiFaceCAD Shell', DisplayRenderer.LINE_FIRST)
            self.context.display_renderer.set_line('v1.0', DisplayRenderer.LINE_SECOND)
            self.context.button_controller.wait_button_press()

        while True:
            self.selected_option = self.context.input_controller.wait_selector(
                title='# Start Menu',
                options=[
                    # OPTION_TEST,
                    OPTION_WIFI,
                    OPTION_HELLO,
                    OPTION_CAMERA,
                ],
                preselect=self.selected_option,
            )

            if self.selected_option == OPTION_HELLO:
                return AppContext.ACTIVITY_ID_HELLO
            elif self.selected_option == OPTION_WIFI:
                return AppContext.ACTIVITY_ID_WIFI
            elif self.selected_option == OPTION_TEST:
                self.context.input_controller.wait_input()
            elif self.selected_option == OPTION_CAMERA:
                return AppContext.ACTIVITY_ID_CAMERA
