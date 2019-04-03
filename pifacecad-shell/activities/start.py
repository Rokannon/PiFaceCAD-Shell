from common.context import AppContext
from common.display import DisplayRenderer

OPTION_TEST = 'Test'
OPTION_WIFI = 'Setup Wi-Fi'
OPTION_HELLO = 'Say "Hello"'


class StartActivity:
    def __init__(self, context: AppContext):
        self.context = context
        self.index = 0
        self.first_run = True

    def activate(self):
        if self.first_run:
            self.context.display_renderer.set_line('PiFaceCAD Shell', DisplayRenderer.LINE_FIRST)
            self.context.display_renderer.set_line('v1.0', DisplayRenderer.LINE_SECOND)
            self.context.button_controller.wait_button_press()
            self.first_run = False

    def deactivate(self):
        pass

    def update(self):
        if self.first_run:
            return

        selected_option = self.context.input_controller.wait_selector(
            title='# Start Menu',
            options=[
                # OPTION_TEST,
                OPTION_WIFI,
                OPTION_HELLO,
            ]
        )

        if selected_option == OPTION_HELLO:
            return AppContext.ACTIVITY_ID_HELLO
        elif selected_option == OPTION_WIFI:
            return AppContext.ACTIVITY_ID_WIFI_MAIN
        elif selected_option == OPTION_TEST:
            pass
