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

    def wait_process(self, args):
        start_time = time.time()

        self.display_renderer.set_line('Working...', DisplayRenderer.LINE_FIRST)
        self.display_renderer.set_line('kill  -  -  -  -', DisplayRenderer.LINE_SECOND)

        stdout_lines = []
        proc = subprocess.Popen(
            args=args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        while proc.poll() is None or time.time() - start_time < 2:
            time.sleep(0.1)
            if self.button_controller.is_button_pressed(ButtonController.BUTTON_1):
                if proc.poll() is None:
                    proc.kill()
                return None

        for line in proc.stdout:
            utf_line = line.decode('utf-8').strip()
            if utf_line:
                stdout_lines.append(utf_line)

        return stdout_lines
