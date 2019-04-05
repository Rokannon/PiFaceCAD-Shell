import re

from common.context import AppContext
from common.display import DisplayRenderer

PASS_CONFIG_TEMPLATE = '''
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="{ssid}"
    psk="{password}"
}}
'''.lstrip()

NO_PASS_CONFIG_TEMPLATE = '''
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="{ssid}"
    key_mgmt=NONE
}}
'''.lstrip()

ESSID_REGEX = re.compile('.*ESSID:"(.*?)".*')
INET_ADDR_REGEX = re.compile('.*inet addr:(\d+\.\d+\.\d+\.\d+).*')

OPTION_STATUS = 'Show Status'
OPTION_CONNECT = 'Connect...'
OPTION_BACK = 'Back'


class WifiActivity:
    def __init__(self, context: AppContext):
        self.context = context

    def execute(self):
        selected_option = None

        while True:
            selected_option = self.context.input_controller.wait_selector(
                title='# Wi-Fi Setup',
                options=[
                    OPTION_STATUS,
                    OPTION_CONNECT,
                    OPTION_BACK,
                ],
                preselect=selected_option,
            )

            if selected_option == OPTION_STATUS:
                self.execute_status()
            elif selected_option == OPTION_CONNECT:
                self.execute_connect()
            elif selected_option == OPTION_BACK:
                return AppContext.ACTIVITY_ID_START

    def execute_status(self):
        # Show SSID
        result_lines = self.context.process_controller.wait_process(
            title='Getting SSID...',
            args=['iwconfig', 'wlan0'],
        )
        if result_lines is None:
            return
        match = None
        for line in result_lines:
            match = ESSID_REGEX.match(line)
            if match:
                break
        if match:
            self.context.display_renderer.set_line('Connected to:', DisplayRenderer.LINE_FIRST)
            self.context.display_renderer.set_line(match.group(1), DisplayRenderer.LINE_SECOND)
        else:
            self.context.display_renderer.set_line('Not connected', DisplayRenderer.LINE_FIRST)
            self.context.display_renderer.set_line('', DisplayRenderer.LINE_SECOND)
        self.context.button_controller.wait_button_press()

        # Show IP
        result_lines = self.context.process_controller.wait_process(
            title='Getting IP...',
            args=['ifconfig', 'wlan0'],
        )
        if result_lines is None:
            return
        match = None
        for line in result_lines:
            match = INET_ADDR_REGEX.match(line)
            if match:
                break
        self.context.display_renderer.set_line('Device IP:', DisplayRenderer.LINE_FIRST)
        if match:
            self.context.display_renderer.set_line(match.group(1), DisplayRenderer.LINE_SECOND)
        else:
            self.context.display_renderer.set_line('Unknown', DisplayRenderer.LINE_SECOND)
        self.context.button_controller.wait_button_press()

    def execute_connect(self):
        result_lines = self.context.process_controller.wait_process(
            title='Scanning...',
            args=['iwlist', 'wlan0', 'scan'],
        )
        ssids = []
        for line in result_lines:
            match = ESSID_REGEX.match(line)
            if not match:
                continue
            ssid = match.group(1).strip()
            if ssid:
                ssids.append(ssid)

        selected_ssid = self.context.input_controller.wait_selector(
            title='# Select network',
            options=ssids
        )

        need_password = self.context.input_controller.wait_selector(
            title='# With password?',
            options=[
                'yes',
                'no',
            ]
        ) == 'yes'

        if need_password:
            password = self.context.input_controller.wait_input()
            if password is None:
                return
            config_str = PASS_CONFIG_TEMPLATE.format(
                ssid=selected_ssid,
                password=password,
            )
        else:
            config_str = NO_PASS_CONFIG_TEMPLATE.format(
                ssid=selected_ssid
            )

        confirm_setup = self.context.input_controller.wait_selector(
            title='# Confirm setup?',
            options=[
                'yes',
                'no',
            ]
        ) == 'yes'
        if confirm_setup:
            with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as config_file:
                config_file.write(config_str)
