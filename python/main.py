import time
from datetime import *

from mbta import Routes
from map import *
from data import *

def is_on_time():
	now = datetime.now()
	return now.hour >= 7 and now.hour <= 22

def x_is_on_time():
	return datetime.now().second % 2 == 0

def run():
	is_on = None
	api_routes = Routes(mbta.Stations())
	v = RealTimeVisualization(api_routes)
	s = SleepyVisualization()
	f = FlashVisualization()
	r = FlashRouteVisualization()
	c = MapController()
	while True:
		prev_is_on = is_on
		is_on = is_on_time()
		if not is_on is prev_is_on:
			if is_on:
				c.set_visualization(v)
			else:
				c.set_visualization(s)
		c.tick()
        # time.sleep(abs(SLEEP_TIME - elapsed))


if __name__ == '__main__':
    run()


