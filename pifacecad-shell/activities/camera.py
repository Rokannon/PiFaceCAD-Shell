import time

from common.buttons import ButtonController
from common.context import AppContext
from common.display import DisplayRenderer

OPTION_PHOTO = 'Make Photo'
OPTION_TIMELAPSE = 'Make Timelapse'
OPTION_SETTINGS = 'Photo Settings'
# OPTION_DELAY = 'Delay: 15 sec'
OPTION_BACK = 'Back'


class CameraSetting:
    def __init__(
            self,
            name,
            value,
            options,
            command,
            use_index=False,
    ):
        self.name = name
        self.value = value
        self.options = options
        self.command = command
        self.use_index = use_index

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
            # CameraSetting(
            #     name='Mode',
            #     value='640x480 42.1-60fps',
            #     options=[
            #         'auto',
            #         '1920x1080 1-30fps',
            #         '2592x1944 1-15fps',
            #         '2592x1944 0.1666-1fps',
            #         '1296x972 1-42fps',
            #         '1296x730 1-49fps',
            #         '640x480 42.1-60fps',
            #         '640x480 60.1-90fps',
            #     ],
            #     command='--mode',
            #     use_index=True,
            # ),
        ]
        self.delay = 15

    def get_delay_title(self):
        return 'Delay: {} sec'.format(self.delay)

    def execute(self):
        selected_option = None

        while True:
            selected_option = self.context.input_controller.wait_selector(
                title='# Camera',
                options=[
                    OPTION_PHOTO,
                    OPTION_TIMELAPSE,
                    OPTION_SETTINGS,
                    self.get_delay_title(),
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
            elif selected_option == self.get_delay_title():
                self.execute_delay()
            elif selected_option == OPTION_TIMELAPSE:
                self.execute_timelapse()

    def execute_photo(self):
        proc_args = [
            'raspistill',
            '--output', '/home/pi/picamera-images/single/image_{}.jpg'.format(int(time.time())),
            '--timeout', '1000',
        ]

        for setting in self.settings:
            proc_args.append(setting.command)
            if setting.use_index:
                proc_args.append(str(setting.options.index(setting.value)))
            else:
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

    def execute_delay(self):
        self.delay = self.context.input_controller.wait_selector(
            title='# Setup delay:',
            options=[15, 30, 60, 90],
            preselect=self.delay,
        )

    def execute_timelapse(self):
        while True:
            photo_time = time.time()
            self.execute_photo()
            while time.time() - photo_time < self.delay:
                self.context.display_renderer.set_line(
                    text='Next in {}s...'.format(int(photo_time + self.delay + 1 - time.time())),
                    line_id=DisplayRenderer.LINE_FIRST,
                )
                self.context.display_renderer.set_line(
                    text='stop  -  -  -  -',
                    line_id=DisplayRenderer.LINE_SECOND,
                )
                time.sleep(0.1)
                if self.context.button_controller.is_button_pressed(ButtonController.BUTTON_1):
                    return
