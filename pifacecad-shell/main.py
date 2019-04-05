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

        self.current_activity = None
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
        self.activate(AppContext.ACTIVITY_ID_START)
        while True:
            next_activity_id = self.current_activity.update()
            if next_activity_id is not None:
                self.activate(next_activity_id)

    def activate(self, activity_id):
        if self.current_activity:
            self.current_activity.deactivate()
            self.current_activity = None

        self.current_activity = self.activity_by_id[activity_id]
        self.current_activity.activate()


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
