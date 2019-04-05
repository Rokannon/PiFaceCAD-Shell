import time

from common.context import AppContext

OPTION_PHOTO = 'Make Photo'
OPTION_SETTINGS = 'Settings'
OPTION_BACK = 'Back'


class CameraSetting:
    def __init__(
            self,
            name,
            value,
            options,
            command,
    ):
        self.name = name
        self.value = value
        self.options = options
        self.command = command

    def get_title(self):
        return '{}: {}'.format(self.name, self.value)


class CameraActivity:
    def __init__(self, context: AppContext):
        self.context = context
        self.settings = [
            CameraSetting(
                name='Sharpness',
                value=0,
                options=list(range(-100, 101, 20)),
                command='--sharpness',
            ),
            CameraSetting(
                name='Contrast',
                value=0,
                options=list(range(-100, 101, 20)),
                command='--contrast',
            ),
            CameraSetting(
                name='Brightness',
                value=50,
                options=list(range(0, 101, 10)),
                command='--brightness',
            ),
            CameraSetting(
                name='Saturation',
                value=0,
                options=list(range(-100, 101, 20)),
                command='--saturation',
            ),
            CameraSetting(
                name='ISO',
                value=100,
                options=[100, 200, 400, 800],
                command='--ISO',
            ),
            CameraSetting(
                name='Exposure',
                value='auto',
                options=[
                    'auto',
                    'night',
                    'nightpreview',
                    'backlight',
                    'spotlight',
                    'sports',
                    'snow',
                    'beach',
                    'verylong',
                    'fixedfps',
                    'antishake',
                    'fireworks',
                ],
                command='--exposure',
            ),
            CameraSetting(
                name='AWB',
                value='auto',
                options=[
                    'off',
                    'auto',
                    'sun',
                    'cloud',
                    'shade',
                    'tungsten',
                    'fluorescent',
                    'incandescent',
                    'flash',
                    'horizon',
                ],
                command='--awb',
            ),
            CameraSetting(
                name='Image Effect',
                value='none',
                options=[
                    'none',
                    'negative',
                    'solarise',
                    'posterise',
                    'whiteboard',
                    'blackboard',
                    'sketch',
                    'denoise',
                    'emboss',
                    'oilpaint',
                    'hatch',
                    'gpen',
                    'pastel',
                    'watercolour',
                    'film',
                    'blur',
                    'saturation',
                    'colourswap',
                    'washedout',
                    'colourpoint',
                    'colourbalance',
                    'cartoon',
                ],
                command='--imxfx',
            ),
        ]

    def execute(self):
        selected_option = None

        while True:
            selected_option = self.context.input_controller.wait_selector(
                title='# Camera',
                options=[
                    OPTION_PHOTO,
                    OPTION_SETTINGS,
                    OPTION_BACK,
                ],
                preselect=selected_option,
            )

            if selected_option == OPTION_PHOTO:
                self.execute_photo()
            elif selected_option == OPTION_SETTINGS:
                self.execute_settings()
            elif selected_option == OPTION_BACK:
                return AppContext.ACTIVITY_ID_START

    def execute_photo(self):
        proc_args = [
            'raspistill',
            '--output', '/home/pi/picamera-images/single/image_{}.jpg'.format(int(time.time())),
            '--timeout', '1000',
        ]

        for setting in self.settings:
            proc_args.append(setting.command)
            proc_args.append(str(setting.value))

        self.context.process_controller.wait_process(
            title='Making photo...',
            args=proc_args,
        )

    def execute_settings(self):
        selected_option = None

        while True:
            options = [setting.get_title() for setting in self.settings]
            options.append(OPTION_BACK)
            selected_option = self.context.input_controller.wait_selector(
                title='# Cam. Settings',
                options=options,
                preselect=selected_option,
            )

            if selected_option == OPTION_BACK:
                break

            selected_setting = None
            for setting in self.settings:
                if setting.get_title() == selected_option:
                    selected_setting = setting
                    break

            selected_setting.value = self.context.input_controller.wait_selector(
                title='# ' + selected_setting.name,
                options=selected_setting.options,
                preselect=selected_setting.value,
            )
