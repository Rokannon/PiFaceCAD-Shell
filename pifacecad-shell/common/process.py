import subprocess
import time

from common.buttons import ButtonController
from common.display import DisplayRenderer
from common.input import InputController


class ProcessController:
    def __init__(self, display_renderer: DisplayRenderer, button_controller: ButtonController,
                 input_controller: InputController):
        self.display_renderer = display_renderer
        self.button_controller = button_controller
        self.input_controller = input_controller

    def wait_process(self, title, args):
        start_time = time.time()

        self.display_renderer.set_line(title, DisplayRenderer.LINE_FIRST)
        self.display_renderer.set_line('kill  -  -  -  -', DisplayRenderer.LINE_SECOND)

        stdout_lines = []
        proc = subprocess.Popen(
            args=args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.display_renderer.cursor_on()
        while proc.poll() is None or time.time() - start_time < 1:
            cursor_position = int(5 * (time.time() - start_time)) % DisplayRenderer.DISPLAY_WIDTH
            self.display_renderer.set_cursor(cursor_position, DisplayRenderer.LINE_FIRST)
            time.sleep(0.1)
            if self.button_controller.is_button_pressed(ButtonController.BUTTON_1):
                if proc.poll() is None:
                    proc.kill()
                    self.display_renderer.cursor_off()
                return None

        self.display_renderer.cursor_off()

        for line in proc.stdout:
            utf_line = line.decode('utf-8').strip()
            if utf_line:
                stdout_lines.append(utf_line)

        return stdout_lines
