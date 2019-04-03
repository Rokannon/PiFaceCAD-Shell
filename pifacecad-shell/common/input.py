import time

from common.buttons import ButtonController
from common.display import DisplayRenderer
from pifacecad import PiFaceCAD


class InputController:
    LOWER_CHARS = 'abcdefghijklmnopqrstuvwxyz1234567890-='
    UPPER_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+'

    def __init__(self, cad: PiFaceCAD, display_renderer: DisplayRenderer, button_controller: ButtonController):
        self.cad = cad
        self.display_renderer = display_renderer
        self.button_controller = button_controller

    def wait_input(self):
        input_chars = ['a']
        cursor_position = 0
        cancelled = False
        self.cad.lcd.cursor_on()
        while True:
            self.display_renderer.set_line(''.join(input_chars), DisplayRenderer.LINE_FIRST)
            self.display_renderer.set_line('< > del ok cancl', DisplayRenderer.LINE_SECOND)
            self.cad.lcd.set_cursor(cursor_position, 0)
            button_id = self.button_controller.wait_button_press()
            if button_id == ButtonController.BUTTON_1:
                if cursor_position > 0:
                    cursor_position -= 1
            elif button_id == ButtonController.BUTTON_2:
                if cursor_position == DisplayRenderer.DISPLAY_WIDTH - 1:
                    continue
                cursor_position += 1
                if cursor_position == len(input_chars):
                    input_chars.append('a')
            elif button_id == ButtonController.BUTTON_3:
                if len(input_chars) == 1:
                    continue
                input_chars.pop(cursor_position)
                if cursor_position >= len(input_chars):
                    cursor_position -= 1
            elif button_id == ButtonController.BUTTON_4:
                break
            elif button_id == ButtonController.BUTTON_5:
                cancelled = True
                break
            elif button_id == ButtonController.BUTTON_LEFT:
                old_char = input_chars[cursor_position]
                if old_char in self.LOWER_CHARS:
                    new_char = self.LOWER_CHARS[(self.LOWER_CHARS.find(old_char) - 1) % len(self.LOWER_CHARS)]
                else:
                    new_char = self.UPPER_CHARS[(self.UPPER_CHARS.find(old_char) - 1) % len(self.UPPER_CHARS)]
                input_chars[cursor_position] = new_char
            elif button_id == ButtonController.BUTTON_RIGHT:
                old_char = input_chars[cursor_position]
                if old_char in self.LOWER_CHARS:
                    new_char = self.LOWER_CHARS[(self.LOWER_CHARS.find(old_char) + 1) % len(self.LOWER_CHARS)]
                else:
                    new_char = self.UPPER_CHARS[(self.UPPER_CHARS.find(old_char) + 1) % len(self.UPPER_CHARS)]
                input_chars[cursor_position] = new_char
            elif button_id == ButtonController.BUTTON_ENTER:
                old_char = input_chars[cursor_position]
                if old_char in self.LOWER_CHARS:
                    new_char = self.UPPER_CHARS[self.LOWER_CHARS.find(old_char)]
                else:  # old_char in self.UPPER_CHARS
                    new_char = self.LOWER_CHARS[self.UPPER_CHARS.find(old_char)]
                input_chars[cursor_position] = new_char
        self.cad.lcd.cursor_off()
        return None if cancelled else ''.join(input_chars)

    def wait_selector(self, title, options):
        self.display_renderer.set_line(title, DisplayRenderer.LINE_FIRST)
        selected_index = 0
        while True:
            self.display_renderer.set_line('> ' + options[selected_index], DisplayRenderer.LINE_SECOND)
            button_id = self.button_controller.wait_button_press()
            if button_id == ButtonController.BUTTON_RIGHT:
                selected_index = (selected_index + 1) % len(options)
            elif button_id == ButtonController.BUTTON_LEFT:
                selected_index = (selected_index - 1) % len(options)
            elif button_id == ButtonController.BUTTON_ENTER:
                self.display_renderer.set_line('Selected!', DisplayRenderer.LINE_FIRST)
                time.sleep(1.0)
                return options[selected_index]
