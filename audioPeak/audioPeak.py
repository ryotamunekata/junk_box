from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import time
import signal
import sys
import math

class AudioLevelMeter:
    CALC_BAR_METHODS = {
        'logarithmic': lambda x, max_length: int(math.log1p(x * 10) * max_length / math.log1p(10)),
        'sigmoid': lambda x, max_length: int((1 / (1 + math.exp(-5 * (x - 0.5)))) * max_length),
        'step': lambda x, max_length: int(max_length if x > 0.5 else 0),
        'exponential': lambda x, max_length: int((x ** 4) * max_length)
    }

    def __init__(self, refresh_rate=0.033, max_bar_length=50, color_background=False):
        self.refresh_rate = refresh_rate
        self.max_bar_length = max_bar_length
        self.color_background = color_background


        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioMeterInformation._iid_, CLSCTX_ALL, None)
        self.meter = cast(interface, POINTER(IAudioMeterInformation))

    def get_color_gradient(self, percentage):
        if percentage < 0.5:
            red = int(255 * (percentage * 2))
            green = 255
        else:
            red = 255
            green = int(255 * ((1 - percentage) * 2))
        return f"\033[38;2;{red};{green};0m"

    def calculate_bar_length(self, peak_value):
        # ここでバーの長さを計算する式を変更できる
        return self.CALC_BAR_METHODS['sigmoid'](peak_value, self.max_bar_length)

    def signal_handler(self, sig, frame):
        print("\nStopping and exiting...")
        sys.exit(0)

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        while True:
            peak_value = self.meter.GetPeakValue()
            bar_length = self.calculate_bar_length(peak_value)
            bar = ""
            for i in range(self.max_bar_length):
                if i < bar_length:
                    color = self.get_color_gradient(i / self.max_bar_length)
                    bar += color + "█"
                else:
                    bar += "-" if not self.color_background else self.get_color_gradient(i / self.max_bar_length) + " "
            print(f"\r[{bar}\033[0m] {peak_value:.2f}", end='')
            time.sleep(self.refresh_rate)

# 使用例
meter = AudioLevelMeter()
meter.start()
