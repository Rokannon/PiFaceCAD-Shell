from pifacecad import PiFaceCAD


class DisplayRenderer:
    DISPLAY_WIDTH = 16

    LINE_FIRST = 0
    LINE_SECOND = 1

    def __init__(self, cad: PiFaceCAD):
        self.cad = cad

        self.line_by_id = {
            self.LINE_FIRST: [' '] * self.DISPLAY_WIDTH,
            self.LINE_SECOND: [' '] * self.DISPLAY_WIDTH,
        }

    def clear(self):
        self.cad.lcd.clear()
        for line in self.line_by_id.values():
            for char_index, _ in enumerate(line):
                line[char_index] = ' '

    def set_line(self, text, line_id):
        text_chars = list(text[:self.DISPLAY_WIDTH])
        while len(text_chars) < self.DISPLAY_WIDTH:
            text_chars.append(' ')

        line = self.line_by_id[line_id]

        diff_by_index = {}
        diff_buffer = []
        for char_index, text_char in enumerate(text_chars):
            if text_char != line[char_index]:
                diff_buffer.append(text_char)
                line[char_index] = text_char
            elif diff_buffer:
                diff_by_index[char_index - len(diff_buffer)] = ''.join(diff_buffer)
                diff_buffer.clear()

        if diff_buffer:
            diff_by_index[self.DISPLAY_WIDTH - len(diff_buffer)] = ''.join(diff_buffer)

        for diff_index, diff_text in diff_by_index.items():
            self.cad.lcd.set_cursor(diff_index, line_id)
            self.cad.lcd.write(diff_text)

    def cursor_on(self):
        self.cad.lcd.cursor_on()

    def cursor_off(self):
        self.cad.lcd.cursor_off()

    def set_cursor(self, col, row):
        self.cad.lcd.set_cursor(col, row)
