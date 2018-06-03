import time
from datetime import *

import schedule

from map import *
from data import *
from server import setup

ctrl = MapController()

modes = {
    "RealTimeVisualization": RealTimeVisualization(),
    "SleepyVisualization": SleepyVisualization(),
    "SlideVisualization": SlideRouteVisualization()
}

# aliases
modes["on"] = modes["RealTimeVisualization"]
modes["off"] = modes["SlideVisualization"]

brightness = {"on": 0.1, "off": 0.3}


def wake():
    set_mode("on")


def sleep():
    set_mode("off")


def is_on_time():
    now = datetime.now()
    return now.hour >= ON_HOUR and now.hour < OFF_HOUR


def set_mode(m):
    if modes.get(m):
        ctrl.set_visualization(modes.get(m))
        ctrl.set_brightness(brightness.get(m, 0.1))
        return True
    return False


def set_brightness(b):
    b = max(min(float(b) / 100, 1), 0)
    ctrl.set_brightness(b)
    ctrl.reset_board()
    return b


def run():
    schedule.every().day.at("%s:00" % (ON_HOUR % 24)).do(wake)
    schedule.every().day.at("%s:00" % (OFF_HOUR % 24)).do(sleep)
    setup(set_mode, set_brightness)
    if is_on_time():
        wake()
    else:
        sleep()
    while True:
        schedule.run_pending()
        ctrl.tick()


if __name__ == '__main__':
    run()
