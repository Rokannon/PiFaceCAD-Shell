import time

from common.process import ProcessController


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


class CameraController:
    def __init__(self, process_controller: ProcessController):
        self.process_controller = process_controller
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

    def wait_photo(self):
        proc_args = [
            'raspistill',
            '--output', '/home/pi/picamera-images/single/image_{}.jpg'.format(int(time.time())),
            '--timeout', '1000',
        ]

        for setting in self.settings:
            proc_args.append(setting.command)
            proc_args.append(str(setting.value))

        self.process_controller.wait_process(
            title='Making photo...',
            args=proc_args,
        )
