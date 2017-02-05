import time
from datetime import *

import schedule

from mbta import Routes
from map import *
from data import *
from server import setup

ctrl = MapController()

modes = {
    "RealTimeVisualization": RealTimeVisualization(Routes(mbta.Stations())),
    "SleepyVisualization": SleepyVisualization(),
    "SlideVisualization": SlideRouteVisualization()
}

# aliases
modes["on"] = modes["RealTimeVisualization"]
modes["off"] = modes["SlideVisualization"]
modes["sleep"] = modes["SlideVisualization"]

def wake():
    ctrl.set_brightness(0.1)
    set_mode("on")

def sleep():
    ctrl.set_brightness(0.3)
    set_mode("sleep")
 
def is_on_time():
    now = datetime.now()
    return now.hour >= ON_HOUR and now.hour < OFF_HOUR

def set_mode(m):
    if modes.get(m):
        ctrl.set_visualization(modes.get(m))
        return True
    return False

def set_brightness(b):
    b = max(min(float(b) / 100,  1), 0)
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
