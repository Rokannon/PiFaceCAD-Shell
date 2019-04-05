from common.context import AppContext

OPTION_PHOTO = 'Make Photo'
OPTION_SETTINGS = 'Settings'
OPTION_BACK = 'Back'


class CameraActivity:
    def __init__(self, context: AppContext):
        self.context = context

    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(self):
        selected_option = self.context.input_controller.wait_selector(
            title='# Camera',
            options=[
                OPTION_PHOTO,
                OPTION_SETTINGS,
                OPTION_BACK,
            ],
        )

        if selected_option == OPTION_PHOTO:
            self.context.camera_controller.wait_photo()
        elif selected_option == OPTION_SETTINGS:
            while True:
                options = [setting.get_title() for setting in self.context.camera_controller.settings]
                options.append(OPTION_BACK)
                selected_option = self.context.input_controller.wait_selector(
                    title='# Cam. Settings',
                    options=options
                )

                if selected_option == OPTION_BACK:
                    break

                selected_setting = None
                for setting in self.context.camera_controller.settings:
                    if setting.get_title() == selected_option:
                        selected_setting = setting
                        break

                selected_setting.value = self.context.input_controller.wait_selector(
                    title='# ' + selected_setting.name,
                    options=selected_setting.options,
                    preselect=selected_setting.value,
                )

        elif selected_option == OPTION_BACK:
            return AppContext.ACTIVITY_ID_START
