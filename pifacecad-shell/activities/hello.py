import random

from common.context import AppContext
from common.display import DisplayRenderer

RAW_DATA = [
    'Arabic',
    'Marhaba',
    'Austrian German',
    'Grüß Gott',
    'Bengali',
    'Namaskar',
    'Bulgarian',
    'Zdraveite',
    'Catalan',
    'Hola',
    'Chamorro',
    'Hafa adai',
    'Chinese',
    'Nǐ hǎo',
    'Danish',
    'God dag',
    'Dutch',
    'Hallo',
    'Finnish',
    'hyvää päivää',
    'French',
    'Bonjour',
    'Gaeilge',
    'Dia dhuit',
    'German',
    'Guten tag',
    'Greek',
    'Yasou',
    'Hebrew',
    'Shalom',
    'Hindi',
    'Namaste',
    'Hungarian',
    'Jo napot',
    'Icelandic',
    'Góðan dag',
    'Igbo',
    'Nde-ewo',
    'Indonesian',
    'Selamat siang',
    'Italian',
    'Salve',
    'Japanese',
    'Konnichiwa',
    'Latin',
    'Salve',
    'Lithuanian',
    'Sveiki',
    'Luxembourgish',
    'Moïen',
    'Maltese',
    'Bonġu',
    'Nahuatl',
    'Niltze',
    'Nepali',
    'Namastē',
    'Norwegian',
    'Hallo',
    'Persian',
    'Salam',
    'Polish',
    'Cześć',
    'Portuguese',
    'Olá',
    'Romanian',
    'Bună ziua',
    'Russian',
    'Zdravstvuyte',
    'Serbian',
    'Zdravo',
    'Slovak',
    'Ahoj',
    'Spanish',
    'Hola',
    'Swahili',
    'Hujambo',
    'Swedish',
    'Hallå',
    'Tahitian',
    'Ia orna',
    'Thai',
    'Sawasdee',
    'Tsonga',
    'Avuxeni',
    'Turkish',
    'Merhaba',
    'Ukrainian',
    'Zdravstvuyte',
    'Vietnamese',
    'xin chào',
    'Welsh',
    'Shwmae',
    'Zulu',
    'Sawubona',
]


class HelloActivity:
    def __init__(self, context: AppContext):
        self.context = context
        self.hello_by_language = {}

    def execute(self):
        for i, line in enumerate(RAW_DATA):
            if i % 2 == 0:
                self.hello_by_language[line] = RAW_DATA[i + 1]

        language = random.choice(list(self.hello_by_language.keys()))

        self.context.display_renderer.set_line(language + ':', DisplayRenderer.LINE_FIRST)
        self.context.display_renderer.set_line(self.hello_by_language[language], DisplayRenderer.LINE_SECOND)

        self.context.button_controller.wait_button_press()

        self.hello_by_language.clear()

        return AppContext.ACTIVITY_ID_START
