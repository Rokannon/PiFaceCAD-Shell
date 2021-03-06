import pifacecad
from activities.camera import CameraActivity
from activities.hello import HelloActivity
from activities.start import StartActivity
from activities.wifi import WifiActivity
from common.context import AppContext


class Application:
    def __init__(self):
        self.cad = pifacecad.PiFaceCAD()
        self.context = AppContext(self.cad)

        self.activity_by_id = {
            AppContext.ACTIVITY_ID_START: StartActivity(self.context),
            AppContext.ACTIVITY_ID_HELLO: HelloActivity(self.context),
            AppContext.ACTIVITY_ID_WIFI: WifiActivity(self.context),
            AppContext.ACTIVITY_ID_CAMERA: CameraActivity(self.context),
        }

    def run(self):
        self.cad.lcd.backlight_on()
        self.cad.lcd.cursor_off()
        self.cad.lcd.blink_off()

        current_activity = self.activity_by_id[AppContext.ACTIVITY_ID_START]
        while True:
            next_activity_id = current_activity.execute()
            current_activity = self.activity_by_id[next_activity_id]


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
