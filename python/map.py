import math
import random
import mbta
import time
import threading
import util

from color import adjust_brightness

from data import *
from util import *
from bitpusher import *

class MapController(object):
	def __init__(self,board=None):
		self.last_state = MapState()
		self.board = board
		self.steps = 0

	def set_visualization(self,vis):
		self.visualization = vis

	def tick(self):
		delay = None
		res = self.visualization.update(self.steps,time.time())
		if type(res) is tuple:
			state = res[0]
			delay = res[1]
		else:
			state = res
		writes = state.diff_with(self.last_state)
		for w in writes:
			w.color = adjust_brightness(w.color,BRIGHTNESS)
		self.last_state = state
		self.board.write(writes)
		if delay > 0:
			time.sleep(delay)
		self.steps += 1

class Visualization(object):
	def __init__(self):
		pass

	def get_state(self):
		return self.state

	def update(self,tick=None,time=None):
		return self.state

class FlashVisualization(Visualization):
	def update(self,tick,time):
		s = MapState()
		c = adjust_brightness(
			[MapColors.RED, MapColors.GREEN, MapColors.BLUE, MapColors.ORANGE][tick % 4],
			0.5
		)
		if True:
			for strip_name in STRIPS:
				for i in xrange(len(s.strips[strip_name])):
					s.strips[strip_name][i] = c
		return (s,1)

class FlashRouteVisualization(Visualization):
	def update(self,tick,time):
		s = MapState()
		keys = sorted(ROUTES.keys())
		bright_route_name = keys[tick % len(keys)]
		for route_name in ROUTES:
			c = ROUTE_COLORS[route_name]
			c = adjust_brightness(c,0.1)
			for seg in ROUTE_SEGMENTS[route_name]:
				(strip,start,end) = seg[0:3]
				for i in xrange(start,end+1):
					s.strips[strip][i] = c
		c = ROUTE_COLORS[bright_route_name]
		for seg in ROUTE_SEGMENTS[bright_route_name]:
			(strip,start,end) = seg[0:3]
			for i in xrange(start,end+1):
				s.strips[strip][i] = c
		return (s,1)


class RealTimeVisualization(Visualization):
	def __init__(self):
		super(RealTimeVisualization,self).__init__()
		api_stations = mbta.Stations()
		api_routes = mbta.Routes(api_stations)
		self.last_time_update = None
		self.update_time = 10
		self.routes = {}
		self.black()
		for route_name in ROUTES:
			r = MapRoute(route_name,api_routes.get(route_name))
			self.routes[route_name] = r

	def black(self):
		self.state = MapState()

	def update(self,tick=None,time=None):
		should_update = False
		if not self.last_time_update or time - self.last_time_update > self.update_time:
			self.last_time_update = time		
			should_update = True
		self.state = BlinkRouteMapState(self.routes,tick,should_update)
		return self.state

class MapRoute(object):
	def __init__(self,name,route):
		self.name = name
		self.route = route
		self.color = ROUTE_COLORS[name]
		self.stations = {}
		self.station_locations = {}
		self.trains = {}
		self.train_locations = {}
		self.last_train_locations = {}
		self.train_velocities = {}
		self.last_locate_time = time.time()
		self.update_lock = threading.Lock()
		self.segments = map(
			lambda m: LightSegment(*m),
			ROUTE_SEGMENTS[name]
		)
		self.distribute_stations()

	def length(self):
		return sum(map(
			lambda seg: 1 + seg.end - seg.start,
			self.segments
		))

	def distribute_stations(self):
		station_references = STATION_LOCATIONS[self.name]
		for a,b in pairwise(station_references):
			list = collect_between(
				self.route.stations,
				lambda x: x.name == a[0],
				lambda x: x.name == b[0]
			)
			length = b[1] - a[1]
			gap = float(length) / (len(list) - 1)
			for i, s in enumerate(list):
				index = a[1] + int(round(gap * i))
				self.stations[index] = list[i]
				self.station_locations[list[i].name] = index

	def strip_by_index(self,i):
		try:
			it = iter(self.segments)
			seg = it.next()
			while i - seg.length() >= 0:
				i -= seg.length()
				seg = it.next()
			if seg.reverse:
				index = seg.end - i
			else:
				index = seg.start + i
			return (seg.strip,index)
		except StopIteration:
			return (None,None)

	def update_trains(self):
		trains = {}
		for t in self.route.get_trains():
			trains[t.id] = t
		self.update_lock.acquire()
		self.trains = trains
		self.locate_trains()
		self.update_lock.release()

	def nb_update_trains(self):
		update = threading.Thread(target=self.update_trains)
		update.start()

	def locate_trains(self,as_dict=False):
		res_dict = {}
		res_arr = []
		self.train_locations = {}
		for k in self.trains:
			t = self.trains[k]
			location = self.route.locate_train(t)
			start = self.station_locations[location[0].name]
			end = self.station_locations[location[1].name]
			frac = location[2] * (end - start)
			loc = start + frac
			ind = int(loc)
			self.train_locations[t.id] = loc
			if self.last_train_locations and self.last_train_locations.get(t.id):
				avg = (loc - self.last_train_locations[t.id]) / self.elapsed_since_last_location()
				n = 1
				if self.train_velocities.get(t.id):
					n, current = self.train_velocities[t.id]
					n = n + 1
					avg = (1. / n) * ((n - 1) * current + avg)
				self.train_velocities[t.id] = (n,avg)
			if not res_dict.get(ind):
				res_dict[ind] = []
			res_dict[ind].append(t)
			res_arr.append((t,loc))
		self.last_train_locations = self.train_locations.copy()
		self.last_locate_time = time.time()
		if as_dict:
			return res_dict
		else:
			return res_arr

	def elapsed_since_last_location(self):
		return time.time() - self.last_locate_time

	def text_map(self):
		trains = self.locate_trains(True)
		def marker(i):
			if trains.get(i) and len(trains[i]):
				flags = [False,False]
				for t in trains[i]:
					flags[t.direction] = True
				if flags[0] and flags[1]:
					return 'x'
				elif flags[0]:
					return '>'
				else:
					return '<'
			if self.stations.get(i):
				if self.stations.get(i).transfer_station():
					return 'O'
				else:
					return 'o'
			else:
				return '-'
		return self.name + ' ' + ''.join(map(marker,xrange(0,self.length())))

class MapState(object):
	def __init__(self):
		self.strips = {}
		for name, (index,length) in STRIPS.iteritems():
			self.strips[name] = [0] * length

	def diff_with(self,other):
		writes = []
		for k in STRIPS:
			this = self.strips[k]
			if other:
				that = other.strips[k]
			else:
				that = None
			writes = writes + map(
				lambda instr: StripWrite(STRIPS[k][0],*instr),
				fancy_time_diff(this,that)
			)
		return writes

	def set_light_color(self,strip,index,color):
		if self.strips.get(strip):
			if index >= 0 and index < len(self.strips[strip]):
				self.strips[strip][index] = color

	def set_segment_color(self,strip,start,end,color):
		if self.strips.get(strip):
			for i in xrange(start,end+1):
				self.set_light_color(strip,i,color)


class RouteMapState(MapState):
	def __init__(self,routes,tick,should_update=False):
		super(RouteMapState,self).__init__()
		for route_name in ROUTE_SEGMENTS:
			c = adjust_brightness(ROUTE_COLORS[route_name],0.1)
			for seg in ROUTE_SEGMENTS[route_name]:
				strip = seg[0]
				seg_start = seg[1]
				seg_end = seg[2]
				self.set_segment_color(strip,seg_start,seg_end,c)

class FadeRouteMapState(RouteMapState):
	def __init__(self,routes,tick,should_update=False):
		super(FadeRouteMapState,self).__init__(routes,tick,should_update)
		for name, mr in routes.iteritems():
			if should_update:
				mr.update_trains()
				mr.locate_trains()
			for train_id in mr.train_locations:
				location = mr.train_locations[train_id]
				n, vel = mr.train_velocities.get(train_id) or (0,0)
				dt = mr.elapsed_since_last_location()
				location = location + vel * dt
				r_loc = int(location)
				lights = filter(
					lambda p: p[1] > 0,
					map(
						lambda l: (l,max(0,1 - abs(location - l) / FADE_SIZE)), 
						xrange(r_loc - FADE_SIZE, r_loc + FADE_SIZE)
					)
				)
				for r_ind, brightness in lights:
					brightness = max(0.1,util.snap_to(brightness,0.05))
					strip, s_ind = mr.strip_by_index(r_ind)
					if strip != None:
						self.set_light_color(
							strip,
							s_ind,adjust_brightness(
									mr.color,
									brightness
								)
						)

class BlinkRouteMapState(RouteMapState):
		def __init__(self,routes,tick,should_update=False):
			super(BlinkRouteMapState,self).__init__(routes,tick,should_update)
			for name, mr in routes.iteritems():
				if should_update:
					mr.nb_update_trains()
				mr.update_lock.acquire()
				for train_id in mr.train_locations:
					location = int(mr.train_locations[train_id])
					strip, ind = mr.strip_by_index(location)
					color = adjust_brightness(
						mr.color,
						max(0.1,abs(math.cos(0.1 * (tick - ind))))
					)
					self.set_light_color(strip,ind,color)
				mr.update_lock.release()

class TranserStationState(MapState):
	def __init__(self,routes):
		for name, mr in routes.iteritems():
			pass


class StripWrite(object):
	def __init__(self,index,start,end,color):
		self.index = index
		self.start = start
		self.end = end
		self.color = color

	def __str__(self):
		return str((self.index,self.start,self.end,self.color))

	def __eq__(self,other):
		return self.index == other.index and self.start == other.start and self.end == other.end and self.color == other.color

class LightSegment(object):
	def __init__(self,strip,start,end,reverse=False):
		self.strip = strip
		self.start = start
		self.end = end
		self.reverse = reverse

	def length(self):
		return self.end - self.start + 1

if __name__ == '__main__':
	b = ArduinoBridge()
	v = RealTimeVisualization()
	c = MapController(b)
	c.set_visualization(v)
	time.sleep(1)
	while True:
		c.tick()
