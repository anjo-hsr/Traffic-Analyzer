import platform
from os import path
from typing import Optional

from main.helpers import tshark_helper


class PlatformDetectionHelper:
    @staticmethod
    def detect_platform() -> Optional[str]:
        program_path = None

        if platform.system() == "Windows":
            program_path = PlatformDetectionHelper.test_tshark_windows()

        elif platform.system() == "Linux":
            program_path = PlatformDetectionHelper.test_tshark_linux()

        return program_path

    @staticmethod
    def test_tshark_windows() -> Optional[str]:
        windows_defaults = tshark_helper.get_windows_defaults()
        return_value = None

        if path.isfile(windows_defaults["x86"]):
            return_value = windows_defaults["x86"]

        elif path.isfile(windows_defaults["x64"]):
            return_value = windows_defaults["x64"]

        return return_value

    @staticmethod
    def test_tshark_linux() -> Optional[str]:
        return_value = None
        if path.isfile("/usr/bin/tshark"):
            return_value = "tshark"

        return return_value
